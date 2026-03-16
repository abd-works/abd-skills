# Phase 5 — Concept Guidance v2

**Actor:** AI | 
## Purpose

Refine domain structure using evidence graph.

**Domain detail:** Refined concepts, modules.

**Interaction detail:** Same — Epics, Sub-Epics, some stories where possible.

## Trigger

refine concepts, concept guidance v2, second-cut domain, epics and stories, interaction tree structure, refine structure, story placement

## Inputs

`generated/domain/concept_guidance.md`, `evidence/evidence_graph.json`, `evidence/terms.json`, `generated/interaction_model/interaction_tree.md`

## Instructions

### Domain
- merge duplicate concepts
- split overloaded concepts
- **detect hidden concepts by scanning `evidence/terms.json`** — do not rely on background knowledge; surface terms that appear frequently but are not yet in the concept list
- refine modules
- refine operations cautiously

### Interaction tree
- refine epic structure from v1
- add sub-epics under each epic
- place story names under sub-epics where evident
- Epics, Sub-Epics, some stories where possible — defer Trigger, Response, scenarios, steps to later phases
- **scan `performs` edges in `evidence/evidence_graph.json` for predicate clusters** — groups of verbs (e.g. grab, restrain, choke, redirect) that don't map to any existing epic indicate a missing epic or sub-epic; do not assume the v1 epic list is complete

## Outputs

`generated/domain/concept_guidance.md`, `generated/interaction_model/interaction_tree.md` (Epics, Sub-Epics, some stories)
