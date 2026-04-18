# Draw.io Sequence Diagram Layout Rules

This document defines what "correct" looks like for Domain Walkthroughs / Sequence Diagrams in Draw.io. Since sequence diagrams rely heavily on spatial meaning (horizontal = objects, vertical = time), these rules are critical for a valid diagram.

**Templates:** New or updated sequence diagrams should start from **`templates/domain realization template.drawio`**; Markdown walkthroughs should follow **`templates/domain walkthrough template.md`** (see `content/parts/sequence-diagrams.md`).

---

## Crucial Visual Layout Rules for Sequence Diagrams

These spatial expectations must be followed whether the agent is creating or evaluating diagrams:

- **Lifeline Alignment:** All participant lifelines must be perfectly aligned horizontally at the top of the canvas.
- **Execution Bar Placement:** Execution bars (activations) must be placed exactly centered on the vertical dashed line of the lifeline.
- **Nested Executions:** For nested method calls or internal behavior, the nested execution bar must be stacked precisely on the right edge of the parent execution bar and offset slightly downwards to indicate time progression.
- **Strict Time Flow:** Vertical space strictly represents time; there should be no vertical overlap of independent sequential operations.
- **Crucial Connection Anchors:** Message arrows must always snap exactly to the outer edge of the execution bar (activation rectangle), NEVER to the center dashed lifeline itself.
- **Message Angles:** All message arrows must be perfectly horizontal (0-degree angle) without any diagonals.
- **Return Messages:** Returns (dashed open arrows) must originate from the bottom edge of the returning execution bar and snap back to the original caller's execution bar.

---

## 1. Lifeline Alignment

All participant lifelines (the boxes at the top containing object/class names) must be perfectly aligned horizontally.

**Rule:** Every lifeline header cell must share the exact same `y` coordinate.

### ✓ Correct Alignment
```xml
<!-- Initiator at y=40 -->
<mxCell id="lifeline1" value="Initiator" style="shape=umlLifeline;..." vertex="1" parent="1">
  <mxGeometry x="100" y="40" width="100" height="600" as="geometry" />
</mxCell>

<!-- API Controller at y=40 -->
<mxCell id="lifeline2" value="api:Controller" style="shape=umlLifeline;..." vertex="1" parent="1">
  <mxGeometry x="300" y="40" width="100" height="600" as="geometry" />
</mxCell>
```

---

## 2. Execution Bar (Activation) Positioning

Execution bars (the vertical rectangles showing when an object is active) must be perfectly centered on their parent lifeline's dashed line.

**Rule:** Assuming the execution bar has `width=10` and the parent lifeline has `width=100`, the `x` offset of the execution bar *relative to its parent* must be exactly `45` (i.e., `(100 - 10) / 2`).

### ✓ Correct Execution Bar
```xml
<mxCell id="exec1" value="" style="html=1;points=[];perimeter=orthogonalPerimeter;..." vertex="1" parent="lifeline2">
  <mxGeometry x="45" y="80" width="10" height="160" as="geometry" />
</mxCell>
```

---

## 3. Nested Executions (Self-Calls)

When an object makes a call to itself or has a nested execution block, the child execution bar must be visually stacked to the right of the parent bar.

**Rule:** A nested execution bar must have its left edge exactly touching the right edge of its parent. Relative to the parent lifeline, if the parent execution bar is at `x=45` with `width=10`, the nested execution bar must be at `x=55` (with a `y` offset greater than the parent's `y` to show time passing).

### ✓ Correct Nested Execution
```xml
<!-- Parent Execution -->
<mxCell id="exec_parent" value="" style="..." vertex="1" parent="lifeline2">
  <mxGeometry x="45" y="80" width="10" height="160" as="geometry" />
</mxCell>

<!-- Nested Execution (e.g. private method call) -->
<mxCell id="exec_child" value="" style="..." vertex="1" parent="lifeline2">
  <!-- x=55 touches the right edge of the parent (45+10) -->
  <!-- y=110 starts after the parent started (80) -->
  <mxGeometry x="55" y="110" width="10" height="60" as="geometry" />
</mxCell>
```

---

## 4. Message Connections (Crucial)

Message arrows must ALWAYS connect to the edges of the **Execution Bars**, NEVER directly to the dashed center line of the Lifeline.

**Rule:**
- A **synchronous call** (solid line) must originate from the right or left edge of the sender's execution bar and terminate at the top-left edge of the receiver's newly created execution bar.
- A **return message** (dashed line) must originate from the bottom edge (or bottom-left/right edge) of the receiver's execution bar and return to the edge of the sender's execution bar.

*Note: Draw.io handles this via `source` and `target` attributes pointing to the IDs of the execution bars, not the lifelines.*

### ❌ Wrong Connection (Connected to Lifeline)
```xml
<!-- WRONG: source and target point to the lifelines themselves -->
<mxCell id="msg1" edge="1" source="lifeline1" target="lifeline2">
  ...
</mxCell>
```

### ✓ Correct Connection (Connected to Execution Bars)
```xml
<!-- CORRECT: source and target point to the execution rectangles -->
<mxCell id="msg1" edge="1" source="exec1" target="exec2">
  ...
</mxCell>
```

---

## 5. Message Angles

Time flows strictly downwards. A single message happens conceptually in an instant of visual time.

**Rule:** All message lines (calls and returns) must be perfectly horizontal (0-degree angle). The `y` coordinate of the start point must equal the `y` coordinate of the end point. Diagonal message lines are strictly prohibited.

### ❌ Wrong (Diagonal Message)
```xml
<!-- A message originating at y=150 but arriving at y=170 -->
```

### ✓ Correct (Horizontal Message)
```xml
<!-- The message stays perfectly horizontal -->
```

*(In Draw.io XML, when correctly snapped to execution bars, the orthogonal router ensures horizontal lines if the target execution bar's `y` placement matches the origin point's `y`).*

---

## 6. Time Flow Overlaps

Vertical space represents time.

**Rule:** Independent, sequential operations must not overlap vertically. If Object A calls Object B, and then waits, and then calls Object C, the execution bar for Object C must have a `y` coordinate that starts *after* (is numerically greater than) the bottom edge of Object B's execution bar.

### ✓ Correct Time Flow
```xml
<!-- Call to B happens first -->
<mxCell id="execB" ...>
  <!-- starts at y=100, ends at y=160 -->
  <mxGeometry x="45" y="100" width="10" height="60" as="geometry" />
</mxCell>

<!-- Call to C happens sequentially AFTER B returns -->
<mxCell id="execC" ...>
  <!-- starts at y=180, which is > 160 -->
  <mxGeometry x="45" y="180" width="10" height="50" as="geometry" />
</mxCell>
```