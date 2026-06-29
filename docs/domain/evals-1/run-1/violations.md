# Violations — Run 1 (AbdSkill tab only)

Generated: `abd-skills-domain-mode-generated.drawio` — page 1, `AbdSkill`
Good:      `abd-skills-domain-model-good.drawio` — page 1, `AbdSkill`
Rules checked: all six files under `drawio-domain-sync/rules/`.

---

## Rule: `class-diagram-base-classes-positioned-above-derived-classes` — FAIL

**What the rule says:** Base classes get a *low y-coordinate* (top of page); derived classes sit *below* them.

The generated diagram does the opposite: children sit at the top, parents at the bottom.

| Class                       | Generated y | Role                              |
|-----------------------------|-------------|-----------------------------------|
| `SupportSkill`              | 60          | grandchild (PracticeSkill → AbdSkill) |
| `ContextDrivenDeliverySkill`| 60          | child of `AbdSkill`               |
| `PracticeSkill`             | 320         | child of `AbdSkill`               |
| **`AbdSkill`**              | **646**     | **base — sits below all three children** |

Inheritance arrows in the generated file therefore point **downward** (`SupportSkill ↓ PracticeSkill ↓ AbdSkill`), which is the explicit anti-pattern in the rule's "DO NOT" section: *"Place a base class below its derived classes."*

The good diagram solves this by putting `AbdSkill` at y=646 with `PracticeSkill` (y=320) and `SupportSkill` (y=210) above it, and `ContextDrivenDeliverySkill` (y=534) to the left of `AbdSkill`. Even the good diagram has `SupportSkill` above `PracticeSkill` (depth-2 above depth-1), but the *parent→base* trunk is correctly oriented.

**Exact CLI artifact:** in `render_ka`'s call to `SugiyamaLayout`, `import_nodes` lifts imported boundary classes to the top — but the layout has no analogous "sink" for derived classes. The longest-path layer assignment puts the deepest derived class at layer 0 because it has no outgoing inheritance edge, so children end up *above* their parents whenever the parent also has non-inheritance outgoing edges.

---

## Rule: `class-diagram-multiple-edges-use-distinct-anchor-points` — PARTIAL FAIL

**What the rule says:** Two or more edges sharing the same side of a class must each carry **explicit and distinct** `exitX/exitY` / `entryX/entryY`.

The generated CLI does set distinct anchors per edge, but it does so by **bucketing every edge into one of three positions (0.15, 0.5, 0.85)**. When more than three edges share the same side that bucketing collapses.

**Concrete failure — AbdSkill bottom edge:** five edges leave the bottom of `AbdSkill`:

| Edge                    | Generated exit anchor |
|-------------------------|------------------------|
| `AbdSkill → Reference`  | exitX=1.0, exitY=0.5 (right side, not bottom — see next violation) |
| `AbdSkill → Rule`       | exitX=0.15, exitY=1   |
| `AbdSkill → Scanner`    | exitX=0.5, exitY=1    |
| `AbdSkill → Template`   | exitX=0.85, exitY=1   |
| `ContextDrivenDeliverySkill → AbdSkill` (entry) | entryX=0.85, entryY=0 |
| `PracticeSkill → AbdSkill` (entry)              | entryX=0.15, entryY=0 |

That's mechanically distinct, but the spacing reveals the second bug:

**Inheritance edge 12 (`PracticeSkill → AbdSkill`):** `exitX=0.15, entryX=0.15` — exit from the bottom-left of `PracticeSkill` enters the top-left of `AbdSkill`. The good diagram routes the same edge with `exitX=0.15, exitY=1` *plus a waypoint at (540, 486)* so the edge dog-legs cleanly. The generated diagram drops the waypoint entirely; the auto-router will draw a tight S-curve across the gap.

---

## Rule: `class-diagram-cross-model-ancestors-shown-on-page` — PASS (with a layout quirk)

The boundary class `AbdAgent «from: AiChatAgent»` is rendered correctly with `dashed=1` and the `«from: AiChatAgent»` stereotype. Good.

However: the good diagram puts `AbdAgent` at (960, 200) — visually grouped near `Practice` whose `agents: AbdAgent` property is the reason it's there. The generated diagram puts `AbdAgent` at (914, 60) — top row, far from `Practice` at (698, 646). The relationship that pulled `AbdAgent` onto the page (`Practice → AbdAgent`) now traverses ~600 vertical pixels diagonally.

This isn't a rule violation per se, but it amplifies the next one.

---

## Rule: `class-diagram-ka-spatial-cohesion` — FAIL

