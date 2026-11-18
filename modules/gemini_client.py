import os
from dotenv import load_dotenv
from google import genai 

load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

def generate_response(prompt: str) -> str:
    # To send a prompt to GEMINI and return its text response
    if not prompt or not prompt.strip():
        raise ValueError("PROMPT CANNOT BE EMPTY.")
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    
    client = genai.Client(api_key = api_key)
    # Client is the connection between your Python application and Google's AI service and authenticates requests using the API key
    
    response = client.models.generate_content(
        model = GEMINI_MODEL,
        contents = prompt
    )
    
    # VALIDATE RESPONSE
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    
    return response.text.strip()