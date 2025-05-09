from typing import List
from pydantic import BaseModel, Field

class DevOpsState(BaseModel):
    Devops_input: str
    Devops_output: str = ""
    gh_token: str
    gh_repo: str
    logs: List[str] = Field(default_factory=list)
    github_status: str = ""
    gh_file_path: str = ".github/workflows/generated_pipeline.yml"
    gh_branch: str = "main"
    gh_commit_msg: str = "Add GitHub Actions workflow"
    

def refactor_devops(state: DevOpsState) -> DevOpsState:
    comments = []

    if "resource" in state.Devops_input.lower():
        comments.append("# Consider splitting resources into modules")

    if "aws_instance" in state.Devops_input.lower():
        comments.append("# Use variables for AMI and instance type")

    comments.append("# Follow naming conventions for Jenkins resources")

    state.Devops_output += "\n# Refactoring Suggestions\n" + "\n".join(comments)
    return state
