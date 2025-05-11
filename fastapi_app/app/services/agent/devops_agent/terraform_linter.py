import logging
from fastapi_app.app.services.agent.devops_agent.devops_types import DevOpsState

logger = logging.getLogger(__name__)

def terraform_linter(state: DevOpsState) -> DevOpsState:
    """
    Simple Terraform linter to check for basic structure and common practices.
    """
    code = state.Devops_input  # Corrected from Devops_output

    if "resource" in code:
        state.logs.append("Terraform Linter: ✅ 'resource' block detected.")
    else:
        state.logs.append("Terraform Linter: ⚠️ Missing 'resource' block.")

    if "aws_" in code:
        state.logs.append("Terraform Linter: ✅ AWS-specific resources found.")
    else:
        state.logs.append("Terraform Linter: ⚠️ No AWS resources detected.")

    if "variable" not in code:
        state.logs.append("Terraform Linter: ⚠️ No variables used. Consider using variables for flexibility.")

    if "provider" not in code:
        state.logs.append("Terraform Linter: ⚠️ Missing 'provider' block. Required for cloud deployment.")

    logger.info("Terraform Linter completed.")
    return state
