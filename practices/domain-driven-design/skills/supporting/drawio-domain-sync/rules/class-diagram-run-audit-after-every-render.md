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
