import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_FEEDER = "gpt-3.5-turbo"
MODEL_INTERPRETER = "gpt-3.5-turbo"
MODEL_DEPARTMENT = "gpt-3.5-turbo"