---
name: class-responsibility-collaborator
catalog_garden_order: 5
description: >-
  For every domain concept: assign responsibilities, name collaborators,
  and declare invariants — all in one structured pass before object-model.
---
# class-responsibility-collaborator

## Purpose

This skill takes domain concepts from a completed Ubiquitous Language and produces a structured CRC model: for each concept, what it is responsible for, who it collaborates with, and what must always remain true. The result is a module file with `### Class Responsibility Collaborator` sections appended after the existing Ubiquitous Language content.

**CRC (Class-Responsibility-Collaborator)** modeling, introduced by Ward Cunningham and Kent Beck, is a lightweight way to explore object-oriented designs. This skill extends the classic technique by requiring explicit property and operation names, inline invariants, and subtype deltas — so the team can reason about ownership and boundaries before writing code.

---

## When to use this skill

- You have a completed Ubiquitous Language with behavior bullets but ownership, boundaries, and invariants are not yet explicit.
- The user asks to "run CRC," "assign responsibilities," or "build the CRC."
- The domain has sufficient complexity that explicit responsibility boundaries and always-true constraints are worth modeling.

---

## Core concepts

For OO fundamentals, read [`content/oo-concepts.md`](../../content/oo-concepts.md) in full before proceeding. The sections below cover only what is specific to the CRC format.

### The CRC block format

Each concept gets one `#### **ConceptName**` block. Responsibilities are listed as rows in a two-column table separated by `|`: the left column names the responsibility, the right column names collaborators.

```markdown
#### **ConceptName**
responsibility name         | Collaborator, Another Collaborator
another responsibility      | Collaborator
                            |   invariant: declarative constraint that must always hold
```

- **Left column** — the responsibility name. Use a **noun phrase** for state (something the concept holds or carries) and a **verb phrase** for behaviour (something the concept does). Use domain language vocabulary from the behavior bullet that inspired it — not bare nouns, not technical terms.
- **Right column** — comma-separated collaborator class names, or a value description in parentheses for primitive/enum values.
- **Invariants** — indented continuation rows `|   invariant:` under the responsibility they constrain.
- **`|` separators** — align consistently within each block.

### Subtypes

Subtypes use `#### **ConceptName : BaseConcept**` on the heading line. The block lists **only delta responsibilities** — what the subtype adds or overrides. Inherited responsibilities are not repeated — see `## Inheritance and subtypes` in `oo-concepts.md` for the delta rule.

```markdown
#### **ConceptName : BaseConcept**
added responsibility        | Collaborator
                            |   invariant: constraint specific to this subtype
```

### Value objects and state-carrier classes

When applying a concept to an entity requires state that is unique from the concept itself, introduce a separate **state-carrier class** — do not add that state to the concept or to the entity.

- **`Condition`** is a value object: its values are *dazed*, *stunned*, etc. It holds the label, modifier, and supersession relationships that are the same for every character.
- **`Imposed Condition`** is a state-carrier class: it manages the state required to impose a condition on a specific character — active/inactive status, suppressing condition, source. That state does not belong on `Condition` and should not be held on `Character`.

Use the word *instance* only for values of a value object (e.g. *dazed* is an instance of `Condition`). Never use *instance* as a synonym for a separate state-carrier class.

### Collection classes

When a concept owns multiple related objects **and** the collection has unique behavior beyond holding them — such as supersession logic, end-of-turn checks, or add/remove rules — introduce a named collection class that owns that behavior.

```markdown
#### **Imposed Conditions**
applied conditions          | Imposed Condition
apply new condition         | Condition Source, Condition, Imposed Condition
                            |   invariant: same-source more-severe — remove lesser
                            |   invariant: different-source more-severe — park lesser as inactive
```

### Collaborators

Collaborators are the other domain classes a concept works with to fulfil a responsibility — the CRC-level record of the relationships described in `oo-concepts.md` (`## Relationships`). List every class that participates in making the responsibility work. Do not leave implied actors unnamed — if a behavior implies a chain of actors, every actor must appear as a collaborator on some responsibility.

A concept is **not** responsible for receiving an action directed at it. The receiver of an operation does not need a responsibility to be acted upon. The actor that performs the action owns the responsibility. Example: a `Power Effect` does not resist itself — a `Character` (via its traits) makes the resistance check. The effect may declare *what* is used to resist it (`resistance trait`), but it does not own the act of resisting.

### Invariants

An **invariant** is a short declarative constraint — phrased as a statement of what must always be true — placed inline under the responsibility it constrains using `|   invariant:`. Invariants are not procedures; they describe constraints, not steps.

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

