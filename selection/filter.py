select_nodes(structure_output)
from typing import Dict, Any, List


def build_working_set(structure_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Layer 3 — Selection

    Purpose:
    Filter structured nodes into a working set.

    Rules:
    - deterministic only
    - preserve order
    - do not modify node content
    - do not interpret meaning
    """

    document_id = structure_output.get("documentId")
    input_type = structure_output.get("inputType")
    nodes = structure_output.get("nodes", [])

    errors: List[str] = []

    if not structure_output.get("canProceed", False):
        return _fail(document_id, input_type, ["Structure layer failed"])

    if not nodes:
        return _fail(document_id, input_type, ["No nodes available for selection"])

    selected_nodes = []

    for node in nodes:
        if _is_valid_node(node):
            selected_nodes.append(node)

    if not selected_nodes:
        return _fail(document_id, input_type, ["No nodes passed selection rules"])

    return {
        "documentId": document_id,
        "inputType": input_type,
        "selectedNodes": selected_nodes,
        "selectionErrors": [],
        "canProceed": True,
    }


def _is_valid_node(node: Dict[str, Any]) -> bool:
    """
    Deterministic filtering rules only.
    """

    text = node.get("text", "")

    # Rule 1: must have text
    if not text or not text.strip():
        return False

    # Rule 2: ignore extremely short fragments
    if len(text.strip()) < 3:
        return False

    return True


def _fail(document_id: str, input_type: str, messages: List[str]) -> Dict[str, Any]:
    return {
        "documentId": document_id,
        "inputType": input_type,
        "selectedNodes": [],
        "selectionErrors": messages,
        "canProceed": False,
    }
