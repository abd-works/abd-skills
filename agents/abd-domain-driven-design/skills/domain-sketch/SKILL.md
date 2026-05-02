---
name: domain-sketch
description: >-
  Enrich a module file with structured, plain-English concept blocks so the team
  has a readable object model before committing to classes.
---
# domain-sketch

## Purpose

The purpose of this skill is to create a robust domain model that describes domain concepts in a structured, plain-English form — before anyone commits to classes, methods, or properties. The skill applies object-oriented analysis to the source material, producing a **concept** for every domain idea that has distinct identity, state, behavior, structure, or interactions. Each concept spells out what it **is for**, what it **does**, and who it **works with**, grounded in evidence from the real source so a business reader can challenge it and a modeler can build from it. By the time the team finishes the model, every important idea in the module has a name, an intent, traceable behaviors, explicit collaborations, and clear boundary relationships — organized well enough to drive responsibility assignment and scenario walks downstream.

## When to use

- The user asks to sketch concepts, build an object model, or identify domain objects.
- A module file exists at **`state: key-abstractions`** and needs the next enrichment pass.
- The user provides raw source context (documents, notes, specs) and wants concepts identified from scratch.
- Downstream work (e.g. CRC) needs defined concepts to assign responsibilities to.
- The team wants a structured but readable inventory of domain ideas before committing to technical design.

## Core concepts

### Domain logic

Domain logic is a set of short prose bullets that the team extracts from the source context. The bullets describe how the business actually behaves: its rules, interactions, constraints, and state transitions. Each bullet is one testable observation a non-technical person can validate against the real source material. Domain logic is **not** implementation design — it captures what the business enforces, not how code will enforce it.

Good domain-logic bullets ground themselves in the source ("where did that come from?"), stay specific enough to test, and cover behavior and interactions — not only hard constraints.

### Concept

A **concept** is a named domain idea the team treats as a candidate object: something the business talks about that has its own purpose, its own behavior, and relationships with other concepts. A concept is **not** a class — it is the plain-English precursor to one. Each concept block answers four questions:

1. **Role** — What is it for? Who does it cooperate with? (One paragraph, no subheading.)
2. **Behaviors** — What does it do? (Short, verb-led lines describing actions and rules it is responsible for.)
3. **Collaborations** — Who does it depend on or work with? (Other concepts it leans on or connects to, in prose.)
4. **Decisions made** — The judgment calls behind this concept that a reviewer or domain expert should be able to challenge.

Every concept also carries **Core terms** (vocabulary that belongs with it) and `**Ref —**` entries (evidence from the source so anyone can trace a concept back to where it came from).

### Modeling each term: concept, subtype, property, instance, or invariant

Not every domain term deserves its own `### Concept` heading. Before classifying any term, **read the source material for that term** and do proper object-oriented analysis on what the source actually says. Surface similarity is not enough — verify whether terms actually differ in behavior, identity, state, or structure.

A term becomes a **concept** when it has **distinct identity**, **state**, **behavior**, **structure**, or **interactions** — not just when it appears frequently. A term that is a **specialized version** of another concept and adds **different behavior** is a **subtype**. A term that differs from its siblings only by **data values** (not behavior) is an **instance** or **type property** on the parent concept. A term that is a **value, slot, or attribute** another concept carries is a **property** of that concept. A term that describes a **rule that must always hold** is an **invariant** on the concept it constrains. A term that connects two concepts is a **relationship**.

New concepts emerge not only from Key Abstractions but also from their **terms** and the **interactions between those terms**. An output of one concept, an input to one concept, a property, or even a behavior line may turn out to be a first-class concept if it carries its own identity, state, behavior, or interactions. When a behavior bullet describes something with its own distinct structure, its own rules, and its own interactions, it is hiding a concept — extract it.


### Typing: a thing is a kind of other thing

Quick decision guide:
When a term looks like it fals into "a thing is a kind of another thing," three modeling options exist:

**Subtype (*is a type of*)** — the specialized thing adds **behavior the base does not have**. Each subtype does something differently enough that you need to describe it separately. Use this when the distinction changes **what the thing does**, not just what data it carries. Example: an *international shipment* is a type of *shipment* — it introduces customs filing and duty handling that a domestic shipment does not have.

