<!-- section: story_synthesizer.diagrams -->
# Class Diagrams

When a run produces or modifies domain model concepts, render the changes to a DrawIO class diagram. One page per foundational model. The diagram is the visual representation of `domain-model.md` — they stay in sync.

## Diagram File

**Path:** `<session>/class diagram.drawio` (alongside `domain-model.md`)

Each foundational model section in `domain-model.md` maps to one page in the diagram. Page names must match section names exactly (e.g., "Resolution System", "Combat System").

## When to Render

- **After producing domain model output** in a run — render new/changed concepts to the diagram
- **After corrections that change domain model** — update the diagram to match
- **After user edits the diagram in DrawIO** — sync back to `domain-model.md` using `sync-to-model`

## Tools

All tools are in `scripts/` in the synthesizer skill. Run from that directory.

```bash
cd skills/abd-story-synthesizer/scripts
python drawio_class_cli.py <command> <drawio-file> [options]
```

### Diagram Management

| Command | Usage |
|---------|-------|
| `init` | `init <file> --page <name>` — create file or add page |
| `inspect` | `inspect <file> [--page <name>]` — JSON: classes, edges, overlaps |
| `sync-to-model` | `sync-to-model <file> [--page <name>] [--model <md-path>]` — sync diagram classes back to domain-model.md with diffs |

### Class CRUD

| Command | Usage |
|---------|-------|
| `add-class` | `add-class <file> --page <page> --name <Name> [--base <Base>] [--props "p1\|p2"] [--ops "o1\|o2"] [--invs "i1\|i2"] [--x N] [--y N]` |
| `update-class` | `update-class <file> --page <page> --name <Name> --add-prop "..." \| --remove-prop "..." \| --add-op "..." \| --remove-op "..." \| --add-inv "..." \| --set-base <Base>` |
| `delete-class` | `delete-class <file> --page <page> --name <Name>` — removes class and all its edges |
| `move` | `move <file> --page <page> --name <Name> --x N --y N` |

### Relationship CRUD

| Command | Style | Usage |
|---------|-------|-------|
| `add-inheritance` | Hollow triangle (straight or orthogonal) | `--child <Child> --parent <Parent> [--orthogonal]` |
| `add-composition` | Filled diamond on owner (orthogonal) | `--owner <Owner> --part <Part> [--straight]` |
| `add-aggregation` | Hollow diamond on owner (orthogonal) | `--owner <Owner> --part <Part> [--straight]` |
| `add-association` | Open arrow (orthogonal) | `--from <Source> --to <Target> [--straight]` |
| `add-dependency` | Dashed open arrow (straight) | `--from <Source> --to <Target> [--label <text>]` |
| `delete-edge` | — | `--from <Source> --to <Target>` |

## Layout Guidelines

- **Key Abstraction cohesion:** Classes within the same Key Abstraction form a tight cluster; different KAs are separated by visible distance (≥200px gap). Cross-KA edges are naturally longer, communicating that the connection crosses a boundary. Instance notes sit inside their KA cluster, near the class they describe.
- **Constrained inherited properties:** When a subtype constrains an inherited property (fixed value, narrower format, locked instance), the constraint is modeled as a **new subtype of the property's type** — not as a text invariant on the child class. The constrained subtype appears as its own class cell on the diagram with an inheritance edge (hollow triangle) to the base property type and an association edge from the child class. This applies to any constraint that narrows a type: fixed currency, restricted destination, format-specific identifiers. If you find yourself writing an invariant that says "X is always Y," create the type instead. See `abd-domain-model/rules/constrained-inherited-property-gets-subtype.md`.
- **Inheritance:** Base on top, extensions below. Straight vertical lines preferred when parent and child are in the same column. Use `inheritance-orthogonal` when the child is in a different column from the parent — straight diagonal lines cut through intervening classes.
- **Composition/aggregation:** Orthogonal routing (right-angle corners). Diamond on the owner (parent) side.
- **Association:** Orthogonal routing. Use `--straight` when classes are on the same row to avoid bends.
- **Dependency:** Dashed line for creates/uses relationships (e.g., Rollable creates Check). Use `dependency-orthogonal` (right-angle routing) when any class sits between source and target — straight dashed lines cut through intervening classes. Default to orthogonal; use straight only when source and target are adjacent with nothing between them.
- **Grid layout:** Position classes in rows — parents row 0, children/dependents row 1+. Avoid all-on-one-row; aim for a square diagram.
- **No overlaps:** After positioning, run `inspect` to check for overlapping classes. Use `move` to fix.
- **No crossing edges:** Position classes so edges don't cross over other classes. Place related classes adjacent. After adding edges, visually trace each one — if it would pass through another class's bounding box, either reposition the source/target class or switch to orthogonal routing.

