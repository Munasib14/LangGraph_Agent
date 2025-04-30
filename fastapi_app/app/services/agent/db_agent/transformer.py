import os
from pathlib import Path
from groq import Groq
from openai import OpenAI
from .prompt_engine import load_prompt
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[4] / ".env")


# Load API key from env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def transform_sql(state: dict, prompt_template="transform_identity.j2") -> dict:
    sql_text = state["input"]
    context = {"input_sql": sql_text}
    prompt = load_prompt(prompt_template, context)

        # Call Groq model
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",  # or another model Groq supports
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    transformed_sql = response.choices[0].message.content.strip()
    state["output"] += f"\n-- Transformed SQL --\n{transformed_sql}"
    return state