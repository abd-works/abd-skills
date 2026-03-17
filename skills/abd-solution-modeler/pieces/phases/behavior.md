# Phase 8 — Behavior

**Actor:** AI

## Purpose

Assign operations to concepts by decision ownership; link each behavior to the step(s) that exercise it; group steps into scenarios.

## Trigger

behavior model, assign operations, trigger response, linked behaviors

## Inputs

- `generated/solution_model.json` v1 (from Structure)

## Instructions

- Assign operations to concepts based on interaction steps
- Link each step to at least one behavior (linked_behaviors)
- Group steps into scenarios (e.g. hit vs miss)
- Add Trigger, Response to steps

## Outputs

`generated/solution_model.json` v2 — concepts gain operations, behavior_refs; interaction_tree gains linked_behaviors, when_then, scenarios