**Type property (constrained list)** — the thing varies by **category**, but every category follows the **same behavior**. The difference is purely which label from a known list applies. Use this when you could swap one label for another and the behavior description would not change. Example: a *notification* has a *notification priority type* drawn from (*low*, *normal*, *urgent*) — every notification still has a recipient, still carries a message, still follows the same delivery and read-receipt rules. The *notification priority type* tells you how soon it surfaces, not how it behaves differently.

**Instance** — the thing is one **concrete member** of a parent concept, distinguished only by its **specific data values**. Many instances exist side by side and they all work the same way — each just carries different numbers or names. Use this when listing them out would produce rows that repeat the same structure with different fill. Example: *bronze*, *silver*, *gold* are all instances of *membership tier* — each names a specific discount rate and benefit set, but they all follow the same upgrade, renewal, and expiry rules that Membership Tier defines.

A common modeling journey begins with treating domain elements as *instances* or *type properties* on a concept, and as understanding of behavior differences grows, moves these into subtypes through inheritance or specialization.

**Example — Evolving a Payment System Domain Model:**

- **Early model (Instances or Type properties):**
  - Model *Payment* as a concept.
  - Each *payment* instance carries data like channel (e.g., "credit card", "bank transfer"), transaction amount, reference id, etc.
  - All payments go through the same core behaviors: *initiate payment*, *set channel*, *approve transaction limit*, and attach required data to the payment instance.

- **Transition point:**
  - As behaviors diverge (e.g., approval workflow or fraud checks differ by channel), notice that some payment types must satisfy additional steps or rules. 
  - Subtle differences in fulfillment or submission arise: submitting a bank transfer may require different fields or succeed asynchronously, while a credit card might authorize instantly.

- **Evolved model (Subtypes / Inheritance):**
  - Define subtypes such as `CreditCardPayment`, `BankTransferPayment`, etc., each *is a type of* `Payment`.
  - Each subtype describes behaviors *only* where they differ. 
    - For example, `CreditCardPayment` enforces an online authorization step, while `BankTransferPayment` may require reference code validation and may be fulfilled later.
  - Shared behaviors (initiate, submit) stay on the base `Payment`, but fulfillment logic, submission differences, and approval steps diverge in the subtypes.
  - Now, *type* drives both *attached data* and *behavior* — shifting the focus from properties on instances to explicit, responsibility-led subtypes.

This approach ensures your model remains DRY and only adds complexity when real business behavior demands it. It surfaces differences organically: what begins as just a *label* on an instance becomes a *distinct concept* once its life cycle or rules can no longer be cleanly unified.

> When you reach the point where a domain element's *type* alters not only the data needed but also the sequence of steps or the rules followed, it's time to refactor from type-property instances to true subtypes with their own behaviors.


### Subtypes

A subtype is one concept **being a type of** another. Write generalizations in plain English (`### International Shipment *is a type of* Shipment`), not in code notation. Keep **shared** behavior and collaborations on the **base** concept; the subtype block adds only what is **extra** — delta behaviors, delta collaborations, its own decisions and refs. This avoids telling the same story twice.

### Roles and actors

A role (gamemaster, administrator, operator, reviewer) **is** a domain object if it has distinct identity, state, or behavior from the system's perspective — apply the same test as any other term. A role that the system tracks, assigns permissions to, or whose actions change domain state is a concept. A role that performs a task outside the system or the UI is a contextual label — note it in Decisions, do not model it as a concept or collaborator. When excluding a role, do not handwave away the mechanics it pointed at — trace what logic, procedures, or interactions the role referenced and ensure those mechanics survive in the model as behaviors on the concepts that actually own them.

### Behaviors and collaborations

**Behaviors** are verb-led short lines describing what a concept does — the domain actions, rules, and state changes it owns. They sit between `----` separators.

**Collaborations** describe who the concept depends on, uses, or relates to — other concepts it leans on. They sit between `-----` separators (one dash longer than behaviors). Prefer prose over machine-style `uses:` notation.

