---
name: abd-ubiquitous-language
catalog_garden_order: 3
description: >-
  Build a shared, rigorous vocabulary for the scope you are modeling — extract
  terms, group them into Key Abstractions, and sketch each concept's behavior —
  all in one file every downstream artifact can rely on.
---
# abd-ubiquitous-language

## Purpose

Build a shared, rigorous vocabulary for the scope you are modeling so that domain experts and modelers agree on what each term means, what each concept does, and which rules must always hold — and capture that agreement in **one** living document the whole team uses without translation. The scope of one run can be a single module, several modules, or a whole-system sweep; the skill and its output shape stay the same.

This is a three-pass skill. It does not produce a flat term list first, a key-abstractions file second, and a concept-sketch file third. It reads source, extracts terms with definitions, groups them into Key Abstractions, sketches each concept's behavior and properties, and writes **one** file.

The final output is a robust domain model that describes domain concepts in a structured, plain-English form — before anyone commits to classes, methods, or properties. The skill applies object-oriented analysis to the source material, producing a **concept** for every domain idea that has distinct identity, state, behavior, structure, or interactions. Each concept spells out what it **is for**, what it **does**, and who it **works with**, grounded in evidence from the real source so a business reader can challenge it and a modeler can build from it.

---

## When to use

- The user asks to "build the ubiquitous language", "extract domain terms", "identify Key Abstractions", "sketch the domain", or "what are the building blocks."
- A scope has source material — rules, transcripts, training materials, design notes — but no agreed vocabulary or concept sketch yet.
- Downstream modeling (CRC, object model, scenarios, code) needs defined concepts with named behavior — more than a flat glossary.
- You want to confirm business logic with subject-matter experts in their own language before committing to classes or schemas or other modelling syntax.

---

## Core concepts

### Ubiquitous language

The **ubiquitous language** is the single set of names, definitions, and rules a team uses everywhere — conversations, requirements, tests, code, and diagrams. It is not a glossary collected from many places; it is one curated vocabulary the team commits to and updates together. Each named concept carries its own purpose, its own behavior, and its own invariants, so anyone reading the file can challenge what is true and anyone writing downstream artifacts can re-use the same words without paraphrase.

### Terms

A **term** is any named concept in the source that has behavior, rules, interactions, or distinct identity. The first pass of the skill extracts every term and assigns it a short plain-English definition and a placement decision: keep under a KA, move to boundary, or move out entirely. Terms appear as a flat list in the output file header — one bullet per term, definition only, no source references. A term's placement decision is recorded there with a parenthetical note and fleshed out later in `### Decisions made`.

### Key Abstraction (KA)

A **Key Abstraction** is a named domain building block that anchors a group of related terms. KAs are concepts that act as **centers of gravity** — the named ideas domain experts reach for first when explaining the domain. Because of that, their intro paragraphs carry the richest treatment of all five aspects: role, boundary, relationships, responsibilities, and rules/invariants. Relationships to other KAs get particular weight, because that is how domain experts discuss them — "*Check* depends on *Trait* for its modifier; *Trait* knows nothing about *Check*."

The KA name is itself the primary term. The KA's intro paragraph opens with "*KAName* is …" and IS the term definition — there is no separate subordinate entry that re-states it. A typical module has three to eight Key Abstractions; more usually means subordinate terms have been promoted prematurely.

### Concept

A **concept** is a named domain idea the team treats as a candidate object: something the business talks about that has its own purpose, its own behavior, and relationships with other concepts. A concept is not a class — it is the plain-English precursor to one. Every concept — KA or subordinate — can be described across five aspects:

- **Role** — the unique purpose this concept serves that no other does.
- **Boundary** — what it owns (single source of truth), what is external, how it collaborates.
- **Relationships** — explicit connections to other concepts and KAs.
- **Responsibilities** — the specific behaviors it performs and services it provides.
- **Rules / invariants** — non-negotiable truths that must always hold.

These are not independent sections in the output — they are woven into the concept's story as verb-led behavior bullets. Same format for every concept. The KA's own concept block doubles as the term definition for the KA itself. How much any concept has to say is driven by the complexity of what the source actually says about it. Domain terms in bullets are *italicized* so the language stays visually precise.

The first `### concept` listed under each `## KA` heading **must be the KA's own concept** — the one whose name matches the KA. Other concepts grouped under the KA are subordinate.

### Two tests for every term

**1. Independence test.** Can this concept be defined and reasoned about on its own, without the parent it came from? If it has no meaning outside another concept, it stays as a subordinate term, not a KA of its own.