A subtype carries **only what it adds or overrides**. Inherited responsibilities are not repeated at any level of fidelity — ubiquitous-language, CRC, or object model. If the parent owns a responsibility, the subtype block is silent on it.

## Output file

This skill produces a **standalone, self-contained file** at:

```
<deliverables-folder>/[<name>-]crc.md
```

**File name:** Default to `crc.md`. Add a `<name>-` engagement prefix only when you need disambiguation — multiple products living in the same workspace, or the user asks for it explicitly. Both `crc.md` and `<name>-crc.md` are valid. For multi-module engagements (with `abd-module-partition` output), the module name is the disambiguator: `<deliverables-folder>/modules/<module-name>-crc.md`.

**Resolving `<deliverables-folder>`** — pick in this order:

1. **The path the user told you to use.** If the user names a file or folder, use exactly that.
2. **Where the engagement already keeps deliverables.** Look at the workspace; if previous phase output already lives in a folder, write next to it.
3. **The workspace root.** If neither applies, write to the workspace root.

Do **not** assume a predetermined folder name like `domain/`. The only DDD/story skill that creates a sub-folder is **`abd-module-partition`**.

The file is **not** an in-place enrichment of the ubiquitous-language file. It is a fresh artifact in the same flat heading shape every other DDD phase skill uses.

---

## Consistent shape (used by every DDD phase skill)

```
## **{{KAName}}**

[Optional 1–2 sentence intro]

### **{{ka_name as a Class}}**             ← MUST appear first; matches the KA
property name              | Collaborator
operation name             | Collaborator
                           |   invariant: rule that must always hold

### **{{another Class}}**
property name              | Collaborator
operation name             | Collaborator, Collaborator

### **{{SubtypeName}} : {{BaseClass}}**
delta responsibility       | Collaborator

### references                              ← one per KA, peer to classes
**Ref — title**
Source: ...
Locator: ...
Extract: whole

```source
verbatim
```

### decisions made                          ← one per KA, peer to classes
- decision rationale
```

The Boundary Domain is one flat section — all boundary classes share a single `# Boundary Domain` group with one `### references` and one `### decisions made` at the bottom.

---

## Build

1. **Read the prerequisite file.** Read `<deliverables-folder>/<name>-ubiquitous-language.md`. Every behavior bullet on a concept is a candidate responsibility. Each `### **concept**` seeds one CRC class block.
2. **Resolve slash terms.** Any concept named `A / B` in the Ubiquitous Language must be resolved to one canonical name before writing CRC class blocks.
3. **Identify state-carrier needs.** For each concept, ask: does applying this concept to an entity require state unique from the concept? If yes, introduce a state-carrier class.
4. **Identify collection class needs.** For each entity that holds multiple related objects, ask: does managing that collection require unique behavior? If yes, introduce a collection class.
5. **Write the CRC class blocks.** Under `# Core Domain`, for each KA from the ubiquitous-language file:
   - `## **KAName**` heading.
   - `### **ka_name_as_a_class**` — the KA's own class, listed FIRST, with its responsibility table.
   - `### **another Class**` for each grouped concept, with its responsibility table. Subtypes use `### **ConceptName : BaseConcept**` and carry only deltas.
   - `### references` listing all Refs for classes in this KA, with fenced ```source``` blocks.
   - `### decisions made` listing CRC-level judgments (slash-term resolutions, state-carrier introductions, collection-class introductions, Liskov decisions, dependency-magnet splits).
6. **Trace every behavior to a responsibility.** Each behavior bullet in the Ubiquitous Language must map to at least one responsibility (property or operation) in the CRC. If a bullet is missing coverage, add the responsibility or note the gap in `### decisions made`.
7. **Verify explicit chains.** For every responsibility that implies multiple actors or steps, confirm every implied actor appears as a collaborator on some responsibility. Nothing nebulous.
8. **Set the state marker** to `crc`.
9. **Write the file** to `<deliverables-folder>/<name>-crc.md`. Follow the template in `templates/crc-outline-template.md`.
10. **Write `domain.json`** to `<deliverables-folder>/domain.json`. For every class block, add one entry whose key is the class name and whose `attributes` array lists every noun-phrase responsibility (left-column state rows — things the concept *holds* — not verb-phrase operations). For subtypes, set `inherits` to the base class name; for root classes set it to `null`. Use the template in `templates/domain.json`. This file is read by the specification-by-example scanner to validate example-table column names.

---

## Validate