### Decisions made

Every concept and every Key Abstraction carries a **Decisions made** list — the specific judgment calls the modeler had to make. Each decision is a short statement that names the choice and enough reasoning that a domain expert or downstream modeler can challenge it. Decisions include boundary calls ("this concept owns X, not Y"), scope calls ("kept as a term, not promoted"), structural calls ("these two things merged into one concept"), and open questions that the team still needs to resolve.

### Source extracts

Every concept and term carries `**Ref —**` entries that trace its prose back to source: `**Ref — title**` followed by `Source:`, `Locator:`, and `Extract: whole|partial`. Refs are inherited from earlier stages and new ones are added when domain-logic bullets or concept behaviors introduce claims not yet cited. The team must cite every in-scope item.

## The shape of an Object Sketch

```markdown
## Module: [Fulfillment]

*(Prior key-abstractions work — Key Abstractions, term bullets, and Ref entries — stays in the file. Object-sketch adds the sections below; nothing upstream is deleted.)*

## Domain logic

Module-level behaviors that connect the concepts below (summarize or extend what’s already evidenced under Key Abstractions — do not contradict it).

- A shipment may leave the warehouse only after payment has cleared.
- Delivery is confirmed when the carrier posts a terminal scan or the customer signs.

### Shipment Lifecycle

Coordinates whether a shipment is allowed to leave the warehouse and when it is considered delivered. Works with **Payment Clearance** to gate exit, and with **Carrier Events** to interpret scans and signatures.

----
gates warehouse exit until payment clearance is on record
marks the shipment delivered when carrier or customer confirmation is present
-----
depends on Payment Clearance for the all-clear to ship
uses Carrier Events to interpret tracking and proof of delivery
#### Decisions made
- Shipment Lifecycle owns the exit gate and delivery confirmation, not Payment Clearance — payment is a prerequisite, not an orchestrator.
- Customer sign-off vs carrier scan: when they disagree, policy must pick one — this is an open question for the domain expert.

#### Core terms
- clearance
- proof of delivery

**Ref — Gate before ship**
Source: Fulfillment requirements (source context)
Locator: Operations manual 4.1
Extract: partial
Part: Release rule paragraph.

### International Shipment *is a type of* Shipment Lifecycle

Adds customs documentation and duty handling before the same exit and delivery rules apply.

----
collects customs commodity codes for each line
holds duty estimate until the broker accepts
-----
uses Customs Broker to file declarations
depends on Shipment Lifecycle for the same exit and delivery gates
#### Decisions made
- International Shipment is a subtype, not a separate concept — it adds customs paperwork but reuses the same exit and delivery gates from the base.

#### Core terms
- customs declaration
- duty estimate

**Ref — Broker filing**
Source: Fulfillment requirements (source context)
Locator: Customs addendum B
Extract: partial
Part: Duty finalization sentence.
```

## Output file

This skill enriches the growing module file in place at `<workspace>/abd-domain-driven-design/modules/<module-name>.md`. Read it, extend it, write it back to the same path.

**Copy-output mode:** when the user says "copy output," also produce a snapshot at `<workspace>/abd-domain-driven-design/modules/<module-name>-domain-sketch.md`.

## Build

1. **Assess the starting point.** Read the module file. If `state: key-abstractions`, you have `## KA` blocks and `### term` headings to enrich. If working from raw context with no prior modeling, first identify candidate terms and KA groupings using the UL and KA skills, then return here.

2. **Read the source material.** For each `### term`, follow its `#### References` entries and read the source chunks they point to. Understand the term's behavior deeply before writing any bullets.

3. **Add `#### Domain Sketch` under each `### term`.** For each `### term` heading:
   - Optionally open with one sentence describing what the term is for and who it works with (plain prose, no subheading).
   - Write verb-led behavior bullets — each one describing what the term does, enforces, or produces. Use active voice; every bullet should naturally start with a verb the term performs.
   - Add an **Invariant:** bullet for any rule that must always hold.
   - Do NOT repeat what is already in `#### Domain Language` — add new analytical behavior, not a restatement.

