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

- **Verb-led behavior bullets** — what the concept does, enforces, or produces. Use active voice; every bullet should naturally start with a verb the concept performs. Every domain term in a bullet must be *italicized*.
- **Invariant bullet** — `**Invariant:** ...` for any rule that must always hold. Domain terms in invariants are also *italicized*.

### Every KA must have a term that names the KA itself

The first `### concept` listed under each `## KA` heading **must be the KA's own concept** — the one whose name matches the KA. This is the most important concept to describe: it carries the abstraction's behavior, identity, and invariants. Other concepts grouped under the KA are subordinate.

For example, under `## Product Catalog`, the first `### concept` is `### product catalog`, followed by `### product`, `### category`, etc.

### Modeling each term: concept, subtype, property, instance, or invariant

Not every domain term deserves its own `### concept` heading. Before classifying, **read the source material for that term** and do proper object-oriented analysis on what the source actually says.

A term becomes a **concept** when it has **distinct identity**, **state**, **behavior**, **structure**, or **interactions**. A term that is a **specialized version** of another concept and adds **different behavior** is a **subtype**. A term that differs from its siblings only by **data values** is an **instance** or **type property** on the parent. A term that is a **value, slot, or attribute** another concept carries is a **property**. A term that describes a **rule that must always hold** is an **invariant** on the concept it constrains.

For typing decisions, see **`## Inheritance and subtypes`** in [`common/oo-concepts.md`](../common/oo-concepts.md). **Do not read or apply the `## Decomposing responsibilities` section** — that section applies at CRC stage and beyond.

### Subtypes

A subtype is one concept **being a type of** another. Write generalizations in plain English (`### International Shipment *is a type of* Shipment`), not in code notation. Keep **shared** behavior on the **base**; the subtype block adds only **delta** behavior.

### Roles and actors

A role (gamemaster, administrator, operator, reviewer) **is** a domain concept if it has distinct identity, state, or behavior from the system's perspective. A role that performs a task outside the system or the UI is a contextual label — note it in `### Decisions made`, do not model it as a concept.

### Behavior and produced result on the same bullet

When a behavior bullet directly produces a result, write both on the same line: `- [behavior], producing a [result]`. Do not split cause and effect across two bullets.

### Decisions made and References — per concept

Every concept carries its own `### Decisions made` list and `### References` section immediately after its behavior bullets. This keeps the reasoning and evidence co-located with the concept they support. Do not bundle decisions or references at the KA level.

### Property and instance stubs

Terms classified as properties, instances, or type properties of another concept get a stub heading (`### term_name`) with a brief classification bullet (e.g., "is a property of *parent_concept*") and a `### References` section. This makes visible that the term was considered and classified, rather than silently dropped.

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
## KAName

[Analytical intro paragraph(s) with *italicized domain terms*]

### ka_name_as_a_concept              ← MUST appear first; matches the KA
- verb-led behavior with *italicized domain terms*
- **Invariant:** rule that must always hold

### Decisions made
- typing call, scope call, structural call, or open question

### References
**Ref — title**
Source: ...
Locator: ...
Extract: whole

---

### another_concept
- verb-led behavior with *italicized domain terms*

### Decisions made
- ...

### References
**Ref — title**
Source: ...

---

### SubtypeName *is a type of* BaseName
- delta behavior — only what the subtype adds

### References
**Ref — title**
Source: ...

---

### property_term
- is a property of *parent_concept* — brief classification note

### References
**Ref — title**
Source: ...

---
```

---

## Build

1. **Read the prerequisite file.** Read `<deliverables-folder>/<name>-key-abstractions.md`. Confirm `state: key-abstractions` and that `## KA` blocks exist with terms grouped under them.
2. **Read the source material.** For each KA, follow its `### references` entries and read the source chunks. Understand each term's behavior deeply before writing any sketch bullets.
3. **For each KA, write a concept block.** Under `# Core Domain`:
   - `## KAName` heading (no bold) with analytical intro paragraph(s) using *italicized domain terms*.
   - `### ka_name_as_a_concept` (no bold) — the KA's own concept, listed FIRST, with verb-led behavior bullets using *italicized domain terms*. Add `**Invariant:**` bullets for rules that must always hold.
   - `### Decisions made` and `### References` for the KA's own concept, immediately after its behavior bullets.
   - `---` separator.
   - `### concept` (no bold) for each grouped term, with verb-led behavior bullets using *italicized domain terms*. Each concept gets its own `### Decisions made` and `### References`, followed by `---`.
   - `### SubtypeName *is a type of* BaseName` (no bold) for any specialization, with delta behaviors only and its own `### References`, followed by `---`.
   - `### property_term` stub for any term classified as a property, instance, or type property, with a brief classification bullet and `### References`, followed by `---`.