## UML Relationship Selection

| Relationship | When to use | DrawIO style |
|-------------|-------------|--------------|
| **Inheritance** | Concept extends another (e.g., Ability : Rollable) | Hollow triangle; `inheritance-orthogonal` when child is offset from parent column |
| **Composition** | Part cannot exist without whole; collection property (e.g., Character ◆→ Ability via Dictionary) | Filled diamond |
| **Aggregation** | Whole references part but part has independent lifecycle (e.g., Character ◇→ PowerLevel) | Hollow diamond |
| **Association** | Concept uses another in operations (e.g., Check → DC, Check → Degree) | Open arrow |
| **Dependency** | Concept creates instances of another (e.g., Rollable --creates-→ Check) | Dashed arrow (orthogonal routing default) |

## Cross-Model Imports

When a concept from one foundational model is referenced in another (e.g., Ability extends Rollable from Resolution System), mark it explicitly in both places.

### Domain Model Convention

Add `[from: Source Module]` after the base class:

```
**Ability** : Rollable [from: Resolution System]
**AttackCheck** : Check [from: Resolution System]
```

### Class Diagram Convention

Add the imported class using `--imported-from`:

```bash
python drawio_class_cli.py add-class <file> --page "Character Trait System" --name Rollable --imported-from "Resolution System" --props "Number modifier" --x 40 --y 620
```

The imported class renders with a dashed border and a `«from: Module»` stereotype label above the name. Add inheritance edges from local classes to the import as normal.

### Keeping Cross-Model References in Sync

When a concept changes in its home model:
1. Update the concept in the home model's page and domain-model.md section
2. Update imported copies in other pages (properties may differ — imports typically show only the key properties)
3. Run `inspect` on pages that import the concept to verify edges still connect

**Imported classes are lightweight copies** — they show the concept name, stereotype, and key properties only. They don't need full operations or invariants (those live in the home model).

## Domain Model Type Conventions

- **Enum types** for constrained options: `EnumType name {value1, value2, ...}` — not `String name (option1/option2)`
- **Derived properties** with invariants: `Number cost` + `Invariant: cost = rank × 2` — not `calculate_cost() → Number`
- **Invariants** for all rules, formulas, and constraints — not embedded in property descriptions or operation signatures

## Class Diagram Rules

Rules tagged `class_diagram` in `rules/` govern diagram rendering conventions. These are injected when using the class diagram CLI tool — they are NOT part of synthesis run instructions. Apply them during the rendering workflow below.

Key rules:
- **Hierarchy flow** — base classes top, children below (`domain-ooa-diagram-hierarchy-flow.md`)
- **Cross-model imports** — import base classes that establish ancestry context (`domain-ooa-diagram-cross-model-imports.md`)
- **Edge routing** — explicit exit/entry points when multiple edges share a source (`domain-ooa-diagram-edge-routing.md`)

## AI Workflow for Rendering

**Per-KA tabs is the default.** Each KA gets its own tab with only its own classes plus directly connected boundary classes (supertypes only, not subtypes from other KAs). The full single-page mode is only used when explicitly requested.

### Per-KA Tab Mode (Default)

#### Boundary class rules

