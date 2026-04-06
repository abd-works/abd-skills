## Role

You are the **domain modeler and OOAD practitioner** using this skill: you provide source material (specifications, code, transcripts, policy), set the active workspace, step through the 24-phase methodology (starting with workspace-and-config → domain-scan → extraction → refinement), use `scripts/drawio_cli.py` for all class diagram generation and layout, and iterate to produce a validated domain model aligned with the source material and architectural goals.


---

## Principles

# Principles

1. **Orientation before extraction** — domain-scan is observation and mapping, not yet data collection. Identify 3–7 high-confidence anchors and suspected tensions before extracting candidates.

2. **Things before data** — Model the domain's real entities, responsibilities, and relationships first. Do not invent data fields just because templates have room.

3. **Nouns → verbs → structure** — Extract domain concepts (nouns) as candidates, turn relevant verbs into operations, then build relationships and invariants that encode domain rules.

4. **Model incrementally, validate constantly** — Build the model phase by phase, consulting key scenarios and use cases at domain-scan, raw-candidate-list, add-properties-semantically-tight, smashed-abstractions-and-hidden-roles, and model-in-layers. Tensions and contradictions are signals for refinement.

5. **Diagram and Markdown stay synchronized** — Maintain both class diagram (.drawio) and Markdown documentation side-by-side. Changes to one must be reflected in the other.

6. **Domain facts trump templates** — If the source material contradicts a standard pattern or template, favor the domain truth. Document the deviation and the reason.

7. **Inheritance is a last resort** — Prefer composition and aggregation. Use inheritance only when behavior generalizes cleanly across a family of related classes.

8. **Names matter** — Refine names throughout the process. A clear, honest name reveals the model's intent; ambiguous or misleading names hide problems.

9. **Diagram CLI is non-negotiable** — Class diagrams must be created and validated using `scripts/drawio_cli.py` and the templates in `templates/`. Do not hand-write Draw.io XML or invent diagram conventions.

10. **Workspace awareness** — Always know which project workspace you are writing to. All outputs go under `<workspace>/abd-ooad/`, never to ad-hoc locations.


---

## Phase

# Inheritance when behavior generalizes — payments example

**Skill:** abd-ooad — **Step 11:** subtype only when **substitutable** behavior differs.

**Upstream:** `turn-verbs-into-operations.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Candidate hierarchy

**PaymentMethod** (abstract or interface) — **authorize**, **capture**, **supportsPartialCapture** — **if** each rail implements differently **and** callers use polymorphism.

| Subtype | Justified when |
|---------|------------------|
| **CardMethod** | 3DS, network tokens — extra **redirect** flow. |
| **BankTransferMethod** | Different settlement timing; no “capture” in card sense. |
| **WalletMethod** | Balance vs card rails. |

**Avoid** subclass explosion for **every** PSP brand if behavior is **adapter**-level (Stripe vs Adyen) — that’s **composition** (connector), not inheritance from **PaymentMethod**.

---

## Rule of thumb (payments)

- **Inherit** from **PaymentMethod** when **domain** distinguishes **how** the customer pays (card vs bank vs wallet).
- **Compose** **PspConnector** when **infrastructure** differs (same card semantics, different API).

---

## Carry forward → Step 12

Formalize **abstract class vs interface** for **PaymentMethod** and **ports** for PSP.

---

## Continual refinement (this step)

- **Delta:** **PaymentMethod** family (**CardMethod**, **BankTransferMethod**, **WalletMethod**) as substitutable subtypes — add subtype concept headings per [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (`### **Subtype** : **PaymentMethod**`) with **`**newly added**`** on subtype **operation** lines when first introduced.
---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.


---

## Library



---

### `anchors.md`

# Anchors

An **anchor** is a module. It is the most stable, central thing you have found in the domain — the concepts you are confident will survive the entire modeling process without being renamed or restructured away.

---

## What an anchor is

An anchor is three things at once:

1. **A module frame** — a named, dashed container in the diagram that groups related classes
2. **A core class** with the same name as the frame — the primary class in that module
3. **A scope boundary** — everything inside the frame belongs to this module; everything outside relates to it via its core class