**2. Scope-fit test.** Does this concept fundamentally connect to the core purpose of the scope being modeled, or does it only touch it tangentially? If it belongs more squarely in an adjacent area, place it in the Boundary Domain or move it out entirely.

### Three outcomes for each candidate term

- **Keep under a KA** — passes both tests; group under the right KA in the Core Domain.
- **Move to boundary** — independent, but this scope depends on it without owning it; record under `# Boundary Domain` with a single named owning module. If a boundary term is relevant to more than one KA, each KA records its own view — only the behaviors that KA actually depends on — as a concept stub inside that KA's block. The `# Boundary Domain` entry is the canonical record; the per-KA stubs are scoped views, not duplicates.
- **Move out** — independent and unrelated to this scope's purpose; note in the header.

### Modeling each term: concept, subtype, property, instance, or invariant

Not every domain term deserves its own concept block. Before classifying, **read the source material for that term** and do proper object-oriented analysis on what the source actually says.

A term becomes a **concept** when it has **distinct identity**, **state**, **behavior**, **structure**, or **interactions**. A term that is a **specialized version** of another concept and adds **different behavior** is a **subtype**. A term that differs from its siblings only by **data values** is an **instance** or **type property** on the parent. A term that is a **value, slot, or attribute** another concept carries is a **property**. A term that describes a **rule that must always hold** is an **invariant** on the concept it constrains.

For typing decisions, see **`### Inheritance and subtypes`** in the OO Concepts section below. Read it before classifying any term as a concept, subtype, property, or instance. **Do not read or apply `### Decomposing responsibilities`** — that section applies at CRC stage and beyond.

Property and instance terms still get a stub heading with a one-line classification note — no term is silently dropped.

### Subtypes

A subtype is one concept **being a type of** another. Write the heading in plain English (`### International Shipment *is a type of* Shipment`), not in code notation. Keep **shared** behavior on the **base**; the subtype block adds only **delta** behavior — what the subtype does differently or additionally.

### Roles and actors

A role (gamemaster, administrator, operator, reviewer) **is** a domain concept if it has distinct identity, state, or behavior from the system's perspective. A role that only performs tasks outside the system or the UI is a contextual label — note it in `### Decisions made`, do not model it as a concept.

### Property and instance stubs

Terms classified as properties, instances, or type properties of another concept get a stub heading (`### term_name`) with a brief classification bullet (e.g., "is a property of *parent_concept*") and a `### References` section. This makes visible that the term was considered and classified, rather than silently dropped.

### Decisions made and References — per KA

Every KA carries one `### Decisions made` list and one `### References` section, placed **after all of its concept blocks**. This keeps the reasoning and evidence co-located with the KA they support. `### Decisions made` records independence test results, scope-fit test results, typing calls, and any open questions for any concept in the KA. `### References` lists every source passage that supports any concept in the KA. Do not bundle decisions or references per concept.

### Three passes, one file

1. **Terms** — flat list of every named concept with a short plain-English definition and a placement decision (keep / boundary / moved out). No source references in the Terms list.
2. **Key Abstractions** — terms grouped under named KAs; each KA gets an intro paragraph that is its term definition.
3. **Concept blocks** — each KA's concept blocks (KA's own first, then subordinates, subtypes, property stubs), with verb-led behavior; **one** `### Decisions made` and **one** `### References` per KA, after all its concept blocks.

---


---


Shared reference for all abd-domain-driven-design skills. This file owns the OO theory. Each skill owns its own notation and format.

---

### What is a class

> **Applies from: ubiquitous language stage and beyond (ubiquitous language → CRC → object-model).**

A class is a named domain idea that earns its own identity because it has at least one of: **distinct identity**, **state**, **behavior**, **structure**, or **interactions** that cannot be collapsed into a property, instance, or type property of something else.

A class knows things (**state**) and does things (**behavior**). Those two dimensions — together with the relationships it maintains and the invariants that constrain it — are what a class IS at every level of fidelity. The notation changes across the pipeline; this definition does not.

A term that is only a data value on another class is a **property**. A term that varies only by label across identical behavior is a **type property**. A term that is one concrete member of a known set is an **instance**. A term that adds distinct behavior to a base is a **subtype**. Only when none of those fit does something deserve its own class.

