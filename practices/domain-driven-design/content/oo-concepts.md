# Object-Oriented Concepts

Shared reference for all abd-domain-driven-design skills. This file owns the OO theory. Each skill owns its own notation and format.

---

## What is a class

> **Applies from: ubiquitous-language stage and beyond (ubiquitous-language → CRC → object-model).**

A class is a named domain idea that earns its own identity because it has at least one of: **distinct identity**, **state**, **behavior**, **structure**, or **interactions** that cannot be collapsed into a property, instance, or type property of something else.

A class knows things (**state**) and does things (**behavior**). Those two dimensions — together with the relationships it maintains and the invariants that constrain it — are what a class IS at every level of fidelity. The notation changes across the pipeline; this definition does not.

A term that is only a data value on another class is a **property**. A term that varies only by label across identical behavior is a **type property**. A term that is one concrete member of a known set is an **instance**. A term that adds distinct behavior to a base is a **subtype**. Only when none of those fit does something deserve its own class.

Each skill records a class in its own form:
- **ubiquitous-language** — a named concept block with intent, behaviors, and collaborations in plain English.
- **CRC** — a `#### **ClassName**` block with responsibility and collaborator columns.
- **Object-model** — a typed class block with properties, operation signatures, relationships, and invariants.

---

## Decomposing responsibilities

> **Applies from: CRC stage and beyond (CRC → object-model → ...).** Do not use this section at ubiquitous-language level — there are no typed properties or operations at that stage.

A responsibility is either something a class **holds** (state) or something it **does** (behaviour) — or both. Classify each responsibility before deciding how to represent it:

- **Property** — the class must remember something across calls. Named as a **noun phrase**: *remaining budget*, *active status*, *target character*.
- **Operation** — the class must perform an action or compute a result; it may be entirely stateless. Named as a **verb phrase**: *calculate shipping cost*, *apply condition*, *resolve check*.
- **Both** — the class holds state **and** exposes an action that works with it.

Never assume every responsibility implies a property, and never assume every responsibility implies an operation. Ask for each one: *hold something, do something, or both?*

---

## Relationships

> **Applies from: CRC stage and beyond (CRC → object-model).** At ubiquitous-language level, dependencies are captured as plain-English collaboration sentences only — no formal relationship modeling.

A relationship describes how two domain classes depend on each other. Before recording a relationship, answer three questions:

1. **Does one class own the other's lifecycle?** — The other cannot exist without the first. If the owning class is gone, so is the owned one.
2. **Does one class exist to collect or group the other?** — The collecting class has no meaningful identity without its members. Remove all members and the collector is empty of purpose.
3. **Are both sides independent?** — Each can exist and be meaningful without the other.

These questions determine the nature of the dependency. Each skill records the answer in its own notation — plain-English collaborations at ubiquitous-language level, named collaborators at CRC level, typed flavors with cardinality at object-model level.

A relationship also has **direction**: the class that depends on, uses, or navigates to the other is the navigating end. Be explicit about which side initiates the dependency.

---

## Inheritance and subtypes

> **Applies from: ubiquitous-language stage and beyond (ubiquitous-language → CRC → object-model).**

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

A subtype carries **only what it adds or overrides**. Inherited responsibilities are not repeated at any level of fidelity — ubiquitous-language, CRC, or object model. If the parent owns a responsibility, the subtype block is silent on it.