4. **Handle subtypes.** Where a term is a specialization of another, add a `### SubtypeName *is a type of* BaseName` heading under the same `## KA` as its base. The subtype `#### Domain Sketch` contains only delta behaviors — what the subtype adds or does differently; shared behavior stays on the base.

5. **Add or extend `#### Decisions made`.** If a `### term` needs modeling decisions recorded, add a `#### Decisions made` section after `#### Domain Sketch`. If `#### Decisions made` already exists (from the KA stage at the `## KA` level), add term-level decisions separately at the `### term` level.

6. **Deduplicate references.** Within each `## KA` block, if the same `**Ref —**` entry appears in more than one `### term`'s `#### References` section, remove the duplicate from the later occurrence. The first term that cites a ref keeps it; later terms in the same KA block drop the duplicate. Add new `**Ref —**` entries to `#### References` for any behavior bullet not yet cited.

7. **Second pass — hidden concepts and boundary clarity.** Re-read every `#### Domain Sketch` block. Apply the active-verb test to each bullet: if the hidden subject ("a *Term*") cannot naturally start the sentence with a verb, the bullet may be hiding a concept that needs its own `### term` heading. Verify every `# Boundary Domain` entry explicitly names what this module defines and what the consuming module enforces.

8. **Set the state marker** to `domain-sketch`.

## Validate

- The module file state marker reads **`state: domain-sketch`**.
- Every `### term` heading in `# Core Domain` has an `#### Domain Sketch` section with at least one verb-led behavior bullet.
- `#### Domain Language` bullets are unchanged from the UDL stage — none removed or reworded.
- Subtypes use the English heading form `### SubtypeName *is a type of* BaseName` under the same `## KA` as their base; subtype `#### Domain Sketch` contains only delta behaviors.
- No `## Domain logic` section — domain logic lives in `#### Domain Sketch` under each `### term`.
- No `----` behavior separators or `-----` collaboration separators — behavior and collaboration are both plain bullets in `#### Domain Sketch`.
- No DDD stereotypes (`<<Entity>>`, `<<Value Object>>`, `<<Service>>`), `Shape hint:` labels, operation signatures, cardinality, or lifecycle tables appear.
- Every in-scope source passage appears as a `**Ref —**` entry in `#### References` under at least one `### term` — no passage is dropped.
- References are deduplicated within each `## KA` block — no identical ref appears in two `### term` sections under the same `## KA`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Boundary concepts are explicit about who defines and who enforces

**Scanner:** AI review

When a concept in this module defines something that another module enforces or consumes, both sides of the relationship must be stated. Passing means every boundary term names who defines, who enforces, and what crosses the boundary. Failing means a boundary term says only "owned by X" without capturing the define/enforce relationship.

#### DO

- State what this module defines and what the consuming module enforces.

  **Example (pass):** "*game modifier* — *conditions* define them (action restrictions, check penalties, defense reductions); enforcement is owned by the consuming module (Combat for action restrictions, this module for check penalties)."

- Name boundary terms in the `#### Boundary terms` section with both sides of the relationship.

  **Example (pass):** "*action round structure* — defined by Combat; consumed by this module when restricting what a conditioned character may do in a round."

#### DO NOT

- Write boundary terms as bare ownership claims with no relationship detail.

  **Example (fail):** "*action round structure* — owned by Combat." — doesn't say what this module sends to Combat or what Combat enforces on behalf of this module.

- Dismiss cross-module mechanics with "another module handles it" and no further detail.

  **Example (fail):** "Condition enforcement is handled elsewhere." — which module? What mechanism? What crosses the boundary?

**Source:** Correction 24 (mm3e-online-holistic engagement).

### Rule: Concept block follows the required structure

**Scanner:** Manual review

Each `### Concept` block (and each subtype block) must follow the prescribed sequence: intent paragraph, `----` behaviors, `-----` collaborations, `#### Decisions made`, `#### Core terms`, `**Ref —**` entries. Passing means every concept follows this order with all required parts. Failing means a concept is missing a required part or has them in the wrong order.

#### DO

