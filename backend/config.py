import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read values from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")