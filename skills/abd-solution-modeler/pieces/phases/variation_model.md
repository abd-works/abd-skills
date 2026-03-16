# Phase 9 — Variation Model

**Actor:** AI | 
## Purpose

Model inheritance/strategy/modifier variation.

**Interaction detail:** Additional detail to interaction based on variation analysis.

## Trigger

variation model, inheritance, strategy, variation paths

## Inputs

`modifiers.json`, `terms.json`, `decisions.json`, `interaction_tree.md`

## Instructions

- **Build inheritance hierarchies from `terms.json`** — scan for subtype candidates (e.g. named Effect subtypes, Check subtypes) rather than relying on background knowledge
- **Build variation paths from `decisions.json`** — conditional branches are in the extracted decisions
- Model Extras/Flaws from `modifiers.json`

## Outputs

`generated/domain/variation_model.md`, `generated/interaction_model/interaction_tree.md`
