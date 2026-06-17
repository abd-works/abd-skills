---
name: ddd-design-building-blocks
catalog_garden_order: 7
description: >-
  Surface the business questions that DDD building block stereotypes encode —
  identity, consistency boundaries, ownership, and integration — and classify
  each domain concept (Entity, Value Object, Aggregate, Service, Domain Event)
  from a CRC, object model, or ubiquitous language.
---
# ddd-design-building-blocks

## Purpose

This skill works through a domain model concept by concept, identifying the right technical constraints through a set of questions that — while technical in framing — can only be answered by business requirements. 

FOr example:
-  if two patients have the same name and date of birth, should we consider them the same patient?  
- If a product changes, when do we update the inventory system? 

This skill answers these questions by introducing **Domain Driven Design Building Blocks**. Every DDD building block — Entity, Value Object, Aggregate, Service, Domain Event — looks technical but **expose a question only the business can answer**. 

THis skill models these elements by understanding business requirements for identity semantics, consistency boundaries, immutability guarantees, and integration contracts across business concepts and business systems.


## When to use this skill

Use this skill when you want to refine your understanding of the business domain you are building a solution for and want to:

- Answer **"is uniqueness important?"** — does this concept need to be tracked as a distinct thing, what makes one instance different from another, or is it just a bundle of data values that can be freely replaced?
- Answer **"what business rules must always hold true?"** — what things must change together to keep those rules honest, and what is the cost to the business if they're briefly violated?
- Answer **"what must be consistent together?"** — which pieces must change atomically in a single transaction and which can tolerate, or even require lag?
- Answer **"how does the business need to store, find, and retrieve this information?"** — what do people search by, when is something considered "done," and how does old information get handled?
- Answer **"how do new instances come into being?"** — is there a business process for creating them, what must be true the moment they're born, and is assembly complex enough to be its own concern?
- Answer **"what are the significant moments in this thing's life?"** — who else needs to know when they happen, and what breaks if they're missed?

---

## Core concepts

### Object-oriented foundations

A **class** is a named domain idea that earns its own place because it has at least one of: **distinct identity**, **state**, **behavior**, **structure**, or **interactions** that cannot be collapsed into a property, instance, or type property of something else. A class knows things (**state**) and does things (**behavior**). Those two dimensions — together with the relationships it maintains and the invariants that constrain it — are what a class IS.

Not everything deserves its own class:
- A term that is only a data value on another class is a **property**.
- A term that varies only by label across identical behavior is a **type property**.
- A term that is one concrete member of a known set is an **instance**.
- A term that adds distinct behavior to a base is a **subtype**.

Only when none of those fit does something deserve its own class.

### Responsibilities

A responsibility is either something a class **holds** (state) or something it **does** (behaviour) — or both:
- **Property** — the class must remember something across calls. Named as a noun phrase.
- **Operation** — the class must perform an action or compute a result; it may be entirely stateless. Named as a verb phrase.
- **Both** — the class holds state **and** exposes an action that works with it.

Never assume every responsibility implies a property, and never assume every responsibility implies an operation.

### Relationships

A relationship describes how two domain classes depend on each other. Answer three questions:

1. **Does one class own the other's lifecycle?** — The other cannot exist without the first. *(Composition)*
2. **Does one class exist to collect or group the other?** — The collecting class has no meaningful identity without its members. *(Aggregation)*
3. **Are both sides independent?** — Each can exist and be meaningful without the other. *(Association)*

A relationship also has **direction**: the class that depends on, uses, or navigates to the other is the navigating end.

### Inheritance and subtypes

A **base class** defines the common identity, state, and behavior shared by a family. A **subtype** is a specialisation — it *is a kind of* the base — adding or overriding behavior specific to it alone. Subtypes carry **only the delta**: inherited responsibilities are never repeated.

**When to choose:**
- **Subtype** — the specialised thing adds **behavior the base does not have** (the distinction changes what the thing *does*).
- **Type property** — the thing varies by category but every category follows **the same behavior**.
- **Instance** — the thing is one concrete member of a parent, distinguished only by specific data values.