- Write an intent paragraph immediately after the concept heading — what it is for, who it cooperates with, two to three sentences, no subheading.

  **Example (pass):**
  ```
  ### Shipment Lifecycle

  Coordinates whether a shipment is allowed to leave the warehouse and when
  it is considered delivered. Works with Payment Clearance to gate exit.
  ```

- Separate behaviors with `----`, collaborations with `-----` (one dash longer).

  **Example (pass):**
  ```
  ----
  gates warehouse exit until payment clearance is on record
  -----
  depends on Payment Clearance for the all-clear to ship
  ```

- Include a `#### Decisions made` section with bullet points listing the judgment calls behind the concept.

  **Example (pass):**
  ```
  #### Decisions made
  - Shipment Lifecycle owns the exit gate, not Payment Clearance — payment is a prerequisite, not an orchestrator.
  - Customer sign-off vs carrier scan disagreement is an open question for the domain expert.
  ```

- End every concept with `#### Core terms` (bullet list) and at least one `**Ref —**` entry.

  **Example (pass):** `#### Core terms` with bullets, then `**Ref — Gate before ship**` with Source/Locator/Extract fields.

#### DO NOT

- Omit the intent paragraph and jump straight to behaviors.

  **Example (fail):** Concept heading followed immediately by `----` with no prose paragraph.

- Use the same separator length for both behaviors and collaborations.

  **Example (fail):** Both behaviors and collaborations separated by `----` — collaborations must use `-----`.

- Skip the `#### Decisions made` section on a concept.

  **Example (fail):** A concept with intent, behaviors, and collaborations but no decisions — the modeling choices are hidden.

- Skip the `**Ref —**` entries on a concept.

  **Example (fail):** A concept with intent, behaviors, and collaborations but no `**Ref —**` entry — uncited concept.

- Use `Shape hint:` or `Tension:` labels instead of `#### Decisions made`.

  **Example (fail):** `Shape hint: orchestration object` or `Tension: customer vs carrier` — these are replaced by Decisions made.

**Source:** Engagement convention (domain-sketch skill).

### Rule: Domain logic section present with testable bullets

**Scanner:** Manual review

After domain-sketch enrichment, the module file must contain a `## Domain logic` section with at least one prose bullet. Each bullet is a testable observation about business behavior, rules, interactions, or constraints — grounded in the source. Passing means the section exists with real bullets. Failing means the section is missing or contains only headings with no content.

#### DO

- Include a `## Domain logic` section with short prose bullets describing business behavior.

  **Example (pass):**
  ```
  ## Domain logic

  - A shipment may leave the warehouse only after payment has cleared.
  - Delivery is confirmed when the carrier posts a terminal scan or the customer signs.
  ```

- Write each bullet as a testable observation a non-technical person can validate against the source.

  **Example (pass):** "A check result must equal or exceed the DC to succeed." — concrete, testable.

#### DO NOT

- Omit the `## Domain logic` section entirely.

  **Example (fail):** File jumps from Key Abstractions content directly to `### Concept` blocks with no domain logic section.

- Include domain logic bullets that are implementation design rather than business behavior.

  **Example (fail):** "Use a strategy pattern for check resolution." — implementation, not domain behavior.

**Source:** Engagement convention (domain-sketch skill).

### Rule: Every Key Abstraction accounted for in a concept

**Scanner:** Manual review

After domain-sketch enrichment, every Key Abstraction from the `## Key Abstractions` section must appear in at least one `### Concept` block — either directly, merged with another, split into multiple, or renamed. No Key Abstraction may be silently dropped. Passing means every KA has a traceable concept. Failing means a KA exists in the Key Abstractions section but has no corresponding concept.

#### DO

- Create at least one `### Concept` block for each Key Abstraction.

  **Example (pass):** KA `### Check` becomes `### Check` concept block with intent, behaviors, collaborations.

- When merging or splitting KAs, note the mapping so a reviewer can trace it.

  **Example (pass):** "Combines KA Check and KA Difficulty Class into a single Check concept" noted in the intent paragraph.

#### DO NOT

