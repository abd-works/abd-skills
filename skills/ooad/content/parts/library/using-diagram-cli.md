# Using the Diagram CLI

## The Rule

**All class diagrams must be created and maintained using `scripts/drawio_cli.py`.**

**Sequence / walkthrough diagrams:** use the same CLI. Initialize from the template, then add lifelines and messages:

```bash
python scripts/drawio_cli.py sequence-init --file <output>.drawio
python scripts/drawio_cli.py sequence-add-lifeline "obj:Class" --file <output>.drawio
python scripts/drawio_cli.py sequence-add-sync <FROM> <TO> "message()" --file <output>.drawio
python scripts/drawio_cli.py sequence-add-return <FROM> <TO> "optionalLabel" --file <output>.drawio
python scripts/drawio_cli.py sequence-list --file <output>.drawio
```

Lifeline labels are matched by exact text or a unique partial match (after stripping HTML). Finer layout (activation bars, nested calls, strict horizontal message rows) may still be adjusted in Draw.io; see **sequence-diagrams** and **sequence-diagram-layout-rules**.

Do not hand-write `.drawio` XML for **class** diagrams. Do not create ad-hoc rectangle layouts. The CLI produces proper UML swimlane class components with separate sections for name, fields, and methods — matching the `templates/domain model template.drawio` visual standard.

---

## Diagram Build Routine

Every class diagram is built from the `.md` companion file. The `.md` is always created first and is the authoritative record. The diagram is then derived from it, component by component.

### Step 1 — Read the MD file line by line

Before writing a single CLI command, read the entire `.md` companion and extract:
- Every class name and its stereotype
- Every **scalar field** (primitive type, not a reference to another class)
- Every invariant `{ }` line
- Every multi-valued reference (these become arrows, NOT diagram fields)
- Every single-valued reference to another class (also an arrow)

**Diagram fields = scalars + invariants only.** Any field whose type is another class in the model must become a relationship arrow. Do not add it as a text field in the diagram — it is already represented by the arrow.

### Step 2 — Add each class one at a time

For each class:
1. `add-class <Name> --stereotype <phase>` — stereotype goes in the class header, not as a field row
2. Add only scalar fields: `add-field <Name> "+ fieldName: PrimitiveType"`
3. Add invariants: `add-field <Name> "{ constraint text }"` — these will be post-processed to taller cell heights
4. After each class, check the class rendered correctly before moving to the next

**Stereotype rule:** Always use `--stereotype scan` (or the current phase) on `add-class`. Never add `<<scan>>` as a separate field row — this causes it to render as `<>` because draw.io HTML interprets `<scan>` as an HTML tag.

**Type completeness rule:** Every type referenced in a field must have a class in the diagram. If `Character` has `powers: Power [0..*]`, then `Power` must be drawn as a class. There are no phantom types — if it appears in a field, it exists in the model.

### Step 3 — Post-process constraint cell heights

After all classes are added, run the height fixup:
```python
for cell in root.iter('mxCell'):
    val = cell.get('value', '')
    if val.startswith('{'):
        geom = cell.find('mxGeometry')
        if geom is not None:
            geom.set('height', '52' if len(val) <= 60 else '78')
```

### Step 4 — Add module frames

Run `add-frame` for each module, listing all member classes. Frames must be added AFTER all classes.

### Step 5 — Add relationships

For each relationship identified in Step 1:
- Composition: `add-composition Whole Part --mult "n..*"` — multiplicity goes at the **part** (many) end, near the part class
- Association: `add-association From To --label "name" --to-mult "0..*"`
- Dependency: `add-dependency From To --stereotype "label"`

Cross-module relationships connect core classes only (not frames). Before drawing any cross-module arrow, confirm there is a field on the source class that references the target — see `class-diagrams` → "Associations Require a Connecting Field".

### Step 6 — Verify and fix layout

```bash
# Fix edge styles first (V3/V4)
python scripts/drawio_cli.py fix-edge-styles --file <output>.drawio

# Fix shared connection points (V5) — always run after adding relationships
python scripts/drawio_cli.py fix-shared-endpoints --file <output>.drawio

# Fix arrow-class overlaps (V6) — routes edges around classes they cross
python scripts/drawio_cli.py fix-arrow-overlaps --file <output>.drawio

# Verify — check all rules V1–V6
python scripts/drawio_cli.py verify --file <output>.drawio
```

