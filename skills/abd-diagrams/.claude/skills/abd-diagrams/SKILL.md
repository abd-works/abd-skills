---
name: abd-diagrams
description: >
  Use this skill whenever the user wants to create, edit, or discuss a UML class
  diagram, a domain walkthrough / domain realization / domain interaction
  (same idea), a UML sequence diagram, an object-oriented analysis and design
  (OOAD) model, or a Draw.io (.drawio) diagram. Triggers include: "class diagram",
  "sequence diagram", "domain walkthrough", "realization", "interaction diagram",
  "UML", "draw a model", "add a class", "add an association", "composition",
  "inheritance", "aggregation", "OOD", "object model", "design this system",
  or any request to model relationships between classes. Use even when the user
  just says something like "relate X to Y through composition" or
  "I need a diagram for this system".
---

# OOAD Class Diagram Skill

This skill lets you create and edit UML class diagrams in Draw.io format by
calling `drawio_cli.py`. The CLI handles all XML — you just issue the right
commands in sequence.

The CLI lives at:
```
{SKILL_DIR}/../../../scripts/drawio_cli.py
```
where `{SKILL_DIR}` is the directory containing this SKILL.md. In practice,
resolve it like this from bash:
```bash
CLI="$(dirname "$(realpath "$0")")/../../../scripts/drawio_cli.py"
# or simply use the absolute path you know from context
```

If the user's workspace folder is mounted, save the `.drawio` file there so
they can open it directly in Draw.io.

**Skill package layout:** The **`abd-diagrams`** skill root contains `scripts/drawio_cli.py`,
`templates/`, `context/`, and **`content/parts/`** (four diagram library `.md` files).
This `SKILL.md` is only the Claude entry point; paths below that use `../../../` from
`.claude/skills/abd-diagrams/` to reach the skill root.

---

## Jeff's Notation Rules (derived from the class-diagrams video)

These are the conventions you MUST follow when producing diagrams:

### Class structure
- Bold class name at top (the CLI handles this automatically via `swimlane;fontStyle=1`)
- Fields listed above the horizontal divider
- Methods listed below the divider
- Format for fields:  `+ fieldName: Type`
- Format for methods: `+ methodName(param: Type): ReturnType`
- Visibility: `+` public, `-` private, `#` protected
- Abstract members use `--abstract` flag (renders italic in Draw.io)

### Rich annotations in field/method text
Jeff's style includes inline dependency hints directly in the field/method text
to show what *uses* or *affects* that member. These go on a second line,
indented with spaces, e.g.:

```
"+ velocity: Number\n   Road; Pedal, CarEngine, SteeringWheel"
"+ turn(degrees:Number): degreesTurned\n   SteeringWheel, Wheels, Velocity, Position"
```

When you know the collaborators, include them. When you don't, leave them out — don't fabricate.

### Relationship types and when to use each

| Relationship   | Meaning                                     | CLI command          | Arrow            |
|---------------|---------------------------------------------|----------------------|-----------------|
| Association    | A uses/knows B (loosely)                    | `add-association`    | A → B           |
| Composition    | A *contains* B; B can't exist without A     | `add-composition`    | A ◆── B         |
| Aggregation    | A *has* B; B can exist independently        | `add-aggregation`    | A ◇── B         |
| Inheritance    | A *is a* B (subclass → superclass)          | `add-inheritance`    | A --▷ B         |
| Dependency     | A *depends on* B (transient/creates)        | `add-dependency`     | A - -> B        |

**Composition vs Aggregation:** The key distinction is lifecycle. A Car *owns*
its Engine (composition — engine dies with car). A Fleet *has* Planes
(aggregation — planes can exist in other fleets).

### Multiplicities
Always add multiplicities when the cardinality is non-trivial:
- `1` — exactly one
- `0..1` — zero or one (optional)
- `0..*` or `*` — zero or many
- `1..*` — one or many
- `4` — exactly four (e.g. Car has 4 Wheels)
- `0..3` — zero to three

### Packages / UML Frames
Group related classes in a named UML frame using `add-frame`. The frame draws
a box with a tab label — use it for namespaces, modules, or logical groupings.

### Object instances
When showing a concrete example, use `add-object` to create an instance box
(underlined bold `Name:Type` header with field=value list) and
`add-instance-of` to draw the `«instance of»` dashed arrow to the class.

---

## Standard Workflow

