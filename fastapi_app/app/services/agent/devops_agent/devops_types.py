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



# from typing import List
# from pydantic import BaseModel, Field

# class DevOpsState(BaseModel):
#     Devops_input: str
#     Devops_output: str = ""
#     gh_token: str
#     gh_repo: str
#     logs: List[str] = Field(default_factory=list)
#     github_status: str = ""
#     gh_file_path: str = ".github/workflows/generated_pipeline.yml"
#     gh_branch: str = "main"
#     gh_commit_msg: str = "Add GitHub Actions workflow"


# def refactor_devops(state: DevOpsState) -> DevOpsState:
#     comments = []

#     content = state.Devops_input.lower()

#     # Terraform-specific suggestions
#     if any(term in content for term in ["resource", "terraform", "provider", "variable", "module"]):
#         if "resource" in content:
#             comments.append("# Consider splitting Terraform resources into reusable modules")
#         if "aws_instance" in content:
#             comments.append("# Use variables for AMI and instance type in Terraform")
#         comments.append("# Follow Terraform naming conventions for consistency")

#     # Jenkins-specific suggestions (only if Jenkins is detected)
#     if any(term in content for term in ["pipeline", "jenkinsfile", "stage", "agent"]):
#         comments.append("# Follow naming conventions for Jenkins resources")

#     # Only add suggestions if any exist
#     if comments:
#         state.Devops_output += "\n# Refactoring Suggestions\n" + "\n".join(comments)

#     return state


# from typing import List
# from pydantic import BaseModel, Field

# class DevOpsState(BaseModel):
#     Devops_input: str
#     Devops_output: str = ""
#     gh_token: str
#     gh_repo: str
#     logs: List[str] = Field(default_factory=list)
#     github_status: str = ""
#     gh_file_path: str = ".github/workflows/generated_pipeline.yml"
#     gh_branch: str = "main"
#     gh_commit_msg: str = "Add GitHub Actions workflow"


# def refactor_devops(state: DevOpsState) -> DevOpsState:
#     comments = []

#     content = state.Devops_input.lower()

#     # Terraform-specific suggestions
#     # Check for common Terraform keywords in the conten
#     if any(term in content for term in ["resource", "terraform", "provider", "variable", "module"]):
#         if "resource" in content:
#             comments.append("# Consider splitting Terraform resources into reusable modules")
#         if "aws_instance" in content:
#             comments.append("# Use variables for AMI and instance type in Terraform")
#         comments.append("# Follow Terraform naming conventions for consistency")

#     # Jenkins-specific suggestions (only if Jenkins is detected)
#     if any(term in content for term in ["pipeline", "jenkinsfile", "stage", "agent"]):
#         comments.append("# Follow naming conventions for Jenkins resources")

#     # Only add suggestions if any exist
#     if comments:
#         state.Devops_output += "\n# Refactoring Suggestions\n" + "\n".join(comments)

#     return state


