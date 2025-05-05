def suggest_jenkins_optimizations(state: dict) -> dict:
    jenkins_script = state.Devops_output
    suggestions = []

    if "agent any" in jenkins_script.lower():
        suggestions.append("Consider specifying a more granular agent label instead of 'any' to optimize resource usage.")
    
    if "sh './gradlew" in jenkins_script and "parallel" not in jenkins_script:
        suggestions.append("Consider using parallel stages to speed up build and test processes.")

    if "post {" not in jenkins_script.lower():
        suggestions.append("Include a 'post' section for better visibility into pipeline success or failure.")

    if "parameters {" not in jenkins_script.lower():
        suggestions.append("Use parameters to make the pipeline reusable for different environments or builds.")

    if suggestions:
        state.Devops_output += "\n\n// -- Jenkins Pipeline Optimization Suggestions --\n" + "\n".join(f"// - {s}" for s in suggestions)

    return state
