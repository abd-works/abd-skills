# Phase 3 — Extract Concepts

**Actor:** Code

## Purpose

Extract concept signals (unguided) from chunks and write term_candidates, definition_candidates, dependency_actions, cooccurrence_graph, table_vocabularies. Deterministic, fast.

## Trigger

extract concepts, concept signals, term candidates, definition candidates

## Inputs

- `context/context_chunks.json` — from Phase 1
- Optional: `generated/extraction_config.json` — from Phase 2 (weights, patterns)

## Outputs

- `concept_signals/term_candidates.json`
- `concept_signals/definition_candidates.json`
- `concept_signals/dependency_actions.json`
- `concept_signals/cooccurrence_graph.json`
- `concept_signals/table_vocabularies.json`

## Run

```bash
python scripts/pipeline.py generate extract_concepts
```

Script: `scripts/extract_concepts.py`
