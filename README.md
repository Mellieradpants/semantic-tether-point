# Traceability Constraint System

## Overview

The Traceability Constraint System is a deterministic parsing and constraint engine designed to extract structured, traceable signals from source text.

It processes real legislative XML (Washington State bill text) and converts it into normalized text and structured outputs representing obligations, permissions, conditions, and constraints.

Every output is directly tied to explicit source text.  
If it cannot be traced to the source, it is not included.

This repository contains the core engine layer of a larger system.

---

## System Role

This repository is the core processing engine that powers higher-level tools, including the Washington Civic Dashboard.

It is responsible for:

- parsing source text
- enforcing traceability constraints
- extracting structured signals
- producing deterministic, source-linked outputs

This is not a user-facing application.

It is designed to be integrated as a backend engine into systems such as:

- Washington Civic Dashboard
- Meaning Buddy
- Origin Maps
- Verification systems

---

## Core Rule

Every output must meet both conditions:

- It must link to a clear source anchor  
- It must not include anything the anchor does not support  

If the source text does not support it, the system does not output it.

There is no summarizing, guessing, or adding meaning beyond what is written.
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

Fetch → Adapter → Parser → Structured Output

### Fetch Layer
- Retrieves live legislative XML (bill body, not metadata)
- Writes raw response as bytes to preserve encoding integrity

### Adapter Layer
- Converts XML into normalized text blocks
- Supports BillBody, BillTitle, Sections
- Handles encoding issues (BOM, malformed bytes)

### Parser Layer
- Detects:
  - obligation (shall, must)
  - permission (may)
  - conditions (if, when)

### Output
- Structured JSON
- Fully traceable
- Deterministic

## Design Principles

- No inference beyond explicit source text  
- No added facts or assumptions  
- Deterministic output  
- Full traceability  
- Separation of layers  

---

## Reliability Safeguards

- XML processed as raw bytes  
- BOM and malformed bytes removed  
- Normalized file deleted before regeneration  
- Pipeline fails loudly on errors  

---

## Project Structure

fetch_wa_legislation.py  
wa_legislature_adapter.py  
test_live_wa_adapter.py  
semantic_tether_engine.py  
traceability_parser.py  

---

## Status

Engine: Functional  
Data Source: Real legislative XML  
Pipeline: Stable  
Integration: In progress (Washington Civic Dashboard)

---

## Role in the Civic Dashboard

This engine is the backend processing layer.

The dashboard:
- sends data in  
- receives structured output  

The engine:
- parses  
- enforces constraints  
- extracts signals  

The dashboard only displays results.
