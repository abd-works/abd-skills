# Phase 6 — Concept Model

**Actor:** AI | 
## Purpose

Identify core concepts and modules. Convert refined concepts into class-like model.

**Interaction detail:** Same depth as concept guidance but more fleshed out; more sub-epics; epics can have stories. Link concepts to stories. No Trigger, Response, steps yet.

## Trigger

concept model, core concepts, link concepts to stories

## Inputs

`generated/domain/concept_guidance.md`, `evidence/terms.json`, `evidence/actions.json`, `generated/interaction_model/interaction_tree.md`

## Instructions

- Convert refined concepts into class-like model with properties and operations
- **Ground properties and operations in `evidence/terms.json` and `evidence/actions.json`** — do not invent from background knowledge; use extracted evidence to confirm what each concept actually does
- **Cite evidence** — for each property and operation, include the evidence ID or raw text snippet that supports it (e.g. `[act_0042: "raw text"]`). If you cannot find evidence for a property/operation, mark it `[UNGROUNDED]` and consider removing it.
- **Read the concept guidance first** — the concept guidance describes what each concept does in interaction-oriented terms. Convert those descriptions into properties and operations. Do not skip concepts from the guidance.
- **Use `concept_hierarchy` as starting point** — the guidance JSON contains `concept_hierarchy` with subtypes and related concepts. Use this as the initial inheritance and composition map. Subtypes become `: Parent` concepts in the model. Related concepts become collaborators. Do not rediscover hierarchy from scratch — refine what guidance provides.
- **Read evidence files per concept** — for each concept, scan actions.json for entries where `matched_concepts` includes that concept name, and scan terms.json for the concept's term entry. Use the `raw` field text to derive properties and invariants.
- **Do not substitute background knowledge** — if the evidence says "X works like Y", model what the evidence says, not what you know about X from training data. The evidence may be from a domain you've seen before, but this model must reflect THIS source material's rules, not the canonical rules.

## Outputs

`generated/domain/concept_model.md`, `generated/interaction_model/interaction_tree.md`
