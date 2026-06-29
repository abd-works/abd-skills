# Run 2 — Violations (AbdSkill page only)

## Context

- Generated file: `run-2/abd-skills-domain-mode-generated.drawio`
- Reference: `evals/abd-skills-domain-model-good.drawio`
- Skill source edited under: `c:\dev\abd-skills\practices\domain-driven-design\skills\supporting\drawio-domain-sync\`
- Deployed to: `c:\dev\paradise-mobile\.cursor\skills\drawio-domain-sync\`

## What changed since run-1

- Added rule `class-diagram-edges-do-not-cross-classes.md`.
- Added rule `class-diagram-edges-do-not-overlap-other-edges.md`.
- Added scanner `scanners/edges_do_not_cross_classes.py`.
- Added scanner `scanners/edges_do_not_overlap_edges.py`.

These two scanners now run and produce concrete violation lists. They expose what
was already broken — the underlying layout engine has not been changed yet.

## Audit summary

```
[edge_crosses_class]   AbdSkill -> Reference (association) crosses ContextDrivenDeliverySkill
[edge_crosses_class]   PracticeSkill -> Reference (association) crosses Practice
[edge_on_edge_overlap] AbdSkill -> Reference overlaps Practice -> Reference at y=1326
```

Hierarchy-flow violations: **0** (run-2 keeps the rule "base above derived" — AbdSkill
at y=60 sits above its subclasses PracticeSkill / ContextDrivenDeliverySkill at y=450,
and SupportSkill at y=952 sits below PracticeSkill). Note this is the opposite of the
hand-curated good reference, which draws derived-above-base; that mismatch is left as-is
for now because the rule file explicitly mandates this direction.

## Concrete violations and root cause

### V1. `AbdSkill -> Reference` crosses `ContextDrivenDeliverySkill`

| Box                          | x range  | y range   |
| ---------------------------- | -------- | --------- |
| AbdSkill (src)               | 535–795  | 60–290    |
| ContextDrivenDeliverySkill   | 548–808  | 450–530   |
| Reference (tgt)              | 201–461  | 1326–1428 |

Edge anchors: `exit=(0.5, 1)` → `(665, 290)`, `entry=(0.15, 0)` → `(240, 1326)`.
Waypoint added by `_route_around_obstacles`: **`(476, 1326)`**.

Resulting orthogonal route (drawio expansion):

```
(665, 290) → (665, 1326) → (476, 1326) → (240, 1326)
```

The vertical segment at `x=665` from y=290 to y=1326 passes straight through
ContextDrivenDeliverySkill (x=548–808, y=450–530).

**Root cause.** `_detour_waypoint` chose the waypoint with the shortest *straight-line*
path that doesn't pierce the worst obstacle (Practice). But drawio renders edges
with H-V-H orthogonal segments, and the resulting orthogonal path crosses a
*different* class (CDDS) that the straight-line check ignored.

### V2. `PracticeSkill -> Reference` crosses `Practice`

| Box                | x range  | y range   |
| ------------------ | -------- | --------- |
| PracticeSkill (src)| 188–448  | 450–616   |
| Practice           | 192–452  | 952–1166  |
| Reference (tgt)    | 201–461  | 1326–1428 |

Edge anchors: `exit=(0.85, 1)` → `(409, 616)`, `entry=(0.5, 0)` → `(331, 1326)`.
Waypoint added: **`(370, 928)`**.

Resulting orthogonal route:

```
(409, 616) → (409, 928) → (370, 928) → (370, 1326) → (331, 1326)
```

The vertical segment at `x=370` from y=928 to y=1326 is inside Practice's x range
(192–452) for y=952–1166. The detour waypoint dog-legs onto a column that itself
goes through Practice.

**Root cause.** Same as V1: straight-line obstacle check approves a candidate
whose orthogonal expansion crosses another class.

### V3. `AbdSkill -> Reference` overlaps `Practice -> Reference` at y=1326

Both edges terminate on Reference's top side (entry on (entry_y=0)). After their
respective detour waypoints, both produce a horizontal segment at `y=1326`:

```
AbdSkill -> Reference :   (476, 1326) → (240, 1326)
Practice -> Reference :   (372, 1326) → (422, 1326)
```

These segments overlap on the interval `x ∈ [372, 422]` at the same y, causing
the visual "edges on top of edges" defect.

**Root cause.** `_route_around_obstacles` doesn't coordinate horizontal-final
segments. Multiple edges entering a target on the same side at distinct anchor
points still produce overlapping horizontal segments when the waypoint
introduces a stub on the same y-row as another edge's final approach.

## What needs to change for run-3

1. **Replace straight-line detour-candidate filtering with orthogonal-route
   filtering.** `_detour_waypoint` (and helpers) must, for every candidate
   waypoint, compute the resulting H-V-H expansion of *both* legs and reject any
   candidate whose expansion crosses *any* non-endpoint class — not just the
   original obstacle.

2. **Iterate the waypoint search.** When no single waypoint produces a
   crossing-free orthogonal route, try a *pair* of waypoints (one to go around
   the worst obstacle, a second to come back into the entry anchor's column /
   row).

3. **Side-stagger the final approach.** When two edges share the same target
   side and the same approach y/x row, perturb the second edge's
   pre-target waypoint by ±NODE_GAP/2 so the two horizontal stubs sit at
   distinct y-rows (e.g. y=1326 vs y=1310).

These three changes together should clear V1, V2, V3 on the AbdSkill page.
