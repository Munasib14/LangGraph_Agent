from pydantic import BaseModel

class DevOpsState(BaseModel):
    input: str
    output: str = ""

def refactor_devops(state: DevOpsState) -> DevOpsState:
    comments = []

    if "resource" in state.input.lower():
        comments.append("# Consider splitting resources into modules")

    if "aws_instance" in state.input.lower():
        comments.append("# Use variables for AMI and instance type")

    comments.append("# Follow naming conventions for Jankins resources")
    
    # Append comments to the output
    state.output += "\n# Refactoring Suggestions\n" + "\n".join(comments)
    
    # Save output to a file (for Jenkins or manual inspection)
    # with open("refactor_output.txt", "w") as f:
    #     f.write(state.output)

    return state