4. **Write boundary concepts** under `# Boundary Domain` as `## boundary_concept` with `Owned by: Module`, verb-led bullets using *italicized domain terms*, and per-concept `### Decisions made` and `### References`.
5. **Italicize every domain term** in behavior bullets, invariants, and KA intro paragraphs. Non-domain words (verbs, articles, prepositions) stay plain.
6. **Apply the active-verb test** to every behavior bullet: the hidden subject ("a *concept*") should naturally start the sentence with a verb. If a bullet describes something with its own distinct structure or interactions, it is hiding a concept — extract it as its own `### concept` heading.
7. **Set the state marker** to `domain-sketch`.
8. **Write the file** to `<deliverables-folder>/<name>-domain-sketch.md`. Follow the template in `templates/domain-sketch-template.md`.

---

## Validate

1. **Per-phase output file.** The file is named `<name>-domain-sketch.md`. No prior or later phase content lives in it.
2. **Every KA has a concept that names it.** Every `## KA` heading is followed by a `### concept` whose name matches the KA itself, listed first, with verb-led behavior bullets.
3. **Every KA from the prior phase appears.** Every `## KA` from the key-abstractions file has a corresponding `## KA` block here.
4. **Every concept has at least one verb-led behavior bullet.** Active voice; subject is the concept itself.
5. **Domain terms italicized.** Every domain term in behavior bullets, invariants, and KA intro paragraphs is *italicized*. Consistent throughout the file.
6. **No bold on headings.** KA headings (`## KAName`) and concept headings (`### concept`) use no bold. Subtypes use `### SubtypeName *is a type of* BaseName`.
7. **Decisions and References per concept.** Every concept (including subtypes and property stubs) has its own `### Decisions made` (where modeling calls were made) and `### References` immediately after its behavior bullets. Not bundled per KA.
8. **Separators between concepts.** A `---` horizontal rule follows every concept block (after its References), before the next concept heading.
9. **Property/instance stubs visible.** Terms classified as properties, instances, or type properties have a stub heading with a classification bullet and References. No silently dropped terms.
10. **No sub-headings under concepts.** Bullets live directly under each `### concept` heading. No `####` sub-sections.
11. **No premature design commitments.** No DDD stereotypes, typed properties, method signatures, cardinality notation, or `Shape hint:`/`Tension:` labels.
12. **State marker.** Front matter reads `state: domain-sketch`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Per-phase file with consistent flat shape

**Scanner:** Manual review

The domain-sketch skill writes a self-contained file at `<deliverables-folder>/<name>-domain-sketch.md`. It does **not** enrich the prior phase's file in place.

#### DO

- Write the file to `<deliverables-folder>/<name>-domain-sketch.md`.

  **Example (pass):** `domain/paw-place-domain-sketch.md`.

- Use `## KAName` (h2, no bold), `### concept` (h3, no bold), `### Decisions made` (h3), `### References` (h3) — per concept, not per KA.

  **Example (pass):**
  ```
  ## Product Catalog

  ### product catalog
  - owns the browsable searchable collection of *pet supplies*
  - **Invariant:** must be the single source of truth for *product* identity

  ### Decisions made
  - ...

  ### References
  **Ref —** …

  ---

  ### product
  - belongs to at least one *category*

  ### References
  **Ref —** …

  ---
  ```

#### DO NOT

- Add `### Domain Sketch` as a sub-heading inside the prior phase's file.

  **Example (fail):** Edit `paw-place-key-abstractions.md` to insert `### Domain Sketch` peers — that is in-place enrichment.

- Insert intermediate sub-headings between the KA and its concepts.

  **Example (fail):**
  ```
  ## Product Catalog
  ### Ubiquitous Language
  #### product
  ### Domain Sketch
  ```

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: Every Key Abstraction has a concept that names the KA itself

**Scanner:** AI review

Every `## KA` heading must be followed by a `### concept` whose name matches the KA itself, listed **first** under the KA, with verb-led behavior bullets. The KA's own concept is the most important to describe.

#### DO

- List the KA's own concept first under the `## KA` heading, with its own behavior bullets.

  **Example (pass):**
  ```
  ## Notification

  ### notification                       ← first; matches the KA
  - delivers *transactional* and *marketing messages* triggered by *lifecycle events*
  - **Invariant:** *transactional* always; *marketing* only with explicit *opt-in*

  ### Decisions made
  - ...

  ### References
  **Ref —** …

  ---

  ### notification preferences
  - …
  ```

#### DO NOT

- Skip the KA's own concept.

  **Example (fail):**
  ```
  ## Notification

  ### notification preferences           ← subordinate first; missing ### notification
  - …
  ```

**Source:** Correction — engagement repo (paw-place).

### Rule: Domain terms italicized in behavior bullets

**Scanner:** AI review

Every domain term referenced in a behavior bullet, invariant, or KA intro paragraph must be italicized using `*term*`. This makes the ubiquitous language visually precise and self-documenting.

#### DO

- Italicize every domain term when it appears in a behavior bullet, invariant, or KA intro paragraph.

  **Example (pass):**
  ```
  - is made *using* the *trait* of a *character*
  - is made *against* a *difficulty class* set by the *GM*
  - is resolved by *rolling* a *d20*, adding the *trait rank* and the *circumstance modifier*, comparing the *roll total* to the *difficulty class*, producing a *check result*
  ```

- Italicize terms consistently throughout the file.

#### DO NOT

