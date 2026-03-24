Traceability Constraint System — Running the Prototype

Overview

This prototype uses the v2 extractor as the current reference implementation.

It demonstrates how the system processes source text and produces traceable outputs.

What This Does

The script:

takes source text
identifies anchors
detects explicit content
produces outputs linked directly to anchors

All outputs remain tied to source text.

Requirements

Python 3.x

Run the Prototype

From the root of the repository:

python real_tether_extractor_v2.py <document>

Current Output Format

The extractor outputs results using the tetherAnchor structure.

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

Output Fields

Each result contains:

anchor
Source text or location

observation
What is explicitly present in the text

sourceDerivedText
Plain-language restatement of the same content without adding or altering information

Example Flow

Document → Anchor Extraction → Feature Detection → Constrained Restatement → Structured Output

Core Rule

Every output must:

reference a specific source anchor
include only what the anchor supports

If the source text does not support it, it is not included.

Constraints

no added meaning
no assumptions
no inference
no interpretation beyond what is explicitly stated

If a result cannot be traced to the source text, it is not produced.

Purpose

This prototype demonstrates:

traceable outputs
constraint-based processing
prevention of meaning drift
consistent, repeatable behavior