1. **Per-phase output file.** The file is named `<name>-crc.md`. No prior or later phase content lives in it.
2. **Every KA has a class that names it.** Every `## **KA**` heading is followed by a `### **Class**` whose name matches the KA itself, listed first, with its responsibility table.
3. **Coverage.** Every concept from the ubiquitous-language file has a corresponding `### **Class**` block.
4. **No sub-headings under classes.** Responsibility tables live directly under each `### **Class**` heading. No `#### Class Responsibility Collaborator`, `#### References`, or `#### Decisions made` sub-sections.
5. **References per KA with verbatim source blocks.** One `### references` per KA, every `**Ref —**` followed by a fenced ```source``` block of verbatim text.
6. **Decisions per KA.** One `### decisions made` per KA listing CRC judgment calls.
7. **No slash terms.** No `A / B` names appear in any CRC heading or block.
8. **Property names.** Every property name is a noun phrase using domain vocabulary — no technical terms (`flag`, `boolean`, `list`, `type` as a bare noun).
9. **Operation names.** Every operation name is a verb phrase.
10. **Vocabulary tight.** Each responsibility name uses vocabulary from the behavior bullet that inspired it.
11. **Subtype deltas only.** Subtype blocks contain only responsibilities that add or override the parent.
12. **Collaborators explicit.** No responsibility with implied actors has an empty or vague collaborator column.
13. **Receiver not responsible.** No concept has a responsibility that amounts to "receive X" or "be acted upon by X."
14. **Invariants indented.** Invariant lines use `|   invariant:` with three spaces after the pipe.
15. **`|` separators aligned.** Column separators are aligned within each block.
16. **State marker.** Front matter reads `state: crc`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Per-phase file with consistent flat shape

**Scanner:** Manual review

The CRC skill writes a self-contained file at `<deliverables-folder>/<name>-crc.md`. It does **not** enrich the prior phase's file in place. The output uses the consistent flat heading shape every DDD phase skill shares: `## **KA** → ### **Class** (with responsibility table directly under) → ### references → ### decisions made`.

#### DO

- Write the file to `<deliverables-folder>/<name>-crc.md`.

  **Example (pass):** `domain/paw-place-crc.md`.

- Place the responsibility table directly under each `### **Class**` heading.

  **Example (pass):**
  ```
  ## **Check**

  ### **Check**
  use trait                  | Trait
  resolve                    | D20, Trait, Difficulty Class, Check Result
                             |   invariant: d20 + trait rank + circumstance modifier >= difficulty class

  ### references
  **Ref —** …

  ### decisions made
  - …
  ```

#### DO NOT

- Add `### Class Responsibility Collaborator` as a sub-section inside the prior phase's file.

  **Example (fail):** Edit `paw-place-ubiquitous-language.md` to insert `### Class Responsibility Collaborator` peers — that is in-place enrichment which produces unrecoverable heading drift.

- Insert intermediate sub-headings between the KA and its classes.

  **Example (fail):**
  ```
  ## **Check**
  ### Class Responsibility Collaborator
  #### **Check**
  ```

**Source:** Engagement convention (DDD phase-skill simplification).

### Rule: Every Key Abstraction has a class that names the KA itself

**Scanner:** AI review

Every `## **KA**` heading must be followed by a `### **Class**` whose name matches the KA itself, listed **first** under the KA, with its full responsibility table. The KA's own class carries the abstraction's behavior, identity, and invariants.

#### DO

- List the KA's own class first under the `## **KA**` heading.

  **Example (pass):**
  ```
  ## **Check**

  ### **Check**                              ← first; matches the KA
  use trait                  | Trait
  resolve                    | D20, Trait, Difficulty Class, Check Result

  ### **Difficulty Class**
  numeric threshold          | (integer 0–40)

  ### **Trait**
  effective rank             | (integer)
  ```

#### DO NOT

- Skip the KA's own class.

  **Example (fail):**
  ```
  ## **Check**

  ### **Difficulty Class**          ← subordinate first; missing ### **Check**
  ```

**Source:** Correction — engagement repo (paw-place); KA's own term must be the most important class modeled.

### Rule: Collaborators trace to sketch collaborations and subtype edges

**Scanner:** Manual review

The collaborator column in each CRC block must list domain concepts that appear in the Ubiquitous Language's behavior bullets or subtype edges for that concept. No collaborator may be invented. An empty collaborator column must contain a value description in parentheses (for primitives/enums) or be explicitly empty only when the responsibility truly has no collaborating concept.

#### DO

- List collaborators that correspond to concepts named in the behavior bullet.

  **Example (pass):** Sketch says "supersedes a less severe condition from the same source"; CRC has `supersede | Condition`.

- Use a parenthetical value description for primitive/enum collaborators.

  **Example (pass):** `active status | (active or inactive)`

#### DO NOT

- Invent collaborators that have no basis in the Ubiquitous Language.

  **Example (fail):** CRC block lists `Logger, EventBus` but neither concept appears anywhere in the sketch.

