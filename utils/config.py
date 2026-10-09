import os
from dotenv import load_dotenv

load_dotenv()

USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")