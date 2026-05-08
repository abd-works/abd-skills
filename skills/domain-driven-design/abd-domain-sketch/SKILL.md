---
name: domain-sketch
catalog_garden_order: 4
description: >-
  Enrich each Key Abstraction with structured, plain-English concept blocks
  so the team has a readable object model before committing to classes.
---
# domain-sketch

## Purpose

The purpose of this skill is to create a robust domain model that describes domain concepts in a structured, plain-English form — before anyone commits to classes, methods, or properties. The skill applies object-oriented analysis to the source material, producing a **concept** for every domain idea that has distinct identity, state, behavior, structure, or interactions. Each concept spells out what it **is for**, what it **does**, and who it **works with**, grounded in evidence from the real source so a business reader can challenge it and a modeler can build from it.

---

## When to use

- A `<deliverables-folder>/<name>-key-abstractions.md` exists.
- The user asks to sketch concepts, build an object model, or identify domain objects.
- Downstream work (e.g. CRC) needs defined concepts to assign responsibilities to.

## Prerequisites

This skill **requires Key Abstractions and grouped terms** to work with. If no key-abstractions file exists, **first run `abd-key-abstractions`** (and `abd-domain-language` and `abd-module-partition` upstream of that as needed). Do not invent KAs from memory — read the upstream file.

---

## Core concepts

### Concept

A **concept** is a named domain idea the team treats as a candidate object: something the business talks about that has its own purpose, its own behavior, and relationships with other concepts. A concept is **not** a class — it is the plain-English precursor to one. Each concept block contains:

- **Verb-led behavior bullets** — what the concept does, enforces, or produces. Use active voice; every bullet should naturally start with a verb the concept performs.
- **Invariant bullet** — `**Invariant:** ...` for any rule that must always hold.

### Every KA must have a term that names the KA itself

The first `### **concept**` listed under each `## **KA**` heading **must be the KA's own concept** — the one whose name matches the KA. This is the most important concept to describe: it carries the abstraction's behavior, identity, and invariants. Other concepts grouped under the KA are subordinate.

For example, under `## **Product Catalog**`, the first `### **concept**` is `### **product catalog**`, followed by `### **product**`, `### **category**`, etc.

### Modeling each term: concept, subtype, property, instance, or invariant

Not every domain term deserves its own `### **concept**` heading. Before classifying, **read the source material for that term** and do proper object-oriented analysis on what the source actually says.

A term becomes a **concept** when it has **distinct identity**, **state**, **behavior**, **structure**, or **interactions**. A term that is a **specialized version** of another concept and adds **different behavior** is a **subtype**. A term that differs from its siblings only by **data values** is an **instance** or **type property** on the parent. A term that is a **value, slot, or attribute** another concept carries is a **property**. A term that describes a **rule that must always hold** is an **invariant** on the concept it constrains.

For typing decisions, see **`## Inheritance and subtypes`** in [`common/oo-concepts.md`](../common/oo-concepts.md). **Do not read or apply the `## Decomposing responsibilities` section** — that section applies at CRC stage and beyond.

### Subtypes

A subtype is one concept **being a type of** another. Write generalizations in plain English (`### **International Shipment** *is a type of* **Shipment**`), not in code notation. Keep **shared** behavior on the **base**; the subtype block adds only **delta** behavior.

### Roles and actors

A role (gamemaster, administrator, operator, reviewer) **is** a domain concept if it has distinct identity, state, or behavior from the system's perspective. A role that performs a task outside the system or the UI is a contextual label — note it in `### decisions made`, do not model it as a concept.

### Behavior and produced result on the same bullet

When a behavior bullet directly produces a result, write both on the same line: `- [behavior], producing a [result]`. Do not split cause and effect across two bullets.

### Decisions made

Every KA carries a `### decisions made` list under it — the specific judgment calls the modeler had to make: boundary calls, scope calls, structural calls, and open questions.

### Source extracts

Every KA carries a `### references` section listing all `**Ref —**` entries for concepts in that KA. Each entry has `Source:`, `Locator:`, `Extract:` and is followed by a fenced ```source``` block of verbatim text from disk.

---

## Output file

