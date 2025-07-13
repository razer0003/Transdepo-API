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
    1: Traditional format (act:action;obj:object;param:value)
    2: Readable abbreviated format  
    3: Symbolic abbreviated format
    4: Ultra-minimal symbolic format
    """
    if verbose_level == 1:
        # Traditional format
        base = f"act:{gt.act};obj:{gt.obj}"
        params = gt.params or {}
        for k, v in params.items():
            base += f";{k}:{v}"
        return base
    
    elif verbose_level == 2:
        # Readable abbreviated format
        base = f"act:{gt.act};obj:{gt.obj}"
        params = gt.params or {}
        for k, v in params.items():
            base += f";{k}:{v}"
        return base
    
    elif verbose_level == 3:
        # Symbolic abbreviated format
        action_map = {
            'flight': 'f', 'hotel': 'h', 'car': 'c', 'news': 'n',
            'joke': 'j', 'translate': 't', 'book': 'b', 'reserve': 'r'
        }
        
        act_short = action_map.get(gt.act.lower(), gt.act)
        
        # Build symbolic parameters
        param_str = build_symbolic_params(gt.params, level=3)
        
        if param_str:
            return f"{act_short}:{param_str}"
        else:
            return f"{act_short}:{gt.obj.lower()}"
    
    else:  # verbose_level == 4
        # Ultra-minimal symbolic format
        action_map = {
            'flight': 'f', 'hotel': 'h', 'car': 'c', 'news': 'n',
            'joke': 'j', 'translate': 't', 'book': 'b', 'reserve': 'r'
        }
        
        act_short = action_map.get(gt.act.lower(), gt.act[0] if gt.act else 'u')
        
        # Build ultra-minimal symbolic parameters
        param_str = build_symbolic_params(gt.params, level=4)
        
        if param_str:
            return f"{act_short}:{param_str}"
        else:
            return act_short

def build_symbolic_params(params: Dict[str, Any], level: int) -> str:
    """Build symbolic parameter string based on efficiency level"""
    if not params:
        return ""
    
    parts = []
    
    # Handle route information
    if "from" in params and "to" in params:
        route = f"{params['from']}>{params['to']}"
        parts.append(route)
    elif "from" in params:
        parts.append(f"<{params['from']}")
    elif "to" in params:
        parts.append(f">{params['to']}")
    
    # Handle time information
    if "when" in params:
        when = params["when"]
        if when.startswith("+") or when.startswith("-"):
            parts.append(when)
        elif level == 4:
            parts.append(f"+{when}")
        else:
            parts.append(f"when:{when}")
    
    # Handle queries and checks
    if "check" in params or "availability" in str(params.values()).lower():
        parts.append("?")
    
    # Handle negations
    if "negate" in params or params.get("negate") == "true":
        parts.append("!")
    
    # Handle operators
    if params.get("operator") == "and":
        parts.append("&")
    elif params.get("operator") == "or":
        parts.append("|")
    
    # Add remaining parameters (for level 3, be more descriptive)
    for k, v in params.items():
        if k not in ["from", "to", "when", "check", "negate", "operator"]:
            if level == 4:
                # Ultra-minimal: just add key abbreviation
                key_map = {
                    "departure": "d", "arrival": "a", "price": "$",
                    "class": "c", "passengers": "p", "date": "d"
                }
                short_key = key_map.get(k.lower(), k[0] if k else "")
                parts.append(f"{short_key}:{v}")
            else:
                parts.append(f"{k}:{v}")
    
    return "".join(parts) if level == 4 else ";".join(parts)

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
    return formatted_string