import os
from dotenv import load_dotenv
import requests

load_dotenv()

LLM_API_URL = os.getenv("LLM_API_URL", "")
MODEL_NAME = os.getenv("LLM_MODEL", "")
LLM_TOKEN = os.getenv("LLM_TOKEN", "")

def generate(prompt: str, system: str = "") -> str:
    """Generate a response from the language model.
    
    Args:
        prompt (str): The input prompt to send to the language model
        system (str, optional): System prompt to guide the model's behavior. Defaults to "".
        
    Returns:
        str: The generated response from the language model
        
    Raises:
        requests.exceptions.HTTPError: If the API request fails
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.95
        }
    }
    if system:
        payload["system"] = system

    headers = {"Authorization": f"Bearer {LLM_TOKEN}"} if LLM_TOKEN else {}
    resp = requests.post(LLM_API_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()["response"].strip()
