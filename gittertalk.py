from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class gittertalk(BaseModel):
    act: str
    obj: str
    params: Optional[Dict[str, str]] = Field(default_factory=dict)

def gittertalk_to_string(gt: gittertalk, verbose_level: int = 2) -> str:
    """
    Converts gittertalk object to a compact string representation.
    Output format depends on verbose_level:
    1: Structured but concise format
    2: Abbreviated format (60% efficiency target)  
    3: Symbolic format (40% efficiency target)
    4: Ultra-minimal format (20% efficiency target = 80% reduction)
    """
    if verbose_level == 1:
        # Structured but concise - remove redundant words
        params = gt.params or {}
        essential_params = []
        
        # Only include essential parameters, use shortest form
        if "from" in params and "to" in params:
            essential_params.append(f"{params['from']}-{params['to']}")
        elif "from" in params:
            essential_params.append(f"from:{params['from']}")
        elif "to" in params:
            essential_params.append(f"to:{params['to']}")
            
        if "when" in params:
            essential_params.append(params["when"])
            
        # Add other critical params
        for k, v in params.items():
            if k not in ["from", "to", "when"] and k in ["class", "time", "type"]:
                essential_params.append(f"{k[0]}{v}")
        
        if "check" in params:
            essential_params.append("?")
            
        return f"{gt.act} {gt.obj} {' '.join(essential_params)}"
    
    elif verbose_level == 2:
        # 60% efficiency target - moderate abbreviation with DEFINED mappings
        act_map = {
            "flight": "flt", "hotel": "htl", "news": "nws", "joke": "jk", 
            "car": "car", "route": "rte", "find": "fnd", "book": "bk", 
            "search": "sch", "get": "get"
        }
        obj_map = {
            "booking": "bkg", "Flight": "Flt", "entertainment": "ent", 
            "Route": "Rte", "Hotel": "Htl", "Car": "Car", "News": "Nws",
            "Joke": "Jke", "Object": "Obj"
        }
        
        # Use defined mappings only - no fallbacks to random abbreviations
        act = act_map.get(gt.act, gt.act)  # Keep full word if not in map
        obj = obj_map.get(gt.obj, gt.obj)  # Keep full word if not in map
        
        params = gt.params or {}
        parts = [f"{act}:{obj}"]
        
        if "from" in params and "to" in params:
            parts.append(f"{params['from']}-{params['to']}")
        
        if "when" in params:
            parts.append(params["when"])
            
        # Only essential modifiers with defined abbreviations
        essential = ["class", "time", "type"]
        for k in essential:
            if k in params:
                # Use defined abbreviations for common values
                value_abbrev = {
                    "business": "bus", "economy": "eco", "first": "1st",
                    "morning": "am", "afternoon": "pm", "evening": "eve"
                }
                v_short = value_abbrev.get(params[k], params[k])
                parts.append(f"{k[0]}{v_short}")
                
        if any(k in params for k in ["check", "availability"]):
            parts.append("?")
            
        return " ".join(parts)
    
    elif verbose_level == 3:
        # 40% efficiency target - heavy symbolism with DEFINED mappings
        act_map = {
            "flight": "f", "hotel": "h", "car": "c", "news": "n", "joke": "j",
            "route": "r", "find": "f", "book": "b", "search": "s", "get": "g"
        }
        act = act_map.get(gt.act, gt.act[0])  # Fallback to first letter only if not defined
        
        params = gt.params or {}
        parts = [act]
        
        # Route with >
        if "from" in params and "to" in params:
            parts.append(f"{params['from'][:3]}>{params['to'][:3]}")
        
        # Time shorthand
        if "when" in params:
            when = params["when"]
            if when.startswith('+'):
                parts.append(when)
            else:
                time_map = {"tomorrow": "+1", "today": "0", "morning": "am"}
                parts.append(time_map.get(when, when[:2]))
        
        # Quick modifiers
        if "class" in params:
            parts.append(f"c{params['class'][:1]}")
            
        if any(k in params for k in ["check", "availability"]):
            parts.append("?")
            
        return "".join(parts)
    
    else:  # verbose_level == 4
        # 20% efficiency target (80% reduction) - maximum compression with DEFINED mappings
        act_map = {
            "flight": "f", "hotel": "h", "car": "c", "news": "n", "joke": "j",
            "route": "r", "find": "f", "book": "b", "search": "s", "get": "g"
        }
        act = act_map.get(gt.act, gt.act[0])  # Fallback to first letter only if not defined
        
        params = gt.params or {}
        result = act
        
        # Ultra-compact route
        if "from" in params and "to" in params:
            # Use airport codes or abbreviations
            from_code = get_location_code(params["from"])
            to_code = get_location_code(params["to"])
            result += f"{from_code}{to_code}"
        
        # Time as single char/digit
        if "when" in params:
            when = params["when"]
            if when == "+1" or "tomorrow" in when:
                result += "1"
            elif when == "+0" or "today" in when:
                result += "0"
            elif "morning" in when:
                result += "m"
            else:
                result += when[0] if when else ""
        
        # Class as single letter
        if "class" in params:
            class_map = {"business": "b", "economy": "e", "first": "f"}
            result += class_map.get(params["class"], params["class"][0])
        
        # Check availability
        if any(k in params for k in ["check", "availability"]):
            result += "?"
            
        return result

