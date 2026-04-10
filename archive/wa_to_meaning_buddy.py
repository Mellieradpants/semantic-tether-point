import json
from pathlib import Path


INPUT_PATH = Path("output_structured.json")
OUTPUT_PATH = Path("meaning_buddy_input.json")


if not INPUT_PATH.exists():
    raise FileNotFoundError(f"Missing {INPUT_PATH}")


data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
units = data.get("units", [])


def detect_layer(unit_type: str) -> str:
    if unit_type == "header":
        return "origin"
    return "parse"


meaning_buddy_units = []

for unit in units:
    meaning_buddy_units.append(
        {
            "id": unit.get("id"),
            "parentId": unit.get("parentId"),
            "label": unit.get("label", ""),
            "type": unit.get("type", ""),
            "title": unit.get("title", ""),
            "sourceText": unit.get("text", ""),
            "layer": detect_layer(unit.get("type", "")),
            "meaning": None
        }
    )


output = {
    "documentType": "wa_legislation",
    "sourceFormat": "wa_legislature_xml",
    "pipeline": {
        "origin": "live-wa-response.xml",
        "parse": "output_structured.json",
        "meaning": "meaning_buddy_input.json"
    },
    "units": meaning_buddy_units
}


OUTPUT_PATH.write_text(
    json.dumps(output, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print(f"Wrote {OUTPUT_PATH}")
print(f"Units: {len(meaning_buddy_units)}")
