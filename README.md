# Traceability Constraint System

## Overview

The Traceability Constraint System is a deterministic parsing engine designed to extract structured, traceable signals from source text.

The system enforces a single rule:

Every output must remain directly traceable to explicit source text.

If a piece of information cannot be traced to the source, it is not included in the output.

This repository contains a backend processing pipeline, not a user-facing application.

---

## What This System Does

The system processes real legislative XML (Washington State bill text) and converts it into structured outputs that preserve:

- source anchoring
- explicit meaning
- traceable structure

There is no summarizing, guessing, or adding meaning beyond what is written.

---

## Core Rule

Every output must meet both conditions:

- It must link to a clear source anchor  
- It must not include anything the anchor does not support  

If the source text does not support it, the system does not output it.

---

## What “Anchor” Means

An anchor is the exact piece of source information the output is derived from.

Examples include:

- text span (quote)
- document section
- structured identifier
- metadata field
- timestamp

All outputs must be tied directly to one of these.

---

## Pipeline Architecture

The system follows a constrained processing pipeline:

Fetch → Adapter → Parser → Structured Output

### 1. Fetch Layer
- Retrieves live legislative XML (bill body, not metadata)
- Writes raw response as bytes to preserve encoding integrity

### 2. Adapter Layer
- Converts XML into normalized text blocks
- Supports real bill structure:
  - BillBody
  - BillTitle
  - Sections / paragraphs
- Handles encoding issues (BOM, malformed leading bytes)

### 3. Parser Layer
- Detects explicit signal language:
  - obligation (shall, must)
  - permission (may)
  - conditions (if, when)
- Produces structured outputs with:
  - tether anchors
  - signal classification
  - trace reasoning

### 4. Output
- Structured JSON
- Fully traceable to source text
- Deterministic (same input → same output)

---

## Output Structure

Each result includes:

- tetherAnchor  
  - group  
  - type  
  - sourceSystem  
  - sourceLocation  
  - anchorText  
  - sourceDerivedText  
  - matchedSignals  
  - traceReason  

- parse (structured breakdown)  
- missingSignals  
- controlFlags  
- driftDetected  
- status  

All outputs remain directly tied to source text.

---

## Design Principles

- No inference beyond explicit source text  
- No added facts or assumptions  
- Deterministic output behavior  
- Full traceability to source  
- Strict separation of layers (fetch, adapter, parser)

---

## Reliability Safeguards

- XML is processed as raw bytes to prevent encoding corruption  
- UTF-8 BOM and malformed leading bytes are removed before parsing  
- Normalized output is deleted before regeneration to prevent stale data reuse  
- Pipeline fails loudly if parsing fails  

---

## Problem

Many systems generate outputs that include details not directly tied to the source.

This makes verification difficult and introduces hidden assumptions.

---

## Solution

This system enforces strict source anchoring:

- No inference  
- No interpretation beyond explicit text  
- No unsupported output  

If it cannot be traced to the source, it is not included.

---

## Why This Matters

Each output can be verified against its source.

This makes the system:

- auditable  
- consistent  
- suitable for high-accuracy use cases  

---

## Potential Uses

- legislation analysis  
- policy review  
- contracts  
- journalism  
- technical documentation  

---

## Status

Engine: Functional  
Data Source: Real legislative XML  
Pipeline: Stable  
Integration: Pending (external systems)

This system has moved from prototype input to real-world legislative processing.

---

## Role in Larger Systems

This engine is designed to be integrated into other tools (e.g., dashboards or analysis systems).

It should be treated as a standalone processing layer:

input → source text  
output → structured, traceable analysis