Each skill records a class in its own form:
- **ubiquitous-language** — a named concept block with intent, behaviors, and collaborations in plain English.
- **CRC** — a `#### **ClassName**` block with responsibility and collaborator columns.
- **Object-model** — a typed class block with properties, operation signatures, relationships, and invariants.

---

### Decomposing responsibilities

> **Applies from: CRC stage and beyond (CRC → object-model → ...).** Do not use this section at ubiquitous language level — there are no typed properties or operations at that stage.

A responsibility is either something a class **holds** (state) or something it **does** (behaviour) — or both. Classify each responsibility before deciding how to represent it:

- **Property** — the class must remember something across calls. Named as a **noun phrase**: *remaining budget*, *active status*, *target character*.
- **Operation** — the class must perform an action or compute a result; it may be entirely stateless. Named as a **verb phrase**: *calculate shipping cost*, *apply condition*, *resolve check*.
- **Both** — the class holds state **and** exposes an action that works with it.

Never assume every responsibility implies a property, and never assume every responsibility implies an operation. Ask for each one: *hold something, do something, or both?*

---

### Relationships

> **Applies from: CRC stage and beyond (CRC → object-model).** At ubiquitous language level, dependencies are captured as plain-English collaboration sentences only — no formal relationship modeling.

A relationship describes how two domain classes depend on each other. Before recording a relationship, answer three questions:

1. **Does one class own the other's lifecycle?** — The other cannot exist without the first. If the owning class is gone, so is the owned one.
2. **Does one class exist to collect or group the other?** — The collecting class has no meaningful identity without its members. Remove all members and the collector is empty of purpose.
3. **Are both sides independent?** — Each can exist and be meaningful without the other.

These questions determine the nature of the dependency. Each skill records the answer in its own notation — plain-English collaborations at ubiquitous language level, named collaborators at CRC level, typed flavors with cardinality at object-model level.

A relationship also has **direction**: the class that depends on, uses, or navigates to the other is the navigating end. Be explicit about which side initiates the dependency.

---

### Inheritance and subtypes

> **Applies from: ubiquitous language stage and beyond (ubiquitous language → CRC → object-model).**

#### Base class and subtype

A **base class** (also called a parent or superclass) defines the common identity, state, and behavior shared by a family of related things. It owns everything that is true of every member of that family — the responsibilities, rules, and collaborations that do not change regardless of which specific variant you are dealing with.

A **subtype** (also called a child class or subclass) is a specialisation of the base. It *is a kind of* the base — everything the base defines applies to it — but it adds or overrides behavior that is specific to it alone. The subtype does not restate what it inherits; it only describes the delta.

**Inheritance** is the mechanism that connects them. The subtype inherits all of the base's identity and behavior automatically. The base never knows about its subtypes; the subtypes always know about their base.

A family can have many subtypes, each specialising the base in a different direction. Subtypes can themselves be bases for further subtypes — but depth should reflect real behavioral distinctions in the domain, not structural tidiness.

#### Liskov Substitution rule

**Anywhere the base is used, a subtype must work correctly in its place.** If swapping in a subtype breaks or weakens a rule the base guarantees, the subtype is not a true specialisation — it is a different thing that happens to share some behavior.

In practice: a subtype may *add* behavior and *strengthen* constraints, but it must never *remove* behavior or *weaken* a guarantee the base makes. If you find yourself writing a subtype that overrides a base operation to do nothing, throw an error, or return a narrower result than the base promises, stop — that is a modeling error, not a subtype.

#### When to use a subtype, type property, or instance

When a term looks like "a thing is a kind of another thing," three modeling options exist:

**Subtype** — the specialised thing adds **behavior the base does not have**. Each subtype does something differently enough that you need to describe it separately. Use this when the distinction changes **what the thing does**, not just what data it carries. Example: an *international shipment* is a type of *shipment* — it introduces customs filing and duty handling that a domestic shipment does not have.

**Type property (constrained list)** — the thing varies by **category**, but every category follows the **same behavior**. The difference is purely which label from a known list applies. Use this when you could swap one label for another and the behavior description would not change. Example: a *notification* has a *notification priority type* drawn from (*low*, *normal*, *urgent*) — every notification still has a recipient, still carries a message, still follows the same delivery and read-receipt rules. The *notification priority type* tells you how soon it surfaces, not how it behaves differently.

**Instance** — the thing is one **concrete member** of a parent concept, distinguished only by its **specific data values**. Many instances exist side by side and they all work the same way — each just carries different numbers or names. Use this when listing them out would produce rows that repeat the same structure with different fill. Example: *bronze*, *silver*, *gold* are all instances of *membership tier* — each names a specific discount rate and benefit set, but they all follow the same upgrade, renewal, and expiry rules that Membership Tier defines.

