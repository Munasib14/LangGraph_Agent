import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from langgraph.graph import StateGraph

# imports from sibling 'agent' folder
from devops_agent.devops_types import DevOpsState
from devops_agent.devops_types import refactor_devops
from devops_agent.transformer import transform_infra
from devops_agent.metadata_logger import log_metadata
from devops_agent.autoscaler import suggest_jenkins_optimizations
from devops_agent.monitoring_tool import suggest_monitoring_integration
from devops_agent.deployment_manager import recommend_deployment_strategy






def devops_agent_main(infra_code: str, prompt_name: str = "devops_infra.j2") -> DevOpsState:
    """
    Orchestrates the DevOps agent pipeline using LangGraph.

    Args:
        infra_code (str): The input infrastructure code (YAML, Terraform, etc.).
        prompt_name (str): The name of the prompt to use for transformation.

    Returns:
        DevOpsState: Final state after all nodes have run.
    """

    # Wrap transform to inject prompt name
    def transform_devops_with_prompt(state: DevOpsState) -> DevOpsState:
        return transform_infra(state, prompt_template=prompt_name)

    # Build LangGraph pipeline
    builder = StateGraph(DevOpsState)

    # Add core transformation node (you can add more later)    
    builder.add_node("transform_infra", transform_devops_with_prompt)
    builder.add_node("refactor_devops", refactor_devops)  # ⬅️ New node after transformation
    builder.add_node("log_metadata", log_metadata)
    builder.add_node("autoscale", suggest_jenkins_optimizations)
    builder.add_node("add_monitoring", suggest_monitoring_integration)
    builder.add_node("deployment_strategy", recommend_deployment_strategy)

    

    # Define execution flow
    builder.set_entry_point("transform_infra")
    builder.add_edge("transform_infra", "refactor_devops")  
    builder.add_edge("refactor_devops", "log_metadata")
    builder.add_edge("log_metadata", "autoscale")
    builder.add_edge("autoscale", "add_monitoring")
    builder.add_edge("add_monitoring", "deployment_strategy")

    # Compile graph and run the pipeline
    graph = builder.compile()
    return graph.invoke({"Devops_input": infra_code, "Devops_output": ""})

    #return graph.invoke(DevOpsState(input=infra_code, output=""))

# if __name__ == "__main__":
#     # Dummy test input
#     state = {
#     "input": '''
# pipeline {
#     agent any
#     environment {
#         APP_ENV = 'dev'
#     }
#     stages {
#         stage('Checkout') {
#             steps {
#                 git 'https://github.com/example/repo.git'
#             }
#         }
#         stage('Build') {
#             steps {
#                 sh './gradlew build'
#             }
#         }
#         stage('Test') {
#             steps {
#                 sh './gradlew test'
#             }
#         }
#         stage('Deploy') {
#             steps {
#                 echo 'Deploying to dev environment...'
#             }
#         }
#     }
# }
# ''',
#     "output": ""
# }

#     result = transform_infra(state)
#     print("🔧 Transformed Infra Output:\n", result["output"])
