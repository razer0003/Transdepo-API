from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_INTERPRETER
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from gittertalk import gittertalk

client = OpenAI(api_key=OPENAI_API_KEY)

async def interpreter_process(structured_prompt: str, verbose_level: int = 2) -> Tuple["gittertalk", str]:
    """
    Converts structured prompt to gittertalk and determines department.
    verbose_level: 1=full format, 2=abbreviated, 4=stenographic
    """
    from gittertalk import gittertalk  # Import here to avoid circular import
    
    # Use ONE consistent system prompt that always outputs the same format
    system_prompt = (
        "You are the Interpreter AI. Convert the structured prompt to gittertalk format using: "
        "act:<action>;obj:<object>;param1:value1;param2:value2... "
        "Always use this exact format regardless of the request. "
        "Common actions: route, flight, hotel, car, news, joke, book, search, find, get. "
        "Common objects: directions, booking, Flight, Hotel, Car, News, Joke, information. "
        "Common parameters: from, to, when, class, type, time, location. "
        "After the gittertalk, suggest which Department should handle the request. "
        "Available departments: 'travel', 'news', 'joke'. "
        "If the request doesn't clearly fit, suggest the most relevant one or use 'other'. "
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
    
    # Parse gittertalk string into object - now using consistent format
    try:
        gittertalk_parsed = parse_consistent_gittertalk(gittertalk_str)
    except Exception as e:
        from gittertalk import gittertalk  # Import here to avoid circular import
        print(f"Error parsing gittertalk: {e}")
        gittertalk_parsed = gittertalk(act="unknown", obj="unknown", params={})
    
    return gittertalk_parsed, department

def parse_consistent_gittertalk(gittertalk_str: str):
    """Parse consistent gittertalk format: act:action;obj:object;param:value;param:value"""
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