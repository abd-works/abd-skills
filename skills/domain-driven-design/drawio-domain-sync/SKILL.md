---
name: drawio-domain-sync
catalog_garden_order: 7
description: >-
  Render Ubiquitous Language, CRC, or object model artifacts to Draw.io class diagrams — one page per Key Abstraction — and sync diagram edits back to the source model.
---
# drawio-domain-sync

## Purpose

This skill turns any domain model artifact — a Ubiquitous Language, CRC model, or object model — into a Draw.io class diagram the whole team can read, annotate, and edit. Each Key Abstraction in the source file becomes its own page in the diagram, keeping visual scope manageable and per-abstraction structure clear. When the team edits the diagram in Draw.io, the skill syncs those changes back to the source model file, so diagram and text never drift apart.

Positioning and layout are AI-driven: the agent reads the source, reasons about class relationships and inheritance chains, and places elements where the diagram reads best. There are no fixed grid scripts to run.

---

## When to use

- A `<deliverables-folder>/<name>-ubiquitous-language.md`, `<name>-crc.md`, or `<name>-object-model.md` file exists and you want a visual class diagram.
- The team asks to "render the diagram", "draw the class diagram", "visualise the domain model", or "update the diagram".
- A `.drawio` file has been edited in the Draw.io app and needs to be reconciled with the source model.

---

## Core concepts

### Source types

Three domain model artifacts can feed this skill. Each expresses domain concepts at a different fidelity level:

- **Ubiquitous Language** — plain-English concept blocks with behavior bullets and invariants; no types. The diagram represents each concept as a class, with behaviors as operations and invariants noted in a third compartment.
- **CRC model** — responsibility and collaborator tables; behaviors are named with collaborators. The diagram shows class boxes with responsibilities as rows, each annotated with its collaborator types using `name : Collaborator` notation (e.g., `modifier : Character, Imposed Conditions`). Collaborator names also drive association edges between classes. Invariants appear in the class compartment.
- **Object model** — typed properties (`+ name: Type`), typed method signatures, ownership semantics. The diagram is a full UML class diagram with typed property and operation compartments.

The agent reads whichever source type is present and maps its content to class diagram elements. Object models produce the richest diagrams; Ubiquitous Languagees produce leaner concept maps that still convey structure and relationships clearly.

### Page per Key Abstraction

A Key Abstraction is a named grouping in the source file, introduced with a `## **KA Name**` heading. Each KA gets **one Draw.io page**. The page name matches the KA name exactly. All concepts that belong to that KA appear as classes on its page. When a concept from one KA extends or uses a concept from another KA, that external concept appears on the page as an imported ghost class — see **cross-model ancestors** below.

### AI-driven layout

Positioning is a judgment call, not a script output. The agent reads the source, identifies which class is the base, which are children, which are collaborators, and then places them so the diagram reads naturally. The rules in `rules/` — base classes above derived classes, cross-model ancestors visible at the page top, distinct anchor points when multiple edges leave the same class side — are applied as reasoning constraints, not as CLI flags.

### Sync back

When a user edits a diagram in Draw.io, the `sync-to-model` command reads the diagram and produces a diff against the source model file. The agent reviews the diff with the user and applies confirmed changes to the source model. The source model remains the authoritative text; the diagram is a derived view.

---

## Build

### Before rendering

1. **Identify the source file.** Locate `<deliverables-folder>/<name>-ubiquitous-language.md`, `<name>-crc.md`, or `<name>-object-model.md`. Read the full file to understand all Key Abstractions and their concepts.

2. **Read the rules.** Read all `rules/*.md` files in this skill before placing any class. The layout decisions below follow those rules.

3. **Identify the diagram file path.** Use `<deliverables-folder>/<name>-class-diagram.drawio` alongside the source. The first `init` call creates the file if it does not exist.

### Incremental vs full rendering

**Prefer incremental edits when the diagram already exists.** If a `.drawio` file is present and the source model has changed, use `update-class`, `add-class`, `delete-class`, and edge commands to apply only the changes — do not regenerate the entire file from scratch. Full regeneration destroys any manual repositioning the user has done in Draw.io. Only use full rendering (steps 4–10 below) when creating a diagram for the first time.

### Rendering (source → diagram)

For each Key Abstraction in the source file, work through these steps (full rendering — use only when no diagram exists yet):

