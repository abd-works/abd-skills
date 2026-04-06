# AGENTS — abd-diagrams

_Merged diagram library from `content/parts/*.md`. Edit those four files, then run `python scripts/build_instructions.py`. **Diagram skill overview:** this skill’s `SKILL.md`. **Linear OOAD walkthrough** (from raw material): sibling **`abd-ooad`** (`../abd-ooad/SKILL.md`)._

---

<!-- source: content/parts/class-diagrams.md -->

# Class Diagrams (Draw.io and Markdown)

## Templates — use these for every create/update

All class-structure work should **start from** or **stay aligned with** the checked-in templates under the skill **`templates/`** folder (paths relative to the skill root):

| Role | Template file | When to use it |
|------|----------------|----------------|
| **Draw.io** | `templates/domain model template.drawio` | **New diagram:** duplicate this file into the workspace, rename, then edit. **Existing diagram:** when adding classes or relationships, keep the same swimlane style, member layout, and collaborator-line conventions as the template. |
| **Markdown** | `templates/domain model template.md` | **New companion doc:** copy structure and headings from this file. **Updates:** when you change the `.drawio` or the `.md`, update the **other** artifact in the same pass and preserve the template’s patterns (classes, `opt` collaborators, `Invariant:` lines). |

Do **not** invent a one-off Markdown shape or Draw.io layout for class models unless the user explicitly opts out — the templates encode Jeff’s notation (collaborators on the second line in Draw.io, matching `opt` / invariants in Markdown).

**CLI:** New diagrams can be created with `scripts/drawio_cli.py`; even then, prefer matching the **visual and structural** conventions of `domain model template.drawio` (or duplicate the template and extend it) so `verify` / layout rules apply cleanly.

## What to keep in sync

When the user asks to **create or update** modeling diagrams:

| Artifact | Draw.io | Markdown companion |
|----------|---------|-------------------|
| **Class structure** | `*.drawio` (see template above; CLI: `drawio_cli.py`) | Same structure and semantics as `templates/domain model template.md` |

**Rule:** If both files exist for a topic, **update both** in the same pass so comments and collaborator lists do not drift. If only one exists, create the missing companion **from the templates** unless the user opts out.

**Speech-to-text note:** “Vast diagram” or “Lost diagram” in informal notes usually means **class diagram**.

## Class diagram — parallel “comments”

Jeff’s style embeds **collaborators** (and optionally **invariants**) next to fields and methods:

- In **Draw.io**, that is the second line in the member cell (indented), as in **`templates/domain model template.drawio`**.
- In **Markdown**, use **`templates/domain model template.md`**: optional collaborators after `opt`, and `Invariant:` lines.

Keep the **same** collaborators and constraints in both places when maintaining dual files.

## Crucial Visual Layout Rules for Class Diagrams

- **Hierarchical Flow:** Superclasses/abstract classes must sit vertically above their subclasses.
- **Orthogonal Routing:** Use right-angled (stepped) routing for associations/compositions. Inheritance arrows must point straight up.
- **Anchor Points:** Lines must snap to the perimeter of class boxes. Never leave them floating or intersecting text.
- **Clear Intersections:** Actively rearrange boxes to minimize crossing lines. Keep labels at the immediate ends of connector lines, and bring text to the front (Z-order) so it isn't obscured.

## File naming (suggested)

| Pair | Example |
|------|---------|
| Class | `orders-model.drawio` + `orders-model.md` |

Shared stem makes sync obvious.

---

<!-- source: content/parts/class-diagram-layout-rules.md -->

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

## 5. Readability: left-to-right, top-to-bottom reading order

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

---

<!-- source: content/parts/sequence-diagrams.md -->

# Sequence Diagrams and Walkthroughs (Draw.io and Markdown)

## Templates — use these for every create/update

All walkthrough / sequence work should **start from** or **stay aligned with** the checked-in templates under the skill **`templates/`** folder (paths relative to the skill root):

| Role | Template file | When to use it |
|------|----------------|----------------|
| **Draw.io** | `templates/domain realization template.drawio` | **New diagram:** duplicate this file into the workspace, rename, replace `{{placeholders}}`, then edit lifelines and messages. **Existing diagram:** when adding lifelines or messages, keep lifeline alignment, execution bars, and arrow-to-activation conventions as in the template. |
| **Markdown** | `templates/domain walkthrough template.md` | **New companion doc:** copy its scenario / walk / pseudo-code structure. **Updates:** when you change the `.drawio` or the `.md`, update the **other** artifact in the same pass so steps and activations stay aligned. |

Optional: add a **Mermaid** `sequenceDiagram` block in the Markdown file for quick preview (GitHub / readers), using **participant names that match** the lifeline headers in the `.drawio` file.

There is **no** `drawio_cli.py` automation for sequence lifelines yet — **always** ground new Draw.io work in `domain realization template.drawio`.

## Terminology (same concept)

These names refer to the **same** kind of artifact:

- **Domain walkthrough**
- **Domain realization**
- **Domain interaction**
- **Sequence diagram**

Use whichever label the user prefers. In deliverables, pick one label per document and stay consistent.

## What to keep in sync

When the user asks to **create or update** modeling diagrams:

| Artifact | Draw.io | Markdown companion |
|----------|---------|-------------------|
| **Sequence / walkthrough** | `*.drawio` (start from `templates/domain realization template.drawio`) | Same structure as `templates/domain walkthrough template.md` |

**Rule:** If both files exist for a topic, **update both** in the same pass so walk steps do not drift. If only one exists, create the missing companion **from those templates** unless the user opts out.

## Sequence / walkthrough — Draw.io (what the template encodes)

`templates/domain realization template.drawio` illustrates:

