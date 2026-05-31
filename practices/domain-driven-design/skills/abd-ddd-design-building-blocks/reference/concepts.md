# DDD Design Building Blocks — Concepts

> **Note:** The purpose of this skill is *not* to perform a detailed object-oriented analysis and design (OOAD) for every domain concept. Instead, use the **Ubiquitous Language** (`abd-ubiquitous-language`), **CRC cards** (`abd-class-responsibility-collaborator`), or an **Object Model** (`abd-object-model`) skill as appropriate to your current level of domain discovery. This skill extends the domain model by layering in the DDD building blocks, highlighting the architectural roles and stereotypes required to implement the concept — not replacing existing analysis methods, but enriching them.

## Building block stereotypes

Domain concepts are **implemented through** DDD building block stereotypes. When you apply DDD to a domain model, the concepts you already have get **refined and extended**:

- Domain objects become **Entities** or **Value Objects** (identity decision)
- Entities and Value Objects get allocated to **Aggregates** and a **Root** is chosen (consistency boundary)
- **Repositories** are added to abstract persistence behind a collection-style interface — add, remove, update, find (persistence)
- Some operations get moved to **Services** (homeless cross-cutting behavior)
- Some operations surface **Domain Events** (significant moments others react to)
- Complex creation logic gets extracted into **Factories** (assembly concern)

This is a **transformation** of the domain model, not a labeling exercise. New classes appear (Repositories, Factories, Events). Existing classes gain new constraints (aggregate boundaries, identity rules). Some operations move to new homes.

## Entity — "Can we tell them apart?"

An Entity is primarily defined by its **identity** — a thread of continuity that persists regardless of changes to its attributes. Two instances with identical attribute values are still different objects if they have different identities.

**Business questions only the domain expert can answer:**

- If two instances of this thing have the same name, are they automatically the same thing?
- What attributes or rules do we use to **establish or verify** the identity of this thing?
- If two instances have different attribute values but the same identity — are they still the same thing? How will we manage this?
- Does this concept need to be **tracked over time** as it changes state?

If the answer is "yes, we need to track this as 'that one' regardless of data changes," it is an Entity.

## Value Object — "Is it just fancy data?"

A Value Object describes an aspect of the domain and has **no identity**. It is distinguishable only by the state of its properties — two Value Objects with the same attribute values are interchangeable. Value Objects should be **immutable**: created once, never modified.

**Business questions only the domain expert can answer:**

- Is this concept **fully described by its attribute values** with nothing else to say about "which one"?
- If two instances have identical properties, does the business treat them as **the same thing**?
- When this thing changes, do we **update it in place** (Entity signal) or **replace it** with a new version?

If the answer is "it's just data — two with the same values are the same thing," it is a Value Object.

## Aggregate — "What must be consistent together?"

An Aggregate is a cluster of associated objects treated as a **single unit for data changes**. Every Aggregate has a **root** (a single Entity) and a **boundary**. The root is the only member that outside objects may hold persistent references to.

**Business questions only the domain expert can answer:**

- What **must** be consistent in a single transaction?
- What **can tolerate a moment of inconsistency**?
- What is the **cost to the business** if this information is briefly out of date?
- Who is the **single access point** that protects the rules? *(the root)*

## Cross-aggregate consistency — "What happens over there when this changes here?"

When two aggregates reference each other (by ID), every relationship crossing that boundary needs an explicit consistency decision. These are the questions developers will silently answer wrong if nobody asks them:

- **When a Customer's address changes, what happens to their open Orders?**
- **When a Product's price changes, what happens to Orders that reference that Product?**
- **When a Customer is deactivated, what happens to their pending Orders?**

For each cross-aggregate relationship, ask:

1. **"If A changes, does B need to know — and how soon?"** — immediately (should be same aggregate), within seconds (eventual consistency via event), or never (B keeps a snapshot).
2. **"Does B keep a copy of A's data, or just a reference?"** — if B copied A's price at order time, a later price change doesn't affect B. If B holds a live reference, it does.
3. **"What does the business do today when this happens?"** — often there is already a manual process. That process IS the consistency rule.

These decisions become Domain Events, eventual-consistency policies, or snapshot-vs-reference design choices in the model.

