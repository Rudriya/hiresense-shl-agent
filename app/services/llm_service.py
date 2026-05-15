# app/services/llm_service.py

import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


MODEL_NAME = "llama-3.1-8b-instant"


SYSTEM_PROMPT = """
You are an SHL assessment recommendation assistant.

STRICT RULES:
- ONLY discuss provided assessments.
- NEVER hallucinate.
- NEVER invent URLs.
- Keep responses concise.
"""


def generate_reply(recommendations):

    names = [
        r["name"]
        for r in recommendations[:3]
    ]

    prompt = f"""
    Generate a short professional response recommending:
    {', '.join(names)}
    """

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=80
    )

    return completion.choices[0].message.content