- Leave the collaborator column blank without explanation.

  **Example (fail):** `supersede |` with nothing on the right.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Introduce a collection class when the collection has unique behavior

**Scanner:** Manual review

When an entity owns multiple related objects and managing that collection requires unique behavior beyond simple holding — such as supersession logic, sequential processing, end-of-turn checks, or constraint enforcement — introduce a named collection class that owns that behavior.

#### DO

- Introduce a collection class and give it the management responsibilities.

  **Example (pass):** `Imposed Conditions` owns `apply new condition` with supersession invariants. `Character` simply holds `imposed conditions | Imposed Conditions`.

  **Example (pass):** `Ongoing Effects` owns `make resistance check` and `end effect`. `Character` simply holds `ongoing effects | Ongoing Effects`.

#### DO NOT

- Put collection management behavior directly on the entity.

  **Example (fail):** `Character` owns `apply new condition` with all supersession logic — the character class becomes bloated with condition-management concerns.

- Leave collection management implied without a named owner.

  **Example (fail):** Ubiquitous Language says "character tracks ongoing effects" with no named class to own the tracking and end-of-turn check.

- Create a collection class when the collection has no behavior beyond holding.

  **Example:** If `Character` simply holds a list of traits with no management logic, `traits | Trait` on `Character` is sufficient — no `Traits` collection class is needed.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Dependency magnet — split unrelated business concerns

**Scanner:** Manual review

A concept whose responsibilities and collaborators span **multiple unrelated business concerns** (distinct domain areas that do not share a coherent purpose) behaves as a **dependency magnet**: it accumulates collaborators and responsibilities from different "worlds" and becomes hard to change or test. When you see that pattern during CRC, split by moving coherent groups of responsibilities to focused concepts or to appropriate collaborators — before the object model hardens the overload.

#### DO

- Group responsibilities by concern; if a single concept mixes concerns (for example catalog + billing + shipping language on one card), extract or reassign so each concept owns one coherent thread.

  **Example (pass):** `Order` coordinates fulfillment; `Pricing`, `Shipment`, and `Payment` hold their own rules and collaborators instead of every rule living on `Order`.

- Use the collaborator column as a smell: a wide, heterogeneous list (many unrelated domain types with no single behavior story) often signals a magnet.

#### DO NOT

- Leave one concept owning checklist-style responsibilities that read like unrelated stakeholder requests stapled together.

  **Example (fail):** One CRC card owns "calculate tax," "send email," "validate inventory," and "render PDF" with collaborators from messaging, tax, inventory, and document domains — none of which share a natural domain boundary.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: English prose only — no method signatures or typed notation

**Scanner:** Manual review

Responsibility names, collaborator names, and invariants must be written in plain domain language using the property/operation table format. No method signatures, typed parameters, return types, UML notation, cardinality markers, or code-level constructs are permitted anywhere.

#### DO

- Write property names as noun phrases and operation names as verb phrases.

  **Example (pass):** `resolve | D20, Trait, Circumstance Modifier, Difficulty Class, Check Result`

- Write invariants as declarative English statements using `|   invariant:`.

  **Example (pass):** `|   invariant: only active conditions apply modifiers`

- Use parenthetical value descriptions for primitives and enums.

  **Example (pass):** `active status | (active or inactive)`

#### DO NOT

- Include operation signatures with parameters or return types.

  **Example (fail):** `resolve(roll: int, dc: int) -> bool`

- Use typed property declarations.

  **Example (fail):** `stored result: CheckResult`

- Include UML or cardinality notation in collaborators.

  **Example (fail):** `DifficultyClass 1..1, Modifier 0..*`

- Use code-style boolean expressions in invariants.

  **Example (fail):** `invariant: damage >= threshold && !isImmune` — write "damage equals or exceeds the threshold and the character is not immune" instead.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Every Ubiquitous Language behavior has a backing responsibility

**Scanner:** Manual review

Each behavior bullet in the Ubiquitous Language must be traceable to at least one responsibility (property or operation) in the CRC block for the same concept. Behaviors that produce no CRC entry must be explained in the Decisions section.

#### DO

- For every behavior bullet, produce at least one property or operation.

  **Example (pass):** Sketch: "makes checks using its traits" → CRC has `traits | Trait`.

  **Example (pass):** Sketch: "carries imposed conditions via its Imposed Conditions collection" → CRC has `imposed conditions | Imposed Conditions`.

  **Example (pass):** Sketch: "has a difficulty ladder" → CRC has `difficulty ladder | Difficulty Ladder`.

#### DO NOT

- Leave a behavior bullet with no corresponding CRC entry and no decision note.

  **Example (fail):** Sketch says "has exactly one rank" but no property for `effectiveness rank` appears in the CRC block for `Trait`.

