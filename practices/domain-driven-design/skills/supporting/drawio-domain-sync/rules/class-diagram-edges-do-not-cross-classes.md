# Rule: Edges Do Not Cross Classes

**Scanner:** `scanners/edges_do_not_cross_classes.py`

An edge in a class diagram represents a relationship between exactly two classes — its source and its target. When the routed segments of that edge pass through a *third* class's bounding box, the third class appears to participate in the relationship even though it does not. Readers misread ownership, multiplicities, and direction. A passing diagram routes every edge so that it never enters the bounding box of any class except its two endpoints; a failing diagram lets edges cut through unrelated class cards.

## DO

- Route edges around intervening classes using explicit `<Array as="points">` waypoints in the edge's `mxGeometry`.

  **Example (pass):** `ContextDrivenDeliverySkill → AbdSkill` exits the bottom of `ContextDrivenDeliverySkill` at x=200 and enters the top of `AbdSkill`. Because `PracticeSkill` (x=506..766, y=320..486) sits on the straight path, the edge inserts a waypoint at (280, 780) — the edge dog-legs left of `PracticeSkill` and clears it cleanly.

- Choose anchor sides that put the obstacle off the direct path before falling back to waypoints.

  **Example (pass):** `AbdSkill → Reference` exits the right side of `AbdSkill` (exitX=1, exitY=0.5) and enters the top of `Reference` (entryX=0.5, entryY=0). The path swings right and down past `Practice` and `Template` because the chosen anchors keep the route in the empty space between cells.

## DO NOT

- Allow an edge's straight-line segment to pass through a non-endpoint class.

  **Example (fail):** `AbdSkill → Reference` exits the bottom of `AbdSkill` (468, 876) and goes straight to `Reference` (1270, 1036). The segment cuts through `Template` (780..1040, 1036..1378) — the reader sees a phantom edge attached to `Template`.

- Rely on Draw.io's auto-router for long inheritance edges that cross sibling classes.

  **Example (fail):** `ContextDrivenDeliverySkill → AbdSkill` is drawn as a single source→target edge with no waypoints. The default orthogonal router takes the shortest L-shape through `PracticeSkill`, making it appear that `PracticeSkill` is on the inheritance chain.
