---
name: abd-map-model-spec-synthesizer
description: >-
  Synthesizes a map-model-spec (domain model + story map) from chunked context.
  Pipeline: Discover → Deepen → Canonicalize → Evidence → Structure → Finalize.
  Use when the user wants to "synthesize map model spec", "build story map from context",
  or "extract domain and stories from chunks".
license: MIT
metadata:
  version: "0.1.0"
---

# abd-map-model-spec-synthesizer

Synthesizes a **map-model-spec** (domain model + story map) from chunked context. Pipeline: Discover → Deepen → Canonicalize → Evidence → Structure → Finalize.

## When to Activate

- User asks to "synthesize map model spec", "build story map from context", "extract domain and stories from chunks"
- Has `context/context_chunks.json` and wants to produce a validated domain model + story map
- Wants module/epic pairs with concepts, stories, and evidence citations

## Inputs

- **Context:** From config. When `conf/abd-config.json` has `solution_workspace`, context path comes from `workspace/solution.conf` (default: `output_dir/context/context_chunks.json`). Otherwise `context/context_chunks.json` at skill root.
- Optional: `mms-junk-defaults.json` — junk term patterns for concept name validation

## Outputs

- `map-model-spec.json` — domain model + story map (modules, epics, concepts, stories)
- `map-model-spec.md` — readable summary
- `mms-chunk-index.json` — reverse index (chunk → concepts/epics/stories)
- `evidence/` — actions.json, decisions.json, states.json, relationships.json (Step 4)

## Structure

| Step | Part | Actor | Output |
|------|------|-------|--------|
| 1 | `parts/step1-discover.md` | AI | map-model-spec.json (scaffold), map-model-spec.md |
| 2 | `parts/step2-deepen.md` | AI | map-model-spec.json (deepened) |
| 3 | `parts/step3-canonicalize.md` | AI | map-model-spec.json (canonical) |
| 4 | `parts/step4-evidence.md` | Code | evidence/*.json |
| 5 | `parts/step5-structure.md` | AI | map-model-spec.json (structured) |
| 6 | `parts/step6-finalize.md` | AI | map-model-spec.json (final) |

## Scripts

- `scripts/build.py` — Assemble AGENTS.md from parts (run `python scripts/build.py`)
- `scripts/mms_build_chunk_index.py` — Build mms-chunk-index.json from map-model-spec.json
- Scanners (`scripts/mms_scan_*.py`): **Step 1–2:** chunks-must-be-referenced, no-duplicates, epic-requires-confirming-stories, no-junk-concepts, concepts-must-have-owns, stories-must-have-trigger-response, domain-interaction-sync, hierarchy-sizing. **Step 3:** + cross-cutting-resolved. **Step 4:** evidence-files-exist, evidence-scaffold-refs, evidence-schema. **Step 5–6:** structural scanners (no-duplicates, domain-sync, hierarchy, concepts-owns, stories-trigger-response). Exit 0 = pass, 1 = violations.

## Parts

- `parts/step1-discover.md` — Discover modules and epics (orientation)
- `parts/step2-deepen.md` — Deepen concepts and stories per module/epic
- `parts/step3-canonicalize.md` — Unify naming, resolve cross-cutting, finalize subtypes
- `parts/step4-evidence.md` — Evidence extraction (code)
- `parts/step5-structure.md` — AI builds full model from scaffold + evidence
- `parts/step6-finalize.md` — Behavior, variation, consolidate, assess, finalize
- `parts/domain.md` — Domain model format
- `parts/story-map.md` — Story map format (Epic → Sub-Epic → Story → Scenario → Step)

## Rules

Rules in `rules/` enforce quality per step. Scanners (`mms_scan_*.py`) check structural violations mechanically. AI performs adversarial validation pass after scanners. **Step 6 AI-only rules:** no-anemia, no-over-centralization, assessment-complete.