- Map a behavior to a responsibility on the wrong concept.

  **Example (fail):** Sketch says `Trait` "has a difficulty ladder" but the `difficulty ladder` property appears on `Check` instead.

#### Note

A responsibility can be either a property (noun phrase) or an operation (verb phrase) — the CRC stage does not require distinguishing between them. What matters is that the behavior has a named responsibility somewhere.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Every concept from Ubiquitous Language has a CRC block

**Scanner:** Manual review

After CRC enrichment, every concept and subtype represented in **`### Ubiquitous Language`** must have a corresponding CRC block in **`### Class Responsibility Collaborator`**. No concept may be silently dropped. Passing means every concept is accounted for. Failing means a concept exists in the Ubiquitous Language but has no CRC block.

#### DO

- Create a CRC block for each `#### **ConceptName**` heading under `### Ubiquitous Language`.

  **Example (pass):** Ubiquitous Language lists `#### **Check**`, `#### **Difficulty Class**`, `#### **Trait`** — CRC section has blocks for `Check`, `Difficulty Class`, and `Trait`.

- Create a CRC block for each subtype the sketch records (however phrased — e.g. bullets or wording that establishes *is a type of* / specialization), using `#### **ChildConcept : ParentConcept**` in the CRC section.

  **Example (pass):** Ubiquitous Language establishes that Saving Throw is a kind of Check — CRC has `#### **Saving Throw : Check**` with delta responsibilities only.

#### DO NOT

- Drop a concept without creating a CRC block for it.

  **Example (fail):** `#### **Trait**` appears under `### Ubiquitous Language` but no CRC block addresses `Trait`.

- Introduce a CRC block that has no corresponding concept in the Ubiquitous Language.

  **Example (fail):** A CRC block for `Resolution Engine` appears but no concept in the Ubiquitous Language supports it.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Explicit chain of responsibility — no nebulous behaviors

**Scanner:** Manual review

When a behavior implies a chain of actors or steps, every actor in that chain must be traceable to a property or operation with explicit collaborators in the CRC. Nothing may be left implied or nebulous. "May" and "requires" language in a behavior must be fully modeled.

#### DO

- Trace each step in the implied chain to a named responsibility with collaborators.

  **Example (pass):** Ubiquitous Language behavior: "may be ongoing for a target character: requires a resistance check at the end of each of the target's turns until ended."

  This implies: someone tracks which characters are ongoing targets, and someone triggers end-of-turn resistance checks. The CRC must reflect both:
  ```
  ongoing targets             | Character
  make resistance check       | Character, Check
                              |   invariant: check made at end of each ongoing target's turn
  ```

  **Example (pass):** Ubiquitous Language behavior: "supersedes a less severe condition from the same source — removing the lesser."

  This implies: someone knows the supersession hierarchy, and someone performs the removal. The CRC must reflect both — `supersedes | Condition` on `Condition` and `apply new condition` with the supersession invariant on `Imposed Conditions`.

#### DO NOT

- Write a property and leave the downstream action it implies without an owner.

  **Example (fail):** CRC has `is ongoing | (active or ended)` with no corresponding operation for who tracks ongoing targets or who triggers the end-of-turn check.

- Leave "may" or "requires" language in a behavior with an incomplete CRC chain.

  **Example (fail):** Behavior says "requires a resistance check at end of each turn" but no operation for making that check appears anywhere in the CRC.

- Leave an implied actor out of the collaborator column.

  **Example (fail):** Operation `make resistance check | Check` with no `Character` collaborator — the character is the one making the check.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Introduce a state-carrier class when application requires unique state

**Scanner:** Manual review

When applying a concept to an entity requires state that is unique from the concept itself — state that varies per application, per entity, or over time — introduce a separate state-carrier class. Do not add that state to the original concept or to the entity.

#### DO

- Introduce a state-carrier class when the applied state is distinct from the concept's definition.

  **Example (pass):** `Condition` holds its label, modifier, and supersession relationships — the same for every character. `Imposed Condition` holds the active/inactive status, suppressing condition, and source — state that is unique to each application on a specific character.

- Name the state-carrier after its role in the application.

  **Example (pass):** `Imposed Condition` — describes what it is: a condition that has been imposed. Not `ConditionState` or `AppliedCondition`.

#### DO NOT

- Add per-application state to the value object concept.

  **Example (fail):** Adding `active status` and `suppressing condition` directly to `Condition` — these vary per character and per imposition, not per condition type.

- Add per-concept state to the entity that holds it.

  **Example (fail):** Adding `active status` directly to `Character` — the character may carry many conditions, each with its own status.

