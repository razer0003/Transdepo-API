from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_DEPARTMENT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gittertalk import gittertalk

client = OpenAI(api_key=OPENAI_API_KEY)

def extract_user_intent(gittertalk_obj: "gittertalk") -> str:
    """
    Convert gittertalk object back to user-friendly language for processing.
    This ensures that department AIs never see internal technical terms.
    """
    try:
        # Build a natural language description from gittertalk components
        action = gittertalk_obj.act
        obj = gittertalk_obj.obj
        params = gittertalk_obj.params or {}
        
        # Start with the basic action and object
        if action and obj:
            if action.lower() == "news":
                base_intent = f"provide news or information about {obj.lower()}"
            elif action.lower() == "joke":
                base_intent = "tell a joke or provide entertainment"
            elif action.lower() == "flight":
                base_intent = "help with flight booking or travel"
            elif action.lower() == "hotel":
                base_intent = "help with hotel booking"
            else:
                base_intent = f"{action.lower()} {obj.lower()}"
        else:
            base_intent = "help with a general request"
        
        # Add parameter details in natural language
        details = []
        for key, value in params.items():
            if key == "from" and value:
                details.append(f"from {value}")
            elif key == "to" and value:
                details.append(f"to {value}")
            elif key == "when" and value:
                if value.startswith("+"):
                    details.append(f"for {value[1:]} day(s) from now")
                else:
                    details.append(f"on {value}")
            elif key == "check" and value == "availability":
                details.append("and check availability")
            elif key and value:
                details.append(f"with {key}: {value}")
        
        # Combine into natural sentence
        if details:
            user_intent = f"{base_intent} {' '.join(details)}"
        else:
            user_intent = base_intent
            
        return user_intent.strip()
        
    except Exception as e:
        # Fallback to a generic description if parsing fails
        return "help with a user request"

async def handle_department(department: str, gittertalk_obj: "gittertalk", fallback_mode: str = "adaptive") -> str:
    """
    Routes the gittertalk to the appropriate department AI and gets the response.
    
    Args:
        department: The department name suggested by the interpreter
        gittertalk_obj: The parsed gittertalk object
        fallback_mode: "adaptive" (creates new dept) or "strict" (refuses unknown depts)
    """
    # Route to the appropriate department based on the department name
    try:
        if department == "travel":
            return await travel_department(gittertalk_obj)
        elif department == "news":
            return await news_department(gittertalk_obj)
        elif department == "joke":
            return await joke_department(gittertalk_obj)
        elif fallback_mode == "adaptive":
            return await adaptive_fallback_department(gittertalk_obj, department)
        else:  # strict mode
            available_departments = ["travel", "news", "joke"]
            return await strict_fallback_department(department, available_departments)
    except Exception as e:
        # Fallback to generic department if there's an error
        return await generic_department(gittertalk_obj)

async def travel_department(gittertalk_obj: "gittertalk") -> str:
    # Use the gittertalk object directly for token efficiency - don't expand back to natural language
    from gittertalk import gittertalk_to_string
    
    # Get the compressed gittertalk string at the same level it was created
    # This maintains the token efficiency benefit
    gittertalk_str = gittertalk_to_string(gittertalk_obj, 2)  # Use level 2 as baseline for departments
    
    prompt = (
        f"You are a Travel Assistant AI. Process this travel request: {gittertalk_str}\n"
        "Interpret the compact request format and provide helpful travel advice or booking suggestions. "
        "Be friendly and professional."
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

async def news_department(gittertalk_obj: "gittertalk") -> str:
    # Use the gittertalk object directly for token efficiency
    from gittertalk import gittertalk_to_string
    
    gittertalk_str = gittertalk_to_string(gittertalk_obj, 2)
    
    prompt = (
        f"You are a News Assistant AI. Process this news request: {gittertalk_str}\n"
        "Interpret the compact request format and provide news updates or information. "
        "Be informative and helpful."
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

async def joke_department(gittertalk_obj: "gittertalk") -> str:
    # Use the gittertalk object directly for token efficiency  
    from gittertalk import gittertalk_to_string
    
    gittertalk_str = gittertalk_to_string(gittertalk_obj, 2)
    
    prompt = (
        f"You are a Comedy Assistant AI. Process this entertainment request: {gittertalk_str}\n"
        "Interpret the compact request format and provide humor or entertainment. "
        "Be funny and engaging."
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

async def adaptive_fallback_department(gittertalk_obj: "gittertalk", department: str) -> str:
    """
    Adaptive fallback: Creates a new department on the spot to handle the request.
    Uses compressed gittertalk format to maintain token efficiency.
    """
    from gittertalk import gittertalk_to_string
    
    gittertalk_str = gittertalk_to_string(gittertalk_obj, 2)
    
    prompt = (
        f"You are a {department.title()} Assistant AI. Process this request: {gittertalk_str}\n"
        f"Interpret the compact request format as a specialist in {department}-related topics. "
        "Be helpful and professional."
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

async def strict_fallback_department(requested_department: str, available_departments: list) -> str:
    """
    Strict fallback: Refuses to handle requests outside of existing capabilities.
    Provides user-friendly response about what the system can actually do.
    """
    return (
        "I'm sorry, but I'm not able to help with that type of request. "
        "I can assist you with:\n\n"
        "• Travel planning and booking\n"
        "• News and current information\n"
        "• Telling jokes and entertainment\n\n"
        "Please try rephrasing your request to match one of these areas, or consider using a different service for this type of assistance."
    )

async def generic_department(gittertalk_obj: "gittertalk") -> str:
    from gittertalk import gittertalk_to_string
    
    gittertalk_str = gittertalk_to_string(gittertalk_obj, 2)
    
    prompt = (
        f"You are a General Assistant AI. Process this request: {gittertalk_str}\n"
        "Interpret the compact request format and provide helpful assistance."
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()