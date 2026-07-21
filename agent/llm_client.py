#Talk to GPT-OSS endpoint

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")


def ask_llm(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "top_p": 0.6,
        "repetition_penalty": 1.15,
        "stream": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(
        API_URL,
        json=payload,
        headers=headers,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]