This skill produces a **standalone, self-contained file** at:

```
<deliverables-folder>/[<name>-]domain-sketch.md
```

**File name:** Default to `domain-sketch.md`. Add a `<name>-` engagement prefix only when you need disambiguation — multiple products living in the same workspace, or the user asks for it explicitly. Both `domain-sketch.md` and `<name>-domain-sketch.md` are valid. For multi-module engagements (with `abd-module-partition` output), the module name is the disambiguator: `<deliverables-folder>/modules/<module-name>-domain-sketch.md`.

The file is **not** an in-place enrichment of the key-abstractions file. It is a fresh artifact in the same flat heading shape.

**Resolving `<deliverables-folder>`** — pick in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output (or other engagement docs like `story-map.md`, `process.md`, `corrections-log.md`) already lives in a folder, write next to them in the **same** folder.
3. **The workspace root.** If neither applies, write to the workspace root.

Do **not** assume a predetermined folder name like `domain/` or `stories/`. The only DDD/story skill that creates a sub-folder is **`abd-module-partition`**, which deliberately uses `modules/<module-name>-…` to carve a partition.

For a multi-module engagement (with `abd-module-partition` output), use `<deliverables-folder>/modules/<module-name>-domain-sketch.md` — i.e. the `modules/` sub-folder lives **inside** the resolved `<deliverables-folder>`.

---

## Consistent shape (used by every DDD phase skill)

```
## **{{KAName}}**

[Optional 1–2 sentence intro — what this KA is for, who it cooperates with]

### **{{ka_name as a concept}}**         ← MUST appear first; matches the KA
- verb-led behavior: what the KA itself does, owns, enforces
- **Invariant:** rule that must always hold

### **{{another concept}}**
- verb-led behavior bullet
- **Invariant:** rule that must always hold

### **{{SubtypeName}}** *is a type of* **{{BaseName}}**
- delta behavior — only what the subtype adds

### references
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

### decisions made
- boundary call, scope call, structural call, or open question
```

---

## Build

1. **Read the prerequisite file.** Read `<deliverables-folder>/<name>-key-abstractions.md`. Confirm `state: key-abstractions` and that `## **KA**` blocks exist with terms grouped under them.
2. **Read the source material.** For each KA, follow its `### references` entries and read the source chunks. Understand each term's behavior deeply before writing any sketch bullets.
3. **For each KA, write a concept block.** Under `# Core Domain`:
   - `## **KAName**` heading with optional 1–2 sentence intro.
   - `### **ka_name_as_a_concept**` — the KA's own concept, listed FIRST, with verb-led behavior bullets describing what the KA itself does, owns, and enforces. Add an `**Invariant:**` bullet for any rule that must always hold.
   - `### **concept**` for each grouped term, with verb-led behavior bullets. Add `**Invariant:**` bullets where rules apply.
   - `### **SubtypeName** *is a type of* **BaseName**` for any specialization, with delta behaviors only.
   - `### references` listing all Refs for concepts in this KA, with fenced ```source``` blocks of verbatim text.
   - `### decisions made` listing typing calls, scope calls, and open questions.
4. **Write boundary concepts** under `# Boundary Domain` as `### **boundary_concept** *(owned by: Module)*` with verb-led bullets describing what this module sees of them. Close with a single `### references` and `### decisions made`.
5. **Apply the active-verb test** to every behavior bullet: the hidden subject ("a *concept*") should naturally start the sentence with a verb. If a bullet describes something with its own distinct structure or interactions, it is hiding a concept — extract it as its own `### **concept**` heading.
6. **Set the state marker** to `domain-sketch`.
7. **Write the file** to `<deliverables-folder>/<name>-domain-sketch.md`. Follow the template in `templates/domain-sketch-template.md`.

---

## Validate

