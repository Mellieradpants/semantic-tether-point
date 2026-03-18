This prototype uses the v2 extractor as the current reference implementation.

Running the Prototype

What This Does

This script shows how the Semantic Tether Point system works on a small example.

It takes source text, finds anchors, and produces output that stays tied to those anchors.

Requirements

Python 3.x

Run the Prototype

From the root of the repository:

python real_tether_extractor_v2.py <document>
 
Current Output Format

The current extractor outputs results using the shared tetherAnchor structure.

Each result includes:
- group
- type
- sourceSystem
- sourceLocation
- anchorText
- structuredValue
- matchedSignals
- traceReason
- driftDetected
- status                                    

What You Will See

The script outputs structured results with three fields:

anchor

observation

operationalMeaning

Each result is tied directly to a piece of source text.

Example Flow

The current extr

document
→ find anchor
→ detect what is in the text
→ restate it in plain language
→ output linked to the anchor

Core Rule Being Tested

Every output must:

point to a specific source anchor

only include what that anchor supports

If the source text does not support something, it is not included in the output.

Important Constraint

No added meaning

No assumptions

No interpretation beyond what is written

If a result cannot be traced to the source text, it is not produced.

Purpose

This prototype shows how to keep outputs tied to source text.

It demonstrates how to:

prevent meaning from drifting

make outputs traceable

keep the system consistent and repeatable

This version removes:

“interpretation drift” language as a concept

“return to tether point” metaphor

And replaces it with:

hard rules

observable steps

deterministic behavior