#### Vocabulary note

Use the word *instance* only for values of a value object (e.g. *dazed* is an instance/value of `Condition`). Never use *instance* as a synonym for a state-carrier class — a state-carrier is a distinct domain class, not an instance of another.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Invariants present for lifecycle concepts

**Scanner:** Manual review

Every concept that has a populated `lifecycle:` block must also have an `invariants:` field with at least one declarative constraint or an explicit `(none yet)` placeholder. Stateless concepts must have `invariants: (none)` or a value. Passing means every CRC block has an invariants field. Failing means a block with a lifecycle has no invariants field at all.

#### DO

- Add at least one invariant tied to the lifecycle for stateful concepts.

  **Example (pass):**
  ```
  Condition
      ...
      lifecycle:
          states: inactive, active, superseded, resolved
          ...
      invariants:
          - a condition already present in the supersession chain is overridden by the more severe one, never duplicated
          - a combined condition is removed entirely when its source effect ends
  ```

- Use `(none yet)` when the lifecycle is clear but invariants are not yet enumerable.

  **Example (pass):**
  ```
  Check Result
      ...
      lifecycle:
          states: pending, succeeded, failed
          ...
      invariants: (none yet)
  ```

- Use `(none)` for stateless concepts with no always-true constraints.

  **Example (pass):**
  ```
  Difficulty Class
      ...
      lifecycle: (stateless)
      invariants: (none)
  ```

#### DO NOT

- Write a lifecycle block and omit the `invariants:` field entirely.

  **Example (fail):** A CRC block ends after `lifecycle: states: ...` with no `invariants:` line — reader cannot tell whether constraints were considered.

- Duplicate lifecycle transitions as pseudo-invariants.

  **Example (fail):** `invariants: must transition from inactive to active before resolving` — that is a transition rule, not a declarative constraint on what must always be true.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Many-to-many association signals a new first-class concept

**Scanner:** Manual review

When the Ubiquitous Language implies that two concepts each relate to *many* of the other (mutual many-to-many), the association itself usually needs a first-class concept with its own responsibilities — not only reciprocal collaborator lists on the two end cards. The classic signal is two entities pointing at each other with "has many" behavior on both sides (for example student–course enrollment).

#### DO

- Introduce a linking concept that owns the association lifecycle, constraints, and facts that belong to the pairing — not to either end alone.

  **Example (pass):** `Student` enrolls in `Course` and `Course` has many students → add `Course Enrollment` (or domain-equivalent name) that owns enrollment date, status, seat assignment, grades — whatever the domain attaches to *this student in this course*.

- Place responsibilities that concern only the pairing on the new concept; keep the end concepts focused on their own identity and rules.

#### DO NOT

- Model many-to-many only as symmetrical responsibilities on the two ends when the domain language or sketch implies facts and behavior on the link itself.

  **Example (fail):** `Student` lists `courses | Course` and `Course` lists `students | Student` with duplicated enrollment rules split across both cards and no concept for the enrollment fact.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: No technical terms in responsibility names

**Scanner:** Manual review (grammar/vocabulary spot-check)

Responsibility names — both property names and operation names — must use domain language vocabulary. Technical implementation terms are forbidden.

#### Forbidden terms (and their replacements)

- `flag` → use a domain state phrase: `is ongoing`, `is routine`
- `boolean`, `bool` → use the domain state name
- `list`, `array`, `collection` → introduce a named collection class instead
- `type` as a bare noun → use a qualified domain noun
- `status` as a bare noun → qualify it from the behavior: `active status`, `activation status`
- `own` as a prefix → use descriptive qualifiers from the behavior language; `own` conveys nothing

#### DO

- Derive the noun or verb from the behavior bullet that inspired the responsibility.

  **Example (pass):** Behavior says "penalizes a suffering character according to a game modifier" → property is `game modifier`, not `modifier` or `penalty flag`.

  **Example (pass):** Behavior says "may be ongoing for a target character" → property is `is ongoing`, not `ongoing flag` or `ongoing boolean`.

  **Example (pass):** Behavior says "is the power effect and attacker that imposed a condition" → property is `imposing source`, not `source` or `own source`.

#### DO NOT

- Use bare nouns when a qualifier is available from the behavior.

  **Example (fail):** `source | Condition Source` when the behavior says "the imposing source" — use `imposing source`.

- Use technical implementation words.

  **Example (fail):** `ongoing flag | (true or false)`, `condition list | Condition`

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: A concept is not responsible for being acted upon

**Scanner:** Manual review

The receiver of an action does not need a responsibility to receive it. Only the actor that performs the action owns the responsibility. If a behavior describes something happening *to* a concept, identify the acting concept and place the responsibility there.

