import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

def generate_response(prompt: str) -> str:
    # To send a prompt to GROQ and return its text response
        if not prompt or not prompt.strip():
            raise ValueError("PROMPT CANNOT BE EMPTY.")
        
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file.")
        
        client = Groq(api_key = api_key)
        # Client is the connection between your Python application and Google's AI service and authenticates requests using the API key
        
        response = client.chat.completions.create(
            model = GROQ_MODEL,
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        answer = response.choices[0].message.content
        
        # VALIDATE RESPONSE
        if not answer:
            raise RuntimeError("Groq returned an empty response.")
        
        return answer.strip()