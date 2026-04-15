# Phase 7 — Evidence index

**Actor:** Code

## Purpose

Build concept-anchored evidence index from evidence files. Output: `evidence_index.json` with concepts as keys and evidence IDs grouped by type.

## Trigger

evidence index, build evidence index, index evidence, concept-anchored index

## Inputs

`evidence/` — extraction outputs (terms.json, actions.json, decisions.json, states.json, relationships.json)

## Instructions

Create concept-anchored index:

- Concept → term_ids, performs, receives, states, decisions, relationships

## Outputs

`evidence/evidence_index.json`

## Run

```bash
python scripts/pipeline.py generate evidence_index
```

Script: `scripts/evidence_index.py`
