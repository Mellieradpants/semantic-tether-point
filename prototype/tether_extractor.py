import json
from pathlib import Path

document_path = Path("examples/example-policy.txt")
document = document_path.read_text()

anchors = [
    {
        "type": "quote",
        "location": "Section 3",
        "text": "Applicants must submit documentation within 30 days."
    },
    {
        "type": "quote",
        "location": "Section 5",
        "text": "The agency may extend deadlines under exceptional circumstances."
    }
]

analysis = []


def build_observation(anchor_text: str) -> str:
    anchor_text_lower = anchor_text.lower()

    features = []

    if "must" in anchor_text_lower:
        features.append("Includes a requirement ('must').")

    if "may" in anchor_text_lower:
        features.append("Includes permission or discretion ('may').")

    if "within 30 days" in anchor_text_lower:
        features.append("Includes a time limit ('within 30 days').")

    if "exceptional circumstances" in anchor_text_lower:
        features.append("Includes a condition ('exceptional circumstances').")

    if not features:
        return "No explicit feature detected."

    return " ".join(features)


def build_operational_meaning(anchor_text: str) -> str:
    if anchor_text == "Applicants must submit documentation within 30 days.":
        return "Applicants are required to submit documentation within 30 days."

    if anchor_text == "The agency may extend deadlines under exceptional circumstances.":
        return "The agency is allowed to extend deadlines under exceptional circumstances."

    return "No plain-language restatement available."


def detect_drift(anchor_text: str, operational_meaning: str) -> bool:
    allowed_pairs = {
        "Applicants must submit documentation within 30 days.": "Applicants are required to submit documentation within 30 days.",
        "The agency may extend deadlines under exceptional circumstances.": "The agency is allowed to extend deadlines under exceptional circumstances."
    }

    expected = allowed_pairs.get(anchor_text)
    if expected is None:
        return True

    return operational_meaning != expected


for anchor in anchors:
    observation = build_observation(anchor["text"])
    operational = build_operational_meaning(anchor["text"])
    drift_detected = detect_drift(anchor["text"], operational)

    result = {
        "anchor": anchor,
        "observation": observation,
        "operationalMeaning": operational,
        "driftDetected": drift_detected,
        "recoveryAction": "Output blocked: text not fully supported by anchor."
        if drift_detected
        else "Anchor check passed."
    }

    analysis.append(result)

output = {
    "document": str(document_path),
    "analysis": analysis
}

print(json.dumps(output, indent=2))
