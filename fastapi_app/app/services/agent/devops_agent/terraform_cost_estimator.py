import logging
from fastapi_app.app.services.agent.devops_agent.devops_types import DevOpsState

logger = logging.getLogger(__name__)

def terraform_cost_estimator(state: DevOpsState) -> DevOpsState:
    """
    Simulated Terraform cost estimator.

    Performs a basic scan of known AWS resource types in the Terraform configuration
    and estimates a rough monthly cost. This is a placeholder and does not query actual pricing APIs.
    
    Returns:
        Updated DevOpsState with cost estimation logs.
    """
    code = state.Devops_output.lower()
    estimated_cost = 0
    cost_breakdown = []

    # Estimate based on simple keyword matching
    if "aws_instance" in code:
        estimated_cost += 120
        cost_breakdown.append("• aws_instance: ~$120/month (t2.medium assumed)")

    if "aws_s3_bucket" in code:
        estimated_cost += 30
        cost_breakdown.append("• aws_s3_bucket: ~$30/month (100GB standard storage)")

    if "aws_rds_instance" in code:
        estimated_cost += 100
        cost_breakdown.append("• aws_rds_instance: ~$100/month (db.t3.micro assumed)")

    if "aws_lambda_function" in code:
        estimated_cost += 10
        cost_breakdown.append("• aws_lambda_function: ~$10/month (based on usage)")

    if not cost_breakdown:
        cost_breakdown.append("⚠️ No recognizable AWS resources found. Cannot estimate cost.")

    # Log the cost estimation
    state.logs.append("Terraform Cost Estimator: Estimated Monthly Cost 💰")
    state.logs.extend(cost_breakdown)
    state.logs.append(f"→ Total Estimated Cost: ~${estimated_cost}/month")

    logger.info("Terraform Cost Estimator completed with estimated cost: $%d", estimated_cost)
    return state
