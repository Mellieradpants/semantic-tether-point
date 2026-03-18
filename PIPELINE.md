PIPELINE.md
Semantic Tether Point Pipeline

Goal

Keep all outputs tied directly to source text.

The system only outputs what can be traced to a specific anchor.

Pipeline Overview

Document Input

A document or text enters the system.

Anchor Extraction

The system identifies anchor points such as:

quoted text

section headers

timestamps

metadata fields

structured identifiers

Each anchor is a direct reference to source content.

Anchor Matching

Each output must link to one of the extracted anchors.

If no anchor supports the output, the output is not generated.

Feature Detection

The system identifies what is explicitly present in the anchor.

Examples:

requirement words (must, may, should)

time constraints (within 30 days)

conditions (if, under, when)

actors (agency, applicant)

No interpretation is added in this step.

Constrained Restatement

The system restates the anchor in plain language.

Rules:

use only information present in the anchor

do not add new facts or conditions

keep meaning equivalent to the source text

Output Generation

Each result follows this structure:

Anchor
→ Observation
→ Operational Meaning

All fields must be traceable to the anchor.

Drift Control

Before output is finalized:

check that all content is supported by the anchor

check that no new information was added

If a check fails, the output is not produced.

Output Structure

Anchor
Source text or reference

Observation
What is explicitly present in the text

Operational Meaning
Plain-language restatement of the same content

Pipeline Diagram

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

What Changed (implicitly in this version)

removed “interpretation” as a free step

removed “uncertainty” language

removed “return to tether” metaphor

replaced with strict pass/fail rules

