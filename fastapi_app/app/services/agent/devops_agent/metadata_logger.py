import json
from datetime import datetime
from .devops_types import DevOpsState

def log_metadata(state: DevOpsState) -> DevOpsState:
    """
    Logs metadata for the DevOps agent including timestamps and transformation details.

    Args:
        state (DevOpsState): Current pipeline state.

    Returns:
        DevOpsState: Unchanged state, after logging.
    """

    # Compose a final log object similar to DB agent format
    final_log = {
        "procedure_name": "devops_transform_infra",  # Analogous field
        "original_code": state.Devops_input,
        "converted_code": state.Devops_output,
        "compatibility_flags": [],  # You can add logic to detect these later
        "optimization_suggestions": [],
        "comments": "",
        "timestamp": str(datetime.utcnow()),
        "status": "success"
    }

    # Output to console (or replace with file write if needed)
    print("\n===== DEVOPS AGENT FINAL OUTPUT =====\n")
    print(json.dumps(final_log, indent=2))

    return state