4. **Init the page** if it does not exist yet:

   ```bash
   python skills/domain-driven-design/drawio-domain-sync/scripts/drawio_class_cli.py init <drawio-file> --page "<KA Name>"
   ```

5. **Plan layout for this page.** Identify which concepts are base classes and which are derived. Apply `rules/class-diagram-base-classes-positioned-above-derived-classes.md`: bases go at low y-values, children below. Identify any cross-KA ancestor classes that need to be imported at the top of the page.

6. **Add imported ancestor classes** — any base that belongs to a different KA — using `--imported-from "<Source KA Name>"`. Imported classes render with a dashed border and a `«from: KA Name»` stereotype. Position these at the very top of the page.

7. **Add local classes** — each concept in this KA — with properties, operations, and invariants at the planned positions. Include collaborator/type annotations according to source fidelity:
   - **Ubiquitous Language** — omit type annotations (behaviors only, no types in source).
   - **CRC model** — show every collaborator from the pipe-separated collaborator column as a type annotation on the property or operation, using `name : Collaborator` notation. When a responsibility has multiple collaborators, list them all: `modifier : Character, Imposed Conditions, Condition, Game Modifier`. Collaborators that are not on this page but appear in the type annotation must either have an edge to an imported class or use parenthetical primitive notation `(integer)` / `(true or false)`.
   - **Object model** — add full typed signatures (`+ name: Type`).

8. **Add edges** in this order: inheritance first (this establishes the vertical structure), then composition and aggregation (ownership), then associations (uses), then dependencies (creates). Use orthogonal routing for dependencies (`dependency-orthogonal`) when any class sits between source and target — straight dashed lines cut through intervening classes. Apply `rules/class-diagram-multiple-edges-use-distinct-anchor-points.md`: whenever more than one edge leaves the same side of a class, assign explicit `exitX/exitY` and `entryX/entryY` values so each path is visually separate. After adding all edges, verify no edge visually crosses through another class's bounding box.

9. **Inspect** to check for overlapping classes and edge stacking:

   ```bash
   python skills/domain-driven-design/drawio-domain-sync/scripts/drawio_class_cli.py inspect <drawio-file> --page "<KA Name>"
   ```

   Use `move` to reposition any overlapping classes.

10. **Verify sync.** Run `sync-to-model` — it should report "no changes" when the diagram accurately reflects the source:

    ```bash
    python skills/domain-driven-design/drawio-domain-sync/scripts/drawio_class_cli.py sync-to-model <drawio-file> --page "<KA Name>" --model <source-file>
    ```

### Persisting module build scripts

When a full render produces a bespoke Python script that builds the diagram programmatically (creating all classes, edges, anchors, and waypoints in a single atomic pass), **keep the script in the destination repo** at `<repo-root>/scripts/build_<name>_diagram.py`. Do not delete it after the render succeeds.

These scripts are valuable because:

- **Re-runnable** — the model evolves; re-running the script regenerates the diagram from the current source without replaying the entire layout reasoning from scratch.
- **Extendable** — adding a new KA page, class, or relationship is a small edit to an existing script rather than a from-scratch generation session.
- **Auditable** — the script is a readable record of every layout decision (positions, widths, anchor points, waypoints) that produced the current diagram.

Each script should:

1. Import `drawio_tools` from the skill's `scripts/` directory.
2. Build the entire diagram atomically — load/create the mxfile, add all pages, classes, and edges, save once.
3. Run `audit_diagram_report()` at the end and print the result.
4. Be runnable standalone: `python scripts/build_<name>_diagram.py`.

When the model changes incrementally, prefer editing the existing build script over writing a new one. The script is the module's diagram source of truth alongside the model markdown.

### Sync back (diagram → source)

When the user edits the diagram in Draw.io and asks to reconcile it with the source model:

11. **Run sync-to-model** to surface the diff:

    ```bash
    python skills/domain-driven-design/drawio-domain-sync/scripts/drawio_class_cli.py sync-to-model <drawio-file> [--page "<KA Name>"] --model <source-file>
    ```

12. **Review the diff** with the user. Apply confirmed additions, changes, and deletions to the source model file. The source model is the record of intent; the diagram is the visual surface.

### CLI reference

