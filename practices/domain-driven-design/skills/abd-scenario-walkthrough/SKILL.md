---
name: scenario-walkthrough
catalog_garden_order: 7
description: >-
  Walk concrete scenarios through the object model. Every step maps to a
  class and operation; lifecycle guards and invariants come from the
  prior phase. Output is a standalone per-phase file.
---

# scenario-walkthrough

## Purpose

**Walk** concrete scenarios through the typed object model (or CRC where the object model is not yet built). Each step must map to a **class** and an **operation** from the prior phase's file. When a step crosses a state change or must respect a guard, align with the invariants and interactions captured upstream. If a step has no owner, record a gap and revise upstream artifacts.

## When to use

- A `<deliverables-folder>/<name>-object-model.md` (preferred) or `<name>-crc.md` exists.
- The team needs to validate that the typed model can express realistic flows end-to-end.
- The user asks to walk scenarios, validate the model with examples, or pressure-test ownership.

## Prerequisites

This skill **requires a typed model or CRC** to walk through. If neither exists, run `abd-class-responsibility-collaborator` and (optionally) `abd-object-model` first. Do not invent scenarios disconnected from the modeled classes.

---

## Output file

This skill produces a **standalone, self-contained file** at:

```
<deliverables-folder>/[<name>-]walkthrough.md
```

**File name:** Default to `walkthrough.md`. Add a `<name>-` engagement prefix only when you need disambiguation — multiple products living in the same workspace, or the user asks for it explicitly. Both `walkthrough.md` and `<name>-walkthrough.md` are valid. For multi-module engagements (with `abd-module-partition` output), the module name is the disambiguator: `<deliverables-folder>/modules/<module-name>-walkthrough.md`.

**Resolving `<deliverables-folder>`** — pick in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output already lives in a folder, write next to it.
3. **The workspace root.** If neither applies, write to the workspace root.

Do **not** assume a predetermined folder name like `domain/`. The only DDD/story skill that creates a sub-folder is **`abd-module-partition`**.

The file is **not** an in-place enrichment of the object-model or CRC file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

---

## Consistent shape (used by every DDD phase skill)

```
## **{{KAName}}**

[Optional 1–2 sentence intro: which scenarios live under this KA]

### **{{Scenario Name}}**
**Purpose:** what this scenario validates
**Concepts traced:** Class, Class, Class

#### Walk 1 — Covers: {walk scope}
```
object: ReturnType = new Class(param: Type, param: Type)
result: Type = object.someMethod()
    variable: CollaboratingClass = getter_or_lookup
    inner: InnerType = variable.method(parameter: Type)
        nested: NestedType = AnotherClass.method(param: Type)
        return nested
    return result
return
```

#### Walk 2 — Covers: {alternate / failure path}
```
…
```

### **{{Another Scenario}}**
**Purpose:** …
**Concepts traced:** …

#### Walk 1 — Covers: …
```
…
```

### references                              ← one per KA, peer to scenarios
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

### decisions made                          ← one per KA, peer to scenarios
- gap recorded, ownership decision, alternate-path trade-off, or open question
```

The Boundary Domain is one flat group with shared `### references` and `### decisions made`.

---

## Build

1. **Read the prerequisite file.** Read `<deliverables-folder>/<name>-object-model.md` (preferred) or `<name>-crc.md`. Group scenarios under their `## **KA**` from the prior phase.
2. **Pick scenarios per KA.** Cover at minimum: one happy path, one failure or edge path, one path involving cooperation or shared resources. Use real domain values, not placeholders.
3. **Write the scenario blocks.** Under `# Core Domain`, for each KA from the prior phase:
   - `## **KAName**` heading.
   - `### **Scenario Name**` for each scenario, with `**Purpose:**` and `**Concepts traced:**` lines, then one or more `#### Walk N — Covers: …` indented pseudocode blocks.
   - `### references` listing all Refs that ground the scenarios in source, with fenced ```source``` blocks.
   - `### decisions made` listing gaps, ownership decisions, and open questions.
4. **Validate ownership of every step.** Each pseudocode line that performs domain logic must trace to a class and operation in the prior-phase file. If a step has no owner, record a gap in `### decisions made` and revise upstream.
5. **Set the state marker** to `walkthrough`.
6. **Write the file** to `<deliverables-folder>/<name>-walkthrough.md`. Follow the template in `templates/domain-walkthrough-scaffold.md`.

---

## Validate

- **Per-phase output file.** The file is named `<name>-walkthrough.md`. No prior or later phase content lives in it.
- **No sub-headings under scenarios.** Walk blocks live directly under each `### **Scenario**` heading. No `#### Walkthrough` or `#### References` sub-sections.
- **References per KA with verbatim source blocks.** One `### references` per KA, every `**Ref —**` followed by a fenced ```source``` block of verbatim text.
- **Decisions per KA.** One `### decisions made` per KA listing gaps and ownership calls.
- **Every walk line that performs domain logic ties to a class and operation** from the prior-phase file.
- **State marker.** Front matter reads `state: walkthrough`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Per-phase file with consistent flat shape

**Scanner:** Manual review

The scenario-walkthrough skill writes a self-contained file at `<deliverables-folder>/<name>-walkthrough.md`. It does **not** enrich the prior phase's file in place. The output uses the consistent flat heading shape every DDD phase skill shares: `## **KA** → ### **Scenario** (with walks directly under) → ### references → ### decisions made`.

#### DO

- Write the file to `<deliverables-folder>/<name>-walkthrough.md`.

  **Example (pass):** `domain/paw-place-walkthrough.md`.

- Place `**Purpose:**`, `**Concepts traced:**`, and `#### Walk N` blocks directly under each `### **Scenario**` heading.

#### DO NOT

- Append scenarios as a sub-section inside the prior phase's file.

  **Example (fail):** Edit `paw-place-object-model.md` to insert scenario blocks — that is in-place enrichment which produces unrecoverable heading drift.

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: Every walk line traces to a class and operation

**Scanner:** Manual review

Every pseudocode line that performs domain logic must map to a class and an operation defined in the prior-phase file (`<name>-object-model.md` or `<name>-crc.md`). Lines that have no owner must be recorded as gaps under `### decisions made` and revised upstream.

#### DO

- Use class names, property names, and operation names that exist in the prior-phase file.

  **Example (pass):** Walk line `roll: Integer = d20.roll()` traces to `D20.roll()` which exists in `paw-place-object-model.md`.

- Record any line that cannot be traced as a gap.

  **Example (pass):**
  ```
  ### decisions made
  - GAP: walk step `restock_alert.send()` has no owner — Notification class needs a `send()` operation; revisit object-model.
  ```

#### DO NOT

- Invent class names or operations that do not exist in the prior-phase file.

  **Example (fail):** Walk uses `OrderManager.dispatchOrder()` but no `OrderManager` class is modeled.

- Leave untraceable lines without a recorded gap.

**Source:** Engagement convention (scenario-walkthrough skill).
<!-- execute_rules:bundle_rules:end -->