A common modeling journey begins with treating domain elements as *instances* or *type properties*, and as understanding of behavior differences grows, promotes them into subtypes.

**Example — Evolving a Payment System Domain Model:**

- **Early model (Instances or Type properties):**
  - Model *Payment* as a concept.
  - Each *payment* instance carries data like channel (e.g., "credit card", "bank transfer"), transaction amount, reference id, etc.
  - All payments go through the same core behaviors: *initiate payment*, *set channel*, *approve transaction limit*.

- **Transition point:**
  - As behaviors diverge (e.g., approval workflow or fraud checks differ by channel), notice that some payment types must satisfy additional steps or rules.
  - Subtle differences in fulfillment or submission arise: submitting a bank transfer may require different fields or succeed asynchronously, while a credit card might authorize instantly.

- **Evolved model (Subtypes):**
  - Define subtypes such as `CreditCardPayment`, `BankTransferPayment`, each *is a type of* `Payment`.
  - Each subtype describes behaviors *only* where they differ — `CreditCardPayment` enforces an online authorization step; `BankTransferPayment` requires reference code validation and may be fulfilled later.
  - Shared behaviors (initiate, submit) stay on the base `Payment`.
  - Now *type* drives both *attached data* and *behavior*.

> When a domain element's *type* alters not only the data needed but also the sequence of steps or the rules followed, it's time to promote from type-property instances to true subtypes with their own behaviors.

#### The delta rule

A subtype carries **only what it adds or overrides**. Inherited responsibilities are not repeated at any level of fidelity — ubiquitous language, CRC, or object model. If the parent owns a responsibility, the subtype block is silent on it.

## Output file

This skill produces **one** standalone file:

```
<deliverables-folder>/[<name>-]ubiquitous-language.md
```

**File name:** Default to `ubiquitous-language.md`. Add a `<name>-` prefix for disambiguation — multiple products in the same workspace, or when the user asks. For multi-module engagements with `abd-module-partition` output, use the module name as the prefix: `<deliverables-folder>/modules/<module-name>-ubiquitous-language.md`.

**Multi-module scope in one file:** When the scope spans more than one module and the user wants a single combined file, organize the output with `# Module: [ModuleName]` sections. Each module section carries its own `**Terms**`, `**Key Abstractions (term grouping)**`, `# Core Domain`, and `# Boundary Domain` content. The file header summarizes the overall scope.

**Resolving `<deliverables-folder>`** — pick in this order:

1. The path the user told you to use.
2. Where the engagement already keeps deliverables.
3. The workspace root.

Do not assume a predetermined folder name. Existing engagement convention wins.

---

## Consistent shape

```
# Module: [ScopeName]           ← omit if single-scope; include per-module for multi-module

**Terms**:
- **KAName**
  - **ka_term** — short plain-English definition
  - **subordinate_term** — short plain-English definition
- **AnotherKAName**
  - **another_term** — short plain-English definition

---

{{Analytical overview paragraph(s) — end-to-end domain mechanic with *italicized domain terms*.}}

---

# Core Domain

## KAName                                       ← h2, no bold

KAName is [definition as term — role, boundary, responsibilities,
relationships, invariants woven naturally. This paragraph IS the
term definition for the KA.]

### ka_name_as_a_concept                        ← MUST appear first; matches the KA
- verb-led behavior with *italicized domain terms*
- **Invariant:** rule that must always hold

### another_concept
- verb-led behavior with *italicized domain terms*

### SubtypeName *is a type of* BaseName
- delta behavior — only what the subtype adds

### property_term
- is a property of *parent_concept* — brief classification note

### Decisions made                              ← ONE per KA, after ALL concept blocks
- independence test result, scope-fit test result, typing call, or open question

### References                                  ← ONE per KA, after Decisions made
**Ref — title**
Source: ...
Locator: ...
Extract: whole

---                                             ← separator between KAs

# Boundary Domain

## boundary_concept

Owned by: ModuleName

- verb-led behavior with *italicized domain terms*

### Decisions made
- boundary placement reasoning

### References
**Ref — title**
Source: ...

---
```

---

## Build

1. **Read all source.** Read every source file the user names or the engagement makes available — rules documents, transcripts, design notes, prior deliverables. If a `<name>-module-partition.md` exists, use its term list and Refs as the starting set.

