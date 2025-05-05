from .devops_types import DevOpsState

def recommend_deployment_strategy(state: DevOpsState) -> DevOpsState:
    """
    Adds deployment strategy recommendations based on the type of infrastructure/code.

    Args:
        state (DevOpsState): Current pipeline state.

    Returns:
        DevOpsState: Updated state with deployment strategy suggestions.
    """
    jenkins_script = state.Devops_output

    # Recommendations specific to containerized deployments using DockerHub
    if "dockerhub" in jenkins_script.lower():
        jenkins_script += (
            "\n\n# Deployment Strategy Tip: Use Docker tags and automated builds in DockerHub. "
            "Integrate Jenkins with DockerHub webhooks to trigger builds and deployments on image push."
        )
    
    # Recommendations specific to Kubernetes
    if "kubernetes" in jenkins_script.lower():
        jenkins_script += (
            "\n\n# Kubernetes Deployment Tip: Use Rolling Updates or Blue/Green deployment strategies "
            "with readiness probes for zero-downtime deployments."
        )
    
    # Generic CI/CD recommendation
    if "pipeline" in jenkins_script.lower() or "jenkins" in jenkins_script.lower():
        jenkins_script += (
            "\n\n# CI/CD Tip: Automate your deployment process with stages like Build, Test, and Deploy. "
            "Use proper error handling and post-build actions to ensure stability."
        )

    state.Devops_output = jenkins_script
    return state
