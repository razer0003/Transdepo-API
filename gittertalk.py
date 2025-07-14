from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class gittertalk(BaseModel):
    act: str
    obj: str
    params: Optional[Dict[str, str]] = Field(default_factory=dict)

def gittertalk_to_string(gt: gittertalk, verbose_level: int = 2) -> str:
    """
    Converts gittertalk object to a string representation.
    Output format depends on verbose_level:
    1: Full format - act:route;obj:directions;from:Zanesville;to:Columbus
    2: Abbreviated format - act:rte;obj:dir;from:Zan;to:Col  
    4: Stenographic format - rt:ct;zv:st;OH>ct;cb:st;OH
    """
    if verbose_level == 1:
        # Level 1: Full format with no abbreviations
        params = gt.params or {}
        parts = [f"act:{gt.act}", f"obj:{gt.obj}"]
        
        for key, value in params.items():
            parts.append(f"{key}:{value}")
            
        return ";".join(parts)
    
    elif verbose_level == 2:
        # Level 2: Simple abbreviations with comprehensive mappings
        
        # Comprehensive action abbreviation map
        act_map = {
            "route": "rte", "flight": "flt", "hotel": "htl", "car": "car",
            "news": "nws", "joke": "jk", "book": "bk", "search": "sch", 
            "find": "fnd", "get": "get", "rent": "rnt", "reserve": "rsv"
        }
        
        # Comprehensive object abbreviation map  
        obj_map = {
            "directions": "dir", "booking": "bkg", "Flight": "Flt", 
            "Hotel": "Htl", "Car": "Car", "News": "Nws", "Joke": "Jke",
            "Route": "Rte", "information": "inf", "entertainment": "ent"
        }
        
        # Location abbreviation map for common places
        location_map = {
            "Zanesville": "Zan", "Columbus": "Col", "Cleveland": "Clv",
            "Cincinnati": "Cin", "New York": "NYC", "Los Angeles": "LAX", 
            "Chicago": "Chi", "Boston": "Bos", "Austin": "Aus",
            "Denver": "Den", "Miami": "Mia", "Seattle": "Sea"
        }
        
        act = act_map.get(gt.act, gt.act)
        obj = obj_map.get(gt.obj, gt.obj)
        
        params = gt.params or {}
        parts = [f"act:{act}", f"obj:{obj}"]
        
        for key, value in params.items():
            # Abbreviate common location names
            if key in ["from", "to", "location"] and value in location_map:
                value = location_map[value]
            parts.append(f"{key}:{value}")
            
        return ";".join(parts)
    
    elif verbose_level == 4:
        # Level 4: Stenographic format with context markers
        return create_stenographic_format(gt)
    
    else:
        # Fallback to level 2 for any invalid level
        return gittertalk_to_string(gt, 2)

def create_stenographic_format(gt: gittertalk) -> str:
    """
    Create stenographic compression with context markers:
    - Context markers: ct=city, st=state, ap=airport, ht=hotel, tm=time
    - Relationship markers: :=defines, ;=adds context, >=direction, +=time offset, ?=query
    - Stenographic compression: Remove vowels, keep key consonants
    """
    
    # Stenographic action compression
    action_steno = {
        "route": "rt", "flight": "fl", "hotel": "ht", "car": "cr",
        "news": "nw", "joke": "jk", "book": "bk", "search": "sr", 
        "find": "fn", "get": "gt", "rent": "rn", "reserve": "rs"
    }
    
    # Stenographic object compression  
    object_steno = {
        "directions": "dr", "booking": "bk", "Flight": "fl", 
        "Hotel": "ht", "Car": "cr", "News": "nw", "Joke": "jk",
        "Route": "rt", "information": "if", "entertainment": "et"
    }
    
    params = gt.params or {}
    parts = []
    
    # Add action with context
    act_short = action_steno.get(gt.act, stenographic_compress(gt.act))
    parts.append(f"{act_short}:ct")  # ct = context type
    
    # Process locations with stenographic compression
    if "from" in params and "to" in params:
        from_steno = stenographic_location(params["from"])
        to_steno = stenographic_location(params["to"])
        parts.append(f"{from_steno}>{to_steno}")
    elif "from" in params:
        from_steno = stenographic_location(params["from"])
        parts.append(f"fr:{from_steno}")
    elif "to" in params:
        to_steno = stenographic_location(params["to"])
        parts.append(f"to:{to_steno}")
    
    # Process other parameters with context markers
    for key, value in params.items():
        if key not in ["from", "to"]:
            if key == "when":
                parts.append(f"tm:{stenographic_compress(value)}")  # tm = time marker
            elif key == "class":
                parts.append(f"cl:{stenographic_compress(value)}")
            elif key == "type":
                parts.append(f"tp:{stenographic_compress(value)}")
            else:
                key_short = stenographic_compress(key)
                value_short = stenographic_compress(value)
                parts.append(f"{key_short}:{value_short}")
    
    return ";".join(parts)

def stenographic_compress(text: str) -> str:
    """
    Stenographic compression: Remove vowels, keep key consonants
    Zanesville → zv, Columbus → cb
    """
    if not text:
        return text
        
    text = text.lower().strip()
    
    # Special cases for common locations
    special_cases = {
        "zanesville": "zv", "columbus": "cb", "cleveland": "cv", 
        "cincinnati": "cn", "new york": "ny", "los angeles": "la",
        "chicago": "cg", "boston": "bt", "austin": "at", "denver": "dv",
        "miami": "mi", "seattle": "st", "tomorrow": "tm", "today": "td",
        "morning": "mr", "afternoon": "af", "evening": "ev", 
        "business": "bs", "economy": "ec", "first": "fs"
    }
    
    if text in special_cases:
        return special_cases[text]
    
    # General stenographic compression
    # Remove vowels except at start, keep important consonants
    result = ""
    vowels = "aeiou"
    
    for i, char in enumerate(text):
        if char.isalpha():
            if i == 0:  # Keep first letter always
                result += char
            elif char not in vowels:  # Keep consonants
                result += char
            # Skip vowels except at start
        elif char.isdigit():
            result += char
        # Skip other characters
    
    # Ensure minimum 2 characters for readability
    if len(result) < 2 and len(text) >= 2:
        result = text[:2]
        
    return result

def stenographic_location(location: str) -> str:
    """
    Convert location to stenographic format with state context
    Zanesville Ohio → zv:st;OH, Columbus Ohio → cb:st;OH
    """
    location = location.strip()
    
    # Handle "City, State" or "City State" patterns
    if "," in location:
        parts = location.split(",")
        city = parts[0].strip()
        state = parts[1].strip() if len(parts) > 1 else ""
    elif " " in location and any(state in location.upper() for state in ["OH", "OHIO", "NY", "CA", "TX", "FL"]):
        parts = location.split()
        city = " ".join(parts[:-1])
        state = parts[-1]
    else:
        city = location
        state = ""
    
    city_steno = stenographic_compress(city)
    
    if state:
        state_abbrev = get_state_abbreviation(state)
        return f"{city_steno}:st;{state_abbrev}"
    else:
        return f"{city_steno}:ct"

def get_state_abbreviation(state: str) -> str:
    """Get standard state abbreviation"""
    state_map = {
        "ohio": "OH", "new york": "NY", "california": "CA", 
        "texas": "TX", "florida": "FL", "illinois": "IL",
        "massachusetts": "MA", "colorado": "CO", "washington": "WA"
    }
    
    state_lower = state.lower()
    return state_map.get(state_lower, state.upper()[:2])