The `fix-shared-endpoints` command detects classes where 2+ edges arrive or
leave without explicit `entryX/Y` / `exitX/Y` constraints. It determines the
dominant approach side (top / bottom / left / right) and distributes port
coordinates evenly so arrowheads no longer pile up.

The `fix-arrow-overlaps` command detects edges whose straight-line path passes
through an unrelated class body (V6). It automatically inserts 1–2 waypoints to
route the edge around all obstacles, using a recursive shortest-path algorithm
with up to 2 bypass points. V4 info messages about explicit waypoints on
previously-fixed edges are expected and can be ignored.

After verify, address any remaining warnings:

| Code | Severity | Meaning | Action |
|------|----------|---------|--------|
| V1 | ERROR | Class bounding boxes overlap | `relayout` |
| V2 | ERROR | Subclass above superclass | `relayout` |
| V3 | WARN | Wrong edge style for relationship type | `fix-edge-styles` |
| V4 | WARN | Explicit waypoints on orthogonal edges | `fix-edge-styles` |
| V5 | WARN | 2+ edges share unconstrained connection point | `fix-shared-endpoints` |
| V6 | WARN | Straight edge passes through unrelated class | `fix-arrow-overlaps` |

Then run the frame containment check (Python XML script) to confirm all classes are inside their frames.

### Step 7 — AI layout pass

The programmatic build will produce correct structure but imperfect visual routing. After running verify (with 0 errors), open the diagram and inspect for:
- Labels obscured by other elements (drag to clear space)
- Any class that is outside its frame boundary (fix with `add-frame` or XML edit)
- Any remaining V6 warnings after `fix-arrow-overlaps` — move the blocking class manually as a last resort

`fix-arrow-overlaps` automatically routes edges around any class they pass through, inserting 1–2 waypoints using a recursive shortest-path algorithm. Re-run it if V6 warnings remain after the initial fix.

---

### Standard workflow (single classes, no modules)

Every class diagram follows this sequence:

```
new → add-class (×N) → add-field (×N) → add-method (×N) → add-relationships → fix-edge-styles → fix-shared-endpoints → fix-arrow-overlaps → verify
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

# 6. Fix edge styles, spread shared endpoints, fix overlaps, then verify
python scripts/drawio_cli.py fix-edge-styles --file <output>.drawio
python scripts/drawio_cli.py fix-shared-endpoints --file <output>.drawio
python scripts/drawio_cli.py fix-arrow-overlaps --file <output>.drawio
python scripts/drawio_cli.py verify --file <output>.drawio
```

---

### Module/anchor workflow (domain-scan — anchors as modules)

When the diagram represents anchor modules (domain-scan phase), each anchor needs a **dashed frame** enclosing its core class and any supporting classes. The module name = the frame title = the core class name.

```
new → add-class (core classes + supporting classes) → add-field → add-frame (×N, one per module) → add-relationships → fix-edge-styles → fix-shared-endpoints → fix-arrow-overlaps → verify
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

# 6. Fix edge styles, spread shared endpoints, fix overlaps, then verify
python scripts/drawio_cli.py fix-edge-styles --file <output>.drawio
python scripts/drawio_cli.py fix-shared-endpoints --file <output>.drawio
python scripts/drawio_cli.py fix-arrow-overlaps --file <output>.drawio
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

## Diagram fidelity as the model evolves

You maintain **one** class diagram (and its Markdown companion) for the domain — not a separate `.drawio` per pipeline phase. The table below is **how complete that single diagram should be** when you finish a **stage** (or when you sync after a phase pass), not a license to duplicate the model per step.

| Stage / exit | What to show | Properties | Methods | Relationships |
|----------------|-------------|------------|---------|---------------|
| After **`domain-scan`** | Anchor modules: one dashed frame per anchor, core class inside frame + confirmed supporting classes | Scan-identified fields on core class only | None | High-confidence only, between core classes |
| After **Scaffold** (`nouns-verbs-rules-and-states` → `thing-vs-data-about-a-thing`) | Named class stubs / candidates in structure | As discovered | None or stubs | Structural only |
| After **Model** (`responsibilities-and-collaborators` → `inherit-interface-or-compose`) | All confirmed classes | Semantic properties | Confirmed methods | All known, cardinality as decided |
| After **Behaviour** (`invariants` → `scenario-validation`) | Full model for validation | Full | Full | Full with cardinality; invariants as agreed |

**Domain-scan constraint:** The first diagram pass should match the scan sketch: one frame per anchor module; core class inside each frame matches the frame name. If you cannot find a core class for a frame, the anchor is incomplete — explore further before drawing.

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