### Step 1 — Create or load the file
```bash
python drawio_cli.py new --file MyDiagram.drawio
# or work with an existing file (just use --file existing.drawio on every command)
```

### Step 2 — Add classes
```bash
python drawio_cli.py add-class ClassName --file MyDiagram.drawio
```

### Step 3 — Add fields (above divider) and methods (below divider)
```bash
python drawio_cli.py add-field ClassName "+ fieldName: Type" --file MyDiagram.drawio
python drawio_cli.py add-method ClassName "+ methodName(p: Type): ReturnType" --file MyDiagram.drawio
# Use --abstract for italic (abstract) members
python drawio_cli.py add-method ClassName "+ abstractOp(): void" --abstract --file MyDiagram.drawio
```

### Step 4 — Add relationships
```bash
# Association with label + multiplicities
python drawio_cli.py add-association Person Car \
  --label "drives a" --from-mult "1" --to-mult "0..3" \
  --file MyDiagram.drawio

# Composition: Car contains 4 Wheels
python drawio_cli.py add-composition Car Wheel --mult 4 --file MyDiagram.drawio

# Aggregation: Fleet has many Planes
python drawio_cli.py add-aggregation Fleet Plane --mult "1..*" --file MyDiagram.drawio

# Inheritance: Car is a Vehicle
python drawio_cli.py add-inheritance Car Vehicle --file MyDiagram.drawio

# Dependency with stereotype
python drawio_cli.py add-dependency Car CarFactory --stereotype "created by" --file MyDiagram.drawio
```

### Step 5 — Group with frames (optional)
```bash
python drawio_cli.py add-frame "Vehicles" \
  --classes "Vehicle,Car,Plane,Train,Wheel" --file MyDiagram.drawio
```

### Step 6 — Add object instances (optional)
```bash
python drawio_cli.py add-object "Dash8:Plane" \
  --fields "pilot=BobThePilot,dash8Engine=PlaneEngine" --file MyDiagram.drawio
python drawio_cli.py add-instance-of "Dash8:Plane" Plane --file MyDiagram.drawio
```

### Step 7 — Relayout (REQUIRED — run after ALL fields/methods added)
```bash
python drawio_cli.py relayout --file MyDiagram.drawio
```
`add-class` uses a rough placeholder position because class heights aren't known
yet. After all content is added, `relayout` reads actual heights and uses a
**hierarchical algorithm**: inheritance depth 0 (abstract roots) goes in row 0,
depth 1 in row 1, etc. Siblings are grouped under their parent. This guarantees:
- **Vertical Hierarchy:** Superclasses and abstract classes are strictly positioned vertically above their subclasses. The diagram flows from general (top) to specific (bottom).
- **Horizontal Peers:** Peer associations and composition relationships are arranged horizontally to balance the footprint.
- **No row overlaps** (row height = tallest class in that row).
- **Spacing:** Maintains generous, consistent spacing to prevent visual clutter and leave room for labels.

Options: `--hgap PX` (default 80), `--vgap PX` (default 60).

### Step 8 — Verify + Fix (REQUIRED — treat errors as blocking)

```bash
python drawio_cli.py verify --file MyDiagram.drawio --verbose
python drawio_cli.py fix-edge-styles --file MyDiagram.drawio
```

`verify` runs checks for proper layout and routing. **If any ERROR is reported, fix it before presenting**:

| Code | What it checks                                    | Fix                  |
|------|---------------------------------------------------|----------------------|
| V1   | Class bounding boxes don't intersect              | `relayout`           |
| V2   | Subclass `y` > parent `y` (child below parent)    | `relayout`           |
| V3   | Inheritance = straight diagonal; structural = orthogonal corners | `fix-edge-styles` |
| V4   | No explicit waypoints (they cause extra bends)    | `fix-edge-styles`    |

**Crucial Layout & Connection Rules for Class Diagrams:**
- **Anchor Points:** Relationship lines must snap to the fixed connection anchor points on the perimeter of the class boxes. Lines should never float unattached, terminate inside the box, or intersect with text.
- **Line Routing:** Use orthogonal (right-angled) routing for associations/compositions. Inheritance arrows must be straight diagonals pointing *upwards*.
- **Avoid Crossing Lines:** If you are editing spatial layout manually, actively rearrange boxes to minimize intersecting relationship lines.
- **Label Positioning:** Keep relationship labels (like `1..*`) positioned clearly at the immediate ends of the connector lines so there is no ambiguity.
- **Z-Ordering:** Ensure text labels are brought to the front so they aren't obscured by lines.