---
> **Note:** The purpose of this skill is *not* to perform a detailed object-oriented analysis and design (OOAD) for every domain concept. Instead, use the **Ubiquitous Language** (`abd-ubiquitous-language`), **CRC cards** (`abd-class-responsibility-collaborator`), or an **Object Model** (`abd-object-model`) skill as appropriate to your current level of domain discovery. This skill extends the domain model by layering in the DDD building blocks, highlighting the architectural roles and stereotypes required to implement the concept — not replacing existing analysis methods, but enriching them.

### Building block stereotypes

Domain concepts are **implemented through** DDD building block stereotypes. When you apply DDD to a domain model, the concepts you already have get **refined and extended**:

- Domain objects become **Entities** or **Value Objects** (identity decision)
- Entities and Value Objects get allocated to **Aggregates** and a **Root** is chosen (consistency boundary)
- **Repositories** are added to abstract persistence behind a collection-style interface — add, remove, update, find (persistence)
- Some operations get moved to **Services** (homeless cross-cutting behavior)
- Some operations surface **Domain Events** (significant moments others react to)
- Complex creation logic gets extracted into **Factories** (assembly concern)

This is a **transformation** of the domain model, not a labeling exercise. New classes appear (Repositories, Factories, Events). Existing classes gain new constraints (aggregate boundaries, identity rules). Some operations move to new homes.

#### Example: CRC before and after DDD building blocks

**Before** — vanilla CRC from `abd-class-responsibility-collaborator`:

```
#### **Order**
place                              | Customer, OrderLine
Order Lines                        | OrderLine, Product
calculate total                    | OrderLine
                                   |   invariant: total = sum of line amounts

#### **OrderLine**
hold quantity and price            | Product
calculate line amount              | (quantity × product price)

#### **Product**
provide price                      | (decimal amount)
provide description                | (name, category)

#### **Customer**
place orders                       | Order
contact info              | Address
```

**After** — the same model with DDD building blocks applied:

```
#### **Order** [Entity, Aggregate Root]
identity: customer + order date + items (no two orders from the same customer with identical items on the same day) |
place order                        | Customer (by ID), OrderLine
order lines                        | OrderLine, Product (by ID)
calculate total                    | OrderLine
                                   |   invariant: total = sum of line amounts
                                   |   invariant: status only advances (Draft→Confirmed→Fulfilled)
                                   |   aggregate boundary: OrderLine, Money

#### **OrderLine** [Value Object, within Order Aggregate]
hold quantity and price            | Money
calculate line amount              | (quantity × unit price)

#### **Money** [Value Object]
represent amount and currency      | (amount, currency)
                                   |   invariant: immutable — arithmetic returns new instances

#### **Product** [Entity, separate Aggregate Root]
identity: SKU                      |
provide price                      | (decimal amount)
provide description                | (name, category)

#### **Customer** [Entity, separate Aggregate Root]
identity: email + phone number (no two customers share both) |
place orders                       | Order (by ID)
maintain contact info              | Address

#### **Address** [Value Object]
represent location                 | (street, city, province, postal code)
                                   |   invariant: immutable — replaced, never mutated

#### **OrderRepository** [Repository — added by DDD]
add order                          | Order
remove order                       | Order
update order                       | Order
find orders by customer            | Customer (by ID)
find orders by status              | (status filter)

#### **OrderConfirmed** [Domain Event — surfaced from place order]
notify: payment, inventory         | Order (by ID), Customer (by ID)
                                   |   payload: order ID, customer ID, lines, total, timestamp

#### **OrderFactory** [Factory — extracted from complex creation]
assemble Order with lines          | OrderLine, Product (by ID), Money
                                   |   invariant: new Order always valid (at least one line, correct total)
```

**What changed:**
- `Order` gained stereotype annotations, aggregate boundary, and an identity rule
- `Money` and `Address` were extracted as Value Objects (were implicit in "price" and "contact info")
- `OrderRepository` was **added** — it didn't exist in the domain model
- `OrderConfirmed` was **surfaced** from the "place order" operation as a Domain Event
- `OrderFactory` was **extracted** because assembly has invariants worth protecting
- Cross-aggregate references became **by ID** (Customer, Product) — no object graph coupling

