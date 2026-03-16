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

## Outputs

`generated/domain/concept_model.md`, `generated/interaction_model/interaction_tree.md`
