# Run 17 — AbdSkill page only

## Audit result

**Status: ALL THREE SCANNERS PASS on AbdSkill.**

- `edges_do_not_cross_classes` — pass
- `edges_do_not_overlap_edges` — pass
- `edges_do_not_cross_other_edges` — pass

## What changed since run-16

Two bugs from the prior runs were addressed and a third one — that the
scanner and the renderer disagreed on what an edge actually looks like — was
removed.

### Fix 1 — anchor pool merge (exit + entry share one side pool)

Previously every (node, side) had two anchor pools: one for outgoing edges
and one for incoming edges. The two pools were allocated independently, so
when a side carried exactly one exit and one entry they BOTH landed on the
default `0.5` anchor. Concretely in run-13:

- `AbdSkill` left side: `AbdSkill→Rule` exit and `PracticeSkill→AbdSkill`
  entry both at `(0, 0.5) = (721, 175)`.
- `PracticeSkill` bottom: `PracticeSkill→Reference` exit and
  `SupportSkill→PracticeSkill` entry both at `(0.5, 1) = (444, 616)`.

Now `side_groups[(node, side)]` is one list with `(pair, role)` tuples, and
`_spread_anchors(len(items))` allocates distinct fractions across the
side. Two items on a side become `0.15` and `0.85`, three become
`0.15 / 0.5 / 0.85`, etc. The angle-based sort still keeps neighbouring
anchors aligned with target geometry, so non-crossing fanning is preserved.

### Fix 2 — only perpendicularise an association when the alternative side is empty

The `_perpendicular_side` pass was originally introduced because a single
anchor-per-side default forced inheritance edges and association edges to
collide on the same point. With Fix 1 the merged pool already gives them
distinct positions, so the perpendicular move is only useful when both
the perpendicular candidate is truly empty AND the original side is
inheritance-heavy. The new rule:

```text
if original side has inheritance traffic AND perpendicular side is empty:
    move the association to the perpendicular side
else:
    keep the natural side and let the merged anchor pool spread the edges
```

This is why `PracticeSkill→Reference` now exits PS's right side at
`(1, 0.85) = (574, 591)` instead of being shoved down to PS-bottom where it
overlapped `SupportSkill→PracticeSkill`.

### Fix 3 — every emitted segment is axis-aligned (no more drawio ↔ scanner mismatch)

`edgeStyle=orthogonalEdgeStyle` makes drawio render each waypoint pair as
an L-pair (horizontal-then-vertical or vertical-then-horizontal) when the
two points are not axis-aligned. The scanner, however, walked each pair
as a straight line. That meant a single oblique waypoint
(e.g. `[(1010, 256)]` between `(981, 256)` and `(1394, 465)`) silently
passed the audit even though drawio would actually bend it through a
class.

A normalisation pass now runs after stagger:

1. For each edge, expand every non-axis-aligned segment into an L-pair,
   choosing the corner orientation that continues the previous segment's
   direction.
2. Try both orientations for the very first ambiguous bend (H-first and
   V-first) and pick the one with no class crossing and no new transverse
   edge crossing.
3. Collapse colinear consecutive points so the polyline stays minimal.

The scanner's `_compute_edge_segments_ex` was updated with the same
expansion so its model of an oblique waypoint matches what drawio
renders. Defence in depth: even hand-edited diagrams now audit against
the geometry drawio actually draws.

## AbdSkill page summary

```text
NODES (y-major, key abstraction first)
  y =   60   AbdSkill                            ← KA, top
  y =  450   PracticeSkill  Rule  CDDS  Reference  Scanner  Template
  y =  968   SupportSkill   Practice
  y = 1342   AbdAgent

EDGES (each segment now axis-aligned)
  PS  → AbdSkill   PS-right(0.15) → AbdSkill-left(0.15)
  SS  → PS         SS-top(0.5)    → PS-bottom(0.85)
  CDDS→ AbdSkill   CDDS-top(0.5)  → AbdSkill-bottom(0.85)
  AbdSkill→ Reference   right(0.85) → left(0.15)
  AbdSkill→ Rule        bottom(0.15) → top(0.5)
  AbdSkill→ Scanner     right(0.5) → left(0.5)
  AbdSkill→ Template    right(0.15) → left(0.5)
  PS  → Practice   PS-bottom(0.15) → Practice-top(0.5)
  PS  → Reference  PS-right(0.85) → Reference-left(0.5)
  Practice→ Reference  right(0.5) → left(0.85)
  Practice→ AbdAgent   bottom(0.5) → top(0.5)
```

No two anchors share a point. No edge segment travels along another edge
segment for more than 8 pixels. No segment crosses a non-endpoint class.
