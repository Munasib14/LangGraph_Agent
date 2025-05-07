from jinja2 import Environment, FileSystemLoader
import os

# Define the folder where your Jinja2 templates are stored
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")

# Set up the Jinja2 environment
env = Environment(
    loader=FileSystemLoader(PROMPT_DIR),
    trim_blocks=True,
    lstrip_blocks=True
)

def load_prompt(template_name: str, context: dict) -> str:
    try:
        template = env.get_template(template_name)
        return template.render(context)
    except Exception as e:
        print(f"Error loading template {template_name}: {str(e)}")
        raise

