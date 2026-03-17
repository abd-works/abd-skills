# Phase 7 — Structural Model

**Actor:** AI | 
## Purpose

Add relationships and composition between concepts.

**Interaction detail:** Add Triggering-Actor and Responding-Actor per story; additional stories as gleaned from structure; add long name; initiating and resulting state; pre-conditions.

## Trigger

structural model, relationships, composition, collaborators

## Instructions

- define composition relationships
- attach collaborators
- **Preserve subtype structure** — each subtype from concept_model must have its own section with its own composition and collaborators. Do not collapse subtypes into the parent.
- **Ground relationships in `evidence/relationships.json`** — scan the relationship evidence for `from_entity` → `type` → `to_entity` patterns. Only add relationships that evidence supports. Cite the evidence (e.g. `[rel_0042: "raw text"]`).
- **Use `evidence/states.json` for state-based relationships** — states describe what conditions/states concepts can be in, which reveals lifecycle and escalation relationships.
- **Use `evidence/decisions.json` for conditional relationships** — decisions describe when/if/must/cannot rules that reveal invariants and dependencies between concepts.

## Inputs

`generated/domain/concept_model.md`, `generated/interaction_model/interaction_tree.md`

## Outputs

`generated/domain/structural_model.md`, `generated/interaction_model/interaction_tree.md`