- Leave domain terms as plain text in behavior bullets.

  **Example (fail):**
  ```
  - is made using the trait of a character
  - is made against a difficulty class set by the GM
  ```

- Italicize non-domain words (articles, prepositions, connectives).

  **Example (fail):** `- *is* *made* *using* *the* *trait*` — only domain terms get italics.

**Source:** Correction — check-resolution engagement demonstrated superior precision; adopted as standard.

### Rule: Per-concept Decisions made and References

**Scanner:** Manual review

Every concept block (including subtypes and property stubs) has its own `### Decisions made` (when modeling calls were made) and `### References` immediately after its behavior bullets, followed by a `---` separator. Decisions and References are not bundled at the KA level.

#### DO

- Place `### Decisions made` and `### References` per concept, immediately after its behavior bullets.

  **Example (pass):**
  ```
  ### check
  - is resolved by *rolling* a *d20*...
  - **Invariant:** ...

  ### Decisions made
  - *Check* alone owns *success/failure*...

  ### References
  **Ref — Game Play**
  Source: ...

  ---

  ### Check Result
  - is produced by a *check*...

  ### References
  **Ref — Degrees Of Success And Failure**
  Source: ...

  ---
  ```

- Separate concept blocks with `---` horizontal rules.

#### DO NOT

- Bundle all decisions and references at the end of the KA.

  **Example (fail):**
  ```
  ### concept_a
  - ...
  ### concept_b
  - ...
  ### references
  ### decisions made
  ```

**Source:** Correction — check-resolution engagement established per-concept structure as standard.

### Rule: Property and instance stubs visible

**Scanner:** AI review

Terms classified as properties, instances, or type properties of another concept get a stub heading (`### term_name`) with a brief classification bullet and a `### References` section. No silently dropped terms.

#### DO

- Give property/instance terms a stub heading with a classification note.

  **Example (pass):**
  ```
  ### d20
  - is the instrument a *check* rolls — a property of *check*, not a separate concept

  ### References
  **Ref — The Die**
  Source: ...

  ---
  ```

#### DO NOT

- Silently drop terms without a stub heading.

  **Example (fail):** A term from the KA grouping has no heading in the sketch and is only mentioned in a decisions-made bullet.

**Source:** Correction — check-resolution engagement; all terms visible.

### Rule: Concept blocks are flat — no sub-headings

**Scanner:** Manual review

Each `### concept` block contains verb-led behavior bullets directly beneath the heading. No `#### Domain Sketch`, `#### References`, `#### Decisions made`, or other sub-section headings appear inside a concept block. The `### Decisions made` and `### References` that follow a concept are peers at h3, not sub-sections.

#### DO

- Place behavior bullets directly under the `### concept` heading.

  **Example (pass):**
  ```
  ### check
  - is resolved by *rolling* a *d20*, adding the *trait rank* and *modifier*, comparing to the *DC*, producing a *check result*
  - **Invariant:** *roll total* versus *difficulty class*; subtypes only vary how *total* or *DC* is produced
  ```

#### DO NOT

- Insert `####` sub-headings inside a concept.

  **Example (fail):**
  ```
  ### check

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

  **Example (pass):** `- is resolved by *rolling* a *d20*, adding the *trait rank* and *modifier*, comparing to the *difficulty class*, producing a *check result*`

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

Subtype concepts use the English heading form (`### SubtypeName *is a type of* BaseName`), not code notation. No bold on either name. Subtype blocks carry only delta behaviors — shared behavior stays on the base.

#### DO

- Use the English heading form (no bold).

  **Example (pass):** `### International Shipment *is a type of* Shipment`

- Include only delta behaviors.

  **Example (pass):** Base owns "gates warehouse exit"; subtype adds "collects customs commodity codes" — no repetition.

#### DO NOT

- Use code-style notation like `### InternationalShipment : Shipment` or `### InternationalShipment extends Shipment`.

- Use bold on names: `### **International Shipment** *is a type of* **Shipment**`.

- Duplicate base behaviors in the subtype block.

**Source:** Inherited from prior domain-sketch guidance.

### Rule: No hidden concepts in behavior bullets

**Scanner:** AI review

Every behavior bullet must pass the **active-verb test**: the hidden subject ("a *concept*") naturally starts the sentence with an active verb. If the bullet describes something with its own distinct structure, its own DC or threshold, its own roles, or its own result-flow, it is hiding a concept that must be extracted as its own `### concept` heading.

#### DO

- Apply the active-verb test to every bullet.

  **Example (pass):** "is made *using* the *trait* of a *character*" — a *Check* is made using the trait. Natural.

- Extract hidden concepts when the test fails.

  **Example (pass):** "team helpers each roll the same trait versus DC 10; each helper success grants the leader +2" — extracted as `### Team Check *is a type of* check`.

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

### Rule: State marker is domain-sketch

**Scanner:** Manual review

After this skill runs, the file's YAML front matter must contain `state: domain-sketch`.

#### DO

- Set the front matter to exactly `state: domain-sketch`.

#### DO NOT

- Leave the marker at `key-abstractions` or omit the front matter.

**Source:** Inherited from prior domain-sketch guidance.
<!-- execute_rules:bundle_rules:end -->