- **Initiator** lifeline (optional actor driving the scenario)
- **Object lifelines** (`{{object}}:{{Class}}`)
  - **Alignment:** All participant lifelines must be perfectly aligned horizontally at the top of the canvas.
- **Synchronous messages** (filled arrow) and **returns** (open arrow, dashed)
  - **Crucial Connection Rule:** Message arrows must *always* snap exactly to the outer edge of the **execution bar (activation rectangle)**, NEVER to the center dashed lifeline itself.
  - **Message Angles:** All message arrows must be perfectly horizontal (0-degree angle).
- **Nested execution** (activation bars / self-segment notation)
  - **Positioning:** Execution bars must be placed *exactly centered* on the vertical dashed line of the lifeline.
  - **Nesting:** For internal behavior or nested calls, the nested execution bar must be stacked precisely on the right edge of the parent execution bar, offset slightly downwards to indicate time progression.
  - **Time Flow:** Vertical space strictly represents time. Elements must flow downwards cleanly without any vertical overlap of independent, sequential operations.
- Small **edge labels** for `new`, parameters, and call text

There is **no** `drawio_cli.py` automation for lifelines yet. **New diagrams:** duplicate the template into the workspace (see **Templates** above), replace placeholders, then adjust lifeline heights and messages as needed.

## Sequence / walkthrough — Markdown

**Narrative + pseudo-code** — Follow `templates/domain walkthrough template.md` (required structure; see **Templates** above):
- One **Scenario** block per flow.
- **Walk N: Covers** — scope (what responsibilities this walk exercises).
- Indented pseudo-code showing object creation, calls, returns, and nesting (same story as the Draw.io diagram).

## Creating Sequence Diagrams from Walkthroughs (Step-by-step)

### Step 1: Extract Lifelines from Pseudo-code

Read the walkthrough pseudo-code and identify all **distinct objects/participants**:

```
{object}: {Type} = new {Class}()
{result}: {Type} = {object}.{method}()
    {collaborator}: {CollaboratingClass} = {getter}
    {inner}: {InnerType} = {collaborator}.{method}()
```

**Participants:**
- `{object}:{Class}` ← lifeline 1
- `{collaborator}:{CollaboratingClass}` ← lifeline 2
- Any other objects mentioned ← additional lifelines

### Step 2: Translate Pseudo-code to Messages

For each call in the pseudo-code, create a **message arrow** in Draw.io:

| Pseudo-code | Draw.io Message |
|-------------|-----------------|
| `{object}.{method}()` | Synchronous message arrow (filled) from **{object}** to **{collaborator}** labeled `method()` with params |
| `return {value}` | Return arrow (dashed, open) from callee back to caller labeled with `{value}` (if non-void) |
| `{var} = new {Class}()` | Create message (labeled `«new»`) from initiator to the new object's lifeline |
| Nested calls | Stack activation bars (execution rectangles) vertically; nested calls go to the right edge of parent activation |

### Step 3: Align with Template

When creating the `.drawio` file:

1. **Duplicate** `templates/domain realization template.drawio`
2. **Replace placeholder lifelines** with actual participant names from Step 1
3. **Add messages** following the order in the pseudo-code (top to bottom = time flow)
4. **Verify alignment:**
   - All lifelines top-aligned (horizontal line at y=0)
   - All message arrows **horizontal** (0° angle)
   - Message arrows snap to **outer edge of execution bars**, not center lifeline
   - Execution bars centered on lifeline, nested bars stacked right

### Step 4: Keep Markdown ↔ Draw.io in Sync

- **If updating the `.drawio`:** Update the `.md` pseudo-code to match new messages/lifelines
- **If updating the `.md`:** Update the `.drawio` diagram to match new pseudo-code steps
- **Test alignment:** Trace each line of pseudo-code to a message in the diagram; each message should appear in the `.md`

### Example: Character Creation Scenario

**Markdown pseudo-code (Walk 1: Create ability):**
```
player: Player = initiator
character: Character = new Character(power_level: 5)
    abilities: Ability[] = []
strength_ability: Ability = new Ability(type: Strength, rank: 3)
character.add_ability(strength_ability)
    character.spend_power_points(cost: 3)
return character with Strength:3
```

**Lifelines in `.drawio`:**
1. `player:Player`
2. `character:Character`
3. `strength_ability:Ability`

**Messages in `.drawio`:**
1. `player` → `character` : `create(power_level: 5)`
2. `character` → `abilities` : `add(strength_ability)`
3. `character` → `character` : `spend_power_points(3)` (self-call)
4. Return: `character` → `player` : character object

## File naming (suggested)

| Pair | Example |
|------|---------|
| Model + Walkthrough | `step-1-model.md` (domain model) + `step-1-walkthrough.md` (scenarios & walks) + `step-1-walkthrough.drawio` (sequence diagram) |
| Pattern | `{step-name}-model.md`, `{step-name}-walkthrough.md`, `{step-name}-walkthrough.drawio` |

Use `{step-name}` consistently across all three artifacts so their relationship is obvious.

---

## Tips for Large Walkthroughs

If a single scenario has **many walks** (e.g., 5+ different message flows):

- **Option 1:** Create **one `.drawio`** per walk (e.g., `step-1-walkthrough-create.drawio`, `step-1-walkthrough-combat.drawio`)
- **Option 2:** Create **one merged `.md`** with all walks, but only extract **critical walks** to `.drawio` (mark non-diagrammed walks with `[Not diagrammed]`)

**Rule:** Keep the pairing obvious (shared stem) and the `.drawio` count manageable (1–3 per major flow).

---

<!-- source: content/parts/sequence-diagram-layout-rules.md -->

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

---
