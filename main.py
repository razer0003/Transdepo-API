from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from feeder import feeder_process
from interpreter import interpreter_process
from departments import handle_department
from gittertalk import gittertalk_to_string

app = FastAPI()

class HumanRequest(BaseModel):
    request: str
    fallback_mode: Optional[str] = "adaptive"  # "adaptive" or "strict"
    verbose: Optional[int] = 2  # 1=full format, 2=abbreviated, 4=stenographic (default: level 2)

@app.post("/process")
async def process_request(human: HumanRequest):
    # Validate verbose level - only 1, 2, and 4 are supported
    verbose_level = human.verbose or 2
    if verbose_level not in [1, 2, 4]:
        return {
            "error": "Invalid verbose level. Only levels 1, 2, and 4 are supported.",
            "supported_levels": {
                "1": "Full format with no abbreviations", 
                "2": "Abbreviated format with simple mappings",
                "4": "Stenographic compression with context markers"
            }
        }
    
    # 1. Feeder step: Human → Structured
    structured = await feeder_process(human.request)
    # 2. Interpreter step: Structured → gittertalk (+ department)
    fallback_mode = human.fallback_mode or "adaptive"
    gittertalk, department = await interpreter_process(structured, verbose_level)
    # 3. Department step: gittertalk → Final response
    result = await handle_department(department, gittertalk, fallback_mode)
    return {
        "gittertalk": gittertalk_to_string(gittertalk, verbose_level),
        "department": department,
        "result": result,
        "fallback_mode": fallback_mode,
        "verbose_level": verbose_level
    }

@app.get("/")
async def root():
    return {
        "message": "Transdepo API",
        "endpoints": {
            "/process": "Main processing endpoint",
            "/info": "API information and options"
        }
    }

@app.get("/info")
async def api_info():
    return {
        "api_name": "Transdepo API",
        "description": "Multi-stage AI processing pipeline",
        "available_departments": ["travel", "news", "joke"],
        "fallback_modes": {
            "adaptive": "Creates new departments on the spot (default)",
            "strict": "Only handles requests for existing departments"
        },
        "verbose_levels": {
            "1": "Full format - complete descriptive gittertalk with no abbreviations",
            "2": "Abbreviated format - simple abbreviations and readable compression (default)",
            "4": "Stenographic format - contextual compression with stenographic markers"
        },
        "request_format": {
            "request": "string (required) - Your request text",
            "fallback_mode": "string (optional) - 'adaptive' or 'strict', defaults to 'adaptive'",
            "verbose": "integer (optional) - 1, 2, or 4, gittertalk efficiency level, defaults to 2"
        },
        "example_requests": [
            {
                "request": "Book a flight to NYC",
                "fallback_mode": "adaptive",
                "verbose": 2
            },
            {
                "request": "Tell me about current events",
                "fallback_mode": "strict",
                "verbose": 4
            }
        ]
    }