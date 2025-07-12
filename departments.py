from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_DEPARTMENT
from gittertalk import gittertalk

client = OpenAI(api_key=OPENAI_API_KEY)

async def handle_department(department: str, gittertalk: gittertalk, fallback_mode: str = "adaptive") -> str:
    """
    Routes the gittertalk to the appropriate department AI and gets the response.
    
    Args:
        department: The department name suggested by the interpreter
        gittertalk: The parsed gittertalk object
        fallback_mode: "adaptive" (creates new dept) or "strict" (refuses unknown depts)
    """
    # List of available departments
    available_departments = ["travel", "summarize", "joke"]
    
    if department == "travel":
        return await travel_department(gittertalk)
    elif department == "summarize":
        return await summarize_department(gittertalk)
    elif department == "joke":
        return await joke_department(gittertalk)
    else:
        # Handle fallback based on mode
        if fallback_mode == "strict":
            return await strict_fallback_department(department, available_departments)
        else:  # fallback_mode == "adaptive" (default)
            return await adaptive_fallback_department(gittertalk, department)

async def travel_department(gittertalk: gittertalk) -> str:
    prompt = (
        f"You are the Travel Department AI.\n"
        f"Handle this request (gittertalk): {gittertalk}\n"
        "Respond with booking details or next steps."
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

async def summarize_department(gittertalk: gittertalk) -> str:
    prompt = (
        f"You are the Summarization Department AI.\n"
        f"Summarize based on this gittertalk: {gittertalk}\n"
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

async def joke_department(gittertalk: gittertalk) -> str:
    prompt = (
        f"You are the Joke Department AI.\n"
        f"Tell a joke as per this gittertalk: {gittertalk}\n"
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

async def adaptive_fallback_department(gittertalk: gittertalk, department: str) -> str:
    """
    Adaptive fallback: Creates a new department on the spot to handle the request.
    This is the original behavior - acts as a generic AI that adapts to any request.
    """
    prompt = (
        f"You are the {department.title()} Department AI.\n"
        f"Handle the following gittertalk: {gittertalk}\n"
        f"Respond as a specialist in {department}-related topics."
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
        "• Summarizing text or information\n"
        "• Telling jokes and entertainment\n\n"
        "Please try rephrasing your request to match one of these areas, or consider using a different service for this type of assistance."
    )

async def generic_department(gittertalk: gittertalk) -> str:
    prompt = (
        f"You are a Generic Department AI.\n"
        f"Handle the following gittertalk: {gittertalk}\n"
    )
    response = client.chat.completions.create(
        model=MODEL_DEPARTMENT,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()