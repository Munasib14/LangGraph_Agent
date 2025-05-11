import logging
from fastapi_app.app.services.agent.devops_agent.devops_types import DevOpsState

logger = logging.getLogger(__name__)

def terraform_plan_validator(state: DevOpsState) -> DevOpsState:
    """
    Validator to simulate terraform plan validation checks.
    """
    code = state.Devops_input  # Corrected from Devops_output

    if "aws_instance" in code:
        state.logs.append("Terraform Plan Validator: ✅ EC2 instance resource defined.")
    else:
        state.logs.append("Terraform Plan Validator: ⚠️ No EC2 resource found.")

    if "provider" not in code:
        state.logs.append("Terraform Plan Validator: ⚠️ Missing 'provider' block.")

    required_fields = ["ami", "instance_type"]
    for field in required_fields:
        if field not in code:
            state.logs.append(f"Terraform Plan Validator: ⚠️ Missing required EC2 field: {field}")

    logger.info("Terraform Plan Validator completed.")
    return state
