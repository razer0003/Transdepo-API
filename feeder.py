from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_FEEDER

client = OpenAI(api_key=OPENAI_API_KEY)

async def feeder_process(human_request: str) -> str:
    """
    Converts a raw human request to a structured prompt for the Interpreter.
    """
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