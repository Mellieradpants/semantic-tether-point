Traceability Constraint System — Design Rules

Rule 1: Output Requires an Anchor

Every output must reference a verified anchor.

An anchor is a direct reference to source text.

Examples:

quoted text
document sections
page numbers
timestamps
structured metadata fields

If no anchor exists, no output is produced.

Rule 2: Anchor Before Output

The system must extract anchors before producing any output.

Pipeline:

Document → Anchor Extraction → Feature Detection → Constrained Restatement → Structured Output

No output is produced before an anchor is identified.

Rule 3: Traceability

Every part of the output must be traceable to its anchor.

This includes:

words used in the restatement
conditions
requirements
time references

If a part of the output cannot be traced to the anchor, it is removed.

Rule 4: No Added Information

The system does not add, remove, or alter information.

Allowed:

direct restatement using the same information
reordering of phrasing without changing meaning

Not allowed:

inferred outcomes
implied consequences
external context
added or removed conditions
wording changes that alter meaning

Rule 5: Drift Control

Before output is finalized, the system verifies:

all content is supported by the anchor
no additional information was introduced

If either condition fails, the output is blocked.

Rule 6: No Guessing

The system does not guess, infer, or fill missing information.

If the source text is incomplete or unclear:

only explicit content is output
or no output is produced

Core Rule

If it cannot be traced to the source, it is not included.
