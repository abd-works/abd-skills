# Phase 10 — Consolidate

**Actor:** AI

## Purpose

Detect anemia, over-centralization, orphans; fix anti-patterns; add examples to stories.

## Trigger

consolidate, refine, anti-patterns, examples

## Inputs

- `generated/solution_model.json` v3 (from Variation)

## Instructions

- Detect and fix: anemia (concept with no operations), over-centralization (one concept does too much), orphans (unused concepts)
- Add examples to concepts and steps

## Outputs

`generated/solution_model.json` v4 — concepts gain examples; interaction_tree gains examples on steps
