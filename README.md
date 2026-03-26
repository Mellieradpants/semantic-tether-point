Traceability Constraint System
Experimental Architecture

What This System Does

The Traceability Constraint System enforces a single rule:

Every output must remain directly traceable to explicit source text.

If a piece of information cannot be traced to the source, it is not included in the output.

Project Summary

The system prevents meaning from drifting away from the original text.

It does this by requiring every output to:

reference a specific source anchor
include only what the source text explicitly supports

There is no summarizing, guessing, or adding meaning beyond what is written.

Core Rule

Every output must meet both conditions:

it must link to a clear source anchor
it must not include anything the anchor does not support

If the source text does not support it, the system does not output it.

What “Anchor” Means

An anchor is the exact piece of source information the output is derived from.

Examples include:

a quote
a document section
a page reference
a timestamp
a metadata field

All outputs must be tied directly to one of these.

How the System Works

The system follows a constrained parsing pipeline:

Document → identify anchor → extract explicit content → restate without adding meaning → link output to anchor

No new meaning is introduced at any stage.

Output Structure

Each output includes three parts:

Anchor
The exact source text or location

Observation
What is explicitly present in the text (words, requirements, conditions)

Source Derived Text
A restatement that preserves the exact meaning of the source text without adding or altering information

Example:

{
  "document": "example-policy.txt",
  "analysis": [
    {
      "anchor": {
        "type": "quote",
        "location": "Section 3",
        "text": "Applicants must submit documentation within 30 days."
      },
      "observation": "Includes a requirement ('must') and a time constraint ('within 30 days').",
      "sourceDerivedText": "Applicants must submit documentation within 30 days."
    },
    {
      "anchor": {
        "type": "quote",
        "location": "Section 5",
        "text": "The agency may extend deadlines under exceptional circumstances."
      },
      "observation": "Includes conditional language ('may') and a condition ('under exceptional circumstances').",
      "sourceDerivedText": "The agency may extend deadlines under exceptional circumstances."
    }
  ]
}

Problem

Many systems generate outputs that include details not directly tied to the source.

This makes it difficult to verify how the output was produced.

Solution

Require all outputs to remain anchored to source text.

no added facts
no hidden assumptions
no inference
no interpretation beyond what is explicitly stated

If it cannot be traced to the source, it is not included.

Why This Matters

Each part of the output can be traced to a specific source.

This makes the system:

verifiable
consistent
suitable for high-accuracy use cases

Potential Uses

policy analysis
contracts
legislation
journalism
technical documentation

Status

Early prototype.

Implements drift control by enforcing source anchoring and constraint rules.

Current Engine Output

The current prototype produces tetherAnchor objects using a consistent structure.

Each result includes:

group
type
sourceSystem
sourceLocation
anchorText
sourceDerivedText
matchedSignals
traceReason
driftDetected
status

All outputs follow a traceable, structured format
