---
name: drawio-domain-sync
catalog_garden_order: 7
catalogue_one_liner: >-
  Domain model to Draw.io class diagrams — one page per Key Abstraction — with sync back to source.
description: >-
  Render Domain Language, Domain Model, or Domain Specification artifacts to Draw.io class
  diagrams — one page per Key Abstraction — and sync diagram edits back to the
  source model. Use when you want a visual class diagram from a domain model,
  when the team asks to "render the diagram" or "visualise the domain model",
  or when a .drawio file has been edited and needs reconciliation with the source.
---
# drawio-domain-sync

## Purpose

This skill turns any domain model artifact — a Domain Language, Domain Model, or Domain Specification — into a Draw.io class diagram the whole team can read, annotate, and edit. Each Key Abstraction in the source file becomes its own page in the diagram, keeping visual scope manageable and per-abstraction structure clear. When the team edits the diagram in Draw.io, the skill syncs those changes back to the source model file, so diagram and text never drift apart.

Positioning and layout are AI-driven: the agent reads the source, reasons about class relationships and inheritance chains, and places elements where the diagram reads best. There are no fixed grid scripts to run.

---

## Output file

**Deliverables folder:** see `../common/skill-rule-workflow.md` — Output file resolution.

**File name:** `<name>-class-diagram.drawio` alongside the source model file.

---

## Agent Instructions

> **MANDATORY — read `../common/skill-rule-workflow.md` before starting. It defines read-gates, output file resolution, and the per-rule verdict format.**

### 1. Read context

Read these files:
- **`reference/concepts.md`** — source types (Domain Language, Domain Model, Domain Specification), page-per-KA convention, AI-driven layout, sync-back rules, incremental vs full rendering, build script persistence, and CLI reference pointer.
- **`diagrams.md`** — full CLI command reference, layout guidelines, UML relationship selection, and cross-model import conventions.

### 2. Generate

Read every file in **`rules/`**; author to those rules.

**Rendering (source → diagram):**

1. **Identify the source file** — locate `<name>-domain-specification.md` / `class-model.md`, `<name>-domain-model.md` / `domain-model.md`, or `<name>-domain-language.md` / `domain-language.md`. Prefer highest fidelity available (Domain Specification > Domain Model > Domain Language).
2. **For each Key Abstraction**, init a page, plan layout (bases above derived), add imported ancestors, add local classes with rows/collaborators per source fidelity, add edges (inheritance → composition → association → dependency), inspect for overlaps, verify sync.
3. **Persist build scripts** when full renders produce bespoke Python scripts.

**CLI (from skill's scripts/):**

```bash
python scripts/drawio_class_cli.py init <drawio-file> --page "<KA Name>"
python scripts/drawio_class_cli.py inspect <drawio-file> --page "<KA Name>"
python scripts/drawio_class_cli.py sync-to-model <drawio-file> --page "<KA Name>" --model <source-file>
```

**Sync back (diagram → source):** Run `sync-to-model` to surface the diff; review with the user; apply confirmed changes to the source model.

### 3. Validate

Run the scanners:

```bash
python skills/common/scripts/run_scanners.py \
  --skill-root skills/drawio-domain-sync \
  --workspace <path-to-output>
```

Then emit per-rule verdicts per `../common/skill-rule-workflow.md`.

---

## Validate

**Goal:** Inspect the rendered diagram as reviewers.

- **Source identified** — a Domain Language, Domain Model, or Domain Specification file was located before any diagram work began; the agent read the full file.
- **Rules read** — all `rules/*.md` in this skill were consulted before placing any class on any page.
- **One page per KA** — the `.drawio` file has one page per `## **KA**` heading; page names match KA headings exactly.
- **All KA concepts represented** — every concept listed under a KA appears as a class on that KA's page.
- **Domain Language bullets become rows** — when source is a Domain Language file, every behavior bullet renders as a row, every italicized term resolves to a collaborator, cross-concept references are folded into one association edge, subtype headings produce inheritance edges, boundary stubs render as imported cards.
- **Cross-KA ancestors imported** — ancestor classes from other KAs appear as imported classes (dashed border, `«from: KA Name»` stereotype).
- **Base classes above derived** — base and imported classes are at lower y-coordinates than their children.
- **Distinct anchor points** — no two edges from the same side use the same default anchor.
- **Build script persisted** — when a full render used a bespoke build script, it was saved to `scripts/build_<name>_diagram.py`.
- **Sync verified** — after rendering each page, `sync-to-model` reported "no changes".
- **Audit clean** — `audit_diagram_report()` shows zero `edge_crosses_class` violations.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