The business questions surface **which transformations apply** to each concept and **what constraints** each transformation carries.

### Entity — "Can we tell them apart?"

An Entity is primarily defined by its **identity** — a thread of continuity that persists regardless of changes to its attributes. Two instances with identical attribute values are still different objects if they have different identities.

**Business questions only the domain expert can answer:**

- If two instances of this thing have the same name, are they automatically the same thing? *(e.g. two patients named "John Smith" — same patient or different?)*
- What attributes or rules do we use to **establish or verify** the identity of this thing?
- If two instances have different attribute values but the same identity — are they still the same thing? How will we manage this? *(e.g. a patient changes address, insurance, and name — still the same patient?)*
- Does this concept need to be **tracked over time** as it changes state?

If the answer is "yes, we need to track this as 'that one' regardless of data changes," it is an Entity.

### Value Object — "Is it just fancy data?"

A Value Object describes an aspect of the domain and has **no identity**. It is distinguishable only by the state of its properties — two Value Objects with the same attribute values are interchangeable. Value Objects should be **immutable**: created once, never modified.

**Business questions only the domain expert can answer:**

- Is this concept **fully described by its attribute values** with nothing else to say about "which one"? *(e.g. the color "Midnight Blue" is "Midnight Blue" — there is no "that particular midnight blue" to track)*
- If two instances have identical properties, does the business treat them as **the same thing**?
- When this thing changes, do we **update it in place** (Entity signal) or **replace it** with a new version?

If the answer is "it's just data — two with the same values are the same thing," it is a Value Object.

### Aggregate — "What must be consistent together?"

An Aggregate is a cluster of associated objects treated as a **single unit for data changes**. Every Aggregate has a **root** (a single Entity) and a **boundary**. The root is the only member that outside objects may hold persistent references to.

**Business questions only the domain expert can answer:**

- What **must** be consistent in a single transaction? *(e.g. "an order's total must always equal the sum of its lines" — lines and order must change together)*
- What **can tolerate a moment of inconsistency**? *(e.g. "a customer's lifetime spend can lag behind their latest order for a few seconds" — separate aggregates, eventually consistent)*
- What is the **cost to the business** if this information is briefly out of date?
- Who is the **single access point** that protects the rules? *(the root)*

### Cross-aggregate consistency — "what happens over there when this changes here?"

When two aggregates reference each other (by ID), every relationship crossing that boundary needs an explicit consistency decision. These are the questions developers will silently answer wrong if nobody asks them:

- **When a Customer's address changes, what happens to their open Orders?** *(Do existing orders keep the old address? Do they update? Is that a business rule or a bug?)*
- **When a Product's price changes, what happens to Orders that reference that Product?** *(Do in-flight orders get the new price? Only confirmed ones stay locked? What about the current billing cycle?)*
- **When a Customer is deactivated, what happens to their pending Orders?** *(Cancel them? Fulfill them? Freeze them until resolved?)*

For each cross-aggregate relationship, ask:

1. **"If A changes, does B need to know — and how soon?"** — immediately (should be same aggregate), within seconds (eventual consistency via event), or never (B keeps a snapshot).
2. **"Does B keep a copy of A's data, or just a reference?"** — if B copied A's price at order time, a later price change doesn't affect B. If B holds a live reference, it does.
3. **"What does the business do today when this happens?"** — often there is already a manual process (someone calls the customer, someone re-runs the invoice). That process IS the consistency rule.

These decisions become Domain Events, eventual-consistency policies, or snapshot-vs-reference design choices in the model.

Design constraints flow from those answers:
- Code outside the boundary can only load, save, delete, or create the aggregate through its root Entity.
- Entities within the boundary have local identity only — meaningful inside the aggregate, not globally.
- Keep aggregates small: one root, the minimum set of objects needed to enforce the business's stated invariants.

### Repository — "How does the business store, find, and retire this?"