#### DO

- Place the responsibility on the concept that performs the action.

  **Example (pass):** A character makes a resistance check against a power effect. `Ongoing Effects` (on `Character`) owns `make resistance check for ongoing targets`. `Power Effect` owns `resistance trait` (declaring how it is resisted) — not a `resist` operation.

  **Example (pass):** A condition is applied to a character. `Imposed Conditions` owns `apply new condition`. `Character` does not own `receive condition`.

#### DO NOT

- Give a concept a responsibility that amounts to "be resisted," "be applied to," or "receive X."

  **Example (fail):** `Power Effect` has `resist | Resistance Check` — the effect does not resist itself; the character makes the check.

  **Example (fail):** `Character` has `receive condition | Condition` — the character does not receive; the `Imposed Conditions` collection applies it.

  **Example (fail):** `Condition` has `be imposed | Character` — the condition doesn't impose itself; it is imposed by a `Power Effect` through `Imposed Conditions`.

#### Clarification

A concept *may* have a property that describes what is used to act upon it. This is not the same as a responsibility to be acted upon.

  **Example (pass):** `Power Effect` has `resistance trait | Trait` — this declares which trait a character uses to resist the effect. The effect is not doing the resisting; it is providing the information needed for the character to resist.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Responsibility vocabulary matches inspiring behavior

**Scanner:** Manual review (grammar/vocabulary spot-check)

Each responsibility name must use vocabulary that is tight to the Ubiquitous Language behavior bullet that inspired it. The match need not be word-for-word, but the key domain terms must be recognizable. A reader who sees the responsibility name and the behavior bullet should be able to connect them without explanation.

#### DO

- Use the key noun or verb from the behavior bullet.

  **Example (pass):** Behavior: "carries *imposed conditions* via its *Imposed Conditions* collection" → responsibility: `imposed conditions | Imposed Conditions`.

  **Example (pass):** Behavior: "is removed when its *condition source* ends" → operation: `end | Imposed Conditions`.

  **Example (pass):** Behavior: "penalizes a *suffering character* according to a *game modifier*" → property: `game modifier | (penalty value or restriction description)`.

#### DO NOT

- Use a generic name that could apply to any concept.

  **Example (fail):** Behavior says "enforces penalties and restrictions only when active" but responsibility is named `apply` — too vague; use `enforce | Character, Check`.

- Rename a domain term to a technical synonym or generic substitute.

  **Example (fail):** Behavior says "imposing source" but responsibility is named `origin` or `cause`.

- Use vocabulary from a different concept's behavior.

  **Example (fail):** `Condition` has a responsibility named `roll` — that term comes from `Check`, not from any `Condition` behavior.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Shared responsibility and inheritance require Liskov substitution

**Scanner:** Manual review

When the **same domain responsibility** (same behavioral contract in domain terms, not merely the same English label) appears on multiple concepts, that is a **signal to investigate** shared abstraction — often a base class with subtypes. Inheritance is appropriate **only if the Liskov substitution principle holds**: code written against the base concept must work correctly for **any** subtype without branching on which subtype it is. If a subtype would need to weaken a precondition, strengthen a postcondition, throw in cases the base promises not to, or otherwise change the contract, **inheritance is the wrong tool** — prefer a shared collaborator, a role interface at the point of use, composition, or two parallel concepts.

This rule supplements **Subtype uses child : parent** — it is the gate for *when* to introduce that hierarchy.

#### DO

- Before adding `#### **Child : Parent**`, ask: *Could every responsibility inherited or lifted to the parent be fulfilled by every subtype with the same expectations?*

  **Example (pass):** `StandardCheck` and `OpposedCheck` both "resolve" with the same caller expectations (input concepts, outcome shape); differences are *how* total or DC is formed — delta responsibilities stay on subtypes; shared resolution contract stays on `Check`.

- When contracts genuinely align, extract the common responsibility to the parent and keep only deltas on subtypes.

#### DO NOT

- Introduce a base class because two concepts share a noun in a responsibility name when their rules or collaborations differ incompatibly.

  **Example (fail):** `SavingsAccount` and `TradingAccount` both have "post transaction" but one forbids negative balance and the other allows margin — a single `Account.postTransaction` contract cannot serve both without subtype-specific checks that violate substitutability.

- Use inheritance to deduplicate implementation detail when the domain types are not substitutable for callers.

  **Example (fail):** Base `Bird` with `fly()` and subtype `Penguin : Bird` that cannot fly — same label, incompatible contract; use composition or separate roles instead.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Slash terms resolved before CRC

**Scanner:** Manual review

