# Draw.io Class Diagram Layout Rules

This document defines what "correct" looks like at the XML level so that
the `verify` command and any reviewing agent have unambiguous ground truth.

**Templates:** New or updated class diagrams should follow the structure and style of **`templates/domain model template.drawio`**; Markdown companions should follow **`templates/domain model template.md`** (see `content/parts/class-diagrams.md`).

---

## Crucial Visual Layout Rules for Class Diagrams

These spatial expectations must be followed whether the agent is creating or evaluating diagrams (either directly via the CLI's relayout and fix-edge-styles, or through manual editing instructions):

- **Vertical Hierarchy:** Superclasses and abstract classes must be positioned vertically above their subclasses, with the diagram flowing from general (top) to specific (bottom).
- **Horizontal Peers:** Peer associations and composition relationships are arranged horizontally to balance the diagram's footprint.
- **Anchor Points:** Relationship lines must snap to the fixed connection anchor points on the perimeter of the class boxes. Lines should never float unattached, terminate inside the box, or intersect with text.
- **Line Routing:** Use orthogonal (right-angled/stepped) routing for associations and compositions. Inheritance arrows must point straight up.
- **Avoid Crossings:** When tweaking layouts manually, actively rearrange boxes to minimize the number of relationship lines that cross over one another.
- **Z-Ordering & Labels:** Ensure text labels (like multiplicities) are kept clearly at the immediate ends of connector lines, and bring text/labels to the front (Z-order) so they aren't obscured by lines or grid elements.

---

## 1. Class bounding boxes must never overlap (V1)

### What overlap means in XML

A class is a `<mxCell>` with `style` containing `swimlane` whose `<mxGeometry>`
gives its bounding rectangle: `x`, `y`, `width`, `height`.

Two classes A and B overlap when ALL FOUR of these are true simultaneously:

```
A.x          < B.x + B.width    (A's left edge is left of B's right edge)
A.x + A.width > B.x             (A's right edge is right of B's left edge)
A.y          < B.y + B.height   (A's top edge is above B's bottom edge)
A.y + A.height > B.y            (A's bottom edge is below B's top edge)
```

### ❌ Overlapping example

```xml
<!-- Car: x=100 y=100 w=200 h=242  →  right=300 bottom=342 -->
<mxCell id="Car" value="Car" style="swimlane;..." vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="200" height="242" as="geometry" />
</mxCell>

<!-- CreditCard: x=200 y=200 w=200 h=190  →  overlaps Car by 100×142px -->
<mxCell id="CC" value="CreditCard" style="swimlane;..." vertex="1" parent="1">
  <mxGeometry x="200" y="200" width="200" height="190" as="geometry" />
</mxCell>
```

### ✓ Non-overlapping example

```xml
<!-- Car: x=100 y=100 h=242  →  bottom=342 -->
<mxCell id="Car" ...>
  <mxGeometry x="100" y="100" width="200" height="242" as="geometry" />
</mxCell>

<!-- CreditCard starts 80px below Car's bottom -->
<mxCell id="CC" ...>
  <mxGeometry x="100" y="422" width="200" height="190" as="geometry" />
</mxCell>
```

**Fix:** run `relayout` — it computes actual heights and spaces rows correctly.

---

## 2. Child class must be below parent class (V2)

In a UML class diagram the inheritance arrow points FROM subclass TO superclass,
meaning the arrow goes **upward** on the canvas.  The subclass must therefore
have a **larger `y` value** (lower on the page) than its superclass.

Draw.io coordinate system: `y=0` is the TOP of the canvas, y increases downward.

### ❌ Wrong direction (subclass above parent)

```xml
<!-- Vehicle (superclass) at y=400 — BELOW Car -->
<mxCell id="Vehicle" ...>
  <mxGeometry x="100" y="400" width="200" height="164" as="geometry" />
</mxCell>

<!-- Car (subclass) at y=100 — ABOVE Vehicle — WRONG -->
<mxCell id="Car" ...>
  <mxGeometry x="100" y="100" width="200" height="242" as="geometry" />
</mxCell>

<!-- Inheritance arrow Car→Vehicle goes DOWN, but it should go UP -->
<mxCell style="endArrow=block;dashed=1;endFill=0;..." edge="1"
        source="Car" target="Vehicle" .../>
```

### ✓ Correct direction (subclass below parent)

```xml
<!-- Vehicle (superclass) at y=100 — TOP -->
<mxCell id="Vehicle" ...>
  <mxGeometry x="100" y="100" width="200" height="164" as="geometry" />
</mxCell>

<!-- Car (subclass) at y=344 — BELOW Vehicle (100+164+80 gap) -->
<mxCell id="Car" ...>
  <mxGeometry x="100" y="344" width="200" height="242" as="geometry" />
</mxCell>

<!-- Inheritance arrow goes UP from Car to Vehicle ✓ -->
<mxCell style="endArrow=block;dashed=1;endFill=0;endSize=12;html=1;rounded=0;"
        edge="1" source="Car" target="Vehicle" .../>
```

**Fix:** run `relayout` — it assigns rows by inheritance depth (depth 0 = top).

---

## 3. Edge styles by relationship type (V3)

### 3a. Inheritance — straight diagonal line (NO edgeStyle)

Inheritance uses a **plain straight line** between the two class boxes.
Draw.io draws a straight diagonal when no `edgeStyle` token is present.

**✓ Correct inheritance style:**
```xml
<mxCell style="endArrow=block;dashed=1;endFill=0;endSize=12;html=1;rounded=0;"
        edge="1" source="Car" target="Vehicle" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```
Key: `dashed=1`, `endArrow=block`, `endFill=0`, **no `edgeStyle=`**.

**❌ Wrong — inheritance with orthogonal routing:**
```xml
<!-- edgeStyle=orthogonalEdgeStyle on inheritance creates ugly zig-zags -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;endArrow=block;dashed=1;..."
        edge="1" source="Car" target="Vehicle" .../>
```

### 3b. Association — orthogonal routing (right-angle corners)

```xml
<!-- ✓ Correct association: orthogonal routing, open arrow -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;
               jettySize=auto;html=1;"
        edge="1" source="Person" target="Car" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 3c. Composition — orthogonal routing, filled diamond at WHOLE end

```xml
<!-- ✓ Correct: diamond at the Car (whole) end, orthogonal routing -->
<!-- Edge goes FROM part (Wheel) TO whole (Car); diamond is endArrow -->
<mxCell style="endArrow=diamondThin;endFill=1;endSize=24;html=1;rounded=0;
               edgeStyle=orthogonalEdgeStyle;orthogonalLoop=1;jettySize=auto;"
        edge="1" source="Wheel" target="Car" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 3d. Aggregation — orthogonal routing, hollow diamond at WHOLE end

```xml
<!-- ✓ Correct: hollow diamond at Fleet (whole), line to Plane (part) -->
<!-- Edge goes FROM whole (Fleet) TO part (Plane); diamond is startArrow -->
<mxCell style="endArrow=open;html=1;endSize=12;
               startArrow=diamondThin;startSize=14;startFill=0;
               edgeStyle=orthogonalEdgeStyle;rounded=0;"
        edge="1" source="Fleet" target="Plane" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 3e. Dependency — dashed open arrow (no edgeStyle needed)

```xml
<!-- ✓ Stereotype label on a dependency -->
<mxCell style="endArrow=open;endSize=12;dashed=1;html=1;rounded=0;"
        edge="1" source="Car" target="CarFactory" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<!-- stereotype label child -->
<mxCell style="edgeLabel;html=1;align=center;..." value="&lt;&lt;created by&gt;&gt;"
        vertex="1" connectable="0" parent="EDGE_ID">
  <mxGeometry x="0" y="0" relative="1" as="geometry" />
</mxCell>
```

---

## 4. Explicit waypoints cause extra bends (V4)

Draw.io's orthogonal auto-router finds the minimum-bend path automatically.
Explicit `<Array as="points">` waypoints override that, often producing
unnecessary bends when classes are repositioned.

**❌ Edge with hard-coded waypoints (fragile):**
```xml
<mxCell style="edgeStyle=orthogonalEdgeStyle;..." edge="1"
        source="Fleet" target="Plane" parent="1">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="140" y="-120" />
      <mxPoint x="720" y="-120" />
    </Array>
  </mxGeometry>
</mxCell>
```

**✓ Same edge without waypoints — router picks the clean path:**
```xml
<mxCell style="edgeStyle=orthogonalEdgeStyle;..." edge="1"
        source="Fleet" target="Plane" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

**Fix:** run `fix-edge-styles` — it removes all `<Array as="points">` elements.

---

## 5. Multiple edges must not share an unconstrained connection point (V5)

When two or more edges arrive at (or leave from) the same class without explicit
`entryX`/`entryY` (or `exitX`/`exitY`) port constraints in their `style` string,
Draw.io stacks them all at the same default midpoint — producing a visual pile-up
where multiple arrowheads overlap and the diagram becomes unreadable.

### ❌ Six compositions converging at the same bottom-centre of Character

```xml
<!-- All six arrive at the default bottom-centre of Character — they pile up -->
<mxCell style="endArrow=diamondThin;endFill=1;edgeStyle=orthogonalEdgeStyle;..."
        edge="1" source="Ability"      target="Character" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell style="endArrow=diamondThin;endFill=1;edgeStyle=orthogonalEdgeStyle;..."
        edge="1" source="Skill"        target="Character" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<!-- … same for HeroPoint, Advantage, Complication, Power … -->
```

### ✓ Spread across the bottom side with explicit entry points

```xml
<!-- entryX evenly distributes 6 arrows across the bottom edge -->
<mxCell style="endArrow=diamondThin;endFill=1;edgeStyle=orthogonalEdgeStyle;...
               entryX=0.143;entryY=1;entryDx=0;entryDy=0;"
        edge="1" source="Ability"  target="Character" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<mxCell style="endArrow=diamondThin;endFill=1;edgeStyle=orthogonalEdgeStyle;...
               entryX=0.286;entryY=1;entryDx=0;entryDy=0;"
        edge="1" source="Skill"    target="Character" parent="1">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
<!-- … and so on up to entryX=0.857 for the sixth arrow … -->
```

**Fix:** run `fix-shared-endpoints` — it determines the dominant approach side
(top / bottom / left / right) and distributes `entryX`/`entryY` (or
`exitX`/`exitY`) evenly across it for all unconstrained edges in the group.

> **Preferred over bare entry-point spreading:** see Section 5a below — anchor
> each composition to its specific field row instead. This fully eliminates V5
> and produces a far more readable diagram.

---

## 5a. Field-anchored composition — the preferred routing pattern

When a parent class (e.g. `Character`) owns several child classes through
composition, the cleanest layout is to:

1. **Add a field row** inside the parent for each owned type (e.g. `+ abilities: Ability`)  
2. **Connect the diamond to that field row**, not to the parent class border  
3. **Exit from the SIDE of the child class** (left or right, never top or bottom)  
4. **Keep the diamond co-linear with the line** (diamond faces the same direction as the line segment it is part of — never sideways)  
5. **Use as few waypoints as possible** — ideally zero or one  

### Visual goal

```
[Character]                     [Ability]
┌───────────────────────┐       ┌──────────────┐
│ + powerLevel: int     │       │ + rank: int  │
│─────────────────────  │       │              │
│ + abilities: Ability ◆│───────│              │
│ + skills: Skill      ◆│       └──────────────┘
└───────────────────────┘
```

The diamond (`◆`) sits at the **field row** and points toward the child class.
The line exits the **right or left side** of the child and enters the field row.

### Layout recommendation

Place child classes **to the left or right of the parent**, not directly below.
This allows clean horizontal routing with zero or one waypoint and avoids
long vertical runs that pass through other classes.

```
[Advantage]──────◆ advantages: Advantage  │
[Ability]────────◆ abilities: Ability      │ Character
[HeroPoint]──────◆ heroPoints: HeroPoint  │
[Skill]──────────◆ skills: Skill          │
```

### ✓ Correct XML pattern

```xml
<!-- Source = child class; Target = field row cell inside parent;
     endArrow=diamondThin places the diamond at the field row.
     Child exits from its RIGHT side (exitX=1) toward the field row. -->
<mxCell id="edge-ability" value=""
        style="endArrow=diamondThin;endFill=1;endSize=24;
               edgeStyle=orthogonalEdgeStyle;
               exitX=1;exitY=0.5;exitDx=0;exitDy=0;"
        parent="1" source="AbilityClass" target="AbilitiesFieldRow" edge="1">
  <mxGeometry as="geometry" />
</mxCell>

<!-- The field row cell must have portConstraint=eastwest so the
     diamond connects to its LEFT or RIGHT side, not top/bottom -->
<mxCell id="AbilitiesFieldRow"
        value="+ abilities: Ability"
        style="text;...;portConstraint=eastwest;"
        parent="CharacterClass" vertex="1">
  <mxGeometry y="118" width="300" height="26" as="geometry"/>
</mxCell>
```

Key style attributes:

| Attribute | Value | Reason |
|-----------|-------|--------|
| `source` | child class cell id | composition originates at child |
| `target` | field row cell id (inside parent) | diamond lands at the field |
| `endArrow` | `diamondThin` | filled diamond at target (field row) |
| `exitX=1;exitY=0.5` | right-side exit of child | side exit = clean orthogonal route |
| `portConstraint=eastwest` | on field row | constrains diamond to left or right side |

### ❌ Anti-pattern: diamond entering from the top or bottom

```xml
<!-- Diamond arrives at the parent's bottom edge — produces V5 pile-up
     AND diamond appears sideways or flipped relative to the line -->
<mxCell style="endArrow=diamondThin;endFill=1;
               entryX=0.5;entryY=1;..."   <!-- ← bottom of CHARACTER class -->
        target="CharacterClass" ...>
```

### Rule: diamond co-linearity

The composition diamond must always face **in the same direction as the line
segment it terminates**. If the last segment arrives from the left, the diamond
opens to the left. A sideways diamond (arriving vertically but pointing
horizontally) indicates a mismatched `exitX`/`exitY` or `entryX`/`entryY` and
must be corrected.

### Minimum-waypoint routing

| Child position relative to parent | Typical exit | Waypoints needed |
|------------------------------------|-------------|-----------------|
| Directly left or right, same Y     | right/left   | 0 |
| Left/right but offset vertically   | right/left   | 1 (adjust Y) |
| Below or above (avoid)             | top/bottom   | 2+ (not ideal) |

Prefer placing child classes **laterally** (left/right) so that routes remain
single-segment or single-bend. Stacking child classes directly below the parent
forces multi-waypoint routes and risks V6 overlaps.

---

## 6. Straight-line edges must not pass through unrelated classes (V6)

Dependency edges (`dashed=1`, no `edgeStyle`) draw a straight diagonal line.
When source and target are on opposite sides of the canvas that line can slice
through intermediate class boxes, hiding those classes behind an unrelated arrow.

The `verify` command checks straight-line edges by testing the segment from
source-centre to target-centre against every third class's bounding box
(shrunk by 5 px to avoid false positives at shared borders).

### ❌ Dependency passes through an unrelated class

```
[Check] ————————————————→ [Effect]
           ╱ Power ╲         (Power's box sits on the direct path)
```

### ✓ Resolved options

1. **Run `fix-arrow-overlaps`** — automatically inserts 1–2 waypoints using a
   recursive shortest-path algorithm to route the dependency around all blockers;
   then rerun `verify` to confirm V6 is clear.
2. **Reposition the blocking class** — move it off the arrow corridor as a last
   resort if `fix-arrow-overlaps` cannot find a clean path.

> Note: V6 is a **WARN** (not ERROR) because the obstruction is a layout
> issue. `fix-arrow-overlaps` resolves most cases automatically.

---

## 7. Readability: left-to-right, top-to-bottom reading order

A diagram reads well when:

- Abstract/root classes are at the **top** (small y)
- Concrete subclasses are below (larger y)
- Closely related classes are **horizontally adjacent** (similar x)
- Unrelated groups are visually separated

The `relayout` command implements this automatically by assigning
`y` based on inheritance depth. Within each depth level, siblings
are kept together next to their parent.

---

## Quick summary table

| Relationship    | endArrow         | dashed | edgeStyle         | Diamond  |
|----------------|-----------------|--------|-------------------|----------|
| Inheritance    | `block`          | yes    | **none**          | —        |
| Association    | (default open)   | no     | `orthogonalEdge…` | —        |
| Composition    | `diamondThin`    | no     | `orthogonalEdge…` | filled ◆ |
| Aggregation    | `open` + start   | no     | `orthogonalEdge…` | hollow ◇ |
| Dependency     | `open`           | yes    | none              | —        |