A Repository abstracts persistence behind a **collection-style interface** — add, remove, update, find. From the domain's perspective, it looks like a collection of aggregates you can put things into and take things out of. The implementation (database, file system, API) is hidden; the domain only sees the collection operations.

**Business questions only the domain expert can answer:**

- How does the business **find** this thing? *(by name? by date range? by status? by customer?)*
- When is this thing **done** — and what does "retire" or "archive" mean for it?
- Does the business need to **search** across these things, and by what criteria?

At object-model fidelity, a Repository should implement a collection type. At CRC or UL fidelity, it is expressed as responsibilities (add, remove, find by...).

### Factory — "How are new instances born?"

A Factory handles the **creation** of complex objects or aggregates — when construction requires assembling multiple parts, enforcing invariants at birth, or choosing between subtypes. If a simple constructor suffices, no Factory is needed.

**Business questions only the domain expert can answer:**

- Is there a **business process** for creating this thing? *(e.g. "onboarding a new customer involves verification, default preferences, and welcome communication")*
- What must be **true the moment it's born**? *(the invariants a new instance must satisfy)*
- Is there a **choice** at creation time about what kind of thing gets made? *(subtype selection)*

### Service — "Who owns this action?"

A Service represents a domain operation that does **not naturally belong** to any Entity or Value Object. If forcing the operation onto a concept would distort that concept's definition, it belongs in a Service.

**Business questions only the domain expert can answer:**

- When the business describes this action, do they name **one** thing that does it — or does it span several? *(e.g. "matching a buyer to a pet" involves the buyer, the pet, and breed standards — nobody owns it alone)*
- Would adding this responsibility to an existing concept **change what that concept is**?
- Is this action a **named domain activity** that business people would recognise? *(not a technical utility — a real business operation)*

Services are typically **stateless** — they coordinate work across domain objects without holding their own state between calls.

### Domain Event — "What are the significant moments?"

A Domain Event captures **something that happened** — a significant state change in the domain, named in **past tense** using domain language. Events carry enough data for interested parties to react without calling back.

Domain Events are the **preferred** mechanism for synchronising across aggregate boundaries — but they are not the only one. The cross-aggregate consistency questions (above) determine **how** synchronisation happens: some systems use events, others use batch processes, scheduled jobs, or direct remote calls. The Domain Event building block identifies **what** the significant moments are and who reacts; the consistency approach decides the transport.

**Business questions only the domain expert can answer:**

- What are the **significant moments** in this thing's life that others care about?
- When this thing happens, **who else in the business reacts**? *(e.g. "when a pet is sold, inventory updates, the customer gets a receipt, and reporting logs revenue")*
- If we missed notifying someone about this, **what would break**?
- What past-tense phrase would a domain expert use to describe this moment? *("Pet Sold", "Patient Admitted", "Claim Rejected")*

If other parts of the system, outside this aggregate, must react to a state change — that change is a Domain Event regardless of whether it's delivered via an event bus, a batch file, or a method call.

### Specification — "Can we express this rule as a reusable question?"

A Specification is a business rule or condition expressed as a **first-class object** — a predicate you can pass around, compose, and reuse. Instead of burying a complex eligibility check or search filter inside an operation, you extract it into its own named concept that can be used for:

- **Querying** — "find all overdue invoices"
- **Validating** — "is this order eligible for express shipping?"
- **Constructing / Specifying** — "take this Person and produce an Adult that satisfies the adult spec" (e.g. `adult = adultSpec.specify(person)` — the spec constrains or transforms a concept to match itself)

**Business questions only the domain expert can answer:**

