# Using the Diagram CLI

## The Rule

**All class diagrams must be created and maintained using `scripts/drawio_cli.py`.**

Do not hand-write `.drawio` XML. Do not create ad-hoc rectangle layouts. The CLI produces proper UML swimlane class components with separate sections for name, fields, and methods — matching the `templates/domain model template.drawio` visual standard.

---

## Class Diagram — Workflow

### Standard workflow (single classes, no modules)

Every class diagram follows this sequence:

```
new → add-class (×N) → add-field (×N) → add-method (×N) → add-relationships → relayout → verify
```

```bash
# 1. Create the diagram file
python scripts/drawio_cli.py new --file <workspace>/abd-ooad/<output>.drawio

# 2. Add each class (use --x/--y to set explicit 2D positions — never rely on relayout alone)
python scripts/drawio_cli.py add-class <ClassName> --x <n> --y <n> --file <output>.drawio

# 3. Add fields to classes
python scripts/drawio_cli.py add-field <ClassName> "+ <name>: <Type>" --file <output>.drawio

# 4. Add methods to classes
python scripts/drawio_cli.py add-method <ClassName> "+ <name>(<param>: <Type>): <ReturnType>" --file <output>.drawio

# 5. Add relationships (choose the right type)
python scripts/drawio_cli.py add-composition <Whole> <Part> --mult <n> --label "<label>" --file <output>.drawio
python scripts/drawio_cli.py add-aggregation <Whole> <Part> --file <output>.drawio
python scripts/drawio_cli.py add-association <From> <To> --label "<label>" --from-mult "<m>" --to-mult "<n>" --file <output>.drawio
python scripts/drawio_cli.py add-inheritance <Subclass> <Superclass> --file <output>.drawio
python scripts/drawio_cli.py add-dependency <From> <To> --stereotype "<label>" --file <output>.drawio

# 6. Fix edge styles and verify
python scripts/drawio_cli.py fix-edge-styles --file <output>.drawio
python scripts/drawio_cli.py verify --file <output>.drawio
```

---

### Module/anchor workflow (domain-scan — anchors as modules)

When the diagram represents anchor modules (domain-scan phase), each anchor needs a **dashed frame** enclosing its core class and any supporting classes. The module name = the frame title = the core class name.

```
new → add-class (core classes + supporting classes) → add-field → add-frame (×N, one per module) → add-relationships → fix-edge-styles → verify
```

```bash
# 1. Create the diagram file
python scripts/drawio_cli.py new --file <workspace>/abd-ooad/<output>.drawio

# 2. Add ALL classes first (core + supporting), with explicit positions
#    Core classes positioned first; supporting classes near their core class
python scripts/drawio_cli.py add-class <CoreClass> --x <n> --y <n> --file <output>.drawio
python scripts/drawio_cli.py add-class <SupportingClass> --x <n> --y <n> --file <output>.drawio

# 3. Add fields to core classes
python scripts/drawio_cli.py add-field <CoreClass> "<<scan>>" --file <output>.drawio
python scripts/drawio_cli.py add-field <CoreClass> "+ <field>: <Type>" --file <output>.drawio

# 4. Add module frames (AFTER all classes are in the diagram)
#    Frame name = anchor/module name = core class name
python scripts/drawio_cli.py add-frame "<ModuleName>" --classes "<CoreClass>,<SupportingClass1>" --file <output>.drawio

# 5. Add relationships BETWEEN modules (core-class to core-class)
python scripts/drawio_cli.py add-composition <CoreA> <CoreB> --file <output>.drawio
python scripts/drawio_cli.py add-dependency <CoreA> <CoreB> --stereotype "<label>" --file <output>.drawio

# 6. Fix edge styles and verify
python scripts/drawio_cli.py fix-edge-styles --file <output>.drawio
python scripts/drawio_cli.py verify --file <output>.drawio
```

**Important rules for module frames:**
- `add-frame` must be called AFTER all classes are in the diagram
- Frame title must match the core class name exactly
- Do NOT call `relayout` after `add-frame` — relayout ignores frame membership and will scatter classes outside their frames
- Cross-module relationships always connect core classes, never the frames themselves
- A frame with no matching core class = an incomplete anchor identification (explore further)

