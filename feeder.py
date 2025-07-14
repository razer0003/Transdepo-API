from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_FEEDER

# Only initialize OpenAI client if API key is available
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("Warning: OpenAI API key not found. The feeder will not work without it.")

async def feeder_process(human_request: str) -> str:
    """
    Converts a raw human request to a structured prompt for the Interpreter.
    """
    if not client:
        raise ValueError("OpenAI client not initialized. Please set OPENAI_API_KEY environment variable.")
        
    system_prompt = (
        "You are the Feeder AI. Your job is to extract intent, object, and key parameters from a human request, "
        "and output a structured summary suitable for further AI processing. "
        "Use concise English, list intent (action), object, and parameters explicitly."
    )
    response = client.chat.completions.create(
        model=MODEL_FEEDER,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_request}
        ]
    )
    return response.choices[0].message.content.strip()