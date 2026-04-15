# Phase 9 — Variation

**Actor:** AI

## Purpose

Split stories by subtype when mechanics differ; add failure modes. Subtype concepts already exist from Phase 4; Variation does not discover them.

## Trigger

variation, subtype stories, failure modes, split by mechanics

## Inputs

- `generated/solution_model.json` v2 (from Behavior)

## Instructions

- Split stories by subtype when mechanics differ (per Story vs Scenario rule)
- Add failure-mode scenarios
- Do not discover new subtypes — work with existing concepts from hypothesis

## Outputs

`generated/solution_model.json` v3 — interaction_tree gains subtype stories, failure-mode scenarios
