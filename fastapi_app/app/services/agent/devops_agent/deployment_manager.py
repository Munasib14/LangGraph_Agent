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



# from .devops_types import DevOpsState

# def append_recommendation(content: str, condition: bool, recommendation: str) -> str:
#     """
#     Appends a recommendation to the content if the condition is True.
    
#     Args:
#         content (str): The existing output content.
#         condition (bool): Whether to append the recommendation.
#         recommendation (str): The text to append.

#     Returns:
#         str: Updated content.
#     """
#     if condition:
#         content += f"\n\n{recommendation}"
#     return content


# def recommend_deployment_strategy(state: DevOpsState) -> DevOpsState:
#     """
#     Adds deployment strategy recommendations based on the infrastructure or pipeline content.
    
#     Args:
#         state (DevOpsState): The current state of the DevOps pipeline.

#     Returns:
#         DevOpsState: Updated state with appended strategy tips.
#     """
#     content = state.Devops_output.lower()
#     updated_output = state.Devops_output

#     # Define tips
#     tips = {
#         "jenkins": "# CI/CD Tip: Automate your deployment process with stages like Build, Test, and Deploy. "
#                    "Use proper error handling and post-build actions to ensure stability.",

#         "dockerhub": "# Deployment Strategy Tip: Use Docker tags and automated builds in DockerHub. "
#                      "Integrate Jenkins with DockerHub webhooks to trigger builds and deployments on image push.",

#         "kubernetes": "# Kubernetes Deployment Tip: Use Rolling Updates or Blue/Green deployment strategies "
#                       "with readiness probes for zero-downtime deployments.",

#         "terraform": "# Terraform Tip: Use separate workspaces for dev/staging/prod environments. "
#                      "Automate Terraform with GitHub Actions using init, validate, plan, and apply stages. "
#                      "Store the Terraform state securely (e.g., S3 + DynamoDB for locking)."
#     }

#     # Append relevant tips based on keywords
#     updated_output = append_recommendation(updated_output, "jenkins" in content or "pipeline" in content, tips["jenkins"])
#     updated_output = append_recommendation(updated_output, "dockerhub" in content, tips["dockerhub"])
#     updated_output = append_recommendation(updated_output, "kubernetes" in content, tips["kubernetes"])
#     updated_output = append_recommendation(updated_output, "terraform" in content or "resource" in content, tips["terraform"])

#     # Update the state
#     state.Devops_output = updated_output
#     return state