- Drop a Key Abstraction without creating a concept for it.

  **Example (fail):** `### Trait` exists as a Key Abstraction but no concept block mentions Trait — it simply vanished.

- Create a concept that does not trace back to any Key Abstraction or source material.

  **Example (fail):** A concept block for "Resolution Engine" appears but no KA or source passage supports it.

**Source:** Engagement convention (domain-sketch skill).

### Rule: No hidden concepts in behavior bullets

**Scanner:** AI review

Every behavior bullet must pass the **active-verb test**: the hidden subject ("a *Concept*") naturally starts the sentence with an active verb — "is made using", "produces", "has", "applies". If the bullet describes something with its own distinct structure, its own DC or threshold, its own roles, or its own result-flow, it is hiding a concept that must be extracted. Passing means every bullet describes behavior that belongs to its parent concept. Failing means a bullet smuggles in a separate concept with distinct identity, state, or interactions.

#### DO

- Apply the active-verb test to every behavior bullet: "a *[parent concept]* [verb]…" — does this read naturally?

  **Example (pass):** "is made using the *trait* of a *character*" — a *Check* is made using the trait. Natural.

- Extract hidden concepts when the test fails or the bullet describes distinct structure.

  **Example (pass):** "team helpers each roll the same trait versus difficulty class 10; each helper success grants the leader +2" — this has its own roles (leader, helper), its own DC (always 10), and its own result-flow (modifier on another check). Extracted as `### Team Check *is a type of* Check`.

#### DO NOT

- Leave complex multi-actor behavior as a single bullet on a parent concept.

  **Example (fail):** Team check mechanics crammed into one bullet on Check — hides a subtype with distinct behavior.

- Accept vague statements that hide modeling decisions.

  **Example (fail):** "the system handles condition enforcement" — which system? What module? What mechanism?

**Source:** Corrections 22, 25 (mm3e-online-holistic engagement).

### Rule: No premature design commitments

**Scanner:** Manual review

The module file at `state: domain-sketch` must contain no DDD stereotypes, operation signatures, cardinality notation, lifecycle tables, or structural classification labels. The object sketch is a plain-English domain model — design decisions belong to later skills. Passing means the file stays at the concept level. Failing means design-level notation has leaked in.

#### DO

- Keep concept blocks in plain English — intent paragraphs, prose behaviors, prose collaborations.

  **Example (pass):** "depends on Payment Clearance for the all-clear to ship" — prose collaboration.

- Record modeling choices in `#### Decisions made` as plain-English statements.

  **Example (pass):** "Shipment Lifecycle owns the exit gate, not Payment Clearance — payment is a prerequisite, not an orchestrator."

#### DO NOT

- Add DDD stereotypes like `<<Entity>>`, `<<Value Object>>`, `<<Service>>`, `<<Aggregate>>`.

  **Example (fail):** `### Shipment <<Entity>>` or `<<Aggregate Root>>` anywhere in the sketch.

- Include operation signatures like `release(payment: Payment): void`.

  **Example (fail):** A behavior line includes `checkPayment(orderId: UUID): Boolean`.

- Add cardinality notation like `1..*`, `0..1`, or relationship arrows.

  **Example (fail):** "Shipment 1..* --> LineItem" in a collaboration line.

- Include lifecycle state tables with transition matrices.

  **Example (fail):** A table of states and transitions — that belongs to class-responsibility-collaborator.

- Use `Shape hint:` labels to classify concepts structurally.

  **Example (fail):** `Shape hint: orchestration object` — this is jargon that tells the reader nothing they can't see from the behaviors and collaborations.

**Source:** Engagement convention (domain-sketch skill).

### Rule: Source accounting complete — no uncited passages

**Scanner:** Manual review

Every in-scope source passage must be mentioned as a `**Ref —**` entry at concept level, module level, or in `[Unallocated]` / `[Rejected]`. No source passage may be silently dropped. Passing means a reviewer can trace every source passage to a citation somewhere in the file. Failing means a source passage exists in the referenced context but has no citation.

#### DO

