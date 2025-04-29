from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from app.services.langgraph.db_graph import db_agent_main
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = os.path.join(BASE_DIR, "app", "services", "agent", "prompts")
env = Environment(loader=FileSystemLoader(PROMPT_DIR))

@app.get("/")
async def root():
    return {"message": "DB Agent FastAPI Server is running🚀"}

class SQLRequest(BaseModel):
    sql_code: str
    prompt_name: str

@app.post("/run-db-agent/")
async def run_db_agent(request: SQLRequest):
    prompt = request.prompt_name.strip() or "transform_identity.j2"
    result = db_agent_main(request.sql_code, prompt_name=prompt)
    return {"result": result}

@app.get("/get-prompt/{prompt_name}")
async def get_prompt(prompt_name: str):
    try:
        template = env.get_template(prompt_name)
        rendered = template.render({"input_sql": "-- Your SQL here"})
        return {"prompt_content": rendered}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))