**Describe / inspect:**
```bash
python scripts/drawio_cli.py describe --file <output>.drawio
python scripts/drawio_cli.py list-classes --file <output>.drawio
python scripts/drawio_cli.py show-class <ClassName> --file <output>.drawio
```

**Inline invariants** — add as a field entry with curly braces (brief, one-line constraints):
```bash
python scripts/drawio_cli.py add-field <ClassName> "{ invariant text }" --file <output>.drawio
```
Example: `add-field Check "{ result = d20 + modifier; succeeds if result >= dc }"`

**Note invariants** (longer — multiple lines): the CLI does not support notes. Add manually in draw.io after CLI build: Insert → Shape → Note, enclose text in `{ }`, connect to class with a dashed line. See `class-diagrams` in this library for full invariant guidance.

---

## Domain Realization (Sequence) Diagram — Workflow

Sequence/walkthrough diagrams use the checked-in template rather than the CLI:

```bash
# 1. Duplicate the template
cp "templates/domain realization template.drawio" <workspace>/abd-ooad/<output>.drawio

# 2. Edit the .drawio file to replace placeholder lifelines, messages, and notes
#    with the actual actors and interactions from the walkthrough

# 3. Create the companion markdown
cp "templates/domain walkthrough template.md" <workspace>/abd-ooad/<output>.md
#    Fill in the scenario description, step-by-step walkthrough, and notes
```

---

## Markdown Companion — Always Paired

Every `.drawio` class diagram has a `.md` companion. Use `templates/domain model template.md` as the starting structure:

```
<ClassName> : <BaseClass>
+ <property>: <Type>
     opt  <CollaboratingClass>, ...
      Invariant: <constraint>
+ <method>(<param>: <Type>): <ReturnType>
      <CollaboratingClass>, ...
      Invariant: <constraint>
-----
```

Keep both files in sync — when you add a class to the `.drawio`, add the same class to the `.md` in the same pass.

---

## Per-Phase Diagram Rules

| Phase | What to Show | Properties | Methods | Relationships |
|-------|-------------|------------|---------|---------------|
| domain-scan | Anchor modules: one dashed frame per anchor, core class inside frame + confirmed supporting classes | Scan-identified fields on core class only | None | High-confidence only, between core classes |
| nouns-verbs → raw-candidate-list | Candidates added | None | None | Structural only |
| responsibilities → turn-verbs-into-operations | All confirmed classes | Semantic properties | Confirmed methods | All known |
| relationships → model-state-transitions | Refined model | Full | Full | Full with cardinality |
| iterative-refinement → model-in-layers | Final layered model | Full | Full | Full |

**Domain-scan constraint:** The diagram fidelity must match the sketch exactly. One frame per anchor module. Core class inside each frame has the same name as the frame. If you cannot find a core class for a frame, the anchor is incomplete — explore further before drawing.

---

## Relationship Type Guide

| Relationship | Command | When to Use |
|-------------|---------|-------------|
| Composition | `add-composition` | WHOLE owns PART; PART cannot exist without WHOLE |
| Aggregation | `add-aggregation` | WHOLE references PART; PART exists independently |
| Association | `add-association` | General directed relationship between two classes |
| Inheritance | `add-inheritance` | IS-A — subclass extends superclass |
| Dependency | `add-dependency` | Uses or creates — ephemeral, not structural |

---

## Templates Reference

| Template | Path | Use for |
|----------|------|---------|
| Class diagram (Draw.io) | `templates/domain model template.drawio` | All class structure diagrams |
| Class diagram (Markdown) | `templates/domain model template.md` | All class diagram companions |
| Walkthrough (Draw.io) | `templates/domain realization template.drawio` | Sequence/realization diagrams |
| Walkthrough (Markdown) | `templates/domain walkthrough template.md` | Walkthrough narrative companions |

**Never** create a class diagram without using the CLI. **Never** create a walkthrough without using the realization template. These conventions encode the visual and structural standards for the domain model.

---

See also: `class-diagrams.md`, `class-diagram-layout-rules.md`, `sequence-diagrams.md`, `sequence-diagram-layout-rules.md` in this library for full rules on layout, edge styles, and verification codes.
