
ARCHITECTURE.md
Semantic Tether Point Architecture

Goal

Keep all outputs tied directly to source text.

The system only outputs what can be traced to a specific anchor.

Problem

AI systems often produce summaries or explanations without showing where the information came from.

This breaks traceability and allows meaning to drift away from the source.

Core Rule

Every output must:

point to a specific source anchor

only include what that anchor supports

If the source does not support it, it is not included.

Core Flow

Document
→ Anchor Extraction
→ Feature Detection
→ Constrained Restatement
→ Structured Output

Anchor Types

An anchor is a direct reference to source content.

Examples:

quoted text

document sections

page numbers

timestamps

metadata fields

Output Structure

Each result includes three parts:

Anchor
Source text or location

Observation
What is explicitly present in the text

Operational Meaning
Plain-language restatement of the same content

System Behavior

anchors are identified before any output is generated

all outputs must link to an anchor

no output may include information not present in the anchor

if no valid anchor exists, no output is produced

Design Principle

If it cannot be traced to the source, it is not included
