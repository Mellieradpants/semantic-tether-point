import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Tuple


# =========================
# XML COMPATIBILITY LAYER
# =========================

CANONICAL = {
    "root": "act",
    "part": "part",
    "section": "section",
    "subsection": "subsection",
    "clause": "clause",
    "title": "heading",
    "text": "content",
    "id": "id",
}

ROLE_ALIASES = {
    "root": ["act", "bill", "measure"],
    "part": ["part", "chapter", "division"],
    "section": ["section", "sec"],
    "subsection": ["subsection", "subsec"],
    "clause": ["clause", "paragraph", "item"],
    "title": ["heading", "title", "head"],
    "text": ["content", "text", "body"],
    "id": ["id"],
}


def preprocess_xml(raw_text: str) -> Tuple[str, Dict[str, Any]]:
    try:
        root = ET.fromstring(raw_text)
    except Exception:
        return raw_text, {
            "schemaDetected": None,
            "mappingUsed": None,
            "fallbackUsed": True,
            "unsupportedSchemaReason": None,
        }

    root_tag = root.tag.lower()

    all_known_tags = set(t for v in ROLE_ALIASES.values() for t in v)
    generic_roots = {"act", "bill", "statute", "regulation", "law", "legislation", "document", "body"}

    if root_tag not in all_known_tags and root_tag not in generic_roots:
        child_tags = {child.tag.lower() for child in list(root)}
        structural = set(
            ROLE_ALIASES["part"]
            + ROLE_ALIASES["section"]
            + ROLE_ALIASES["subsection"]
            + ROLE_ALIASES["clause"]
        )

        if not any(tag in structural for tag in child_tags):
            return raw_text, {
                "schemaDetected": None,
                "mappingUsed": None,
                "fallbackUsed": False,
                "unsupportedSchemaReason": f"Unsupported root element <{root_tag}> with no recognized structural children.",
            }

    if root_tag == CANONICAL["root"]:
        return raw_text, {
            "schemaDetected": "canonical",
            "mappingUsed": None,
            "fallbackUsed": True,
            "unsupportedSchemaReason": None,
        }

    mapping = {root_tag: CANONICAL["root"]}

    for role in ["part", "section", "subsection", "clause", "title"]:
        for alias in ROLE_ALIASES[role]:
            if alias == CANONICAL[role]:
                continue
            if root.findall(f".//{alias}"):
                mapping[alias] = CANONICAL[role]

    if len(mapping) <= 1:
        if root_tag in ROLE_ALIASES["root"]:
            structural_aliases = (
                ROLE_ALIASES["part"]
                + ROLE_ALIASES["section"]
                + ROLE_ALIASES["subsection"]
                + ROLE_ALIASES["clause"]
            )
            return raw_text, {
                "schemaDetected": None,
                "mappingUsed": None,
                "fallbackUsed": False,
                "unsupportedSchemaReason": f"Root <{root_tag}> has no recognized structural roles. Expected one of: {', '.join(structural_aliases)}",
            }

        return raw_text, {
            "schemaDetected": "canonical",
            "mappingUsed": None,
            "fallbackUsed": True,
            "unsupportedSchemaReason": None,
        }

    normalized = raw_text

    for source, target in mapping.items():
        if source == target:
            continue

        normalized = re.sub(
            rf"<{source}(\s|>|/>)",
            lambda m: f"<{target}{m.group(1)}",
            normalized,
            flags=re.IGNORECASE,
        )

        normalized = re.sub(
            rf"</{source}>",
            f"</{target}>",
            normalized,
            flags=re.IGNORECASE,
        )

    mapping_used = {}
    for source, target in mapping.items():
        for role, canonical in CANONICAL.items():
            if target == canonical and source != canonical:
                mapping_used[role] = f"{source} → {canonical}"

    return normalized, {
        "schemaDetected": f"{root_tag}-based",
        "mappingUsed": mapping_used if mapping_used else None,
        "fallbackUsed": False,
        "unsupportedSchemaReason": None,
    }


# =========================
# STRUCTURE PARSER
# =========================

TAG_TYPE_MAP = {
    "act": "part",
    "bill": "part",
    "statute": "part",
    "regulation": "part",
    "part": "part",
    "chapter": "part",
    "title": "part",
    "division": "part",
    "book": "part",
    "section": "section",
    "article": "section",
    "rule": "section",
    "subsection": "subsection",
    "subdivision": "subsection",
    "paragraph": "subsection",
    "subparagraph": "clause",
    "clause": "clause",
    "subclause": "clause",
    "item": "clause",
    "point": "clause",
}

DEPTH_TYPE_FALLBACK = ["part", "section", "subsection", "clause"]

SKIP_TAGS = {
    "heading",
    "title",
    "num",
    "label",
    "meta",
    "header",
    "footer",
    "note",
    "footnote",
    "annotation",
    "comment",
}


def build_structure(document_id: str, raw_text: str, input_type: str) -> Dict[str, Any]:
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


def parse_xml_to_nodes(xml: str) -> List[Dict[str, Any]]:
    root = ET.fromstring(xml)
    nodes: List[Dict[str, Any]] = []
    counter = {"value": 0}

    def next_id():
        counter["value"] += 1
        return f"node-{counter['value']}"

    def resolve_type(tag: str, depth: int) -> str:
        return TAG_TYPE_MAP.get(tag, DEPTH_TYPE_FALLBACK[min(depth, 3)])

    def walk(el, parent_id, depth):
        tag = el.tag.lower() if isinstance(el.tag, str) else ""

        if not tag or tag in SKIP_TAGS:
            return

        node_id = el.attrib.get("id", next_id())
        text = (el.text or "").strip()

        nodes.append({
            "id": node_id,
            "parentId": parent_id,
            "text": text,
            "type": resolve_type(tag, depth),
        })

        for child in list(el):
            walk(child, node_id, depth + 1)

    walk(root, None, 0)
    return nodes


def _normalize_nodes(raw_nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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
 