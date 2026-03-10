import json
import re
import sys
from pathlib import Path


def extract_anchors(document_text: str):
    anchors = []
    lines = [line.strip() for line in document_text.splitlines() if line.strip()]

    section_pattern = re.compile(r"^(Section\s+\d+):\s*(.+)$", re.IGNORECASE)

    for line in lines:
        match = section_pattern.match(line)
        if match:
            location = match.group(1)
            text = match.group(2).strip()

            anchors.append({
                "type": "quote",
                "location": location,
                "text": text
            })

    return anchors


def interpret_anchor(anchor):
    text = anchor["text"].lower()

    if "must" in text and "within 30 days" in text:
        observation = "A required action with a defined deadline is present."
        operational = "The person or group affected must complete the requirement within 30 days."
    elif "may" in text and "extend deadlines" in text:
        observation = "Discretionary authority to extend a deadline is present."
        operational = "The agency is allowed, but not required, to extend the deadline in exceptional cases."
    else:
        observation = "A policy statement is present but no specialized rule was matched."
        operational = "The statement should be reviewed directly against the source anchor before drawing conclusions."

    return observation, operational


def detect_drift(anchor_text: str, operational_meaning: str) -> bool:
    anchor_text = anchor_text.lower()
    operational_meaning = operational_meaning.lower()

    if "within 30 days" in anchor_text and "30 days" not in operational_meaning:
        return True

    if "extend deadlines" in anchor_text and "extend the deadline" not in operational_meaning:
        return True

    if "must" in anchor_text and "must" not in operational_meaning:
        return True

    return False


def build_analysis(document_path: Path):
    document_text = document_path.read_text(encoding="utf-8")
    anchors = extract_anchors(document_text)

    analysis = []

    for anchor in anchors:
        observation, operational = interpret_anchor(anchor)
        drift_detected = detect_drift(anchor["text"], operational)

        result = {
            "anchor": anchor,
            "observation": observation,
            "operationalMeaning": operational,
            "driftDetected": drift_detected,
            "recoveryAction": (
                "Return to tether point before continuing analysis."
                if drift_detected
                else "Tether verified."
            )
        }

        analysis.append(result)

    return {
        "document": str(document_path),
        "anchorCount": len(anchors),
        "analysis": analysis
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python prototype/real_tether_extractor.py <document_path>")
        sys.exit(1)

    document_path = Path(sys.argv[1])

    if not document_path.exists():
        print(f"Error: file not found: {document_path}")
        sys.exit(1)

    output = build_analysis(document_path)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
