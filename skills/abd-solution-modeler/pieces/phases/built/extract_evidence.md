# Phase 5 — Extract Evidence

**Actor:** Code

## Purpose

Mine chunks for actions, decisions, states, relationships, and terms, guided by hypothesis. Output: `evidence/*.json` (six files).

## Trigger

extract evidence, guided extraction, extract terms, extract actions, extract decisions

## Inputs

- `context/context_chunks.json` — text chunks extracted from the source material
- `generated/hypothesis.json` or `generated/domain/concept_guidance.json` — guidance produced in Phase 4:
  - priority concepts
  - concept aliases
  - priority mechanisms
  - actors
  - variation axes
  - noise filters
  - focus sections

## Outputs

`evidence/terms.json`, `evidence/actions.json`, `evidence/decisions.json`, `evidence/states.json`, `evidence/relationships.json`

## Run

```bash
python scripts/pipeline.py generate extract_evidence
```

Script: `scripts/evidence_extraction_guided.py`
