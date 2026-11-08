import os
import httpx

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class PromptRequest(BaseModel):
    prompt: str
    tone: str = "neutral"


def generate_text(request: PromptRequest):

    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is missing"
        )

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    final_prompt = f"Write a response in a {request.tone} tone: {request.prompt}"

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        "temperature": 0.7
    }

    try:
        response = httpx.post(
            url,
            headers=headers,
            json=payload,
            timeout=30.0
        )

        response.raise_for_status()

        data = response.json()

        generated_text = data["choices"][0]["message"]["content"]

        return {
            "tone_user": request.tone,
            "original_prompt": request.prompt,
            "final_prompt": final_prompt,
            "response": generated_text
        }

    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=error.response.status_code,
            detail=error.response.json()
        )

    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail=f"Groq API connection error: {str(error)}"
        )


@app.post("/generate")
def generate(request: PromptRequest):
    return generate_text(request)