1. **Per-phase output file.** The file is named `<name>-domain-sketch.md`. No prior or later phase content lives in it.
2. **Every KA has a concept that names it.** Every `## **KA**` heading is followed by a `### **concept**` whose name matches the KA itself, listed first, with verb-led behavior bullets.
3. **Every KA from the prior phase appears.** Every `## **KA**` from the key-abstractions file has a corresponding `## **KA**` block here.
4. **Every concept has at least one verb-led behavior bullet.** Active voice; subject is the concept itself.
5. **Subtypes use English heading form.** `### **SubtypeName** *is a type of* **BaseName**` — no code notation.
6. **References per KA with verbatim source blocks.** One `### references` per KA, every `**Ref —**` followed by a fenced ```source``` block of verbatim text.
7. **Decisions per KA.** One `### decisions made` per KA listing modeling judgment calls.
8. **No sub-headings under concepts.** Bullets live directly under each `### **concept**` heading. No `#### Domain Sketch`, `#### References`, or `#### Decisions made` sub-sections.
9. **No premature design commitments.** No DDD stereotypes, typed properties, method signatures, cardinality notation, or `Shape hint:`/`Tension:` labels.
10. **State marker.** Front matter reads `state: domain-sketch`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Per-phase file with consistent flat shape

**Scanner:** Manual review

The domain-sketch skill writes a self-contained file at `<deliverables-folder>/<name>-domain-sketch.md`. It does **not** enrich the prior phase's file in place. The output uses the consistent flat heading shape every DDD phase skill shares.

#### DO

- Write the file to `<deliverables-folder>/<name>-domain-sketch.md`.

  **Example (pass):** `domain/paw-place-domain-sketch.md`.

- Use `## **KA**` (h2), `### **concept**` (h3), `### references` (h3), `### decisions made` (h3) — all peers under each `## **KA**`.

  **Example (pass):**
  ```
  ## **Product Catalog**

  ### **product catalog**
  - owns the browsable searchable collection of pet supplies
  - **Invariant:** must be the single source of truth for product identity

  ### **product**
  - belongs to at least one category
  - exposes real-time stock availability

  ### references
  **Ref —** …

  ### decisions made
  - …
  ```

#### DO NOT

- Add `### Domain Sketch` as a sub-heading inside the prior phase's file.

  **Example (fail):** Edit `paw-place-key-abstractions.md` to insert `### Domain Sketch` peers — that is in-place enrichment which produces unrecoverable heading drift.

- Insert intermediate sub-headings between the KA and its concepts.

  **Example (fail):**
  ```
  ## **Product Catalog**
  ### Ubiquitous Language
  #### **product**
  ### Domain Sketch
  ```

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: Every Key Abstraction has a concept that names the KA itself

**Scanner:** AI review

Every `## **KA**` heading must be followed by a `### **concept**` whose name matches the KA itself (lowercased or as written in the source), listed **first** under the KA, with verb-led behavior bullets. The KA's own concept is the most important to describe — it carries the abstraction's behavior, identity, and invariants.

#### DO

- List the KA's own concept first under the `## **KA**` heading, with its own behavior bullets.

  **Example (pass):**
  ```
  ## **Notification**

  ### **notification**                    ← first; matches the KA
  - delivers transactional and marketing messages triggered by lifecycle events
  - **Invariant:** transactional always; marketing only with explicit opt-in

  ### **notification preferences**
  - …
  ### **restock alert**
  - …
  ```

#### DO NOT

- Skip the KA's own concept.

  **Example (fail):**
  ```
  ## **Notification**

  ### **notification preferences**           ← subordinate first; missing ### **notification**
  - …
  ```

**Source:** Correction — engagement repo (paw-place); KA's own term must be the most important concept modeled.

### Rule: Concept blocks are flat — no sub-headings

**Scanner:** Manual review

Each `### **concept**` block contains verb-led behavior bullets directly beneath the heading. No `#### Domain Sketch`, `#### References`, `#### Decisions made`, or other sub-section headings appear inside a concept block.

#### DO

- Place behavior bullets directly under the `### **concept**` heading.

  **Example (pass):**
  ```
  ### **check**
  - is resolved by rolling a d20, adding the trait rank and modifier, comparing to the DC, producing a check result
  - **Invariant:** roll total versus difficulty class; subtypes only vary how total or DC is produced
  ```

#### DO NOT

