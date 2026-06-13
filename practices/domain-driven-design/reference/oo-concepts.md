# Object-Oriented Concepts

Shared reference for all abd-domain-driven-design skills. This file owns the OO theory. Each skill owns its own notation and format.

---

## What is a class

> **Applies from: domain-language stage and beyond (domain-language → CRC → class-model).**

A class is a named domain idea that earns its own identity because it has at least one of: **distinct identity**, **state**, **behavior**, **structure**, or **interactions** that cannot be collapsed into a property, instance, or type property of something else.

A class knows things (**state**) and does things (**behavior**). Those two dimensions — together with the relationships it maintains and the invariants that constrain it — are what a class IS at every level of fidelity. The notation changes across the pipeline; this definition does not.

A term that is only a data value on another class is a **property**. A term that varies only by label across identical behavior is a **type property**. A term that is one concrete member of a known set is an **instance**. A term that adds distinct behavior to a base is a **subtype**. Only when none of those fit does something deserve its own class.

Each skill records a class in its own form:
- **domain-language** — a named concept block with intent, behaviors, and collaborations in plain English.
- **CRC** — a `#### **ClassName**` block with responsibility and collaborator columns.
- **class-model** — a typed class block with properties, operation signatures, relationships, and invariants.

---

## Decomposing responsibilities

> **Applies from: CRC stage and beyond (CRC → class-model → ...).** Do not use this section at domain-language level — there are no typed properties or operations at that stage.

A responsibility is either something a class **holds** (state) or something it **does** (behaviour) — or both. Classify each responsibility before deciding how to represent it:

- **Property** — the class must remember something across calls. Named as a **noun phrase**: *remaining budget*, *active status*, *target character*.
- **Operation** — the class must perform an action or compute a result; it may be entirely stateless. Named as a **verb phrase**: *calculate shipping cost*, *apply condition*, *resolve check*.
- **Both** — the class holds state **and** exposes an action that works with it.

Never assume every responsibility implies a property, and never assume every responsibility implies an operation. Ask for each one: *hold something, do something, or both?*

---

## Relationships

> **Applies from: CRC stage and beyond (CRC → class-model).** At domain-language level, dependencies are captured as plain-English collaboration sentences only — no formal relationship modeling.

A relationship describes how two domain classes depend on each other. Before recording a relationship, answer three questions:

1. **Does one class own the other's lifecycle?** — The other cannot exist without the first. If the owning class is gone, so is the owned one.
2. **Does one class exist to collect or group the other?** — The collecting class has no meaningful identity without its members. Remove all members and the collector is empty of purpose.
3. **Are both sides independent?** — Each can exist and be meaningful without the other.

These questions determine the nature of the dependency. Each skill records the answer in its own notation — plain-English collaborations at domain-language level, named collaborators at CRC level, typed flavors with cardinality at class-model level.

A relationship also has **direction**: the class that depends on, uses, or navigates to the other is the navigating end. Be explicit about which side initiates the dependency.

---

## Inheritance and subtypes

> **Applies from: domain-language stage and beyond (domain-language → CRC → class-model).**

### Base class and subtype

A **base class** (also called a parent or superclass) defines the common identity, state, and behavior shared by a family of related things. It owns everything that is true of every member of that family — the responsibilities, rules, and collaborations that do not change regardless of which specific variant you are dealing with.

A **subtype** (also called a child class or subclass) is a specialisation of the base. It *is a kind of* the base — everything the base defines applies to it — but it adds or overrides behavior that is specific to it alone. The subtype does not restate what it inherits; it only describes the delta.

**Inheritance** is the mechanism that connects them. The subtype inherits all of the base's identity and behavior automatically. The base never knows about its subtypes; the subtypes always know about their base.

A family can have many subtypes, each specialising the base in a different direction. Subtypes can themselves be bases for further subtypes — but depth should reflect real behavioral distinctions in the domain, not structural tidiness.

### Liskov Substitution rule

**Anywhere the base is used, a subtype must work correctly in its place.** If swapping in a subtype breaks or weakens a rule the base guarantees, the subtype is not a true specialisation — it is a different thing that happens to share some behavior.

In practice: a subtype may *add* behavior and *strengthen* constraints, but it must never *remove* behavior or *weaken* a guarantee the base makes. If you find yourself writing a subtype that overrides a base operation to do nothing, throw an error, or return a narrower result than the base promises, stop — that is a modeling error, not a subtype.

### When to use a subtype, type property, or instance

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

### The delta rule

A subtype carries **only what it adds or overrides**. Inherited responsibilities are not repeated at any level of fidelity — domain-language, CRC, or Class Model. If the parent owns a responsibility, the subtype block is silent on it.

---

### Surfacing the typing choice

When a concept or class plausibly fits more than one typing approach — type field, inheritance, or instance — **surface the choice to the user** before committing. Present the viable options with a recommendation and brief reasoning, ask the user to choose, and record the decision and any rationale they provide. Do not silently pick an approach.

**When to surface:** Any time a concept has varying "kinds" and more than one of the three approaches below could fit.

**Three approaches — quick reference:**

| Approach | Use when | Example |
|----------|----------|---------|
| **Type field (constrained list)** | The kinds differ **only by label** — behavior and properties are identical across all variants. The type is a property drawn from a known set. | *Payment* has a `payment_type` field: `[ach, wire, check]`. All payments initiate, submit, and settle identically; the type is a tag, not a behavioral distinction. |
| **Inheritance** | The kinds are **substitutable** for the base but each adds **distinct behavior or properties** of its own. Liskov must hold — swap any subtype in where the base is expected and nothing breaks. | *ACH payment* and *Wire payment* are each *is a type of* *payment* — they share submission and review, but *wire* carries Fedwire-specific states and *ACH* produces a *NACHA file*. |
| **Instance** | The concept is worth naming because of its **surrounding invariants or behavior context**, but it is just a **specific data value** of the parent class — no separate class or type field needed. | *Kid* is a *Person* with `age < 14`. Worth naming because rules depend on it (cannot view R-rated content), but modeled as a constrained instance of *Person*, not a subtype. |

**How to surface the choice:**

Use `AskQuestion` to present the viable options. Mark the recommended option and **include your reasoning for that specific concept** — not just the general rule, but why the evidence you can see points to that choice. The user may disagree; the reasoning lets them push back on the right thing.

Example prompt structure:

> *Payment has multiple variants (ACH, Wire). Which modeling approach fits best?*
> - **Inheritance** — define *ACH payment*, *Wire payment* each *is a type of* *payment* *(Recommended — ACH and Wire already have distinct submission steps, state machines, and required fields in the source material; those differences will need to be modeled separately)*
> - **Type field** — add a `payment_type` constrained list to *Payment*; use if all variants turn out to behave identically
> - **Instance** — variants are specific data values of *Payment*; no new class or type field needed

After the user chooses, give them space to provide their rationale:

> *Is there anything specific about [concept] that influenced your choice — for example, known behavior differences, domain language your stakeholders use, or constraints you are aware of?*

Record both the choice and the rationale in `#### Decisions made` alongside the concept.

**Carrying rationale forward.** Later-stage skills — domain-model, domain-specification — inherit the same typing decision and rationale unless modeling work uncovers new information (for example, a type-field concept develops distinct behavior at class-model stage). When that happens, note the new evidence and resurface the choice rather than silently overriding the earlier call. A later-stage skill may inform a new typing decision using the same rationale — if the user said "variants feel different but we don't know how yet," that context is evidence at domain-model stage to reassess.
