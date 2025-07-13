from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_INTERPRETER
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from gittertalk import gittertalk

client = OpenAI(api_key=OPENAI_API_KEY)

async def interpreter_process(structured_prompt: str, verbose_level: int = 2) -> Tuple["gittertalk", str]:
    """
    Converts structured prompt to gittertalk and determines department.
    verbose_level: 1=current format, 2=60% efficiency, 3=40% efficiency, 4=20% efficiency
    """
    from gittertalk import gittertalk  # Import here to avoid circular import
    
    # Define the system prompts for different verbose levels
    if verbose_level == 1:
        system_prompt = (
            "You are the Interpreter AI. Read the structured prompt and convert it to a compact, key-value gittertalk format: "
            "act:<action>;obj:<object>;param1:<value1>;param2:<value2>;... "
            "After that, suggest which Department should handle the request. Available departments are: 'travel', 'news', 'joke'. "
            "If the request doesn't clearly fit any of these, suggest the most relevant one or use 'other' if none apply."
            "\nRespond as:\ngittertalk:<gittertalk>\nDEPARTMENT:<department>"
        )
    elif verbose_level == 2:
        system_prompt = (
            "You are the Interpreter AI. Convert the structured prompt to a readable but compact gittertalk format. "
            "Use abbreviated keys like 'from', 'to', 'when', 'type', etc. Use underscores for multi-word values. "
            "Format: act:<action>;obj:<object>;key1:value1;key2:value2... "
            "Omit obvious words like 'find', 'get', 'available'. Use standard abbreviations. "
            "Available departments: 'travel', 'news', 'joke'. "
            "\nRespond as:\ngittertalk:<gittertalk>\nDEPARTMENT:<department>"
        )
    elif verbose_level == 3:
        system_prompt = (
            "You are the Interpreter AI. Convert to abbreviated gittertalk with symbols. "
            "Use format: action:params where action is a single letter and params use symbols. "
            "Actions: f=flight, h=hotel, c=car, n=news, j=joke, r=route/directions, b=book, s=search. "
            "Symbols: > for direction/to, < for from, + for future time, ? for queries. "
            "Use abbreviations for places (Zanesville=Zan, Columbus=Col). "
            "Examples: f:NYC>LAX+1? (flight NYC to LAX tomorrow, check), r:Zan>Col (route from Zanesville to Columbus). "
            "Available departments: 'travel', 'news', 'joke'. "
            "\nRespond as:\ngittertalk:<gittertalk>\nDEPARTMENT:<department>"
        )
    else:  # verbose_level == 4
        system_prompt = (
            "You are the Interpreter AI. Convert to ultra-minimal gittertalk. "
            "Use format: actioncodes where action is single letter and codes are minimal abbreviations. "
            "Actions: f=flight, h=hotel, c=car, n=news, j=joke, r=route, b=book, s=search. "
            "Use 1-2 letter location codes (Zanesville=Z, Columbus=C, NYC=N, LAX=L). "
            "Examples: fNL+1? (flight NYC to LAX tomorrow), rZC (route Zanesville to Columbus). "
            "Ultra-minimal: combine everything into shortest possible string. "
            "Available departments: 'travel', 'news', 'joke'. "
            "\nRespond as:\ngittertalk:<gittertalk>\nDEPARTMENT:<department>"
        )
    response = client.chat.completions.create(
        model=MODEL_INTERPRETER,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": structured_prompt}
        ]
    )
    content = response.choices[0].message.content.strip()
    lines = content.splitlines()
    
    # Find gittertalk line with better error handling
    gt_line = None
    dept_line = None
    
    for line in lines:
        line = line.strip()
        if line.lower().startswith("gittertalk:"):
            gt_line = line
        elif line.upper().startswith("DEPARTMENT:"):
            dept_line = line
        elif "act:" in line and "obj:" in line:
            # This looks like a gittertalk format without the "gittertalk:" prefix
            gt_line = "gittertalk:" + line
    
    # Fallback if expected format not found
    if not gt_line or not dept_line:
        print(f"Warning: Expected format not found in AI response: {content}")
        # Try to extract from the raw content or use defaults
        if "gittertalk:" in content.lower():
            gt_line = content[content.lower().find("gittertalk:"):]
            gt_line = gt_line.split('\n')[0]
        elif any("act:" in line and "obj:" in line for line in lines):
            # Find the line that looks like gittertalk
            for line in lines:
                if "act:" in line and "obj:" in line:
                    gt_line = "gittertalk:" + line.strip()
                    break
        else:
            gt_line = "gittertalk:act:unknown;obj:unknown"
            
        if "department:" in content.lower():
            dept_line = content[content.lower().find("department:"):]
            dept_line = dept_line.split('\n')[0]
        else:
            dept_line = "DEPARTMENT:generic"
    
    # Extract gittertalk and department
    gittertalk_str = gt_line[gt_line.find(":")+1:].strip()
    department = dept_line[dept_line.find(":")+1:].strip().lower()
    
    # Parse gittertalk string into object with error handling
    try:
        # Handle different formats based on verbose level
        if verbose_level >= 3:
            # For levels 3-4, handle symbolic formats
            gittertalk_parsed = parse_symbolic_gittertalk(gittertalk_str, verbose_level)
        else:
            # For levels 1-2, use traditional parsing
            gittertalk_parsed = parse_traditional_gittertalk(gittertalk_str)
            
    except Exception as e:
        from gittertalk import gittertalk  # Import here to avoid circular import
        print(f"Error parsing gittertalk: {e}")
        gittertalk_parsed = gittertalk(act="unknown", obj="unknown", params={})
    
    return gittertalk_parsed, department

