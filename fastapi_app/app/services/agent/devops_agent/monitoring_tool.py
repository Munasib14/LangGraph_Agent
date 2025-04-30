from .devops_types import DevOpsState

def suggest_monitoring_integration(state: DevOpsState) -> DevOpsState:
    """
    Appends monitoring and observability suggestions to Jenkins or infra code output.

    Args:
        state (DevOpsState): Current DevOps agent state.

    Returns:
        DevOpsState: Updated state with appended monitoring recommendations.
    """
    ci_cd_script = state.output  # The CI/CD script to append suggestions to
    pipeline_code = ci_cd_script  # Initialize pipeline_code with the current script

    recommendations = []

    # Look for signs of infrastructure where monitoring is useful
    if "aws_instance" in ci_cd_script or "autoscaling" in ci_cd_script.lower():
        recommendations.append("Consider integrating CloudWatch or Prometheus for monitoring EC2 instances and autoscaling events.")
    
    if "deploy" in ci_cd_script.lower():
        recommendations.append("Add deployment monitoring hooks to track release success and error rates.")
    
    if "sh './gradlew test'" in ci_cd_script:
        recommendations.append("Integrate test result reporting with Jenkins plugins or external dashboards.")

    # If there are any recommendations, append them to the CI/CD script
    if recommendations:
        pipeline_code += "\n\n// -- Monitoring Suggestions --\n" + "\n".join(f"// {s}" for s in recommendations)

    state["output"] = pipeline_code  # Update the state with the modified script
    return state
