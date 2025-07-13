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
        # Readable abbreviated format - more aggressive abbreviation
        action_abbrev = {"flight": "flt", "hotel": "htl", "news": "nws", "joke": "jke", "car": "car", "book": "bk"}
        obj_abbrev = {"Flight": "F", "Hotel": "H", "News": "N", "booking": "bk", "entertainment": "ent"}
        
        act = action_abbrev.get(gt.act, gt.act[:3])
        obj = obj_abbrev.get(gt.obj, gt.obj[:2])
        
        base = f"{act}:{obj}"
        params = gt.params or {}
        for k, v in params.items():
            key_abbrev = {"from": "fr", "to": "to", "when": "wn", "check": "ck", "location": "loc", "type": "ty"}
            k_short = key_abbrev.get(k, k[:2])
            base += f";{k_short}:{v}"
        return base
    
    elif verbose_level == 3:
        # Symbolic abbreviated format
        action_map = {
            'flight': 'f', 'hotel': 'h', 'car': 'c', 'news': 'n',
            'joke': 'j', 'translate': 't', 'book': 'b', 'reserve': 'r'
        }
        
        act_short = action_map.get(gt.act.lower(), gt.act[0])
        param_str = build_symbolic_params(gt.params, level=3)
        
        return f"{act_short}:{param_str}" if param_str else act_short
    
    else:  # verbose_level == 4
        # Ultra-minimal symbolic format - maximum compression
        action_map = {
            'flight': 'f', 'hotel': 'h', 'car': 'c', 'news': 'n',
            'joke': 'j', 'translate': 't', 'book': 'b', 'reserve': 'r'
        }
        
        act_short = action_map.get(gt.act.lower(), gt.act[0] if gt.act else 'u')
        param_str = build_symbolic_params(gt.params, level=4)
        
        return f"{act_short}:{param_str}" if param_str else act_short

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
    return formatted_string