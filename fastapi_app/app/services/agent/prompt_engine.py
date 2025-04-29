from jinja2 import Environment, FileSystemLoader
import os

PROMPT_DIR = os.path.join(os.path.dirname(__file__), "prompts")
env = Environment(loader=FileSystemLoader(PROMPT_DIR))

def load_prompt(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)




