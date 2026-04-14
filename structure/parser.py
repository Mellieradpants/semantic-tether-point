from typing import Any, Dict, List

# You will port these from your TS code
# from your existing logic:
# preprocess_xml
# parse_xml_to_nodes


def build_structure(document_id: str, raw_text: str, input_type: str) -> Dict[str, Any]:
    """
    Layer 2 — Structure

    Responsibilities:
    - preprocess XML
    - parse into nodes
    - normalize node output
    - preserve order + structure
    """

    try:
        if input_type == "xml":
            normalized_xml, detection = preprocess_xml(raw_text)

            if detection.get("unsupportedSchemaReason"):
                return _fail(document_id, input_type, detection["unsupportedSchemaReason"])

            raw_nodes = parse_xml_to_nodes(normalized_xml)

        else:
            return _fail(document_id, input_type, f"Unsupported input type: {input_type}")

    except Exception as e:
        return _fail(document_id, input_type, str(e))

    if not raw_nodes:
        return _fail(document_id, input_type, "No structural nodes extracted")

    nodes = _normalize_nodes(raw_nodes)

    return {
        "documentId": document_id,
        "inputType": input_type,
        "nodes": nodes,
        "errors": [],
        "canProceed": True,
    }


def _normalize_nodes(raw_nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert existing node shape into system node shape.
    """

    normalized: List[Dict[str, Any]] = []

    for idx, node in enumerate(raw_nodes, start=1):
        normalized.append({
            "nodeId": node.get("id") or f"node-{idx}",
            "text": node.get("text", "").strip(),
            "path": _build_path(node),
            "sourceRef": {
                "type": node.get("type", "unknown"),
                "locator": node.get("id", ""),
            },
            "order": idx,
        })

    return normalized


def _build_path(node: Dict[str, Any]) -> str:
    """
    Deterministic path builder.
    """

    parts: List[str] = []

    if node.get("parentId"):
        parts.append(str(node["parentId"]))

    if node.get("id"):
        parts.append(str(node["id"]))

    return "/".join(parts)


def _fail(document_id: str, input_type: str, message: str) -> Dict[str, Any]:
    return {
        "documentId": document_id,
        "inputType": input_type,
        "nodes": [],
        "errors": [message],
        "canProceed": False,
    }