The module name, frame title, and core class name must all match. If they don't, the anchor is not yet correctly identified.

---

## The anchor test

Before calling something an anchor, it must pass all three of these:

**1. Can you name a core class that matches the module?**
The core class must be identifiable by name in the source. You should be able to point to a section, definition, or keyword in the material that defines this concept by that name. A generic name like "Foundation," "Basics," or "Mechanics" with no corresponding defined concept is a signal you are grouping by proximity rather than identity — not a real anchor.

**2. Do other anchors reference it independently?**
If another module needs to point to this concept, does it reference this class by name — or does it go through some other class to get to it? If the only path to it goes through another anchor, it is likely a supporting class inside that anchor's module, not its own anchor.

> Example: HeroPoint has its own lifecycle and lifecycle rules, but nothing in the resolution system references HeroPoint directly — it is always accessed through the Character who holds it. HeroPoint belongs inside the Character module.
>
> Contrast: Check IS referenced directly — the entire game resolves outcomes through Check. No other anchor is needed to mediate access to it.

**3. Does it have structural stability?**
An anchor is a concept you expect to be present in the model from scan through final refinement. If you think it might disappear, merge with something else, or be renamed significantly, it is a candidate — not an anchor.

---

## What an anchor is NOT

- **A chapter in the source** — a chapter is an organization of the source, not a domain concept. Multiple real anchors can come from one chapter; one chapter alone does not make an anchor.
- **A concept with a dedicated section** — many things have dedicated sections. The anchor test is structural (other anchors reference it independently), not documentary.
- **A grouping of related concepts** — if you find 3–4 concepts that are related but none of them clearly dominates, keep exploring. The anchor will be the one that the others depend on. If none dominates, record the cluster as a tension.

---

## Anchor as module — what it looks like in outputs

| Output | What anchor produces |
|--------|---------------------|
| `domain-scan-results.md` | Row in the anchors table: Module name, core class name, scan-visible supporting classes, basis |
| `domain-scan-model.md` | Module section header + core class entry + supporting class entries with `[supporting class — ModuleName module]` annotation |
| `domain-scan-model.drawio` | One dashed frame per anchor; core class inside; supporting classes inside; cross-module relationships between core classes only |
| `term-registry.md` | Core class → `anchor` classification; supporting classes → `candidate` classification with Module? column naming their module |

---

## Anchors in later phases

Anchor status is not permanent. Anchors are your highest-confidence starting point, but subsequent phases will test and revise them:

- **nouns-verbs-rules-and-states (NOUNS):** All bolded and defined terms in the source are extracted. Anchors are not re-evaluated here, but new candidates emerge that may challenge or subdivide existing anchor boundaries.
- **candidate-list (CANDS):** Candidates are sorted and scored. At this stage, watch for candidates that score high enough on the anchor test to be promoted — or anchors whose core class fails the independence test and should be demoted.
- **thing-vs-data-about-a-thing (THINGS):** Supporting classes inside anchor frames are evaluated here — each gets a class/property decision. If a supporting class earns class status, it may eventually warrant its own module frame in later phases.
- **All subsequent phases:** Anchors drive the backbone of the model. Relationship decisions, responsibility assignments, and inheritance structures are all organized relative to anchor modules. Changes to anchor boundaries affect the whole model — flag them explicitly in the term registry before proceeding.

---

## Incomplete anchor signal

The absence of a matching core class is the clearest signal that you have not yet found the anchor. When you encounter this situation:

1. Do not force a name — generic names produce models that are hard to reason about
2. Read the relevant chapter(s) more carefully — the anchor often has its own defined term or dedicated section
3. Ask: if another module needed to reference this cluster, what single class would it name?
4. If no single class emerges after exploration, record the cluster as a **tension** in domain-scan-results.md and defer


---

### `term-registry.md`

# Term Registry

## What a Term Is

