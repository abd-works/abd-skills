# Phase 4 — Concept Index

**Actor:** Code

## Purpose

Merge concept signals from Phase 3 into a hypothesis (concept index). Output: `hypothesis.json` in concepts + registries format, with **chunk_ids** per concept for Phase 5 Concept Synthesis.

## Trigger

concept index, hypothesis, concept guidance, merge signals

## Inputs

- `concept_signals/concept_signals.json` — combined signals from Phase 3 (tf_weights, dependency_verbs, actor_detection, centrality, etc.)

## Instructions

**Code phase.** Builds `hypothesis.json` from concept signals. Output format:

- **concepts** — object keyed by concept name; each has `term_ids`, `performs`, `receives`, `states`, `decisions`, `relationships`, **chunk_ids** (list of chunk IDs that touch this concept)
- **registries** — `actions` (act_XXXX from dep_id), `decisions`, `states`, `relationships`; Phase 3 provides actions only; Phase 6 (`evidence_extraction`) fills the rest
- **concept_guidance** — priority_concepts, concept_aliases, mechanisms, actors, variation_axes, noise_filters for Phase 5 (Concept Synthesis)

**Workspace curation:** `solution/concept_guidance.json` can override:

- **priority_concepts** — list of **foundational** concepts in order of importance. Not volume-based (e.g. a base type like "Transaction" matters more than a frequent subtype like "Refund"). Curate by domain structure.
- **concept_aliases** — canonical → [alias] mappings (e.g. `"Transaction": ["Txn"]`)

`chunk_ids` are aggregated from all evidence signals: tf_weights, dependency_verbs, definition_patterns, table_mining, enumeration_patterns, contrast_patterns, verb_interaction.sample_interactions.

## Outputs

- `generated/hypothesis.json`

## Run

```bash
python scripts/pipeline.py generate concept_index
```
