# Run 4 — Violations (AbdSkill page only)

## Audit summary

```
Page AbdSkill — PASS  (no edge_crosses_class, no edge_on_edge_overlap)
Page AiChatAgent — PASS
Page Context-Driven Delivery — PASS
```

Both new scanners agree:

```
[PASS] AbdSkill: no edges cross non-endpoint classes
[PASS] AbdSkill: no edges overlap other edges
[PASS] AiChatAgent: no edges cross non-endpoint classes
[PASS] AiChatAgent: no edges overlap other edges
[PASS] Context-Driven Delivery: no edges cross non-endpoint classes
[PASS] Context-Driven Delivery: no edges overlap other edges
```

## Diff from run-3

| Category               | Run 1 | Run 2 | Run 3 | Run 4   |
| ---------------------- | ----- | ----- | ----- | ------- |
| edge_crosses_class     | 2     | 2     | 0     | **0** ✅ |
| edge_on_edge_overlap   | 1     | 1     | 3     | **0** ✅ |
| hierarchy_flow         | 0     | 0     | 0     | 0       |

## What changed since run-3

A single new step in the pipeline cleared all remaining overlaps:

**Side reassignment** (`render_ka` → `_add_edges`). After `_dominant_side`
chooses an initial exit/entry side per edge, a second pass walks all
association/composition/aggregation edges and reroutes them off any
side a class also uses for inheritance. The rule is:

> If a source's chosen exit side already carries inheritance traffic
> (incoming or outgoing), move the association exit to the
> perpendicular side that points toward the target.

Concretely, on the AbdSkill page:

| Edge                          | Run 3 exit | Run 4 exit | Reason                                                 |
| ----------------------------- | ---------- | ---------- | ------------------------------------------------------ |
| AbdSkill → Reference          | bottom     | **left**   | AbdSkill's bottom has inheritance entries from PS, CDDS |
| PracticeSkill → Reference     | bottom     | **right**  | PS's bottom has inheritance entry from SS              |
| PracticeSkill → Practice      | bottom     | **right**  | Same reason                                            |

With the source-side stub moved off the crowded row, the U-shape detour now
fits in clean lanes and the lane-aware detour picker (added in run-3) has
plenty of room.

## Pipeline state — done

The four-step pipeline now reliably produces a clean diagram for the
abd-skills domain model:

1. **Layout (Sugiyama)** — base above derived, association targets below.
2. **Side selection** — dominant side + reassign-off-inheritance-rows.
3. **Anchor spread** — multiple edges sharing a side get distinct anchor
   positions.
4. **Obstacle-avoiding U-shape detour** — fully axis-aligned, lane-aware,
   crossing-validated against the audit's interpretation.

All three pages of the abd-skills domain model render with zero
`edge_crosses_class` and zero `edge_on_edge_overlap` violations.
