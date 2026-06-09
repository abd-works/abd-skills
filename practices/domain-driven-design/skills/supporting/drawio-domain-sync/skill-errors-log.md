# drawio-domain-sync — skill errors log

---

### Collaborator types omitted from class diagram properties and operations

- **Context:** Rendering a Domain Model to a Draw.io class diagram
- **DO / DO NOT:** **DO** always include collaborator types as type annotations on every property and operation, using `name : Collaborator` notation. When a responsibility has multiple collaborators, list them all (e.g., `modifier : Character, Imposed Conditions, Condition, Game Modifier`). **DO NOT** render properties or operations as bare names without their collaborator types.
- **Example (wrong):** Properties rendered as `+ character`, `+ modifier`, `+ perform check` — no collaborator type shown. The reader cannot see what type each property holds or what collaborators each operation uses without consulting the domain model source.
- **Example (correct):** Properties rendered as `+ character : Character`, `+ modifier : Character, Imposed Conditions, Condition, Game Modifier`, operations as `+ perform check : Check, Rank, Check Result`. Every collaborator from the domain model pipe column appears inline.
- **Likely source:** `prompt gap` — SKILL.md step 7 said "omit type annotations when the source is a Domain Language; add full typed signatures when the source is an Class Model" but did not mention domain models at all. Fixed: step 7 now has explicit sub-bullets for all three source types.
- **Status:** confirmed

---

### Imported classes positioned far from the classes that reference them

- **Context:** Rendering the Check KA page — Character (imported) placed at x=1300 (far right) while Opposed Check (x=40) and Team Check (x=780) both need edges to it
- **DO / DO NOT:** **DO** position imported classes adjacent to or in the same column as the local classes that reference them most. **DO NOT** push all imported classes to the far edge of the diagram just because they are imports — proximity to referencing classes matters more than grouping imports together.
- **Example (wrong):** Character placed at x=1300 y=40 (top-right corner). Opposed Check at x=40 y=580 and Team Check at x=780 y=580 both draw association edges across the entire page width, crossing over Routine Check and other classes.
- **Example (correct):** Character placed at x=40 y=280 — directly above Opposed Check (x=40 y=520) and one column left of Team Check (x=760 y=520). Edges are short and do not cross other classes.
- **Likely source:** `prompt gap` — the layout rules say "imported classes at the top of the page" but do not say to position them near the classes that use them. The rule about "base classes above derived" was followed, but horizontal proximity was ignored.
- **Status:** confirmed

---

### Cell width too narrow for collaborator type annotations

- **Context:** Rendering a Domain Model with collaborator types — default cell width 260px caused excessive text wrapping on long collaborator strings
- **DO / DO NOT:** **DO** widen class cells (320px or more) when collaborator type annotations produce long property/operation text. **DO NOT** use a fixed narrow width that causes collaborator lists to wrap excessively, making the diagram harder to read.
- **Example (wrong):** `modifier : Character, Imposed Conditions, Condition, Game Modifier` in a 260px-wide cell wraps across 3+ lines, making the properties compartment disproportionately tall.
- **Example (correct):** Same text in a 320px-wide cell wraps once or not at all, keeping the cell compact and readable.
- **Likely source:** `prompt gap` — no guidance existed on adjusting cell width based on content length; the tooling defaults to 260px regardless of content.
- **Status:** confirmed

---

### Regenerating entire diagram from scratch instead of incremental edits

- **Context:** When updating an existing class diagram after Domain Model changes, a full-regeneration script was written that replaced the entire `.drawio` file — discarding any manual repositioning the user had done in Draw.io.
- **DO / DO NOT:** **DO** use incremental operations (`update-class`, `move`, `add-class`, `delete-class`, `add-*` / `delete-edge`) to modify an existing diagram in place, preserving user layout. **DO NOT** write a script that regenerates the entire diagram from scratch when the diagram already exists — only generate from scratch when no diagram file exists yet.
- **Example (wrong):** domain model changed three properties on two classes. Agent wrote a 250-line Python script that recreated every class and edge on all three pages, resetting all positions to computed defaults and losing the user's manual layout adjustments.
- **Example (correct):** domain model changed three properties on two classes. Agent used `update-class` to add/remove the changed properties on those two classes, leaving all other classes, edges, and positions untouched.
- **Likely source:** `prompt gap` — SKILL.md describes both full rendering and incremental sync workflows but does not state a preference for incremental when the diagram already exists. The agent defaulted to full regeneration because it was simpler to implement.

