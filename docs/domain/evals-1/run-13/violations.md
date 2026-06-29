# run-13 — violations report

## Result

**ALL SCANNERS PASS on all three pages (AbdSkill, AiChatAgent, Context-Driven Delivery).**

- `edges_do_not_cross_classes`: PASS
- `edges_do_not_cross_other_edges` (transverse crossings): PASS
- `edges_do_not_overlap_edges` (colinear overlaps): PASS
- Inline `audit_diagram_report`: PASS

## Trajectory (runs 5 → 13)

| Run | AbdSkill edge-crosses | AbdSkill class-crosses | CDD edge-crosses | Notes |
|-----|----------------------|------------------------|-------------------|-------|
| 5   | 2                    | 0                      | 3                 | After `_pull_up_assoc_sinks` (median) — pulled single-source sinks onto source row, forcing same-row U-shapes |
| 6   | 3                    | 1                      | 0                 | After fix #1: `min(src_layers)+1` for sink placement |
| 7   | 1                    | 1                      | 0                 | After fix #2: anchor sort by direction-aware key (group by above/below, sort by distance with correct sign) |
| 8   | 0                    | 1                      | 0                 | All edge-edge crossings gone; class crossing was `Practice → Reference` via SupportSkill |
| 9   | 1                    | 0                      | 0                 | After fix #3: `_stagger_target_approach` inserts an axis-aligned corner before the stagger point so source→stagger isn't a diagonal |
| 10  | 0                    | 0                      | 0                 | After fix #4: stagger validates each offset against class rects AND other-edge transverse crossings; tries multiple offsets |
| 11  | 1                    | 0                      | 0                 | After fix #5: reject negative offsets that put the stagger point inside the target rect — broke Practice→Reference |
| 12  | 1                    | 0                      | 0                 | After fix #6: `_detour_waypoint` prefers transverse-cross-free candidates; added transverse-cross repair pass to `_route_around_obstacles` |
| **13**  | **0**                | **0**                  | **0**             | After fix #7: stagger validator expands bare 2-point paths to H-V-H so it sees the same geometry drawio/scanner see |

## Fixes deployed (cumulative)

1. **`SugiyamaLayout._pull_up_assoc_sinks`** — pure-association sinks placed at `min(src_layers) + 1` instead of median; collapses multi-layer U-snakes without collapsing single-source sinks onto their source row.
2. **Anchor sort by direction-aware distance** — within each `(node, side)` exit/entry group, edges are ordered so the anchor closest to the corner pointing toward each target gets that target. Primary key: above/below (or left/right) of source; secondary key: distance with sign that puts farthest target at the corner first.
3. **Axis-aligned corner before stagger point** — when the stagger pre-entry waypoint and the previous path point differ in both X and Y, insert a corner so every segment stays axis-aligned.
4. **Stagger validation against class rects and other-edge transverse crossings** — try multiple offsets (smaller, larger, opposite-direction); only accept offsets that introduce no new class or edge crossings.
5. **Reject negative offsets inside the target rect** — the stagger pre-entry waypoint must lie outside the target's bounding box, otherwise the edge enters from the wrong side.
6. **Transverse-cross repair pass in `_route_around_obstacles`** — detects perpendicular edge-on-edge crossings (not just colinear overlaps) and re-routes via `_detour_waypoint` with the other edge's path as forbidden lanes. `_detour_waypoint` itself now prefers candidates that don't transversely cross any existing edge.
7. **H-V-H expansion of 2-point paths in transverse-cross checks** — bare edges with no waypoints render as L-shapes (H-V-H), so the validator now expands them before checking, matching drawio and the audit scanners.

## New scanner added

`scanners/edges_do_not_cross_other_edges.py` — detects **transverse** (perpendicular) edge-on-edge crossings. Earlier runs had silent crossings because the existing `edges_do_not_overlap_edges` scanner only checked **colinear** overlaps.
