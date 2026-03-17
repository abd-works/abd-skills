---
name: abd-solution-modeler
description: >-
  Transforms raw context into a validated OO domain model and interaction tree.
  Pipeline: Guidance → Sketch → Refine. Use when the user wants to "model domain",
  "build interaction tree", "extract domain from rules", or "solution model".
license: MIT
metadata:
  author: agilebydesign
  version: "0.1.0"
---

# abd-solution-modeler

Transforms raw context (rules, requirements, documentation) into a **Domain model** and **Interaction tree (Story Map)**. Pipeline: Guidance → Sketch → Refine. Process is code-driven — scripts orchestrate phases; AI produces output when a phase invokes it.

## When to Activate

- User asks to "model domain", "build interaction tree", "extract domain from rules"
- Wants to "solution model" from rulebooks, specs, or documentation
- Has context and wants to produce validated Object Oriented Domain Model + interaction tree (Story Map and Story Spec By Exampled)

## Dependencies

**abd-context-to-memory** — Use for context preparation (chunk, index). Run before Phase 1 if source is documents. See `pieces/process.md` for details.

## Spec and Plan

- **Full spec:** `docs/requirements.md` — phases, formats, outputs, checkpoints
- **Implementation plan:** `docs/plan.md` — skill structure, dependencies, implementation order

## Pipeline

12-phase concept-anchored pipeline (see `docs/concept-anchored-pipeline-overview.md`):

1. **Phases 1–6** — Normalize, configure extraction, extract concepts, concept synthesis, extract evidence, index
2. **Phases 7–12** — Structure, Behavior, Variation, Consolidate, Assess, Finalize (single artifact: solution_model.json)

## Scripts

Run from workspace root. Scripts in `skills/abd-solution-modeler/scripts/`.

- `pipeline.py generate <phase>` — Run phase (code phases execute; AI phases print instructions)
- `pipeline.py scan <phase>` — Run scanners against output
- `pipeline.py validate <phase>` — Print rules for validation
- `pipeline.py pipeline [--stop <phase>]` — Run phases 1–12 in sequence
- `assemble_agents.py` — Assemble AGENTS.md and build phase files. Run after editing `pieces/*.md`.