2. **Step 1 — Extract and list terms.** Walk the source and identify every named concept that has behavior, rules, interactions, or distinct identity. Write the **Terms** list in the file header as a single hierarchical list: KA names as top-level bullets, their terms indented beneath with short plain-English definitions. No source paths in the Terms list.

3. **Step 1 — Apply the independence and scope-fit tests** to every candidate. Record the outcome for each: keep under a KA, move to boundary (name the owning module), or move out (name the destination). The outcomes land in the Terms list and later in `### Decisions made`.

4. **Step 2 — Group kept terms into Key Abstractions.** Name each KA from the source's own vocabulary. A typical module has three to eight KAs. The grouping is already visible in the **Terms** list — KA names are the top-level bullets, terms are indented beneath them.

5. **Step 2 — Write the KA intro paragraph for each KA.** Open with "*KAName* is …" and weave together role, boundary, responsibilities, relationships, and invariants. This paragraph is the KA's own term definition — do not add a separate `### ka_name` definition block on top of the concept.

6. **Step 3 — Write the KA's own concept block first** under `## KAName`. Use `### ka_name` (no bold) with verb-led behavior bullets and `**Invariant:**` lines. Italicize every domain term in bullets and invariants.

7. **Step 3 — Write each subordinate concept block** in the same flat shape: `### concept_name` (no bold), verb-led behavior bullets with *italicized domain terms*, optional `**Invariant:**` lines. Use `### SubtypeName *is a type of* BaseName` for specializations (delta behavior only). Use a stub heading with a one-line classification note for property, instance, or type-property terms.

8. **Apply the active-verb test** to every behavior bullet: the hidden subject ("a *concept*") should naturally start the sentence with an active verb. If a bullet hides something with its own distinct structure, interactions, or result-flow, extract it as its own `### concept` heading.

9. **Write ONE `### Decisions made` per KA**, after all its concept blocks. Gather all typing calls, independence test results, scope-fit test results, and open questions for the KA here.

10. **Write ONE `### References` per KA**, immediately after `### Decisions made`. List every source passage that supports any concept in the KA.

11. **Write boundary entries** under `# Boundary Domain` as `## boundary_concept` with `Owned by: ModuleName`, verb-led bullets, then `### Decisions made` and `### References`.

12. **For multi-module scope in one file**, wrap each module's content in a `# Module: [ModuleName]` section with its own Terms list, KA grouping header, Core Domain, and Boundary Domain.

13. **Set the state marker** to `state: ubiquitous-language` in the file's YAML front matter.

14. **Write the file** to `<deliverables-folder>/[<name>-]ubiquitous-language.md` following `templates/ubiquitous-language-template.md`.

---

## Validate

- **One file.** Named `[<name>-]ubiquitous-language.md`. No separate domain-language, key-abstractions, or ubiquitous-language files alongside it.
- **State marker.** Front matter reads `state: ubiquitous-language`.
- **Terms list in header.** A single hierarchical `**Terms**` list — KA names as top-level bullets, their terms indented with short plain-English definitions. No source references in this list.
- **Every KA has an intro paragraph.** Opens with "*KAName* is …" — this is the term definition for the KA.
- **Every KA's own concept appears first.** The first `### concept` under each `## KA` heading matches the KA name, with verb-led behavior bullets.
- **Every concept has at least one verb-led behavior bullet.** Active voice; the concept itself is the subject.
- **Domain terms italicized.** Every domain term in behavior bullets, invariants, and KA intro paragraphs is *italicized*; non-domain words stay plain.
- **No bold on headings.** `## KAName`, `### concept`, and subtype headings carry no bold.
- **One `### Decisions made` per KA, after all concept blocks.** Not per concept. Covers all independence tests, scope-fit tests, and typing calls for that KA.
- **One `### References` per KA, after `### Decisions made`.** Covers all source passages for that KA.
- **`---` separators between KAs.** A horizontal rule after each KA's `### References` block.
- **Boundary entries have a single named owner.** Every entry under `# Boundary Domain` carries `Owned by: ModuleName` naming exactly one module.
- **Property and instance stubs visible.** Terms classified as properties, instances, or type properties have a stub heading with a classification bullet — nothing is silently dropped.
- **No premature design commitments.** No UML stereotypes, typed properties, method signatures, cardinality notation, `Shape hint:` or `Tension:` labels.
- **Multi-module files have `# Module:` sections.** When the scope spans multiple modules in one file, each module has its own `# Module: [Name]` section with its own header and body content.