**What the rule says:** Classes within the same KA cluster tightly; boundary classes from other KAs sit visibly outside the cluster (≥200px gap).

In the AbdSkill tab the local KA is `AbdSkill` (9 classes); the boundaries are `Practice`, `AbdAgent`. In the generated diagram those boundary classes are **interleaved** with local AbdSkill-KA classes:

| x range          | Class                          | KA           |
|------------------|--------------------------------|--------------|
| 60               | `Rule`                         | AbdSkill     |
| 194              | `SupportSkill`                 | AbdSkill     |
| 338              | `AbdSkill`                     | AbdSkill     |
| 420              | `Scanner`                      | AbdSkill     |
| 506              | `PracticeSkill`                | AbdSkill     |
| 554              | `ContextDrivenDeliverySkill`   | AbdSkill     |
| **698**          | **`Practice`**                 | **AbdSkill (KA-internal — it IS in this KA)** |
| 780              | `Template`                     | AbdSkill     |
| **914**          | **`AbdAgent` (boundary)**      | **AiChatAgent** |
| 1140             | `Reference`                    | AbdSkill     |

`AbdAgent` at x=914 sits **between** `Template` (x=780) and `Reference` (x=1140) — both AbdSkill-KA locals. The 200px isolation gap the rule asks for does not exist. The good diagram solves this by pushing `AbdAgent` up to y=200 with `Practice` at (1110, 400) — the boundary class is in the top-right corner with `Practice` directly under it, both visibly offset from the AbdSkill cluster.

---

## Rule: `class-diagram-run-audit-after-every-render` — PASS

The CLI does call `audit_diagram_report` at end of run and prints `Audit: VIOLATIONS FOUND` with specifics. The audit ran. The issue is the layout engine doesn't *consume* the audit — it prints and exits.

---

## Edge-routing failures (covered by the rule's spirit, not a separate rule file)

Auditor output already flagged these; restating with the specific source/target so you know what code produced them:

| Generated edge                | Crosses through | Why it happens                       |
|-------------------------------|-----------------|--------------------------------------|
| `ContextDrivenDeliverySkill → AbdSkill` (inh) | `PracticeSkill` | Both children sit at y=60; parent at y=646. The middle-child `PracticeSkill` at (506, 320) blocks the path. |
| `AbdSkill → Reference` (assoc) | `Practice`      | `AbdSkill` exits right (x=598, y=761); `Reference` is far right at (1140, 1036). `Practice` at (698, 646)..(958, 860) sits on the diagonal. |
| `AbdSkill → Reference` (assoc) | `Template`      | Same edge — also clips `Template` (780, 1036)..(1040, 1378) which sits between `AbdSkill`'s bottom-right corner and `Reference`. |
| `PracticeSkill → Reference` (assoc) | `Template` | `PracticeSkill` exits at (727, 486) heading to `Reference` at (1140, 1036). `Template`'s x-range 780..1040 is directly in the path. |

Root cause in the CLI:
1. `_spread_anchors` (line ~614 of `drawio_domain_cli.py`) only spreads anchors per *side* — it doesn't add **waypoints** to route edges around intervening classes. The good diagram uses `<Array as="points">` with explicit waypoints on every problem edge (edges 12, 14, 15, 16, 18, 19, 21, 22). The generated diagram emits zero `<Array as="points">` blocks — every edge is a pure source-to-target line.
2. The Sugiyama layer assignment uses *longest-path from sources*, where "sources" are imported nodes. Locally-defined classes with no outgoing inheritance get pushed to layer 0 (the top), regardless of whether they are inheritance parents or children. That's why `SupportSkill` and `ContextDrivenDeliverySkill` end up at y=60.

---

## Summary

| Rule                                              | Verdict |
|---------------------------------------------------|---------|
| base-classes-positioned-above-derived-classes     | **FAIL** — children at y=60, base at y=646 |
| cross-model-ancestors-shown-on-page               | PASS (stereotype + dashed border correct) |
| ka-spatial-cohesion                               | **FAIL** — boundary `AbdAgent` interleaved between local classes |
| multiple-edges-use-distinct-anchor-points         | PARTIAL — anchors are distinct but lack waypoints, so edges cross other classes |
| run-audit-after-every-render                      | PASS — audit runs |
| ubiquitous-language-bullets-become-rows           | N/A — domain-model source, not domain-language |

The single biggest source of damage is the **layer-assignment direction**: derived classes end up above their parents. Fixing that alone would eliminate ~half the edge crossings because inheritance edges would no longer have to traverse the parent's siblings.
