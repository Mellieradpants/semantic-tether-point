DESIGN.md
Semantic Tether Point – Design Rules

Rule 1: Output Requires an Anchor

Every output must reference a verified anchor.

An anchor is a direct reference to source text.

Examples:

quoted text

document sections

page numbers

timestamps

structured metadata fields

If no anchor exists, no output is generated.

Rule 2: Anchor Before Output

The system must extract anchors before producing any output.

Pipeline:

Document
→ Anchor extraction
→ feature detection
→ constrained restatement
→ structured output

No output is generated before an anchor is identified.

Rule 3: Traceability

Every part of the output must be traceable to its anchor.

This includes:

words used in the restatement

conditions

requirements

time references

If a part of the output cannot be traced to the anchor, it is removed.

Rule 4: No Added Information

The system must not add new facts, conditions, or implications.

Allowed:

direct restatement

simpler wording

reordered phrasing

Not allowed:

inferred outcomes

implied consequences

external context

Rule 5: Drift Control

Before output is finalized, the system checks:

does every part of the output match the anchor

is any new information introduced

If either check fails, the output is not produced.

Rule 6: No Guessing

The system does not guess, infer, or fill in missing information.

If the source text is incomplete or unclear:

the system outputs only what is present

or produces no output

Core System Rule

If it cannot be traced to the source, it is not included.

What changed (for your awareness, not needed in file)

removed “interpretation” as a free concept

removed “uncertainty” as a trigger

removed “return to tether” metaphor

replaced everything with pass/fail constraints