- Cite every in-scope source passage at the most specific level possible — a `**Ref —**` entry under the concept is preferred.

  **Example (pass):** A concept carries `**Ref — Gate before ship**` with `Source:`, `Locator:`, `Extract: partial`, `Part:`.

- When a passage supports the whole module rather than one concept, cite it in the module-level `### Extract` inventory.

  **Example (pass):** `### Extract` bullet: `- Source: Fulfillment requirements | Locator: Policy ch.4 (warehouse gate)`

- When a passage cannot be allocated to any concept, place it in `[Unallocated]` with its own ref.

  **Example (pass):** `## Module: [Unallocated]` with a `**Ref —**` entry for the orphaned passage.

#### DO NOT

- Leave a referenced source passage without any citation in the file.

  **Example (fail):** The module's Key Abstractions reference `chunk_009.md` but no `**Ref —**` entry mentions it.

- Remove `**Ref —**` entries that existed in the Key Abstractions stage.

  **Example (fail):** A `**Ref —**` entry from key-abstractions has no corresponding entry in the object sketch sections.

**Source:** Engagement convention (domain-sketch skill).

### Rule: State marker is domain-sketch

**Scanner:** Manual review

After this skill runs, the module file's YAML front matter must contain `state: domain-sketch`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

#### DO

- Set the front matter to exactly `state: domain-sketch`.

  **Example (pass):**
  ```
  ---
  state: domain-sketch
  ---
  ```

#### DO NOT

- Leave the state at `key-abstractions` (the previous step).

  **Example (fail):**
  ```
  ---
  state: key-abstractions
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.

**Source:** Engagement convention (domain-sketch skill).

### Rule: Subtypes use English heading form with delta only

**Scanner:** Manual review

Subtype concepts must use the English heading form (`### [Subtype] *is a type of* [Base]`), not code notation. Subtype blocks carry only delta behaviors and collaborations — shared behavior stays on the base concept. Passing means every subtype uses the English form and adds only what is new. Failing means a subtype uses code notation or duplicates base behavior.

#### DO

- Use the English heading form with italicized "is a type of."

  **Example (pass):** `### International Shipment *is a type of* Shipment Lifecycle`

- Include only delta behaviors and collaborations — what the subtype adds beyond the base.

  **Example (pass):** Base owns "gates warehouse exit"; subtype adds "collects customs commodity codes" — no repetition.

#### DO NOT

- Use code-style notation for generalization.

  **Example (fail):** `### InternationalShipment : Shipment` or `### InternationalShipment extends Shipment`

- Duplicate base behaviors in the subtype block.

  **Example (fail):** Subtype repeats "gates warehouse exit until payment clearance is on record" — that belongs on the base only.

**Source:** Engagement convention (domain-sketch skill).

### Rule: All typing decisions grounded in source and pass the decision checks

**Scanner:** AI review

Every modeling classification (concept, subtype, type property, instance, property, invariant, relationship, role exclusion) must be grounded in the source material for that specific term. Passing means a reviewer can trace the classification to source evidence. Failing means a term was classified based on surface similarity, assumption, or pattern-matching without reading what the source says about that term's behavior.

#### DO

- Read the source material for a term before classifying it.

  **Example (pass):** Classified *ability*, *defense*, *skill*, *power*, *advantage* as subtypes of *Trait* after reading that each is defined in its own module with distinct behavior — abilities set base scores, defenses derive from abilities and supply resistance DCs, powers have effect ranks and extras.

- Record the classification rationale in `#### Decisions made`.

  **Example (pass):** "Ability, defense, skill, power, advantage are subtypes of Trait with distinct behavior — each is owned by its own module."

#### DO NOT

- Classify based on surface similarity without reading the source.

  **Example (fail):** "They all have ranks, so they're a type property on Trait" — without checking whether abilities, powers, and skills actually behave differently.

- Promote every term to a concept heading without checking whether it has distinct identity, state, behavior, structure, or interactions.

  **Example (fail):** Twenty Key Abstraction terms produce twenty `### Concept` headings — flat inventory, no modeling.

**Source:** Correction 21 (mm3e-online-holistic engagement).
<!-- execute_rules:bundle_rules:end -->
