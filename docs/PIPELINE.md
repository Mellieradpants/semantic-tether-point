Traceability Constraint System — Pipeline

Goal

Ensure all outputs are directly traceable to explicit source text.

The system only produces outputs supported by a specific anchor.

Pipeline Overview

Document Input

A document or text enters the system.

Anchor Extraction

The system identifies anchor points, including:

quoted text
section headers
timestamps
metadata fields
structured identifiers

Each anchor is a direct reference to source content.

Anchor Matching

Each output must link to one extracted anchor.

If no anchor supports the output, the output is not produced.

Feature Detection

The system detects what is explicitly present in the anchor.

Examples:

requirement terms (must, may, should)
time constraints (within 30 days)
conditions (if, under, when)
actors (agency, applicant)

No interpretation is introduced in this step.

Constrained Restatement

The system restates the anchor in plain language.

Rules:

use only information present in the anchor
do not add facts or conditions
preserve the meaning of the source text

Output Generation

Each result follows a structured format:

Anchor → Observation → Source Derived Text

All fields must be traceable to the anchor.

Drift Control

Before output is finalized:

verify all content is supported by the anchor
verify no additional information was introduced

If a check fails, the output is blocked.

Output Structure

Anchor
Source text or reference

Observation
What is explicitly present in the text

Source Derived Text
Plain-language restatement of the same content without adding or altering information

Pipeline Flow

Document
↓
Anchor Extraction
↓
Anchor Matching
↓
Feature Detection
↓
Constrained Restatement
↓
Structured Output
↓
Drift Check