Design constraints flow from those answers:
- Code outside the boundary can only load, save, delete, or create the aggregate through its root Entity.
- Entities within the boundary have local identity only — meaningful inside the aggregate, not globally.
- Keep aggregates small: one root, the minimum set of objects needed to enforce the business's stated invariants.

## Repository — "How does the business store, find, and retire this?"

A Repository abstracts persistence behind a **collection-style interface** — add, remove, update, find. From the domain's perspective, it looks like a collection of aggregates you can put things into and take things out of. The implementation (database, file system, API) is hidden; the domain only sees the collection operations.

**Business questions only the domain expert can answer:**

- How does the business **find** this thing?
- When is this thing **done** — and what does "retire" or "archive" mean for it?
- Does the business need to **search** across these things, and by what criteria?

At object-model fidelity, a Repository should implement a collection type. At CRC or UL fidelity, it is expressed as responsibilities (add, remove, find by...).

## Factory — "How are new instances born?"

A Factory handles the **creation** of complex objects or aggregates — when construction requires assembling multiple parts, enforcing invariants at birth, or choosing between subtypes. If a simple constructor suffices, no Factory is needed.

**Business questions only the domain expert can answer:**

- Is there a **business process** for creating this thing?
- What must be **true the moment it's born**?
- Is there a **choice** at creation time about what kind of thing gets made?

## Service — "Who owns this action?"

A Service represents a domain operation that does **not naturally belong** to any Entity or Value Object. If forcing the operation onto a concept would distort that concept's definition, it belongs in a Service.

**Business questions only the domain expert can answer:**

- When the business describes this action, do they name **one** thing that does it — or does it span several?
- Would adding this responsibility to an existing concept **change what that concept is**?
- Is this action a **named domain activity** that business people would recognise?

Services are typically **stateless** — they coordinate work across domain objects without holding their own state between calls.

## Domain Event — "What are the significant moments?"

A Domain Event captures **something that happened** — a significant state change in the domain, named in **past tense** using domain language. Events carry enough data for interested parties to react without calling back.

Domain Events are the **preferred** mechanism for synchronising across aggregate boundaries — but they are not the only one. The cross-aggregate consistency questions determine **how** synchronisation happens: some systems use events, others use batch processes, scheduled jobs, or direct remote calls. The Domain Event building block identifies **what** the significant moments are and who reacts; the consistency approach decides the transport.

**Business questions only the domain expert can answer:**

- What are the **significant moments** in this thing's life that others care about?
- When this thing happens, **who else in the business reacts**?
- If we missed notifying someone about this, **what would break**?
- What past-tense phrase would a domain expert use to describe this moment?

If other parts of the system, outside this aggregate, must react to a state change — that change is a Domain Event regardless of whether it's delivered via an event bus, a batch file, or a method call.

## Specification — "Can we express this rule as a reusable question?"

A Specification is a business rule or condition expressed as a **first-class object** — a predicate you can pass around, compose, and reuse. Instead of burying a complex eligibility check or search filter inside an operation, you extract it into its own named concept that can be used for:

- **Querying** — "find all overdue invoices"
- **Validating** — "is this order eligible for express shipping?"
- **Constructing / Specifying** — "take this Person and produce an Adult that satisfies the adult spec"

**Business questions only the domain expert can answer:**

- Is there a **named business rule** that gets applied in multiple places or contexts?
- Can the business **describe this condition** without referring to how it's implemented?
- Does this rule **compose** with others?

If a rule is named, reusable, and expressible as a true/false question the business can articulate, it is a Specification.

## Source fidelity

Write the DDD building blocks at the **same level of fidelity** as the input source:
- From a **CRC** → use CRC notation: class blocks with responsibilities, collaborators, invariants, and stereotype annotations.
- From an **Object Model** → use typed notation: properties, operation signatures, relationships, and stereotype annotations.
- From a **Ubiquitous Language** → use structured concept blocks: intent, behaviors, collaborations, and stereotype annotations.
- From **Domain Terms** → use plain-language concept descriptions with stereotype annotations.
- From **no formal source** → use plain language and produce domain terms as part of the output.

The building-blocks document **extends** the source model — include the original classes/concepts and show the DDD annotations layered on top.