def parse_traditional_gittertalk(gittertalk_str: str):
    """Parse traditional gittertalk format (levels 1-2)"""
    from gittertalk import gittertalk  # Import here to avoid circular import
    
    parts = gittertalk_str.split(";")
    if len(parts) >= 2:
        act_part = parts[0]
        obj_part = parts[1]
        
        act = act_part.split(":")[1] if ":" in act_part else "unknown"
        obj = obj_part.split(":")[1] if ":" in obj_part else "unknown"
        
        # Parse parameters safely
        params = {}
        for p in parts[2:]:
            if ":" in p:
                key, value = p.split(":", 1)  # Split only on first colon
                params[key] = value
    else:
        act = "unknown"
        obj = "unknown"
        params = {}
        
    return gittertalk(act=act, obj=obj, params=params)

def parse_symbolic_gittertalk(gittertalk_str: str, verbose_level: int):
    """Parse symbolic gittertalk format (levels 3-4)"""
    from gittertalk import gittertalk  # Import here to avoid circular import
    
    if verbose_level == 4:
        # Handle ultra-minimal format like "rZC" or "fNL+1?"
        if len(gittertalk_str) >= 2:
            action_char = gittertalk_str[0]
            params_part = gittertalk_str[1:]
            
            # Expand single-letter actions using SAME mappings as gittertalk_to_string
            action_map = {
                'f': 'flight', 'h': 'hotel', 'c': 'car', 'n': 'news', 
                'j': 'joke', 'r': 'route', 'b': 'book', 's': 'search', 'g': 'get'
            }
            
            act = action_map.get(action_char.lower(), 'unknown')
            
            # Parse ultra-minimal parameters
            params = parse_ultra_minimal_params(params_part)
            
            # Determine object based on action
            obj_map = {
                'flight': 'Flight', 'hotel': 'Hotel', 'car': 'Car',
                'news': 'News', 'joke': 'Joke', 'route': 'Route'
            }
            obj = obj_map.get(act, 'Object')
            
        else:
            act = "unknown"
            obj = "unknown"
            params = {}
            
    elif verbose_level == 3:
        # Handle level 3 format like "r:Zan>Col"
        if ":" in gittertalk_str:
            action_part, params_part = gittertalk_str.split(":", 1)
            
            # Expand single-letter actions using SAME mappings as gittertalk_to_string
            action_map = {
                'f': 'flight', 'h': 'hotel', 'c': 'car', 'n': 'news', 
                'j': 'joke', 'r': 'route', 'b': 'book', 's': 'search', 'g': 'get'
            }
            
            act = action_map.get(action_part.lower(), action_part)
            
            # Parse symbolic parameters
            params = parse_symbolic_params(params_part, verbose_level)
            
            # Determine object based on action
            obj_map = {
                'flight': 'Flight', 'hotel': 'Hotel', 'car': 'Car',
                'news': 'News', 'joke': 'Joke', 'route': 'Route'
            }
            obj = obj_map.get(act, 'Object')
            
        else:
            # Fallback for malformed input
            act = "unknown"
            obj = "unknown"
            params = {}
    else:
        # Fallback for other levels
        act = "unknown"
        obj = "unknown"
        params = {}
        
    return gittertalk(act=act, obj=obj, params=params)

