# def suggest_jenkins_optimizations(state: dict) -> dict:
#     jenkins_script = state.Devops_output
#     suggestions = []

#     if "agent any" in jenkins_script.lower():
#         suggestions.append("Consider specifying a more granular agent label instead of 'any' to optimize resource usage.")
    
#     if "sh './gradlew" in jenkins_script and "parallel" not in jenkins_script:
#         suggestions.append("Consider using parallel stages to speed up build and test processes.")

#     if "post {" not in jenkins_script.lower():
#         suggestions.append("Include a 'post' section for better visibility into pipeline success or failure.")

#     if "parameters {" not in jenkins_script.lower():
#         suggestions.append("Use parameters to make the pipeline reusable for different environments or builds.")

#     if suggestions:
#         state.Devops_output += "\n\n// -- Jenkins Pipeline Optimization Suggestions --\n" + "\n".join(f"// - {s}" for s in suggestions)

#     return state


# from .devops_types import DevOpsState

# def suggest_jenkins_optimizations(state: DevOpsState) -> DevOpsState:
#     """
#     Adds deployment strategy recommendations based on the detected infrastructure/tooling in the output.

#     Args:
#         state (DevOpsState): Current pipeline state.

#     Returns:
#         DevOpsState: Updated state with relevant suggestions.
#     """
#     content = state.Devops_output
#     suggestions = []

#     # Determine context and gather suggestions
#     is_jenkins = "pipeline" in content.lower() or "jenkins" in content.lower()
#     is_terraform = "resource" in content.lower() or "aws_instance" in content.lower() or "terraform" in content.lower()

#     if "dockerhub" in content.lower():
#         suggestions.append("Use Docker tags and enable automated builds in DockerHub. "
#                            "Set up webhooks to trigger builds and deployments on image push.")

#     if "kubernetes" in content.lower():
#         suggestions.append("Use rolling updates or blue/green deployments in Kubernetes with readiness probes "
#                            "for zero-downtime rollouts.")

#     if is_jenkins and not is_terraform:
#         suggestions.append("Automate Jenkins pipeline with stages like Build, Test, Deploy. "
#                            "Ensure proper error handling and post-build actions.")

#     if is_terraform:
#         suggestions.append("Use workspaces for dev/staging/prod. Automate with GitHub Actions using init, "
#                            "validate, plan, and apply steps. Store state securely using S3 and DynamoDB.")

#     # Add suggestions under a context-aware header
#     if suggestions:
#         if is_jenkins:
#             header = "// -- Jenkins Pipeline Optimization Suggestions --"
#             bullet = "// - "
#         elif is_terraform:
#             header = "# -- Terraform Optimization Suggestions --"
#             bullet = "# - "
#         else:
#             header = "# -- General Deployment Recommendations --"
#             bullet = "# - "

#         content += f"\n\n{header}\n" + "\n".join(f"{bullet}{s}" for s in suggestions)

#     state.Devops_output = content
#     return state

from .devops_types import DevOpsState

def suggest_jenkins_optimizations(state: DevOpsState) -> DevOpsState:
    """
    Adds deployment strategy recommendations based on the detected infrastructure/tooling in the output.

    Args:
        state (DevOpsState): Current pipeline state.

    Returns:
        DevOpsState: Updated state with relevant suggestions.
    """
    content = state.Devops_output
    suggestions = []

    # Check if the content contains Terraform-specific keywords or patterns
    is_terraform = (
        "resource" in content.lower() or
        "provider" in content.lower() or
        "terraform" in content.lower() or
        "variable" in content.lower() or
        "module" in content.lower()
    )
    
    # Check if the content contains Jenkins-specific keywords
    is_jenkins = "pipeline" in content.lower() or "jenkins" in content.lower()

    # Debugging: Print detection status
    print(f"Terraform detected: {is_terraform}")
    print(f"Jenkins detected: {is_jenkins}")

    # Terraform-specific suggestions
    if is_terraform:
        suggestions.append("Use workspaces for dev/staging/prod. Automate with GitHub Actions using init, "
                           "validate, plan, and apply steps. Store state securely using S3 and DynamoDB.")
    
    # Jenkins-specific suggestions (only if no Terraform content is detected)
    if is_jenkins and not is_terraform:
        suggestions.append("Automate Jenkins pipeline with stages like Build, Test, Deploy. "
                           "Ensure proper error handling and post-build actions.")

    # General suggestions for DockerHub and Kubernetes
    if "dockerhub" in content.lower():
        suggestions.append("Use Docker tags and enable automated builds in DockerHub. "
                           "Set up webhooks to trigger builds and deployments on image push.")

    if "kubernetes" in content.lower():
        suggestions.append("Use rolling updates or blue/green deployments in Kubernetes with readiness probes "
                           "for zero-downtime rollouts.")

    # Add suggestions under a context-aware header
    if suggestions:
        if is_terraform:
            header = "# -- Terraform Optimization Suggestions --"
            bullet = "# - "
        elif is_jenkins:
            header = "// -- Jenkins Pipeline Optimization Suggestions --"
            bullet = "// - "
        else:
            header = "# -- General Deployment Recommendations --"
            bullet = "# - "

        content += f"\n\n{header}\n" + "\n".join(f"{bullet}{s}" for s in suggestions)

    state.Devops_output = content
    return state
