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
