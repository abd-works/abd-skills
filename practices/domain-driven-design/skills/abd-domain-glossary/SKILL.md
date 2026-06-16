---
name: abd-domain-glossary
catalog_garden_tier: practice
catalog_garden_order: 1
catalogue_one_liner: >-
  Build an organized domain glossary — terms grouped by Key Abstraction, KAs grouped into modules by shared concern.
description: >-
  Build a domain glossary: terms grouped under Key Abstractions, KAs grouped
  into modules by shared concern. Use when the user asks to "build a domain
  glossary", "define domain terms", "identify Key Abstractions", or needs
  agreed terminology before deeper modeling begins.
---
# abd-domain-glossary

## Purpose

Produce a **structured domain glossary** — terms grouped by Key Abstraction, Key Abstractions grouped into modules by shared concern — so that every downstream artifact (domain language, acceptance criteria, specification, code) draws from a single agreed vocabulary.

The primary output is a glossary, not a boundary diagram. Modules are the organizing container: a module groups the KAs and terms that share a core concern and can be understood together. Each module file contains:
- **Key Abstractions** — named building blocks that own a cluster of related terms
- **Terms per KA** — behavioral bullets and source references (exact file + location) per term
- **Boundary terms** — concepts this module depends on but does not own
- **Scope** — what region of the domain this module covers (emerges from the terms, not the other way around)

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

## Agent Instructions

### 1. Read context

Read every file listed under **Core concepts** above.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

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

Run the scanners:

```bash
python skills/execute-skill-using-skills-rules/scripts/run_scanners.py \
  --skill-root skills/abd-domain-glossary \
  --workspace <path-to-output>
```

Then emit per-rule verdicts for every rule in `rules/`.

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