The full CLI command reference — `add-class`, `update-class`, `delete-class`, `move`, all relationship commands, `inspect`, and `sync-to-model` — is documented in [`diagrams.md`](./diagrams.md) alongside detailed layout guidelines, UML relationship selection, and cross-model import conventions. Read that file during rendering; this SKILL.md does not duplicate those mechanics.

---

## Validate

- **Source identified** — a Ubiquitous Language, CRC, or object model file was located before any diagram work began; the agent read the full file.
- **Rules read** — all `rules/*.md` in this skill were consulted before placing any class on any page.
- **One page per KA** — the `.drawio` file has one page per `## **KA**` heading in the source; page names match KA headings exactly.
- **All KA concepts represented** — every concept listed under a KA in the source appears as a class on that KA's page; no concepts are silently skipped.
- **Cross-KA ancestors imported** — any ancestor class belonging to a different KA appears as an imported class (dashed border, `«from: KA Name»` stereotype) on the page that extends it.
- **Base classes above derived** — on every page, base and imported classes are at lower y-coordinates than their children; inheritance arrows point upward.
- **Distinct anchor points** — no two edges from the same side of a class use the same default anchor when more than one edge leaves that side.
- **Build script persisted** — when a full render used a bespoke build script, it was saved to `<repo-root>/scripts/build_<name>_diagram.py`, not deleted.
- **Sync verified** — after rendering each page, `sync-to-model` reported "no changes".
- **No placeholder** — no `{{PLACEHOLDER}}` remains in this file.
- **Bundle markers present** — `execute_rules:bundle_rules` begin/end markers exist and the bundled block matches current `rules/*.md` files.

---

<!-- execute_rules:bundle_rules:begin -->

# Rule: Base Classes Positioned Above Derived Classes

**Scanner:** Manual review

A passing diagram positions base (parent) and imported ancestor classes at higher vertical positions (lower y-coordinates) than their derived classes. Inheritance arrows point upward — from child to parent — so the visual hierarchy matches the conceptual hierarchy: readers see the most general abstraction first, then specialisations below. A failing diagram places a derived class at a lower y than its parent, or puts a base class at the bottom of the page with children stacked above it, forcing the reader to scan backwards to find the root of an inheritance chain.

## DO

- Position base and imported classes at the top of the page (low y-value) with derived classes extending downward.

  **Example (pass):** `Rollable` import at y=40, `Check` import at y=180, `AttackCheck` and `DamageResistance` side-by-side at y=400. Inheritance arrows point upward from children to parents.

- Place multiple sibling derived classes at the same y-level, side by side below their shared parent.

  **Example (pass):** `AttackCheck` at (x=40, y=400) and `DamageResistance` at (x=340, y=400) — same row, each pointing up to `Check` at (x=190, y=180).

## DO NOT

- Place a base class below its derived classes.

  **Example (fail):** `AttackCheck` at y=40, `Check` at y=550. Inheritance arrow points downward — readers see the specialisation before the abstraction.

- Mix inheritance depth levels on the same y-row, so a grandchild appears at the same height as its grandparent.

  **Example (fail):** `Rollable` at y=40 and `AttackCheck` (which inherits `Check`, which inherits `Rollable`) also at y=40 on the same page — three levels flattened to one row.

# Rule: Cross-Model Ancestors Shown on Page

**Scanner:** Manual review

When a page's local concepts extend or use concepts that belong to a different Key Abstraction, the full ancestor chain from that other KA must appear at the top of the page as imported classes (dashed border, `«from: KA Name»` stereotype). A passing diagram lets the reader trace the complete ancestry without leaving the page. A failing diagram shows only the immediate imported parent while omitting the grandparent that explains where the parent comes from, leaving an incomplete ancestry chain.

## DO

- Import every ancestor class needed to understand the full ancestry chain, including grandparents, at the top of the page.

  **Example (pass):** An Attack-and-Damage page imports both `Rollable [from: Resolution System]` and `Check [from: Resolution System]`, with a `creates` dependency edge from `Rollable` to `Check`. The reader sees the full chain: `Rollable → Check → AttackCheck / DamageResistance`.

- Render imported classes with a dashed border and a `«from: KA Name»` stereotype label placed above the class name.

  **Example (pass):** `add-class … --imported-from "Resolution System"` produces a dashed-border box with stereotype `«from: Resolution System»` shown above `Rollable`.

