---
name: abd-domain-glossary
catalog_garden_tier: practice
catalog_garden_order: 1
catalogue_one_liner: >-
  Agree on one vocabulary everyone uses — so domain terms don't drift across artifacts and teams.
description: >-
  Build a domain glossary — terms grouped under Key Abstractions, KAs grouped into modules by shared concern. Use when agreed terminology is needed before deeper modeling begins.
context-perspective: domain
context-fidelity:
  - level: shaping
    mode: glossary
---
# abd-domain-glossary

## Purpose

Agree on one vocabulary everyone uses — so domain terms don't drift across artifacts and teams.

---

## Output file

**Deliverables folder:** `<active_skill_workspace>/domain/`

**Single file** (default): `domain/domain-glossary.md` — all modules, KAs, and terms in one file. Use this unless the system is large enough that one file becomes unnavigable.

**Per-module files** (large systems only): `domain/domain-glossary/<module-name>.md` — one file per module with its KAs and terms. Use when there are enough modules that a single file would be unwieldy.

---

## Core concepts

A **domain glossary** is a structured vocabulary for the domain — terms grouped under Key Abstractions, Key Abstractions grouped into modules by shared concern. Every claim traces to an exact source file and location on disk.

Read the supporting reference files before generating:
- **`reference/modules.md`** — what a module is and how to decide boundaries
- **`reference/key-abstractions.md`** — KA definition and the five aspects
- **`reference/terms.md`** — domain terms, boundary terms, and placement decisions
- **`reference/source-references.md`** — reference format and grouping rules

---

## Grill prompts

Read `common/grill-me-with-practice-skill.md` before grilling.

Before generating, surface these common input traps:

- **Overloaded terms** — which word means different things to different people in the organization — and where is that collision hiding?
- **Missing concepts** — what concepts does the team use in conversation but nobody has named yet — the implicit vocabulary that hasn't been surfaced?
- **Concept vs. property confusion** — which things are being treated as standalone concepts that are really just attributes of something else — and vice versa?
- **Module boundary assumptions** — are these terms grouped together because they genuinely share a concern, or because they appeared in the same document?
- **Boundary term ownership** — when a term is used here but owned elsewhere, do we actually know who owns it — or are we assuming?

---

## Agent Instructions

### 1. Read context

Read every file listed under **Core concepts** above.

### 2. Generate

**Produce output from the template:**

| Template | What to produce |
| --- | --- |
| `templates/module-file-template.md` | `domain/domain-glossary.md` (default) or one file per module under `domain/domain-glossary/` for large systems. |

**Every `Source:` reference must point to a real file on disk at an exact location.**

**Quality bar:**
- Single-noun module names, no kind-mixing
- Every KA intro opens with "*KAName* is …"
- `#### Decisions made` under each `## KA` — why these terms belong together
- Every `### term` has behavioral bullets; references at KA level under `### KA References`
- Boundary terms carry `*(owned by: Module)*`
- Domain terms *italicized* throughout

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/skill-rule-workflow.md` § Validate output.

---

## Validate

**Goal:** Read the glossary as a vocabulary reviewer.

- **KA inventory** — every KA intro paragraph opens with "*KAName* is …" and weaves role, responsibilities, relationships, and invariants.
- **Decisions under KA** — `#### Decisions made` appears under each `## KA`, not under terms. Records why these terms belong together.
- **Terms have behavioral bullets** — every `### term` has at least one behavioral bullet.
- **KA refs present** — every KA has a `### KA References` section; every term in the KA is covered by at least one reference entry pointing to an exact file and location on disk.
- **Boundary terms have owners** — every boundary term carries `*(owned by: Module)*`.
- **Domain terms italicized** — throughout bullets and KA intro paragraphs.
- **No kind-mixing** — each module is about one kind of thing.

---
