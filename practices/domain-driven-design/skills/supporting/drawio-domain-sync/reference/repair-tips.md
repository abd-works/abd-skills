# repair-tips — drawio-domain-sync Fix Patterns

Read this alongside `common/reference/agentic-repair-loop.md` § 4 before
writing any fix script for this skill.

---

## Fix script scaffold

```python
from drawio_tools import (
    load_drawio, save_drawio, get_page,
    find_cell_by_name, find_cell_by_id, get_all_edges,
    set_edge_anchors, add_edge_waypoints,
    audit_diagram_report,
)

_, mxfile = load_drawio(DIAGRAM)
_, root   = get_page(mxfile, "PageName")

edge = find_cell_by_id(root, "edge-id")
set_edge_anchors(edge, exit_x=0.5, exit_y=1.0, entry_x=0.5, entry_y=0.0)
add_edge_waypoints(edge, [(x1, y1), (x2, y2)])

save_drawio(DIAGRAM, mxfile)
print(audit_diagram_report(DIAGRAM))
```

---

## Orthogonal edge routing — key insight

`_compute_edge_segments_ex` expands orthogonal edges using the **previous
segment direction** to decide corner orientation:

- `prev_dir = 'v'` → next bend is **vertical first** → corner at `(ax, by)`
- `prev_dir = 'h'` or `None` → next bend is **horizontal first** → corner at `(bx, ay)`

A **5-pixel margin** is added to all class bounding boxes during intersection
tests. Plan waypoints so every segment runs through a clear corridor.

---

## Three reliable escape corridors

1. **Bottom-then-right:** Exit bottom, waypoint below all row classes, travel
   right then up to target.
2. **Left corridor:** Exit top, waypoint to the left of the leftmost blocker
   class, travel up then right to target.
3. **Right corridor:** Exit top/bottom, waypoint to the right of the rightmost
   class on the row, travel up/down then across.

---

## Overlap thresholds

| Check | Parameter | Value |
|-------|-----------|-------|
| Segment overlap | `_segments_overlap_1d` threshold | 8 px |
| Edge proximity | `_edge_segments_overlap` proximity | 12 px |

Parallel segments must be separated by **> 12 px** to avoid `edge_on_edge_overlap`.

---

## shared_anchor rule

Multiple edges that leave or enter the same class at the same anchor point
(same `exitX/Y` or `entryX/Y`) trigger `shared_anchor`. Fix by assigning each
edge a distinct anchor value (even 0.01 apart is enough).