- Show only the key properties on an imported class — enough to recognise it; full detail stays on the home-KA page.

  **Example (pass):** Imported `Check` shows `+ modifier: Integer` and `+ degree: Degree` only. Full operations and invariants are not duplicated.

## DO NOT

- Show only the immediate imported parent while omitting the grandparent that establishes context.

  **Example (fail):** Attack-and-Damage page imports `Check` but not `Rollable` — the reader cannot see that `Check` originates from `Rollable.perform_check()` and cannot understand where the `Check` concept comes from.

- Render an imported class as a normal solid-border class indistinguishable from local classes.

  **Example (fail):** `Rollable` appears with a solid border and no stereotype on the Attack-and-Damage page — readers cannot tell it belongs to a different KA.

# Rule: Multiple Edges Use Distinct Anchor Points

**Scanner:** Manual review

When more than one edge leaves from — or arrives at — the same side of a class, each edge must be given explicit `exitX/exitY` or `entryX/entryY` anchor values so the paths are visually distinct. A passing diagram shows clearly separated lines; a failing diagram stacks all outgoing edges on the default anchor, making them appear as a single thick line where the individual relationships are indistinguishable.

## DO

- Assign explicit exit and entry anchor coordinates when two or more edges share the same source or target side of a class.

  **Example (pass):** `CombatManeuver` has three outgoing edges — inheritance exits top-center (exitX=0.5, exitY=0), a `creates` dependency exits left-low (exitX=0, exitY=0.7), and an opposed `creates` exits left-high (exitX=0, exitY=0.15). Each edge is visually distinct.

- Spread multiple children that inherit from the same parent across the parent's bottom edge using distributed entry points.

  **Example (pass):** Three child classes inherit from `Action`: first child enters at entryX=0.25, second at entryX=0.5, third at entryX=0.75 — three clearly separated arrows arriving at distinct points.

## DO NOT

- Leave multiple edges from the same class side with default anchor routing.

  **Example (fail):** `CombatManeuver` has three edges all using Draw.io's default center anchor — they stack and render as one thick line. A reader cannot distinguish the inheritance edge from the two dependency edges.

- Add explicit anchors only to some edges while leaving others on the default when they share the same exit or entry side.

  **Example (fail):** Two of three inheritance arrows from sibling classes have `entryX` set; the third uses default center entry — it overlaps the second arrow and both appear to merge at the parent class.

# Rule: Run Audit After Every Render

**Scanner:** `audit_diagram_report(path)` from `drawio_tools.py`

After generating or modifying a diagram, run `audit_diagram_report()` and iterate until **all `edge_crosses_class` violations are eliminated**. Secondary violations (`edge_on_edge_overlap`, `shared_anchor`) should be minimized but may be unavoidable in complex diagrams with many edges. Never declare a diagram done while `edge_crosses_class` violations exist.

The audit checks four categories in priority order:

1. **`class_overlap`** — two class boxes intersect. Must be zero.
2. **`edge_crosses_class`** — an edge route passes through a class it is not connected to. Must be zero.
3. **`edge_on_edge_overlap`** — two edges share the same visual path segment. Minimize.
4. **`shared_anchor`** — multiple edges enter/exit the same default anchor point. Minimize (use explicit `exit_x/exit_y/entry_x/entry_y`).

## DO

- Run `audit_diagram_report(path)` after every render pass and read the output.

  **Example (pass):** Agent renders diagram, runs audit, sees `edge_crosses_class: Check→Check Result crosses Difficulty Class`. Repositions Check Result to a row below DC, reruns audit, sees zero crossings.

- Use `inheritance-orthogonal` when a subtype is not directly below the parent in the same column.

  **Example (pass):** Three subtypes inherit from Check. Only Routine Check is directly below. Opposed Check (offset left) and Team Check (offset right) use `inheritance-orthogonal` with explicit anchors.

## DO NOT

- Declare a diagram done when `edge_crosses_class` violations exist.

  **Example (fail):** Audit reports "Edge Routine Check→Check crosses through Check Result". Agent says "the Draw.io router will handle it" and moves on. The rendered diagram shows an inheritance arrow cutting through the Check Result box.

- Skip the audit because the layout "looks right" during generation.

  **Example (fail):** Agent positions 10 classes, writes edges, saves file, and declares done — never running `audit_diagram_report`. Three edges cut through class boxes that the agent didn't notice because it can't see the rendered diagram.

<!-- execute_rules:bundle_rules:end -->
