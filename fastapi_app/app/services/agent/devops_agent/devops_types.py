from pydantic import BaseModel

class DevOpsState(BaseModel):
    Devops_input: str
    Devops_output: str = ""



def refactor_devops(state: DevOpsState) -> DevOpsState:
    comments = []

    if "resource" in state.Devops_input.lower():
        comments.append("# Consider splitting resources into modules")

    if "aws_instance" in state.Devops_input.lower():
        comments.append("# Use variables for AMI and instance type")

    comments.append("# Follow naming conventions for Jenkins resources")

    state.Devops_output += "\n# Refactoring Suggestions\n" + "\n".join(comments)
    return state
