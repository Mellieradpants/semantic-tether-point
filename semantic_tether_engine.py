"""
Traceability Constraint System — Core Engine

Purpose:
Produce outputs that are directly traceable to explicit source text.

Constraints:
- no inference
- no added information
- no narrative
- no unstated meaning

If content is not supported by source text, it is not included.
"""

import sys
import json
from pathlib import Path


def extract_explicit_signal_anchors(document_text: str):
    anchors = []
    lines = [line.strip() for line in document_text.splitlines()]

    for i, line in enumerate(lines):
        if not line:
            continue

        line_lower = line.lower()
        matched_signals = []

        if "must" in line_lower or "shall" in line_lower or "required" in line_lower:
            matched_signals.append("obligation")

        if "may" in line_lower:
            matched_signals.append("permission")

        if "cannot" in line_lower or "prohibited" in line_lower:
            matched_signals.append("prohibition")

        if not matched_signals:
            continue

        anchor_type = "text_span"

        if line_lower.startswith("section "):
            anchor_type = "section"

        anchors.append({
            "line": i + 1,
            "text": line,
            "type": anchor_type,
            "matchedSignals": matched_signals
        })

    return anchors


def build_traceable_output(document_path: Path):
    text = document_path.read_text(encoding="utf-8")
    anchors = extract_explicit_signal_anchors(text)

    results = []

    for anchor in anchors:
        result = {
            "tetherAnchor": {
                "group": "meaning",
                "type": anchor["type"],
                "sourceSystem": "traceability_constraint_system",
                "sourceLocation": f"line_{anchor['line']}",
                "anchorText": anchor["text"],
                "sourceDerivedText": anchor["text"],
                "matchedSignals": anchor["matchedSignals"],
                "traceReason": "Matched explicit signal language in source text"
            },
            "driftDetected": False,
            "status": "ok"
        }

        results.append(result)

    return {
        "document": str(document_path),
        "anchorCount": len(anchors),
        "analysis": results
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python semantic_tether_engine.py <document>")
        sys.exit(1)

    document_path = Path(sys.argv[1])

    if not document_path.exists():
        print(f"Error: file not found: {document_path}")
        sys.exit(1)

    output = build_traceable_output(document_path)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()



        



  
