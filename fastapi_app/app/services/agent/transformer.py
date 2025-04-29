import os
from openai import OpenAI
from .prompt_engine import load_prompt
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def transform_sql(state: dict, prompt_template="transform_identity.j2") -> dict:
    sql_text = state["input"]
    context = {"input_sql": sql_text}
    prompt = load_prompt(prompt_template, context)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    transformed_sql = response.choices[0].message.content.strip()
    state["output"] += f"\n-- Transformed SQL --\n{transformed_sql}"
    return state