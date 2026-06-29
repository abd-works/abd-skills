---
name: drawio-domain-sync
catalog_garden_order: 7
catalogue_one_liner: >-
  Keep domain diagrams and source models in sync — so the team reads one truth, not two.
description: >-
  Render domain artifacts to Draw.io class diagrams and sync edits back to the source model. Use when the team needs a visual diagram from a domain model or when text and diagram need reconciliation.
context-perspective: domain
context-role: support
context-fidelity:
  - level: specification
    mode: diagram-sync
---
# drawio-domain-sync

## Purpose

Keep domain diagrams and source models in sync — so the team reads one truth, not two.

---

## Output file

**Deliverables folder:** see `../common/reference/skill-workflow.md` — Output file resolution.

**Default (per-KA tabs):** `<source-name>.drawio` alongside the source `.md` file — same stem, different extension. The file contains one tab per KA plus an optional "All KAs (Overview)" tab.

**Full-page mode:** Same file name, single page containing all KAs. Only produced when the user explicitly requests it (e.g. `--full`, "full diagram", "single page").

---

## Agent Instructions

Follow `../common/reference/skill-workflow.md` — read-gates, output file resolution, and the per-rule verdict format are defined there.

### 1. Read context

Read these files:
- **`reference/concepts.md`** — source types (Domain Language, Domain Model, Domain Specification), page-per-KA convention, AI-driven layout, sync-back rules, incremental vs full rendering, build script persistence, and CLI reference pointer.
- **`diagrams.md`** — full CLI command reference, layout guidelines, UML relationship selection, and cross-model import conventions.

### 2. Generate — Per-KA Tabs (Default Mode)

**This is the default. Unless the user explicitly asks for a full single-page diagram, produce per-KA tabs.**

**Per-KA tab rules:**

1. **One tab per KA** — Each Key Abstraction gets its own page/tab in the `.drawio` file.
2. **Boundary classes (directly connected only)** — On each KA's tab, include classes from other KAs that are *directly connected* via an edge (association, composition, aggregation, or dependency) to a class in this KA. These appear with dashed borders and reduced opacity to signal they are context, not the focus.
3. **Supertypes only, not subtypes** — A subtype that crosses KA boundaries pulls in its supertype as a boundary class. A supertype does NOT pull in subtypes from other KAs. The rule: if a class on this tab inherits from a class in another KA, show the parent. If a class on this tab is inherited by a class in another KA, do NOT show the child.
4. **Exact layout from source** — Use the same positions as the source diagram for all classes within the KA. Boundary classes are repositioned closer to the KA cluster they connect to.
5. **Edge labels preserved** — Role names (e.g. "fromAccount", "destinationAccount") on edges carry through to per-KA tabs.
6. **Optional overview tab** — Include an "All KAs (Overview)" tab as the first page showing everything on one canvas. This gives context but the per-KA tabs are the primary working view.

**Workflow:**

1. **Identify the source file** — locate the domain model or specification markdown. Prefer highest fidelity available (Domain Specification > Domain Model > Domain Language).

   **If a domain model diagram already exists** — use `--base-diagram` to copy the existing diagram and update cells in place rather than re-laying-out from scratch.

2. **Render all KAs** — Build the multi-tab file. For each KA:
   - Place all classes belonging to that KA on its tab.
   - Identify boundary classes (directly connected from other KAs, supertypes only).
   - Add boundary classes with dashed/opacity styling.
   - Draw all edges where both source and target are on the tab.
   - Include edge labels (cardinality, role names).

3. **Audit** — Run `audit_diagram_report()` on each tab. Fix overlaps.

4. **Report** — Tell the user the diagram is ready for review.

**CLI (from skill's scripts/):**

```bash
# Default: per-KA tabs
python scripts/drawio_domain_cli.py <source.md> --output <file.drawio>

# Full single-page (only when explicitly requested):
python scripts/drawio_domain_cli.py <source.md> --output <file.drawio> --full

# From a base diagram (domain spec inherits domain model layout):
python scripts/drawio_domain_cli.py <spec.md> --base-diagram <existing.drawio> --output <spec-diagram.drawio>

# Inspect:
python scripts/drawio_domain_cli.py inspect <file.drawio>

# Sync back:
python scripts/drawio_class_cli.py sync-to-model <file.drawio> --page "<KA Name>" --model <source-file>
```

**`--base-diagram` workflow:** When rendering a domain specification and a domain model diagram already exists, pass `--base-diagram <model-diagram.drawio>`. This copies the existing layout, updates each class cell in place with specification-level detail (typed properties, operations, invariants), adds new classes near their related classes, and redraws edges from the spec relationships.

**Sync back (diagram → source):** Run `sync-to-model` to surface the diff; review with the user; apply confirmed changes to the source model.

### 2b. Generate — Full Single-Page (Only When Requested)

Use this mode only when the user explicitly asks for it (says "full diagram", "single page", "all on one page", or passes `--full`).

1. **For each Key Abstraction**, init a page, plan layout (bases above derived), add imported ancestors, add local classes with rows/collaborators per source fidelity, add edges (inheritance → composition → association → dependency), inspect for overlaps, verify sync.
2. **Persist build scripts** when full renders produce bespoke Python scripts.

### 3. Validate

Run scanners and emit per-rule verdicts — see `../common/reference/skill-workflow.md` § Validate output.

---

## Validate

**Goal:** Inspect the rendered diagram as reviewers.

- **Source identified** — a Domain Language, Domain Model, or Domain Specification file was located before any diagram work began; the agent read the full file.
- **Rules read** — all `rules/*.md` in this skill were consulted before placing any class on any page.
- **Per-KA tabs produced (default)** — each KA has its own tab/page in the .drawio file unless the user explicitly requested full single-page mode.
- **Boundary classes correct** — only directly connected classes from other KAs appear as boundary (dashed). Supertypes are included; subtypes from other KAs are NOT.
- **No extraneous boundary classes** — classes that are only indirectly connected (e.g. two hops away) do not appear on a KA's tab.
- **Edge labels preserved** — role names and cardinality carry through to per-KA tabs.
- **All KA concepts represented** — every concept listed under a KA appears as a class on its tab.
- **Base classes above derived** — base and imported classes are at lower y-coordinates than their children.
- **Distinct anchor points** — no two edges from the same side use the same default anchor.
- **Audit clean** — `audit_diagram_report()` shows zero `edge_crosses_class` violations.
- **No bundle markers** — `SKILL.md` has no `<!-- execute_rules:bundle_rules -->` markers.

---