For the exact XML that each check is looking for, read:
`../../../content/parts/class-diagram-layout-rules.md` — it has ✓/❌ XML examples for every rule.

**Standard finish sequence:**
```bash
python drawio_cli.py relayout          --file MyDiagram.drawio
python drawio_cli.py fix-edge-styles   --file MyDiagram.drawio
python drawio_cli.py verify --verbose  --file MyDiagram.drawio
# If verify exits 1 (errors), re-run relayout and fix-edge-styles, then verify again
python drawio_cli.py describe          --file MyDiagram.drawio
```

### Step 9 — Semantic check

Read the `describe` output and confirm:
- Every class the user mentioned is present
- Fields and methods match the domain (visibility prefix, type suffix)
- Relationships use the correct type (don't use association when composition is right)
- Multiplicities make sense for the domain
- Packages/frames wrap the right groups

---

## Domain walkthroughs (realization / interaction) and dual artifacts

**Same concept, three names:** *domain walkthrough*, *domain realization*, *domain interaction* — pick one label per deliverable.

### Dual file rule (class and sequence)

When the user maintains **both** Draw.io and Markdown for the same topic, the Markdown serves as the textual source of truth:

| Kind | Templates |
|------|-----------|
| Class structure + rich member comments | `../../../templates/domain model template.drawio` + `../../../templates/domain model template.md` |
| Sequence / walkthrough | `../../../templates/domain realization template.drawio` + `../../../templates/domain walkthrough template.md` |

**On any update request, refresh both sides** so collaborator lines, invariants, and walk steps stay aligned. Full rules: `../../../content/parts/class-diagrams.md` and `../../../content/parts/sequence-diagrams.md`.

### Creating a Markdown Class Diagram

When the user asks for a Markdown class model, structure it using the format in `../../../templates/domain model template.md`:
- Document each class and its base class (`Class : BaseClass`).
- List properties and methods with types.
- Directly beneath the property or method, add `opt CollaboratingClass, AnotherClass` to explicitly show what it uses, affects, or collaborates with.
- Add `Invariant: {constraint}` to define business rules directly on the property or method.

### Creating Sequence Diagrams (Walkthroughs) in Draw.io

`drawio_cli.py` does **not** yet emit lifelines or messages. For sequence work:

1. **Duplicate** `../../../templates/domain realization template.drawio` to the workspace and edit it.
2. Replace the placeholders (`{{Class}}`, `{{object}}`, etc.) with the real object/class names.
3. Set up the **Initiator Lifeline** (the actor driving the scenario) and **Object Lifelines**. 
   - **Alignment:** All participant lifelines must be perfectly aligned horizontally at the top of the canvas.
4. Adjust **Execution Bars** (nested activations / self-segments) to show when an object is actively processing.
   - **Positioning:** Execution bars must be placed *exactly centered* on the vertical dashed line of the lifeline.
   - **Nesting:** For internal behavior or nested calls, the nested execution bar must be stacked precisely on the right edge of the parent execution bar, offset slightly downwards to indicate time progression.
   - **Time Flow:** Vertical space strictly represents time. Elements must flow downwards cleanly without any vertical overlap of independent, sequential operations.
5. Use synchronous calls (filled arrows) and returns (dashed open arrows).
   - **Crucial Connection Rule:** Message arrows must *always* snap exactly to the outer edge of the **execution bar (activation rectangle)**, NEVER to the center dashed lifeline itself.
   - **Synchronous Calls:** Solid line, filled arrowhead. Originate from the edge of the sending execution bar and terminate exactly at the top-left edge of the newly activated receiving execution bar.
   - **Return Messages:** Dashed line, open arrowhead. Originate from the bottom edge of the returning execution bar and snap back to the original caller's execution bar.
   - **Horizontal Accuracy:** All message arrows must be perfectly horizontal (0-degree angle). Diagonal message lines are strictly prohibited.

### Creating Markdown Sequence Diagrams (Walkthroughs)

When creating or updating the Markdown companion (`../../../templates/domain walkthrough template.md`):

1. **Scenario Scope:** Define exactly what rules or responsibilities the "Walk" exercises.
2. **Indented Pseudo-code:** Write structured text that *perfectly aligns* with the Draw.io activation bars. The indentation depth must tell the "same story" as the nested execution bars in the visual diagram (mapping object creation, nested calls, and returns).
3. **Mermaid Sequence Diagram:** Provide a text-based `sequenceDiagram` for a quick preview inside GitHub or a Markdown reader. Ensure that participant names strictly match the lifeline headers in the `.drawio` file.

---

## CLI Quick Reference

```
drawio_cli.py new                                     --file FILE
drawio_cli.py add-class NAME [--x X] [--y Y] [--width W]  --file FILE
drawio_cli.py add-field  CLASS "TEXT" [--abstract]    --file FILE
drawio_cli.py add-method CLASS "TEXT" [--abstract]    --file FILE

drawio_cli.py add-association FROM TO [--label L] [--from-mult M] [--to-mult M]  --file FILE
drawio_cli.py add-composition WHOLE PART [--mult M] [--label L]  --file FILE
drawio_cli.py add-aggregation WHOLE PART [--mult M] [--label L]  --file FILE
drawio_cli.py add-inheritance SUBCLASS SUPERCLASS     --file FILE
drawio_cli.py add-dependency  FROM TO [--stereotype S] --file FILE

drawio_cli.py add-frame NAME [--classes "A,B,C"]      --file FILE
drawio_cli.py add-object "Name:Type" [--fields "k=v,k=v"] [--x X] [--y Y]  --file FILE
drawio_cli.py add-instance-of OBJECT CLASS            --file FILE

drawio_cli.py list-classes          --file FILE
drawio_cli.py show-class CLASS      --file FILE
drawio_cli.py describe              --file FILE

# Post-build quality pass (ALWAYS run these three in order)
drawio_cli.py relayout              --file FILE   # hierarchical, parents above children
drawio_cli.py fix-edge-styles       --file FILE   # orthogonal routing, remove waypoints
drawio_cli.py verify [--verbose]    --file FILE   # V1 overlaps V2 direction V3 styles V4 bends
drawio_cli.py describe       --file FILE
```

---

## Full Worked Example (Vehicles domain from Jeff's video)

```bash
F="vehicles.drawio"
CLI="drawio_cli.py"

python $CLI new --file $F

# Classes
python $CLI add-class Vehicle  --file $F
python $CLI add-class Car      --file $F
python $CLI add-class Plane    --file $F
python $CLI add-class Train    --file $F
python $CLI add-class Wheel    --file $F
python $CLI add-class Person   --file $F
python $CLI add-class Fleet    --file $F

# Vehicle (abstract base)
python $CLI add-field  Vehicle "+ passengers: Person"       --file $F
python $CLI add-field  Vehicle "+ driver: Person"           --file $F
python $CLI add-field  Vehicle "+ velocity: Number"         --abstract --file $F
python $CLI add-method Vehicle "+ turn(degrees:Number): degreesTurned" --abstract --file $F

# Car
python $CLI add-field  Car "+ driver: Person"  --file $F
python $CLI add-field  Car "+ wheels: Wheels"  --file $F
python $CLI add-field  Car "+ velocity: Number\n   Road; Pedal, CarEngine, SteeringWheel" --file $F
python $CLI add-method Car "+ turn(degrees:Number): degreesTurned\n   SteeringWheel, Wheels, Velocity" --file $F

# Wheel / Person / Fleet — minimal
python $CLI add-field  Wheel  "+ field: type"  --file $F
python $CLI add-field  Person "+ field: type"  --file $F
python $CLI add-method Fleet  "addPlane()"     --file $F

# Inheritance
python $CLI add-inheritance Car   Vehicle --file $F
python $CLI add-inheritance Plane Vehicle --file $F
python $CLI add-inheritance Train Vehicle --file $F

# Composition: Car *owns* 4 Wheels
python $CLI add-composition Car Wheel --mult 4 --label "has" --file $F

# Aggregation: Fleet *has* Planes
python $CLI add-aggregation Fleet Plane --mult "1..*" --file $F

# Association: Person drives Car
python $CLI add-association Person Car \
  --label "drives a" --from-mult "1" --to-mult "0..3" --file $F

# Package frame
python $CLI add-frame "Vehicles" \
  --classes "Vehicle,Car,Plane,Train,Wheel,Person,Fleet" --file $F

# Object instance example
python $CLI add-object "Dash8:Plane" \
  --fields "pilot=BobThePilot,dash8Engine=PlaneEngine" --file $F
python $CLI add-instance-of "Dash8:Plane" Plane --file $F

python $CLI describe --file $F
```
