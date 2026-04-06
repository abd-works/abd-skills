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

## Collection Class Anti-Pattern

Never invent wrapper types to represent multi-valued fields. Using `SkillSet`, `AbilitySet`, `PowerList`, or `AdvantageList` as class names implies there is a meaningful class there — but these are just collections with no behavior. They pollute the model.

**Wrong:**
```
+ skills: SkillSet
```

**Right:**
```
+ skills: Skill [0..*]
```

Use cardinality notation directly on the field. The cardinality brackets go on the field entry in the diagram:

```bash
drawio_cli.py add-field Character "+ skills: Skill [0..*]"
drawio_cli.py add-field Character "+ abilities: Ability [1..*]"
drawio_cli.py add-field Character "+ powers: Power [0..*]"
```

The `[0..*]` or `[1..*]` tells you both the type and the multiplicity without introducing a phantom class. Only model a collection type as a real class if the collection itself has behavior, identity, or invariants of its own.

---

## Associations Require a Connecting Field

Before drawing an association or dependency between two classes, you must be able to point to a **field** on the source class that holds a reference to the target. No field = no arrow.

**Wrong:** Drawing `Character → Effect` because "Character uses Effects somewhere" — there is no field on Character that holds an Effect reference directly.

**Right:** Tracing the actual path — `Character` has `powers: Power [0..*]`, and a `Power` wraps an `Effect`. The relationship between Character and Effect is therefore **through Power**, not direct. Draw `Character ◆── Power` and `Power → Effect`, not `Character → Effect` directly.

**Protocol before drawing a cross-module relationship:**
1. Identify the field on the source class that connects to the target
2. If no such field exists yet, investigate the source material more deeply before drawing
3. If the connection is definitely real but indirect (via an intermediate class), model the intermediate explicitly
4. If after investigation you cannot find a direct field, the relationship does not exist at this fidelity — leave it out until extraction reveals the path

This applies at all phases. At scan fidelity, prefer omitting a relationship over drawing an unsupported one.

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