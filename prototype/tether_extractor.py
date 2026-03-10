import json

document = """
Section 3: Applicants must submit documentation within 30 days.
Section 5: The agency may extend deadlines under exceptional circumstances.
"""

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

for anchor in anchors:
    if "30 days" in anchor["text"]:
        observation = "A strict submission deadline is defined."
        operational = "Applicants must provide documents within 30 days or risk rejection."
    elif "extend deadlines" in anchor["text"]:
        observation = "Deadline extensions are allowed."
        operational = "The agency can extend the deadline under special conditions."
    else:
        observation = "No rule detected."
        operational = "No operational meaning extracted."

    analysis.append({
        "anchor": anchor,
        "observation": observation,
        "operationalMeaning": operational
    })

output = {
    "document": "example-policy.txt",
    "analysis": analysis
}

print(json.dumps(output, indent=2))