- Insert `#### Domain Sketch` (or any other sub-heading) inside a concept.

  **Example (fail):**
  ```
  ### **check**

  #### Domain Sketch
  - is resolved by rolling a d20…

  #### References
  **Ref —** …
  ```

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: Behavior and its produced result on the same bullet

**Scanner:** Manual review

When a behavior bullet directly produces a result, the result must appear on the same bullet as the behavior — not as a separate bullet immediately following it.

#### DO

- Combine a behavior and its immediate output on the same bullet using ", producing a [result]" or a similar connective phrase.

  **Example (pass):** `- is resolved by rolling a d20, adding the trait rank and modifier, comparing to the difficulty class, producing a check result`

#### DO NOT

- Write a behavior bullet and follow it with a standalone "produces a [result]" bullet.

  **Example (fail):**
  ```
  - is resolved by rolling a d20, comparing the roll total to the difficulty class
  - produces a check result
  ```

**Source:** Inherited correction (check-resolution engagement).

### Rule: Subtypes use English heading form with delta only

**Scanner:** Manual review

Subtype concepts use the English heading form (`### **SubtypeName** *is a type of* **BaseName**`), not code notation. Subtype blocks carry only delta behaviors — shared behavior stays on the base.

#### DO

- Use the English heading form.

  **Example (pass):** `### **International Shipment** *is a type of* **Shipment**`

- Include only delta behaviors.

  **Example (pass):** Base owns "gates warehouse exit"; subtype adds "collects customs commodity codes" — no repetition.

#### DO NOT

- Use code-style notation like `### InternationalShipment : Shipment` or `### InternationalShipment extends Shipment`.

- Duplicate base behaviors in the subtype block.

**Source:** Inherited from prior domain-sketch guidance.

### Rule: No hidden concepts in behavior bullets

**Scanner:** AI review

Every behavior bullet must pass the **active-verb test**: the hidden subject ("a *concept*") naturally starts the sentence with an active verb. If the bullet describes something with its own distinct structure, its own DC or threshold, its own roles, or its own result-flow, it is hiding a concept that must be extracted as its own `### **concept**` heading.

#### DO

- Apply the active-verb test to every bullet.

  **Example (pass):** "is made using the trait of a character" — a *Check* is made using the trait. Natural.

- Extract hidden concepts when the test fails.

  **Example (pass):** "team helpers each roll the same trait versus DC 10; each helper success grants the leader +2" — extracted as `### **Team Check** *is a type of* **Check**`.

#### DO NOT

- Leave complex multi-actor behavior as a single bullet on a parent concept.

**Source:** Inherited from prior domain-sketch guidance.

### Rule: No premature design commitments

**Scanner:** Manual review

The domain-sketch file contains no DDD stereotypes, operation signatures, cardinality notation, lifecycle tables, or structural classification labels. The sketch is plain English — design decisions belong to later skills.

#### DO

- Keep concept blocks in plain English — verb-led prose bullets and `**Invariant:**` lines.

#### DO NOT

- Add `<<Entity>>`, `<<ValueObject>>`, `<<Service>>`, `<<Aggregate>>`.
- Include operation signatures like `release(payment: Payment): void`.
- Add cardinality notation like `1..*`, `0..1`.
- Use `Shape hint:` or `Tension:` labels.

**Source:** Inherited from prior domain-sketch guidance.

### Rule: References per KA with verbatim source blocks

**Scanner:** Manual review

Each `## **KA**` block has exactly one `### references` section listing all `**Ref —**` entries for concepts in that KA. Every `**Ref —**` is followed by a fenced ```source``` block of verbatim text from disk.

#### DO

- Group all Refs for a KA in one `### references` section.

#### DO NOT

- Insert `#### References` sub-headings under each concept.
- Leave a `**Ref —**` without a fenced source block.

**Source:** Adapted from prior domain-sketch guidance.

### Rule: State marker is domain-sketch

**Scanner:** Manual review

After this skill runs, the file's YAML front matter must contain `state: domain-sketch`.

#### DO

- Set the front matter to exactly `state: domain-sketch`.

#### DO NOT

- Leave the marker at `key-abstractions` or omit the front matter.

**Source:** Inherited from prior domain-sketch guidance.
<!-- execute_rules:bundle_rules:end -->
