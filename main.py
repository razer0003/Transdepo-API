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
    verbose: Optional[int] = 2  # 1=current, 2=60%, 3=40%, 4=20% (default: level 2)

@app.post("/process")
async def process_request(human: HumanRequest):
    # 1. Feeder step: Human → Structured
    structured = await feeder_process(human.request)
    # 2. Interpreter step: Structured → gittertalk (+ department)
    gittertalk, department = await interpreter_process(structured, human.verbose)
    # 3. Department step: gittertalk → Final response
    result = await handle_department(department, gittertalk, human.fallback_mode)
    return {
        "gittertalk": gittertalk_to_string(gittertalk, human.verbose),
        "department": department,
        "result": result,
        "fallback_mode": human.fallback_mode,
        "verbose_level": human.verbose
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
        "available_departments": ["travel", "summarize", "joke"],
        "fallback_modes": {
            "adaptive": "Creates new departments on the spot (default)",
            "strict": "Only handles requests for existing departments"
        },
        "verbose_levels": {
            "1": "Current format - full descriptive gittertalk",
            "2": "60% efficiency - structured but readable (default)",
            "3": "40% efficiency - abbreviated with symbols",
            "4": "20% efficiency - ultra-minimal with heavy symbolism"
        },
        "request_format": {
            "request": "string (required) - Your request text",
            "fallback_mode": "string (optional) - 'adaptive' or 'strict', defaults to 'adaptive'",
            "verbose": "integer (optional) - 1-4, gittertalk efficiency level, defaults to 2"
        },
        "example_requests": [
            {
                "request": "Book a flight to NYC",
                "fallback_mode": "adaptive",
                "verbose": 2
            },
            {
                "request": "Tell me about games",
                "fallback_mode": "strict",
                "verbose": 4
            }
        ]
    }