Any concept named `A / B` in the Ubiquitous Language must be resolved to one canonical name before writing CRC blocks. Slash terms are acceptable in Ubiquitous Language headers as working hedges, but must not appear in CRC headings or responsibility names.

#### DO

- Choose one canonical name and use it consistently throughout the CRC section.

  **Example (pass):** Ubiquitous Language has `#### **Check Result / Graded Check Result**` → CRC uses `#### **Check Result**` throughout; "graded" behavior is expressed via invariants.

- Note the resolution in the Decisions section if the choice is non-obvious.

  **Example (pass):** "Decisions: Check Result / Graded Check Result resolved to Check Result — graded behavior is an invariant, not a separate concept."

#### DO NOT

- Use slash notation in any CRC heading or block.

  **Example (fail):** `#### **Check Result / Graded Check Result**` appears in the CRC section.

- Use one name in the heading and the other in collaborator columns.

  **Example (fail):** Heading is `#### **Check Result**` but collaborator column references `Graded Check Result` elsewhere.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: State marker is crc

**Scanner:** Manual review

After this skill runs, the module file's YAML front matter must contain `state: crc`. Passing means the marker is present and correct. Failing means the marker is missing, still shows a previous state, or has a typo.

#### DO

- Set the front matter to exactly `state: crc`.

  **Example (pass):**
  ```
  ---
  state: crc
  ---
  ```

#### DO NOT

- Leave the state at `ubiquitous-language` (the previous step).

  **Example (fail):**
  ```
  ---
  state: ubiquitous-language
  ---
  ```

- Omit the front matter entirely.

  **Example (fail):** File starts with `## Module:` and has no YAML front matter.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Stateful concepts have lifecycle blocks

**Scanner:** Manual review

Every concept whose responsibilities or sketch behaviors imply state changes, threshold ladders, supersession, or spend/recover must have either a populated `lifecycle:` block or `lifecycle: (stateless)`. Passing means no concept with state-shaped mechanics is left without coverage. Failing means a concept's mechanics imply state but its CRC block has no lifecycle field.

#### DO

- Add a populated lifecycle block for concepts with state-shaped mechanics.

  **Example (pass):**
  ```
  Condition
      ...
      lifecycle:
          states: inactive, active, superseded, resolved
          transitions: inactive → active (source effect imposed), active → resolved (source effect ends)
          illegal: resolved → active (cannot re-activate from same source without new imposition)
          terminal: resolved
  ```

- Write `lifecycle: (stateless)` for concepts that appear in CRC but own no state changes.

  **Example (pass):**
  ```
  Difficulty Class
      responsible: holds the numeric threshold an action must meet or exceed to succeed
      ...
      lifecycle: (stateless)
  ```

#### DO NOT

- Omit the `lifecycle:` field entirely.

  **Example (fail):** A CRC block for `Condition` ends after `collaborators:` with no `lifecycle:` line — reader cannot tell whether lifecycle was considered.

- Assume a concept is stateless without checking its sketch behavior bullets.

  **Example (fail):** `Condition` has sketch behaviors "applied, superseded, resolved" but is given `lifecycle: (stateless)` without any reasoning.

**Source:** Engagement convention (class-responsibility-collaborator skill).

### Rule: Subtypes use ConceptName : BaseConcept on the heading line

**Scanner:** Manual review

When a concept is a specialization of another, its CRC heading must use `#### **ConceptName : BaseConcept**` notation. The block states only delta responsibilities — what the subtype adds or overrides beyond the base. Passing means subtypes are correctly notated and carry only deltas. Failing means subtypes use the wrong format or duplicate base responsibilities.

#### DO

- Use `#### **ConceptName : BaseConcept**` on the heading line for subtypes.

  **Example (pass):**
  ```
  #### **Opposed Check : Check**
  use opposing trait          | Trait
                              |   invariant: both sides resolve as standard Checks; higher result wins
  ```

- State only delta responsibilities that the subtype adds or overrides beyond the parent.

  **Example (pass):** Parent `Check` owns `resolve`; subtype `Opposed Check : Check` adds only `use opposing trait` and its invariants.

#### DO NOT

- Use the Ubiquitous Language English heading form in CRC headings.

  **Example (fail):** `#### **Opposed Check** *(is a type of Check)*` — CRC uses `: BaseConcept` in the heading, not the sketch's English form.

- Use code-style inheritance syntax.

  **Example (fail):** `OpposedCheck extends Check`

- Duplicate base responsibilities in the subtype block.

  **Example (fail):** Subtype repeats `use trait`, `use difficulty class`, `apply circumstance` — those are identical to the parent `Check` and must not be restated.

**Source:** Engagement convention (class-responsibility-collaborator skill).
<!-- execute_rules:bundle_rules:end -->
