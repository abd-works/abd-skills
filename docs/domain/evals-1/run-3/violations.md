# Run 3 — Violations (AbdSkill page only)

## Audit summary

```
Page AbdSkill — FAIL
  [edge_on_edge_overlap] PracticeSkill->AbdSkill (inh) overlaps AbdSkill->Reference at y=290
  [edge_on_edge_overlap] SupportSkill->PracticeSkill (inh) overlaps PracticeSkill->Reference at y=616
  [edge_on_edge_overlap] AbdSkill->Reference overlaps PracticeSkill->Reference at x=476 (vertical column)
```

## Diff from run-2

| Category               | Run 1   | Run 2   | Run 3   |
| ---------------------- | ------- | ------- | ------- |
| edge_crosses_class     | 2       | 2       | **0** ✅ |
| edge_on_edge_overlap   | 1       | 1       | 3 ⚠️    |
| hierarchy_flow         | 0       | 0       | 0       |

All `edge_crosses_class` violations on AbdSkill are eliminated. The new
obstacle-avoiding U-shape router validates candidates against the audit's
straight-line interpretation and uses **fully axis-aligned** routes. It also
treats default H-V-H routes of other edges as occupied lanes, so detours
avoid columns/rows already used. Side benefit: the Context-Driven Delivery
page now passes cleanly (was 1 crossing + 1 overlap in run-2).

The remaining defects on AbdSkill are all `edge_on_edge_overlap` and share a
common root cause: **source-side row collisions**.

## Root causes

### V1. y=290 row (AbdSkill bottom)

- `PracticeSkill→AbdSkill` (inheritance) is an H-V-H route whose final
  horizontal stub at y=290 spans x=318–574 (entering AbdSkill bottom-left).
- `AbdSkill→Reference` (assoc) exits AbdSkill bottom-center at (665, 290),
  so its first horizontal stub at y=290 spans x=476–665 (going LEFT before
  the U-shape drops to Reference).
- Overlap window: x=476–574 at y=290. Length 98 px.

This always overlaps regardless of bypass column choice — any U-shape exit
from AbdSkill's bottom must include an H stub at y=290 that crosses through
the [318, 574] range used by the inheritance edge.

### V2. y=616 row (PracticeSkill bottom)

- `SupportSkill→PracticeSkill` (inheritance, H-V-H) ends with an H stub at
  y=616 from x=318–500.
- `PracticeSkill→Reference` exits PS bottom at (409, 616), starts with an H
  stub at y=616 from x=409–476.
- Overlap window: x=409–476 at y=616. Length 67 px.

Same shape as V1, one storey down.

### V3. x=476 vertical column

- `AbdSkill→Reference`'s U-shape uses column x=476 from y=290 to y=1326.
- `PracticeSkill→Reference`'s U-shape uses the same column x=476 from
  y=616 to y=1326.
- Overlap window: y=616–1326 at x=476. Length 710 px.

Both edges share blockers (only `Practice`), so both compute the same
`cluster_right = 192+260+24 = 476` lane. With my new staggered candidates,
the router did try x=504 and x=560, but those landed within 12px of the
default-routed inheritance verticals at x=500 and x=506, also overlapping.

## What needs to change for run-4

The three remaining defects all stem from **edges sharing a source/target
side** at a row that's already used by an axis-aligned inheritance stub.
Routing alone can't fully fix this — we need to **reassign the side** that
the offending association edges use.

Concrete plan for run-4:

1. **Side reassignment**: after `_dominant_side` chooses an initial side, run
   a follow-up pass that detects "crowded source-side rows" — a row at the
   source's top/bottom where another edge already terminates. For the
   second offender, switch its exit to a perpendicular side (left/right).

2. **Exit-from-side coordination**: track `(source, side)` and `(target, side)`
   occupancy. When a source has >1 association on the same side, force the
   second one off that side. Same for targets.

3. **Stagger inheritance vs association at shared rows**: as a safety net,
   when two edges still share a row, perturb one's anchor by half a row
   (use entryY != 0/1) so the stubs sit at distinct y values.

Hierarchy direction is intentionally unchanged from run-2/3 — the rule file
mandates "base above derived" and we follow it. (Note: the hand-curated good
reference does the opposite, and the audit on the good reference reports
3 hierarchy_flow violations + 4 approximate crossings, so its lines are not
unambiguously "good" by the same audit either. We'll keep the rule.)