def parse_symbolic_params(params_str: str, verbose_level: int) -> dict:
    """Parse symbolic parameters with smart interpretation"""
    params = {}
    
    # Handle route patterns like "NYC>LAX" or "NYC<LAX"
    if ">" in params_str:
        route_part = params_str.split(">")
        if len(route_part) >= 2:
            params["from"] = route_part[0]
            # Extract destination and any additional info
            dest_part = route_part[1]
            # Handle time indicators like "+1" or "?"
            if "+" in dest_part:
                dest, time_part = dest_part.split("+", 1)
                params["to"] = dest
                params["when"] = f"+{time_part.replace('?', '')}"
            elif "-" in dest_part:
                dest, time_part = dest_part.split("-", 1)
                params["to"] = dest
                params["when"] = f"-{time_part.replace('?', '')}"
            else:
                params["to"] = dest_part.replace("?", "")
    
    elif "<" in params_str:
        route_part = params_str.split("<")
        if len(route_part) >= 2:
            params["to"] = route_part[0]
            params["from"] = route_part[1].replace("?", "")
    
    # Handle queries and checks
    if "?" in params_str:
        params["check"] = "availability"
    
    # Handle negations
    if "!" in params_str:
        params["negate"] = "true"
    
    # Handle AND/OR operations
    if "&" in params_str:
        params["operator"] = "and"
    if "|" in params_str:
        params["operator"] = "or"
    
    return params

def parse_ultra_minimal_params(params_str: str) -> dict:
    """Parse ultra-minimal parameters like 'ZC' or 'NL+1?'"""
    params = {}
    
    # Handle queries
    if "?" in params_str:
        params["check"] = "availability"
        params_str = params_str.replace("?", "")
    
    # Handle time indicators
    if "+" in params_str:
        time_part = params_str[params_str.find("+"):]
        params["when"] = time_part
        params_str = params_str[:params_str.find("+")]
    
    # Remaining should be location codes
    if len(params_str) >= 2:
        # Assume first letter is source, second is destination
        params["from"] = expand_location_code(params_str[0])
        params["to"] = expand_location_code(params_str[1])
    
    return params

def expand_location_code(code: str) -> str:
    """Expand single letter location codes using SAME mappings as gittertalk.py"""
    codes = {
        # Major cities
        'N': 'NYC', 'L': 'LAX', 'P': 'Paris', 'T': 'Tokyo', 'C': 'Chicago',
        # Ohio cities (for the user's example)
        'Z': 'Zanesville', 'Cl': 'Cleveland', 'Ci': 'Cincinnati',
        # Other common cities  
        'A': 'Austin', 'B': 'Boston', 'D': 'Denver', 'M': 'Miami',
        'S': 'Seattle', 'Pt': 'Portland', 'At': 'Atlanta'
    }
    # Note: Columbus has conflict (C could be Chicago or Columbus)
    # Handle context-sensitive mapping
    if code.upper() == 'C':
        return 'Columbus'  # Default to Columbus for Ohio context
    return codes.get(code, code)