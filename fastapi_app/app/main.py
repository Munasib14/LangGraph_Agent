from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import logging
# from services.agent.db_agent.langgraph.db_graph import db_agent_main
# from services.agent.devops_agent.langgraph.devops_graph import devops_agent_main
from fastapi_app.app.services.agent.db_agent.langgraph.db_graph import db_agent_main
from fastapi_app.app.services.agent.devops_agent.langgraph.devops_graph import devops_agent_main
from fastapi_app.app.services.agent.devops_agent.github_pusher import push_to_github

from jinja2 import Environment, FileSystemLoader
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))


app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = os.path.join(BASE_DIR, "app", "services","db_agent", "agent", "prompts")
PROMPT_DIR_DEVOPS = os.path.join(BASE_DIR, "app","services", "agent", "devops_agent", "prompts")
env = Environment(loader=FileSystemLoader(PROMPT_DIR))
env_devops = Environment(loader=FileSystemLoader(PROMPT_DIR_DEVOPS))


@app.get("/")
async def root():
    return {"message": "DB Agent abd DevOps Agent FastAPI Server is running🚀"}

class SQLRequest(BaseModel):
    sql_code: str
    prompt_name: str
    
class DevOpsRequest(BaseModel):
    infra_description: str
    prompt_name: str

@app.post("/run-db-agent/")
async def run_db_agent(request: SQLRequest):
    prompt = request.prompt_name.strip() or "transform_identity.j2"
    result = db_agent_main(request.sql_code, prompt_name=prompt)
    return {"result": result}

# @app.post("/run-devops-agent/")
# async def run_devops_agent(request: DevOpsRequest):
#     prompt = request.prompt_name.strip() or "devops_infra.j2"
#     result = devops_agent_main(request.infra_description, prompt_name=prompt)
#     return {"result": result}

@app.post("/run-devops-agent/")
async def run_devops_agent(request: DevOpsRequest):
    prompt = (request.prompt_name or "").strip() or "devops_infra.j2"
    
    # Load GitHub credentials from environment
    gh_token = os.getenv("GH_TOKEN")
    gh_repo = os.getenv("GH_REPO")  # e.g., "your-org/your-repo"

    if not gh_token or not gh_repo:
        logger.error("Missing GH_TOKEN or GH_REPO environment variable.")
        return {
            "result": None,
            "status": "Environment variables GH_TOKEN or GH_REPO are missing"
        }

    try:
        logger.info(f"Running DevOps agent with prompt: {prompt}")
        result = devops_agent_main(
            infra_code=request.infra_description,
            prompt_name=prompt,
            gh_token=gh_token,
            gh_repo=gh_repo
        )
    except Exception as e:
        logger.exception("Error during DevOps agent execution.")
        return {
            "result": None,
            "status": "Workflow generation failed",
            "error": str(e)
        }

    try:
        workflow_path = ".github/workflows/generated_pipeline.yml"
        logger.info(f"Pushing generated workflow to GitHub: {gh_repo}/{workflow_path}")
        push_to_github(gh_repo, workflow_path, result["output"])
        
        return {
            "result": result,
            "status": "Workflow pushed to GitHub successfully"
        }

    except Exception as e:
        logger.exception("Failed to push workflow to GitHub.")
        return {
            "result": result,
            "status": "Workflow generation done, but push failed",
            "error": str(e)
        }

@app.get("/get-prompt/{prompt_name}")
async def get_prompt(prompt_name: str):
    try:
        template = env.get_template(prompt_name)
        rendered = template.render({"input_sql": "-- Your SQL here"})
        return {"prompt_content": rendered}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@app.get("/get-devops-prompt/{prompt_name}")
async def get_devops_prompt(prompt_name: str):
    try:
        template = env_devops.get_template(prompt_name)
        rendered = template.render({"infra_code": "# Your Jenkinsfile or Terraform config here"})
        return {"prompt_content": rendered}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"DevOps Prompt not found: {e}")