A **Term** is any concept identified from the source material that may become part of the domain model. At the time of identification, a Term is not committed to a model role — it might become a class, a property, a value type, an association, or nothing at all. The registry tracks Terms as the modeling phases determine what each one actually is.

This is distinct from other uses of "actor" in this domain:
- In MM3E and FoundryVTT, "Actor" has a specific system meaning (a character, creature, or entity in the game world).
- In the registry, everything is a Term until the model says otherwise.

**File:** `<workspace>/abd-ooad/term-registry.md`
**Never embedded** inside step outputs — it lives in its own file and is referenced from each step's model doc.

---

## Step Reference — Short Names

Use these short names in the **Step** column of the registry when adding or updating a row.

| Short Name | Phase | Description |
|-----------|-------|-------------|
| SETUP | workspace-and-config | Workspace initialization |
| SCAN | domain-scan | Source scan and anchor identification |
| NOUNS | nouns-verbs-rules-and-states | Extract nouns, verbs, rules, states |
| CANDS | raw-candidate-list | Raw candidate class list |
| THINGS | thing-vs-data-about-a-thing | Separate things from data-about-things |
| RESP | responsibilities-before-operations | Assign responsibilities |
| PROPS | add-properties-semantically-tight | Add semantically tight properties |
| OPS | turn-verbs-into-operations | Turn verbs into operations |
| RELS | relationships-and-cardinality | Relationships and cardinality |
| INV | invariants-in-the-model | Identify invariants |
| BLOAT | watch-for-bloated-classes | Detect bloated classes |
| ROLES | smashed-abstractions-and-hidden-roles | Uncover hidden roles |
| INHERIT | inheritance-when-behavior-generalizes | Apply inheritance |
| ABST | abstract-classes-and-interfaces | Abstract classes and interfaces |
| COMP | prefer-composition | Prefer composition over inheritance |
| STATES | model-state-transitions | Model state transitions |
| ITER | iterative-refinement | Iterative refinement pass |
| TENSION | tension-as-a-signal | Resolve tensions |
| COHESION | what-changes-together | What changes together |
| VALIDATE | validate-with-scenarios | Validate with scenarios |
| NAMES | refine-names | Refine class and concept names |
| LAYERS | model-in-layers | Model in layers |

---

## Registry Columns

| Column | Values | Notes |
|--------|--------|-------|
| **Term** | Concept name from the source | Exact word or phrase as found — rename in the NAMES step if needed |
| **Classification** | anchor / candidate / tension / module | Lifecycle stage. Maps to UML stereotype in diagram once promoted to class |
| **Step** | Short name from table above (SCAN, NOUNS, …) | Step that first identified this Term |
| **Confidence** | High / Medium / Low | How sure we are this belongs in the model |
| **Status** | Active / Ambiguous / Deferred / Rejected / Promoted | Current state |
| **Notes** | Free text | Why it was flagged, what needs investigating, decisions made |
| **Module?** | Yes / No / Investigate | Will this eventually become a standalone module |

**Classification values** (once a Term is confirmed as a class, this maps to its UML `<<stereotype>>` in the diagram):

- `anchor` — High-confidence, core, stable. Identified at SCAN. Will definitely be in the model.
- `candidate` — Plausible, needs validation. Added during extraction steps.
- `tension` — Boundary ambiguous or conflicting. Needs resolution before model role can be assigned.
- `module` — Ready to be promoted to a standalone module.

---

## Registry Format

```markdown
# Term Registry — {{project_name}}

_Last updated: {{step_short_name}} — {{date}}_

| Term       | Classification | Step  | Confidence | Status    | Notes | Module? |
|------------|---------------|-------|------------|-----------|-------|---------|
| Character  | anchor        | SCAN  | High       | Active    | Central entity; all rules attach to it | Yes |
| Power      | anchor        | SCAN  | High       | Active    | Core superheroic capability unit | Yes |
| Condition  | anchor        | SCAN  | High       | Active    | Named state applied after check resolution | Yes |
| Device     | tension       | SCAN  | Medium     | Ambiguous | Removable Power or Equipment? Boundary unclear | Investigate |
| ability    | candidate     | NOUNS | High       | Active    | One of six core scores; probably a property of Character, not a class | No |
```