- Is there a **named business rule** that gets applied in multiple places or contexts? *(e.g. "overdue" means the same thing whether you're querying, alerting, or escalating)*
- Can the business **describe this condition** without referring to how it's implemented? *(e.g. "an invoice is overdue if it's unpaid 30 days past due date")*
- Does this rule **compose** with others? *(e.g. "overdue AND high-value" is a compound specification)*

If a rule is named, reusable, and expressible as a true/false question the business can articulate, it is a Specification.

---

## Build

**Goal:** Take an existing domain model and produce a building-blocks portrait for each concept — surfacing the business questions, getting them answered, and recording which stereotypes each concept expresses and why.

1. **Identify the input model.** Read the source artifact — a CRC model (`### Class Responsibility Collaborator` blocks), an object model (`### Object Model` sections), or a ubiquitous language (`### Key Abstraction` blocks). List every named concept.

2. **Ask the identity questions for every concept.** For each concept, surface the Entity vs Value Object questions: "Can we tell two instances apart beyond their data? Does this get tracked over time? Or is it just data — two with the same values are the same thing?" A concept may be an Entity **and** contain Value Objects within it — these are not exclusive.

3. **Ask the consistency questions to find Aggregate boundaries.** For each Entity, ask: "What must be consistent together in a single transaction? What can tolerate a moment of lag?" Identify which Entity is the root (the single access point), which other Entities and Value Objects sit inside its boundary, and what invariants tie them together. A concept that is an Entity may also be an Aggregate Root — and its boundary members may be Entities or Value Objects in their own right.

4. **Ask the ownership question to find Services.** For behaviors that span concepts, ask: "When the business describes this action, who does it? One thing, or several?" If no single concept owns it without distortion, it is a Service. A Service may coordinate across multiple Aggregates.

5. **Ask "who else needs to know?" to find Domain Events.** For significant state changes within each Aggregate, ask: "When this happens, who else reacts?" Name each event in past tense. Events **belong to** a concept (they are raised by an Aggregate) — they are another facet of that concept's building-block portrait.

6. **Produce the building-blocks document.** Use `templates/ddd-building-blocks-template.md` to write the portrait. For every concept, record **all** the stereotypes it expresses — Entity + Aggregate Root + its boundary members + its events — not just one label. Include the business questions asked and answers given for each facet.

7. **Cross-check against the source model.** Every concept from the input model must appear in the output. Concepts where the business question could not be answered should be flagged as **Unresolved** with the unanswered question stated explicitly.

---

- **Outputs:** One `*-ddd-building-blocks.md` file per module, placed beside the source model artifact.
- **Source fidelity:** Write the DDD building blocks at the **same level of fidelity** as the input source:
  - From a **CRC** (`abd-class-responsibility-collaborator`) → use CRC notation: class blocks with responsibilities, collaborators, invariants, and stereotype annotations.
  - From an **Object Model** (`abd-object-model`) → use typed notation: properties, operation signatures, relationships, and stereotype annotations.
  - From a **Ubiquitous Language** (`abd-ubiquitous-language`) → use structured concept blocks: intent, behaviors, collaborations, and stereotype annotations.
  - From **Domain Terms** (`abd-domain-terms`) → use plain-language concept descriptions with stereotype annotations.
  - From **no formal source** → use plain language and produce domain terms as part of the output.
- **Include the source model in the output.** The building-blocks document is not a standalone classification — it **extends** the source. Include the original classes/concepts and show the DDD annotations layered on top (as in the before/after example in Core concepts).
- **While writing:** Use domain language from the source model. Do not invent new names. Stereotype names are capitalised (Entity, Value Object, Aggregate, Service, Domain Event). A concept may appear under multiple stereotype headings — that is expected.

---

## Validate

**Goal:** Inspect the building-blocks portrait as a domain expert and architect would.

- **Business questions surfaced:** Every stereotype facet records the business question that was asked and the answer that was given — not just a technical label.
- **Multi-faceted portraits:** Concepts that are Entities AND Aggregate Roots AND emit Events show all facets — the output is not forced into one-label-per-concept.
- **Domain expert check:** Every concept is named in the domain language from the source model; no technical jargon was introduced.
- **Complete coverage:** Every concept from the input model appears in the output with at least one stereotype facet or an explicit Unresolved note (with the unanswered question stated).
- **Identity test applied:** Entity vs Value Object decisions cite the identity/attribute question and give a domain-grounded answer.
- **Aggregate boundaries defensible:** Each aggregate names its root, lists its boundary members (which may be Entities or Value Objects), and states the invariants the boundary protects.
- **Services are genuinely homeless:** No service could be more naturally placed as a method on an existing Entity or Value Object.
- **Events belong to their Aggregate:** Every Domain Event names which Aggregate raises it, uses a past-tense verb phrase, and names consumers.
- **No premature infrastructure:** The document does not prescribe database tables, message queues, or framework classes — it stays at the design level.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Aggregate boundary protects stated invariants

Every Aggregate in the output must name its root Entity, list its boundary members, and state the invariants the boundary protects. The boundary exists **because** those invariants must hold atomically — not because the concepts happen to be related. Passing means each Aggregate has a defensible reason for its boundary size. Failing means aggregates are drawn by "relatedness" rather than invariant protection, or invariants are missing.

#### DO

- Name the root Entity explicitly — it is the single external access point and the invariant enforcer.

  **Example (pass):** "**Root:** Order (Entity) — all status transitions and total-recalculation pass through Order."

- List boundary members and explain why each one is **inside** rather than a separate aggregate referenced by ID.

  **Example (pass):** "**Boundary members:** OrderLine (local identity within Order) — lines cannot exist without the order; the order-total invariant spans all lines."

- State at least one invariant that requires the boundary members to be modified atomically with the root.

  **Example (pass):** "**Protected invariants:** Order total must equal sum of line amounts at all times; status can only advance forward (Draft → Confirmed → Fulfilled)."

- Keep aggregates small — the minimum cluster needed for invariant enforcement; reference other aggregates by ID.

  **Example (pass):** Customer is a separate Aggregate from Order — they reference each other by ID, not by object graph, because no cross-invariant requires atomic change.

#### DO NOT

- Draw an aggregate boundary around "everything that is related" without stating what invariant requires atomicity.

  **Example (fail):** "**Boundary members:** Customer, Order, OrderLine, Product, Warehouse" — no invariant needs all five to change atomically; this is a relational model, not an aggregate.

- Omit the root or list multiple roots.

  **Example (fail):** "**Root:** Order and OrderLine" — an aggregate has exactly one root Entity.

- State invariants that are actually cross-aggregate eventual-consistency rules as if they required a single boundary.

  **Example (fail):** "**Protected invariants:** Customer's lifetime spend must always equal sum of all orders" — this spans Order and Customer aggregates; it is an eventual-consistency concern, not a single-aggregate invariant.

**Source:** Kept chunks #6, #8 in `inputs/abd-answers-retrieval.md`

### Rule: Domain Events named in past tense with trigger and consumers

Every Domain Event must be named as a **past-tense verb phrase** in domain language, state what triggered it, and name at least one consumer. Events represent something that **already happened** — they are facts, not commands. Passing means events read like history ("OrderConfirmed", "PatientAdmitted") and carry enough context to be actionable. Failing means events are named as commands, lack triggers, or have no stated consumers.

#### DO

- Name every Domain Event in past tense using domain vocabulary.

  **Example (pass):** `PetSold`, `OrderConfirmed`, `AppointmentCancelled`, `PaymentReceived` — each reads as "this happened."

- State the trigger: what state change in which aggregate causes this event to fire.

  **Example (pass):** "**Trigger:** An Order transitions from Draft to Confirmed after payment validation succeeds."

- Name at least one consumer that reacts to the event — another aggregate, bounded context, or external system.

  **Example (pass):** "**Consumers:** Inventory (decrement available count), Notifications (send confirmation email)."

- Include a payload summary — the key data the event carries, enough for consumers to react without calling back.

  **Example (pass):** "**Payload:** order ID, customer ID, pet ID, confirmed timestamp, total amount."

#### DO NOT

- Name events as commands or present-tense verbs.

  **Example (fail):** `ConfirmOrder`, `SellPet`, `ProcessPayment` — these are commands, not events; they say "do this" not "this happened."

- Declare a Domain Event with no consumer identified.

  **Example (fail):** "**Consumers:** None identified." — if nothing reacts to it, it is not yet a Domain Event worth modeling; it is just internal state change.

- Use technical or infrastructure names instead of domain language.

  **Example (fail):** `MessagePublished`, `QueueUpdated`, `RecordInserted` — these are infrastructure concerns, not domain events.

**Source:** Kept chunks #9, #12 in `inputs/abd-answers-retrieval.md`

### Rule: Every concept classified with explicit rationale

Every named concept from the input model (CRC block, object-model class, or ubiquitous-language concept) must appear in the building-blocks output with **at least one** stereotype facet **and** a rationale that records the **business question asked** and the **answer that drove the decision**. A concept may express multiple stereotypes (Entity + Aggregate Root + emits Domain Events) — that is expected and correct. Passing means no concept is left out and every facet traces to a stated question and answer. Failing means a concept is missing, or a stereotype is assigned without surfacing the underlying business question.

#### DO

- Identify **all** stereotype facets that apply to each concept — do not force one-label-per-concept.

  **Example (pass):** "Car — **Entity** (identity: VIN persists across paint jobs), **Aggregate Root** (access point for Driver, Color), **emits:** CarStarted, DriverChanged."

- Write the rationale by stating which business question was asked and what the domain expert's answer was — connecting the answer to each stereotype facet.

  **Example (pass):** "**Business question asked:** 'If two patients have the same name and DOB, are they the same patient?' **Answer:** 'No — each has a unique MRN.' **Rationale:** Identity transcends attributes; Patient is an Entity and the Aggregate Root for its clinical records."

#### DO NOT

- Leave any source-model concept unaccounted for in the output (even if it is Unresolved, it must appear with the unanswered question stated).

  **Example (fail):** Source CRC has `Appointment`, `Patient`, `Clinic`, `TimeSlot`; output only addresses `Patient` and `Clinic` — two concepts silently dropped.

- Assign a stereotype with only a label and no business question or answer.

  **Example (fail):** "**Stereotype:** Value Object / **Rationale:** It's a value object." — circular; does not state what question was asked or what the domain expert said.

- Force each concept into exactly one stereotype when it naturally expresses several.

  **Example (fail):** Order listed only as "Entity" when it is also the Aggregate Root for OrderLines and emits OrderConfirmed — the portrait is incomplete.

**Source:** Kept chunks #3, #4, #5 in `inputs/abd-answers-retrieval.md`

### Rule: Identity test drives Entity vs Value Object

The distinction between Entity and Value Object is decided by asking whether the concept has **identity that transcends its attributes**. An Entity's identity persists even when all its data changes; a Value Object is fully described by its properties and has no independent identity. Passing means every Entity cites an identity reason and every Value Object cites the absence of identity. Failing means the stereotype was assigned by gut feel, by looking at "importance," or by defaulting everything to Entity.

#### DO

- Classify as Entity when the concept must be tracked as "that one" over time, even if all attributes change.

  **Example (pass):** "**Identity:** Patient ID — a patient who changes name, address, and insurance is still the same patient. **Rationale:** Two patients with identical demographics are still different people; identity transcends attributes."

- Classify as Value Object when two instances with identical properties are interchangeable — no "which one" question exists.

  **Example (pass):** "**Defining attributes:** amount, currency. **Rationale:** $50.00 CAD is $50.00 CAD — there is no 'that particular fifty dollars' distinct from another fifty dollars with the same amount and currency."

- Prefer Value Object as the default — select Entity only when the concept genuinely requires tracked identity.

  **Example (pass):** A model with 15 concepts classifies 4 as Entities and 8 as Value Objects — the majority are values, entities are the exception, not the rule.

#### DO NOT

- Default to Entity because the concept "feels important" or "is a noun" without applying the identity test.

  **Example (fail):** "**Stereotype:** Entity / **Rationale:** Address is an important concept." — importance is not identity; Address with no independent tracking is a Value Object.

- Classify as Value Object without confirming immutability and replaceability.

  **Example (fail):** "**Stereotype:** Value Object" on a concept that the domain experts say must be "updated in place" and "tracked for audit" — those are Entity signals, not Value Object.

- Use "it has attributes" as the reason for Value Object — all concepts have attributes; the question is whether identity exists **beyond** them.

  **Example (fail):** "**Rationale:** It has name, size, and color properties." — Entities also have properties; this does not distinguish.

**Source:** Kept chunks #4, #5, #7 in `inputs/abd-answers-retrieval.md`

### Rule: No premature infrastructure in building-blocks output

The building-blocks classification is a **design-level** artifact — it records architectural intent (identity, boundaries, immutability, communication contracts) but does not prescribe implementation technology. Passing means the document stays in domain language and design constraints. Failing means it names database tables, message brokers, framework annotations, REST endpoints, or specific persistence strategies.

#### DO

- Use domain language and DDD pattern vocabulary only: Entity, Value Object, Aggregate root, boundary, invariant, Domain Event, Service.

  **Example (pass):** "**Protected invariants:** When a change to the Order boundary is committed, the total must equal the sum of line amounts." — design constraint, no tech.

- Describe lifecycle in terms of domain state transitions, not persistence mechanisms.

  **Example (pass):** "**Lifecycle:** Created at patient admission, transitions through Active → Discharged → Archived." — domain states, not DB row states.

- Describe event contracts in terms of trigger, payload, and consumer — not transport mechanisms.

  **Example (pass):** "**Payload:** patient ID, discharge reason, discharge timestamp." — what the event carries, not how it's serialized or transported.

#### DO NOT

- Name database tables, columns, or storage engines in the building-blocks output.

  **Example (fail):** "**Lifecycle:** Inserted into the `patients` table with status column set to 'ACTIVE'."

- Prescribe message queue topics, REST endpoints, or framework annotations.

  **Example (fail):** "**Consumers:** Subscribes to `order.confirmed` Kafka topic." — names the transport; should just say "Inventory service reacts."

- Add implementation patterns (Repository, Factory, DTO, Controller) to the stereotype classification — those come later.

  **Example (fail):** "**Stereotype:** Entity with JPA @Entity annotation and Spring Data Repository." — implementation detail, not design intent.

**Source:** Practice convention — building blocks classify design intent before implementation decisions; Kept chunk #1 (Evans: "A Model Expressed in Software" separates model from implementation paradigm).

### Rule: Service is genuinely homeless operation

A Service stereotype is only valid when the operation **does not naturally belong** to any single Entity or Value Object. If the operation could coherently live on one concept without distorting it, it should be a method on that concept — not a Service. Passing means every Service entry explains why placement on any existing concept would distort that concept. Failing means Services are used as a dumping ground for behavior that has a clear owner.

#### DO

- Explain which concepts the operation spans and why none of them can own it alone.

  **Example (pass):** "**Spans:** Customer (preferences), Pet (availability), Breed (standards). **Rationale:** Matching logic requires inputs from three aggregates — placing it on Customer makes Customer a search engine; placing it on Pet makes Pet responsible for customer preferences."

- Confirm the Service is stateless (or explain why state is domain-justified if it is not).

  **Example (pass):** "**Stateless:** Yes — accepts inputs, returns results, holds nothing between calls."

- Name the Service using domain language — the operation it performs, not a technical pattern name.

  **Example (pass):** `PetMatchingService`, `TransferAuthorizationService` — named for what the domain expert would call the action.

#### DO NOT

- Create a Service for an operation that clearly belongs on one Entity just because "services are easier to test."

  **Example (fail):** `OrderTotalCalculationService` when the Order aggregate already owns its lines and the total invariant — this is naturally `Order.recalculateTotal()`.

- Use Service as a catch-all for "I don't know where this goes."

  **Example (fail):** "**Rationale:** Didn't fit anywhere else." — that is not a rationale; ask which concept the operation's inputs and outputs most naturally belong to.

- Name Services with infrastructure terms instead of domain language.

  **Example (fail):** `DataProcessingService`, `HelperService`, `UtilityService` — these are not domain operations.

**Source:** Kept chunks #1, #3, #9 in `inputs/abd-answers-retrieval.md`
<!-- execute_rules:bundle_rules:end -->