| Rule | Include as boundary? |
|------|---------------------|
| Class from another KA directly connected via edge (association, composition, aggregation, dependency) | YES — dashed border, reduced opacity |
| Supertype in another KA (this tab's class inherits from it) | YES — show the parent |
| Subtype in another KA (another KA's class inherits from this tab's class) | NO — do not show children from other KAs |
| Class from another KA connected only indirectly (2+ hops) | NO |

#### Setup

1. **Identify source** — read the domain model/specification file.
2. **Determine KA membership** — map each class ID to its owning KA.
3. **Build all tabs** — for each KA, compute boundary classes per the rules above, copy cells and edges, apply boundary styling.

#### Per-KA tab construction

For each KA:

1. **Collect KA members** — all class cells belonging to this KA.
2. **Find boundary classes** — scan all edges. For each edge where one end is in this KA and the other is not:
   - If the edge is an inheritance edge: include the **parent** (supertype) as boundary only if it belongs to another KA. Do NOT include children (subtypes) from other KAs.
   - If the edge is any other relationship: include the other end as boundary.
3. **Copy cells** — KA members at original positions. Boundary classes repositioned closer to the KA cluster with dashed-border styling.
4. **Copy edges** — only edges where both source and target are on this tab (KA members + boundary).
5. **Copy edge labels** — cardinality labels and role names that parent to included edges.
6. **Overview tab** — optionally include an "All KAs" first tab with everything on one page for navigation.

### Full Single-Page Mode (Only When Requested)

Use when the user explicitly says "full diagram", "single page", "all on one page", or passes `--full`.

**Incremental first.** If the `.drawio` file already exists, use `update-class`, `add-class`, `delete-class`, and edge commands to apply only what changed — do not regenerate the whole file. Full regeneration destroys manual layout adjustments. Use the full workflow below only when creating a diagram for the first time.

After producing domain model output for a slice:

1. **Review `class_diagram` rules** — apply positioning and edge conventions from `rules/domain-ooa-diagram-*.md`
2. **Init** page if needed: `init <file> --page "<Model Name>"`
3. **Add classes** with rows and invariants at planned grid positions (base classes top, children below). **Always include collaborator types** — every row must show its collaborators using `name : Collaborator` notation (e.g., `character : Character`, `resist : Character, Trait, Graded Check Result`). The source determines where the collaborators come from:
   - **domain model source** — the collaborator column after the pipe (`|`) becomes the type annotation on the row.
   - **Domain Language source** — each verb-led behavior bullet becomes one row. Row label = the bullet text with italic markers stripped; collaborators = the `*italicized*` terms in that bullet. `**Invariant:**` bullets render in the third compartment. `### Subtype *is a type of* Base` headings drive inheritance edges. `### term *(boundary)*` scoped stubs render as imported cards with `«boundary: OwningModule»` stereotype. See `rules/class-diagram-domain-language-bullets-become-rows.md`.
   - **Class Model source** — typed signatures (`+ name: Type`) become the row format.
   - Primitives in any source use parenthetical notation: `status : (success or failure)`.
4. **Add edges** — inheritance first (defines vertical structure), then composition/aggregation, then associations/dependencies. Use explicit exitX/exitY/entryX/entryY when multiple edges leave the same class. For ULL sources, **fold duplicate cross-concept references**: if three bullets on the same concept reference the same italicized target, emit one association edge, not three.
5. **Audit** — run `audit_diagram_report(path)` (from `drawio_tools.py`) and read all violations. Priority: (1) `class_overlap` = zero, (2) `edge_crosses_class` = zero, (3) minimize `edge_on_edge_overlap`, (4) minimize `shared_anchor`.
6. **Iterate** — fix violations by repositioning classes (`move`), switching edge styles (e.g., `inheritance` → `inheritance-orthogonal`), or adding explicit `exit_x/exit_y/entry_x/entry_y` anchors. Rerun audit after each fix.
7. **Verify** sync: `sync-to-model` should report "no changes" (diagram matches model). For ULL sources, sync covers added/deleted concepts and inheritance headings only — bullet-level edits do not round-trip; edit the markdown directly.

## Persisting Module Build Scripts

When a full render produces a bespoke Python script that builds the diagram (all classes, edges, anchors, waypoints in one atomic pass), **keep the script** in the destination repo at `<repo-root>/scripts/build_<name>_diagram.py`. Do not delete it after the render succeeds.

| Property | Why it matters |
|----------|---------------|
| **Re-runnable** | Model evolves; re-run the script to regenerate without replaying layout reasoning |
| **Extendable** | New KA page, class, or edge is a small edit, not a from-scratch session |
| **Auditable** | Readable record of every layout decision (positions, widths, anchors, waypoints) |

Each script should:

1. Import `drawio_tools` from the skill's `scripts/` directory.
2. Build atomically — create mxfile, add all pages/classes/edges, save once.
3. Run `audit_diagram_report()` at the end and print the result.
4. Be runnable standalone: `python scripts/build_<name>_diagram.py`.
5. Exit non-zero when audit fails.

When the model changes incrementally, **edit the existing build script** rather than writing a new one.

## When User Edits the Diagram in DrawIO

1. User saves the diagram
2. Run `sync-to-model` to see diffs and apply changes back to `domain-model.md`