- **Status:** confirmed

---

### Dependency edges use straight lines that cut through classes

- **Context:** Rendering dependency edges on the Condition KA page — `Imposed Conditions → Check` and `Applied Effect → Graded Check Result` used the `dependency` edge style (straight dashed line) instead of `dependency-orthogonal`.
- **DO / DO NOT:** **DO** use `dependency-orthogonal` for all dependency edges so they route around classes with right-angle corners, just like associations and compositions. **DO NOT** use the straight `dependency` style when there are classes between the source and target — a straight dashed line will cut directly through them.
- **Example (wrong):** `Imposed Conditions` (x=40, y=320) → `Check` (x=1120, y=320) with `dependency` style. The straight dashed line passes horizontally through `Imposed Condition` and `Condition Source`, making the diagram unreadable.
- **Example (correct):** Same edge with `dependency-orthogonal` style — the line routes around intervening classes using right-angle bends. Additionally, `Check` repositioned to (x=40, y=800) so the edge path is shorter and avoids the congested row entirely.
- **Likely source:** `prompt gap` — the `diagrams.md` layout guidelines say dependency uses "dashed straight line" which is technically correct for UML but fails in practice when classes sit between source and target. No guidance existed to prefer orthogonal routing for dependencies or to verify edges don't cross classes.
- **Status:** confirmed

---

### No automated detection of edge-on-edge overlap or edge-over-class crossing

- **Context:** Diagrams rendered with overlapping lines — edges stacking on top of each other (same route segment) and edges cutting through class boxes they aren't connected to. The tooling had `check_overlaps` for class-on-class and `check_edge_crossings` using naive center-to-center approximation, but nothing that computed actual orthogonal edge routes or detected edge-on-edge visual overlap.
- **DO / DO NOT:** **DO** run `audit_diagram()` (or `python drawio_tools.py audit <file>`) after every render and fix all violations before declaring done. **DO** use `create_edge()` with explicit `exit_x/exit_y/entry_x/entry_y` anchor points when multiple edges share a class side. **DO NOT** render edges without anchors when shared-anchor violations exist. **DO NOT** skip the audit step.
- **Example (wrong):** Check page: `Check→Difficulty Class` and `Check→Check Result` both exit Check's right side at the default center anchor — they stack as one thick line. `Check→Check Result` route passes straight through `Difficulty Class` box. Agent declared rendering done without running any validation.
- **Example (correct):** After rendering, agent runs `audit_diagram_report(<file>)` which reports `[edge_crosses_class] Check→Check Result crosses through Difficulty Class` and `[edge_on_edge_overlap] Check→DC overlaps Check→CR`. Agent repositions classes or adds explicit anchors until audit shows zero `edge_crosses_class`.
- **Likely source:** `automation gap` — the overlap/crossing detection functions existed but were too naive (center-to-center straight lines, no edge route computation, no edge-on-edge check). No audit CLI existed for the agent to call systematically.
- **Status:** confirmed

---

### Straight inheritance edges cut through classes when subtypes aren't directly below parent

- **Context:** Three subtypes (Opposed Check, Routine Check, Team Check) all inherit from Check. With default `inheritance` style (straight line), edges from subtypes not in the same column as the parent cut diagonally through intervening classes.
- **DO / DO NOT:** **DO** use `inheritance-orthogonal` for subtype edges that are not directly below the parent class. **DO** position at most ONE subtype directly below the parent in the same column; offset others to adjacent columns. **DO NOT** use straight `inheritance` when the diagonal path crosses another class bounding box.
- **Example (wrong):** Team Check at (C2, R4) → Check at (C1, R0) using `inheritance` style. Straight diagonal line from (920, 767) to (560, 115) passes through Difficulty Class bounding box at (760, 40).
- **Example (correct):** Same edge using `inheritance-orthogonal` with anchors `exit_x=0.25, exit_y=0.0, entry_x=0.8, entry_y=1.0`. The orthogonal router creates an L-shaped path that avoids Difficulty Class.
- **Likely source:** `automation gap` — no `inheritance-orthogonal` edge style existed in `EDGE_STYLES`. Added as: `f"{EDGE_ORTHOGONAL}endArrow=block;endSize=16;endFill=0;html=1;"`.
- **Status:** confirmed