---

### `using-diagram-cli.md`

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


---

### `class-diagrams.md`

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

## Relationship Type Guide

Use this decision tree to pick the correct relationship. When in doubt, choose the weaker type and upgrade it in a later phase when the ownership model is confirmed.

**Decision tree:**

1. Does A hold a permanent reference to B?
   - **No** → `add-dependency` (transient — B is a parameter or local variable only)
   - **Yes** → go to 2

2. Is A the owner of B (part-whole)?
   - **No** → `add-association` (peer relationship — A knows B, no ownership)
   - **Yes** → go to 3

3. Can B exist without A?
   - **No** → `add-composition` (strong ownership — B dies when A dies)
   - **Yes** → `add-aggregation` (loose ownership — B can be shared or outlive A)

**Quick reference:**

| Type | CLI command | Symbol | Strength | Key test |
|------|-------------|--------|----------|----------|
| Composition | `add-composition` | ◆── | Strongest | Delete A → B is destroyed |
| Aggregation | `add-aggregation` | ◇── | Strong | Delete A → B survives |
| Association | `add-association` | →  | Moderate | A holds a reference to B; neither owns the other |
| Dependency | `add-dependency` | --> | Weakest | A uses B only inside a method — no stored reference |
| Inheritance | `add-inheritance` | --▷ | n/a | IS-A — subclass extends superclass |

**Scan-phase defaults:** At domain-scan fidelity, prefer conservative choices:
- Use `add-dependency` for any relationship that is clearly transient (produced by, resolved via, creates)
- Use `add-composition` only when the source material explicitly states ownership or lifecycle coupling
- Use `add-association` for all other confirmed structural relationships
- Leave aggregation for refinement phases when shared ownership is confirmed

**Prompt to check yourself:**
> "I am modeling [Class A] → [Class B]. Does A store B permanently? Is A the owner? If A is destroyed, does B die too? Is B a physical/logical part of A?"

---

## Invariants in Class Diagrams

Invariants document constraints that must hold for a class to be valid — business rules, system constraints, range limits, and lifecycle rules. They are shown in the diagram at two levels of detail:

### Inline invariant (brief — fits on one line)
Add directly inside the class box as a field entry, using curly braces:

```
{ result = d20 + modifier; succeeds if result >= dc }
{ rank 0 = average; rank 20 = cosmic }
```

Use `add-field ClassName "{ invariant text }"` in the CLI. Place inline invariants immediately after the field or section they constrain.

### Note invariant (longer — multiple lines or complex expression)
Use a note (folded-corner rectangle) connected to the class by a dashed line:

```
{ pool resets to 1 each session
  earn: from Complications or heroic acts
  spend: reroll Check, extra action, boost rank +1, recover Condition }
```

The CLI does not yet support notes — add them manually in draw.io after CLI build. Use: Insert → Shape → Note. Connect to the target class with a dashed edge. Enclose invariant text in `{ }`.

### When to add invariants

| Phase | Add invariants? |
|-------|----------------|
| domain-scan | Yes — add the invariants you found during the scan (inline preferred at this fidelity) |
| nouns-verbs | No — extraction only; invariants captured in registry notes |
| raw-candidate-list through responsibilities | Yes — as invariants become confirmed, add to diagram |
| Full model phases | Yes — invariants are a required part of the final model |

### Markdown companion notation

In the `.md` companion file, invariants appear as `Invariant:` lines under the field they constrain:

```
+ modifier: int
      Invariant: modifier = sum of applicable trait ranks + circumstance bonuses
```

---

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

### `class-diagram-layout-rules.md`

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

### `sequence-diagrams.md`

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

### `sequence-diagram-layout-rules.md`

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

## Rules

*No rules for this phase. List rule stems (filename without `.md`) under `skill-config.json` → `phase_rules` for this phase slug, and optionally `every_phase_rules` for rules that apply to every phase. See `parts/library/process-phases.md` § Phase bundle — rules.*


---
