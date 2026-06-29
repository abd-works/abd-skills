# Rule: Edges Do Not Overlap Other Edges

**Scanner:** `scanners/edges_do_not_overlap_edges.py`

Two edges that share the same anchor point on a class or that run parallel along the same line for a long span are visually indistinguishable — readers see one thick line and lose the information that there are two relationships. A passing diagram routes overlapping pairs apart with distinct anchors or waypoints; a failing diagram lets two or more orthogonal edges run on top of each other along the same column or row of pixels.

## DO

- Spread parallel runs apart by ±20–40px using waypoints, so two segments that would otherwise share the same column or row become visibly separate lines.

  **Example (pass):** `AbdSkill → Rule` and `AbdSkill → Scanner` both exit the bottom of `AbdSkill`. `AbdSkill → Rule` uses exitX=0.15 and a waypoint at (190, 830); `AbdSkill → Scanner` uses exitX=0.5 with no waypoint. The two edges never share a column.

- Give each edge a unique exit/entry anchor on the same class side and choose waypoints that keep the perpendicular runs offset from one another.

  **Example (pass):** Three edges leave the bottom of a class at exitX=0.15, 0.5, 0.85 — three vertical drops in three distinct columns; even if they share the same y-row downstream, each visibly travels its own column for the first segment.

## DO NOT

- Let two orthogonal edges share the same column or row for more than ~12px without an offset.

  **Example (fail):** `AbdSkill → Rule` and `AbdSkill → Scanner` both exit at exitX=0.5, exitY=1. Both drop straight down on column x=468 for ~160px before fanning out. A reader sees one fat vertical line instead of two edges.

- Use identical exit/entry anchor coordinates on the same side of the same class for more than one edge.

  **Example (fail):** Inheritance edge and association edge both exit `AbdSkill` at exitX=0.5, exitY=1; they leave from the literal same point and overlap until they split.
