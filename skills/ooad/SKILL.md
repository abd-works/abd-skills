---
name: abd-ooad
description: >-
  **Object-Oriented Analysis and Design (OOAD) from raw material.** Use this skill whenever you're working with specifications, game manuals, policy docs, messy code, or rule books that need to be modeled as object-oriented domain models. Agile by Design methodology: Steps 0–2 (Domain Scan, Extraction, Refinement) with built-in Draw.io diagram generation via scripts/drawio_cli.py. ALWAYS use this skill when a user provides domain material and asks you to extract domain concepts, build class diagrams, identify responsibilities, or create object models. Create domain-scan-model.md and domain-scan-model.drawio files in the project workspace.
license: MIT
metadata:
  author: agilebydesign
  version: "1.0.0"
  capabilities:
    - workspace: "Ability to specify project workspace directory where domain models are created"
    - diagram-templates: "Built-in Draw.io diagram generation via scripts/drawio_cli.py and templates/"
    - term-registry: "Track Terms with Classification (model role: anchor (class + module), class, property, …) and Status (OOAD scale: Ambiguous → … → Solidified) in term-registry.md"
---

# Object Oriented Analysis and Design (OOAD)

**Agile by Design — `abd-ooad` skill** for turning raw material (specs, manuals, code, policies) into robust object-oriented domain models.

## Quick Start

The core process is **linear and methodical**: Steps 0 → 1 → 2 (Scan → Extract → Refine).

**Step 0: Domain Scan** — Orientation, not extraction
- Read table of contents / section headings
- Identify 3–7 high-confidence anchors
- Flag suspected tensions/ambiguities
- Create **Actor Registry** to track concepts

**Step 1: Extraction & Validation** — Nouns, verbs, rules, states
- Read carefully for domain concepts
- Build candidate class list
- Validate against key scenarios

**Step 2: Refinement** — Relationships, responsibilities, invariants
- Add relationships and cardinality
- Encode domain rules into model
- Validate with walkthroughs

## Where This Skill Fits

This skill handles **model discovery, initial design, and diagram generation** end-to-end. Diagram tooling is built in:
- `scripts/drawio_cli.py` — create, verify, relayout, fix-edge-styles, fix-shared-endpoints, fix-arrow-overlaps
- `templates/` — domain model and domain realization templates
- `content/parts/library/` — class diagram and sequence diagram layout rules
- `runs/` — **reference runs** showing complete real-world OOAD output (format, notation, structure). Use as gold-standard examples before starting a new project run.

## Reference Runs

`runs/run-0/` contains the baseline reference for MM3E Heroes Handbook OOAD — a complete real session output:
- `domain-scan-model.md` / `.drawio` — Step 0 anchors + tensions in canonical format
- `domain-scan-results.md` — source map, anchor justification, tension table
- `1 - basics-checks-conditions/` — Phase 2 (`domain-noun-verb.md`) and Phase 3 (`domain-raw-candidates.md`) slice work
- `progress/` — process and strategy checklists
- `skill/` — snapshot of skill files (SKILL.md, process.md, templates) that governed this run
- `README.md` — reverse-engineered format conventions, notation rules, anchor/tension summary

**Before starting a new project run:** read `runs/run-0/README.md` and `runs/run-0/domain-scan-model.md` to align on the expected output format and notation.

## Workspace Capability

When you invoke this skill, **specify the project workspace** where domain models will be created:

```
workspace: /path/to/project/directory
```

This workspace becomes the default location for:
- `domain-scan-model.md` — Step 0 (source map, anchors, tensions, actor registry)
- `domain-scan-model.drawio` — Step 0 diagram
- **`domain-noun-verb.md`** — **Phase 2** per slice folder only (nouns / verbs / rules / candidate blocks). **Do not** append Phase 3 bucket tables to the end of this file.
- *(Optional)* **`domain-raw-candidates.md`** — **Phase 3 integrated** model: **`### Class : << kind >>`** under anchor modules — **`templates/domain-raw-candidates-template.md`**. Tabular **`raw-candidates.md`** is **deprecated** (see **`templates/raw-candidates-template.md`**).
- Any subsequent step outputs