def get_location_code(location: str) -> str:
    """Convert location to ultra-short code with DEFINED mappings"""
    codes = {
        # Major cities
        "NYC": "N", "New York": "N", "LAX": "L", "Los Angeles": "L",
        "Paris": "P", "London": "Ld", "Tokyo": "T", "Chicago": "C",
        # Ohio cities (for the user's example)
        "Zanesville": "Z", "Columbus": "C", "Cleveland": "Cl", "Cincinnati": "Ci",
        # Other common cities
        "Austin": "A", "Boston": "B", "Denver": "D", "Miami": "M", 
        "Seattle": "S", "Portland": "Pt", "Atlanta": "At"
    }
    return codes.get(location, location[:1])

def build_symbolic_params(params: Dict[str, Any], level: int) -> str:
    """Build symbolic parameter string based on efficiency level"""
    if not params:
        return ""
    
    if level == 4:
        # Ultra-minimal: maximum symbol usage
        parts = []
        
        # Route: from>to or <from or >to
        if "from" in params and "to" in params:
            parts.append(f"{params['from']}>{params['to']}")
        elif "from" in params:
            parts.append(f"<{params['from']}")
        elif "to" in params:
            parts.append(f">{params['to']}")
        
        # Time: +n, -n, or direct
        if "when" in params:
            when = str(params["when"])
            if when.startswith(('+', '-')):
                parts.append(when)
            elif when.isdigit():
                parts.append(f"+{when}")
            else:
                # Abbreviate common time terms
                time_abbrev = {"tomorrow": "+1", "today": "+0", "yesterday": "-1", "weekend": "+7"}
                parts.append(time_abbrev.get(when.lower(), when[:2]))
        
        # Checks and queries
        if any(k in params for k in ["check", "availability"]):
            parts.append("?")
        
        # Other params - heavily abbreviated
        for k, v in params.items():
            if k not in ["from", "to", "when", "check", "availability"]:
                key_map = {"class": "c", "type": "t", "location": "l", "time": "tm"}
                k_short = key_map.get(k, k[0])
                v_short = str(v)[:2] if len(str(v)) > 2 else str(v)
                parts.append(f"{k_short}{v_short}")
        
        return "".join(parts)
    
    else:  # level == 3
        # Symbolic but more readable
        parts = []
        
        if "from" in params and "to" in params:
            parts.append(f"{params['from']}>{params['to']}")
        elif "from" in params:
            parts.append(f"from:{params['from']}")
        elif "to" in params:
            parts.append(f"to:{params['to']}")
        
        if "when" in params:
            parts.append(f"when:{params['when']}")
        
        if "check" in params:
            parts.append("check:?")
        
        for k, v in params.items():
            if k not in ["from", "to", "when", "check"]:
                parts.append(f"{k}:{v}")
        
        return ";".join(parts)

def format_level_3(gittertalk_data):
    # Use consistent abbreviation patterns
    # Example: act:book → >b, obj:plane ticket → obj:pt, etc.
    formatted = []
    
    # Standardize common actions
    action_abbrev = {
        "book": "b",
        "search": "s", 
        "find": "f",
        "get": "g"
    }
    
    # Standardize common objects
    object_abbrev = {
        "plane ticket": "pt",
        "flight": "fl",
        "hotel": "ht"
    }
    
    # Build consistent format: >action;object;from>to
    # Example: >b;pt;Columbus,OH>Austin,TX
    # This function is incomplete - returning empty string for now
    return ""