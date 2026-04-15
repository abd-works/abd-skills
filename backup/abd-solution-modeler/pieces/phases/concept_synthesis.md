# Phase 5 — Concept Synthesis

**Actor:** AI

## Purpose

Curate the concept list from Phase 4 (merge/split/kill), build hierarchy, allocate evidence. Reads source chunks via `chunk_ids` for semantic understanding.

## Trigger

concept synthesis, curate concepts, refine hypothesis, merge split kill, build hierarchy

## Inputs

- `generated/hypothesis.json` — concept index from Phase 4 (concepts, registries, concept_guidance, chunk_ids per concept)
- `context/` — source chunks (read via chunk_ids for semantic understanding)

## Instructions

1. **Curate concepts** — Merge duplicates, split overloaded concepts, remove noise. Use `chunk_ids` to read relevant source chunks; do not guess from chunks alone.
2. **Build concept_hierarchy** — Derive parent-child from evidence (shared mechanics, shared protocol, subtype patterns). See rules for hierarchy-from-evidence.
3. **Update concept_guidance** — priority_concepts, concept_aliases, mechanisms, actors, variation_axes, noise_filters.
4. **Allocate evidence** — Ensure term_ids, performs, receives, states, decisions, relationships are correctly assigned to curated concepts.

Subtype discovery happens here; Phase 10 (Variation) works with concepts that already exist.

## Outputs

- `generated/hypothesis.json` (refined) — concept_hierarchy, updated concept_guidance, evidence allocation

## Run

```bash
python scripts/pipeline.py generate concept_synthesis
```
