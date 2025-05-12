import os
from jinja2 import Environment, FileSystemLoader


DEV_PROMPT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "devops_agent", "devops_prompts")
)


dev_env = Environment(loader=FileSystemLoader(DEV_PROMPT_DIR))

def load_prompt(template_name: str, context: dict) -> str:
    """
    Loads and renders a Jinja2 template for the DevOps Agent.

    Args:
        template_name (str): The name of the prompt template file (including .j2).
        context (dict): The context to render the template with.

    Returns:
        str: The rendered prompt template or an error message if something goes wrong.
    """
    try:
        print(f"🧪 Loading from: {DEV_PROMPT_DIR}")
        print(f"🧪 Template name: {template_name}")
        print(f"🧪 Context: {context}")

        # Normalize template name
        template_name = template_name.strip().lower()

        # Check if the template exists
        full_path = os.path.join(DEV_PROMPT_DIR, template_name)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Template {template_name} not found in {DEV_PROMPT_DIR}")

        # Load and render the template
        template = dev_env.get_template(template_name)
        return template.render(context)

    except Exception as e:
        print(f"Error loading DevOps template {template_name}: {str(e)}")
        return f"Error loading template: {str(e)}"