---

### Layout validation must be run and iterated to zero edge_crosses_class

- **Context:** Complex diagrams (10+ classes, many edges) require iterative layout adjustment guided by `validate_layout` / `audit_diagram_report`. A single layout attempt rarely achieves zero violations. The critical violations to eliminate are `edge_crosses_class`; `edge_on_edge_overlap` and `shared_anchor` are secondary.
- **DO / DO NOT:** **DO** run `audit_diagram_report()` after every layout change and iterate until all `edge_crosses_class` violations are resolved. **DO** prioritize: (1) no class overlaps, (2) no edge-through-class crossings, (3) minimize edge-on-edge overlaps, (4) minimize shared anchors. **DO NOT** declare a diagram done if any `edge_crosses_class` violation exists. **DO** accept that `edge_on_edge_overlap` and `shared_anchor` are sometimes unavoidable in complex diagrams with many edges sharing common classes.
- **Example (wrong):** Agent generated diagram, saw "VIOLATIONS FOUND" in audit, declared done anyway because "the Draw.io router will handle it".
- **Example (correct):** Agent ran audit, found 8 violations. Repositioned Character from C2→C3, switched two inheritance edges from straight to orthogonal, added explicit anchors. Reran audit. Repeated 3 more times until `edge_crosses_class` count was zero.
- **Likely source:** `process gap` — no explicit iteration loop defined for layout validation.
- **Status:** confirmed

---

### Domain Language source rendered as a leaner concept map without rows or collaborators

- **Context:** Rendering a Domain Language file (`*-domain-language.md`) to a Draw.io class diagram. The SKILL said "Domain Language — omit type annotations (behaviors only, no types in source)" — which produced cards with bullet-style behavior lines but no rows, no collaborator column, and no association edges. The user expected the Domain Language to render with the same card-rows-collaborators shape as a Domain Model (a "second pass after Domain Language"), with one row per behavior bullet and one folded association edge per cross-concept italicized reference.
- **DO / DO NOT:** **DO** treat the Domain Language as a structured diagram source with the same shape as a Domain Model — each `### concept` is a card, each verb-led behavior bullet is a row `<bullet text> : Collaborator, Collaborator` (collaborators are the bullet's italicized terms), `### Subtype *is a type of* Base` produces inheritance edges, `### term *(boundary)*` stubs become imported cards with `«boundary: OwningModule»` stereotype, and each unique cross-concept italicized reference produces one folded association edge. **DO NOT** render a Domain Language file as a flat concept map without rows or collaborators just because the source doesn't use typed class blocks — the italicized terms in bullets *are* the collaborators.
- **Example (wrong):** ULL `### check` block with three behavior bullets and two italicized terms each. Diagram rendered with `check` card showing the three bullets as plain text, no collaborator column, no edges to `trait`, `d20`, `difficulty class`, `check result`. The page looked like a vocabulary list, not a class diagram.
- **Example (correct):** Same source rendered with `check` card containing three rows (one per bullet), each row labeled with the bullet text and followed by `: Trait, D20, Difficulty Class, Check Result` etc. Folded association edges drawn from `check` to each unique italicized target. Inheritance edge from `### opposed check *is a type of* check` heading.
- **Likely source:** `prompt gap` — SKILL.md only listed three source types and described Domain Language rendering as "behaviors as operations", with no mention of folding italicized terms into a collaborator column or generating association edges. Fixed by: (1) new rule `rules/class-diagram-domain-language-bullets-become-rows.md`, (2) rewrite of SKILL.md Source types and step 7 Domain Language branches, (3) update of `diagrams.md` AI rendering workflow, (4) new bundled rule in the SKILL.md execute_rules block, (5) upstream rule `italic-terms-resolve-to-named-concepts.md` in `abd-domain-language` that guarantees italicized terms have targets.
- **Status:** confirmed
