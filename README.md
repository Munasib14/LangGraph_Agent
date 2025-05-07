⚙️ LangGraph-Powered DB & DevOps Agent API
This project provides a FastAPI-based backend with two intelligent agents built using LangGraph and LLM-powered prompt templates:

DB Agent: Analyzes, transforms, and optimizes SQL queries.

DevOps Agent: Converts infrastructure descriptions into GitHub Actions workflows and pushes them to a repo.

It also includes a simple UI (db-agent-ui) and GitHub CI/CD support via .github/.

🏗️ Project Structure
bash
Copy
Edit
project-root/
│
├── .github/                    # GitHub workflows
├── db-agent-ui/               # (Optional) UI for interacting with DB Agent
├── fastapi_app/               # FastAPI server and core logic
│   ├── main.py                # Entry point for FastAPI app
│   ├── .env                   # Environment variables
│   ├── requirements.txt       # Python dependencies
│   └── app/
│       └── services/
│           └── agent/
│               ├── db_agent/
│               │   ├── langgraph/
│               │   │   └── db_graph.py
│               │   ├── prompts/
│               │   │   ├── add_try_catch.j2
│               │   │   ├── analyze_security_risks.j2
│               │   │   ├── best_practices.j2
│               │   │   ├── migrate_legacy_azure.j2
│               │   │   ├── optimize_performance.j2
│               │   │   ├── refactor_procedure.j2
│               │   │   └── transform_identity.j2
│               │   ├── metadata_logger.py
│               │   ├── performance_tuner.py
│               │   ├── prompt_engine.py
│               │   ├── refactor_sp.py
│               │   ├── schema_extractor.py
│               │   ├── transformer.py
│               │   └── validator.py
│               └── devops_agent/
│                   ├── langgraph/
│                   │   └── devops_graph.py
│                   ├── prompts/
│                   │   ├── devops_infra.j2
│                   │   └── transform_infra.j2
│                   ├── autoscaler.py
│                   ├── deployment_manager.py
│                   ├── devops_prompt_engine.py
│                   ├── devops_types.py
│                   ├── metadata_logger.py
│                   ├── monitoring_tool.py
│                   └── transformer.py
│                   └── github_pusher.py
                         
🎯 Project Goals
✅ Transform SQL Code: Format, optimize, and secure SQL queries using prompt templates.

✅ Automate DevOps Workflows: Generate GitHub Actions pipelines from plain text infrastructure descriptions.

✅ GitHub Integration: Auto-push generated workflows to your repository.

✅ Prompt-based Execution: Fully configurable via Jinja2-based prompt templates.

🚀 API Endpoints
Health Check
http
Copy
Edit
GET /
→ {"message": "DB Agent and DevOps Agent FastAPI Server is running🚀"}
🧠 DB Agent (SQL Transformation)
http
Copy
Edit
POST /run-db-agent/
{
  "sql_code": "SELECT * FROM users;",
  "prompt_name": "optimize_performance.j2"
}
🛠️ DevOps Agent (Infra to Workflow)
http
Copy
Edit
POST /run-devops-agent/
{
  "infra_description": "Simple Jenkins pipeline with build stage...",
  "prompt_name": "devops_infra.j2"
}
✅ Pushes result to .github/workflows/generated_pipeline.yml in your repo if GitHub credentials are set.

📄 Fetch SQL Prompt
http
Copy
Edit
GET /get-prompt/{prompt_name}
📄 Fetch DevOps Prompt
http
Copy
Edit
GET /get-devops-prompt/{prompt_name}
🔐 Environment Setup
Create a .env file in fastapi_app/:

env
Copy
Edit
GH_TOKEN=your_github_token
GH_REPO=username/repo-name
These are required for the DevOps agent to commit workflows to GitHub.

🧪 Local Development
Install dependencies:

bash
Copy
Edit
pip install -r fastapi_app/requirements.txt
Run the API server:

bash
Copy
Edit
cd fastapi_app
uvicorn main:app --reload
📦 Prompts Inventory
DB Agent Prompts
add_try_catch.j2

optimize_performance.j2

refactor_procedure.j2

analyze_security_risks.j2

migrate_legacy_azure.j2

best_practices.j2

transform_identity.j2

DevOps Prompts
devops_infra.j2

transform_infra.j2

🧠 Powered By
LangGraph – LLM agent orchestration

Jinja2 – Template rendering

FastAPI – High-performance web framework

GitHub REST API – Git-based workflow deployment

Python 3.9+

