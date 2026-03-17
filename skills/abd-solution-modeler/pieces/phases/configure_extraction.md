# Phase 2 — Configure Extraction

**Actor:** AI

## Purpose

Scan the corpus and propose extraction parameters for concept extraction. Output: `extraction_config.json`.

## Trigger

configure extraction, extraction config, weights, patterns, grammar rules

## Inputs

- `context/context_chunks.json` — normalized chunks from Phase 1

## Instructions

Produce `extraction_config.json` with:

- **weights** — heading, default, and other weights for term scoring
- **patterns** — regex or grammar patterns for concept extraction
- **grammar rules** — optional grammar rules for dependency extraction

The config guides Phase 3 (Extract Concepts) code. Do not run extraction yet.

## Outputs

- `generated/extraction_config.json`

## Run

```bash
python scripts/pipeline.py generate configure_extraction
```
