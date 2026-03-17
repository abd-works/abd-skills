# Phase 4 — Concept Synthesis

**Actor:** AI

## Purpose

Merge concept signals from Phase 3 into a hypothesis. Output: `hypothesis.json` with concept_guidance.

## Trigger

concept synthesis, hypothesis, concept guidance, merge signals

## Inputs

- `concept_signals/*.json` — term_candidates, definition_candidates, dependency_actions, cooccurrence_graph, table_vocabularies

## Instructions

Synthesize concepts from the signals. Produce `hypothesis.json` with:

- **concepts** — candidate concepts with names
- **concept_guidance** (optional) — priority concepts, aliases, mechanisms, actors, variation axes, noise filters for Phase 5

## Outputs

- `generated/hypothesis.json`

## Run

```bash
python scripts/pipeline.py generate concept_synthesis
```
