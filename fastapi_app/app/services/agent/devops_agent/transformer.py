import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
from .devops_prompt_engine import load_prompt
from .devops_types import DevOpsState


load_dotenv(Path(__file__).resolve().parents[4] / ".env")


# Load API key from env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def transform_infra(state: DevOpsState, prompt_template="jenkins_pipeline.j2") -> DevOpsState:
    """
    Uses Groq model to transform infrastructure code.
    """
    input_infra = state.Devops_input # Input infrastructure code (YAML, Terraform, etc.)
    
    #  Wrap input_infra in a dictionary for Jinja2
    # context = {"infra_code": input_infra}
    context = {"infra_description": input_infra}
    
    # Load prompt using jinja2 with proper context
    prompt = load_prompt(prompt_template, context)
    

    # Call Groq model
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",  # or another model Groq supports
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    transformed = response.choices[0].message.content.strip()
    state.Devops_output += f"\n# Transformed Infra\n{transformed}"
    return state