Authoring shapes for Phase 2/3 live under **`templates/`** in this skill — do not paste those paths into slice artifacts.

**Slice deliverables** are domain content only. Do **not** write **`Source:`** / **`Slice:`** / **`OOAD phase:`** / registry **`Step`** / **`Upstream:`** / **`Pre-notation:`** / **`Integrated model:`** blocks in slice files — that is skill/process noise, not model output. In **`domain-raw-candidates.md`**, do **not** duplicate Phase 3 bucket tables or tack them onto **`domain-noun-verb.md`** — fold judgments into **`#### Note :`** with typed lines per **`templates/domain-raw-candidates-template.md`**.

**Tensions in `domain-raw-candidates.md`:** Cross-cutting ambiguities (e.g. registry **T1** / **T3**) must appear under the **`#### Note :`** of each **owning class** as **`*[S# · Phase n]* Tension — …`** — **`[S# · Phase n]` first**, then **`Tension`**, same shape as **Trace** / **Evidence** (see **`templates/domain-raw-candidates-template.md`**). Do **not** use **`*Tension — [S# · Phase n]*`**. Do **not** add a closing **tension index table** at EOF.

If no workspace is provided, assume the current working directory.

## How to Use This Skill

**When you have domain material** (specs, manual, code, policy docs) and need to extract an object-oriented model:

1. Provide the **source material** (text, code, spec excerpt, etc.)
2. Specify the **workspace directory** where outputs should be created
3. Ask Claude to "**perform a Step 0 domain scan**" or similar

Claude will then:
- Analyze the material using appropriate technique (spec, code, transcript, expert)
- Create `domain-scan-model.md` with source map, anchors, tensions, actor registry
- Create `domain-scan-model.drawio` with initial class diagram (anchors only)
- Output both files to your workspace

Continue with **Step 1 (Extraction)** and **Step 2 (Refinement)** for deeper modeling.

## Key Output Artifacts

**Slice artifacts:** **`domain-noun-verb.md`** is required per slice (**Phase 2**). **Phase 3** is an optional **`domain-raw-candidates.md`** — classes with **`<< Entity >>` / `<< ValueObject >>` / `<< Process >>` / `<< Policy >>` / `<< Role >>` / `<< Event >>`** under anchor modules. **No** separate bucket-table file and **no** Phase 3 tables appended under **`domain-noun-verb.md`**.

| Global phase | Markdown | Template | Diagram |
|--------------|----------|----------|---------|
| Step 0 (workspace) | `domain-scan-model.md` | — | `domain-scan-model.drawio` |
| **Phase 2** | **`domain-noun-verb.md`** — H1 `# <SliceLabel>: Noun Verb Domain`; anchors + Candidate lists + optional Phase 2 class sketches **only** | **`templates/domain-noun-verb-template.md`** | *(optional)* |
| **Phase 3 (integrated, optional)** | **`domain-raw-candidates.md`** — modules + classes + typed **`#### Note :`** | **`templates/domain-raw-candidates-template.md`** | — |
| **Deprecated** | **`raw-candidates.md`** (tabular buckets) — **do not create** for new work | **`templates/raw-candidates-template.md`** (stub) | — |
| Later (per `process.md`) | Refined model markdown in slice / project layout | varies | Companion `.drawio` per **`templates/domain model template.*`** |

Always maintain **both** Markdown and diagram side-by-side where your project uses diagrams; keep them synchronized as you refine.

## Complete OOAD Methodology

For the full 20-step walkthrough with detailed techniques, worked examples, ASCII diagram notation, and battle-tested patterns, see **`content/parts/process.md`**.

For Step 0 details by source type (specification, codebase, transcript, domain expert), see **`content/parts/domain-scan.md`**.

For diagram CLI usage and layout rules, see **`content/parts/library/using-diagram-cli.md`**.
