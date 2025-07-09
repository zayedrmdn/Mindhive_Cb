# app/memory_agent.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # loads OPENROUTER_API_KEY from project root .env

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY in .env")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct:free"

# In-memory conversation history using OpenAI-compatible structure
history = []

def chat_with_memory(user_input: str) -> str:
    history.append({"role": "user", "content": user_input})

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": history,
            "temperature": 0.1,
            "max_tokens": 60
        }
    )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter error {response.status_code}: {response.text}")

    data = response.json()
    reply = data["choices"][0]["message"]["content"].strip()

    history.append({"role": "assistant", "content": reply})
    return reply
