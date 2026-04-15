# Phase 7 — Structure

**Actor:** AI

## Purpose

Build first `solution_model.json` from hypothesis + evidence index. Assign properties, inheritance, steps; concepts and tree gain structure in parallel.

## Trigger

structure, structural model, relationships, composition, collaborators

## Inputs

- `generated/hypothesis.json`
- `evidence/evidence_index.json`

## Instructions

- Create `solution_model.json` with concepts, behaviors, interaction_tree, evidence_refs
- Define composition relationships; attach collaborators
- Ground relationships in evidence (from_entity → type → to_entity)
- Use evidence/states.json for state-based relationships
- Use evidence/decisions.json for conditional relationships
- Preserve subtype structure from hypothesis

## Outputs

`generated/solution_model.json` v1 — concepts gain story_refs, evidence_refs, properties, relationships, kind; interaction_tree gains stories, steps (actors, pre-conditions), empty linked_behaviors
