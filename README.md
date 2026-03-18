Semantic Tether Point
Experimental Architecture

What This Project Does

Semantic Tether Point tests a simple rule:

Every output must stay tied to the exact source text.

If something cannot be traced back to the source, it should not be included.

Project Summary

Semantic Tether Point is a small system that prevents meaning from drifting away from the original text.

It does this by requiring every output to:

point to a specific piece of source text

only include what that text supports

There is no free summarizing, guessing, or adding extra meaning.

Core Rule

Every output must meet both conditions:

It must link to a clear source anchor

It must not include anything the anchor does not support

If the source text does not support it, the system does not output it.

What “Anchor” Means

An anchor is the exact piece of source information the output comes from.

Examples:

a quote

a document section

a page reference

a timestamp

a metadata field

All outputs must be tied directly to one of these.

How the System Works

The system follows a simple pipeline:

Document
→ find anchor
→ detect what is explicitly in the text
→ restate it in plain language
→ link the result back to the anchor

There is no step where new meaning is added.

Output Structure

Each output includes three parts:

Anchor
The exact source text or location

Observation
What is explicitly present in the text (words, requirements, conditions)

Operational Meaning
A plain-language restatement of the same text without adding new information
{
  "document": "example-policy.txt",
  "analysis": [
    {
      "anchor": {
        "type": "quote",
        "location": "Section 3",
        "text": "Applicants must submit documentation within 30 days."
      },
      "observation": "Includes a requirement ('must') and a time limit ('within 30 days').",
      "operationalMeaning": "Applicants are required to submit documentation within 30 days."
    },
    {
      "anchor": {
        "type": "quote",
        "location": "Section 5",
        "text": "The agency may extend deadlines under exceptional circumstances."
      },
      "observation": "Includes conditional language ('may') and a condition ('exceptional circumstances').",
      "operationalMeaning": "The agency is allowed to extend deadlines when exceptional circumstances occur."
    }
  ]
}
Problem

AI systems often produce summaries or explanations that include details not clearly tied to the original source.

This makes it difficult to verify how the output was created.

Solution

Keep every output tied to the source text.

no added facts

no hidden assumptions

no interpretation beyond what is written

If it cannot be traced to the source, it is not included.

Why This Matters

Users can see exactly where each part of the output comes from.

This makes the system:

easier to check

easier to trust

easier to use in high-accuracy environments

Potential Uses

policy analysis

contracts

legislation

journalism

technical documentation

Status

Early prototype.

Includes basic drift control by requiring all outputs to stay anchored to source text.

Current Engine Output

The current prototype outputs tetherAnchor objects using a shared structure.

Each result includes:
- group
- type
- sourceSystem
- sourceLocation
- anchorText
- structuredValue
- matchedSignals
- traceReason

This keeps all outputs in one consistent, traceable format.
