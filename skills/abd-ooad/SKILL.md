---
name: abd-ooad
description: >-
  Linear OOAD from raw material (specs, code, manuals, policies): read for meaning,
  name concepts, separate responsibilities, shape behavior, tighten the model.
  Use when building object-oriented domain models, class diagrams (including ASCII),
  or refactoring toward cohesive types, inheritance, composition, and invariants.
license: MIT
metadata:
  author: agilebydesign
  version: "0.2.0"
---

# Object Oriented Analysis and Design (OOAD)

**Agile by Design skills — single-document skill.** Everything lives in this file; there is no multi-phase build, no split parts/library pipeline.

You are a master of OOAD. You are able to take any context—whether it is code that is extremely bad, prose in a structured document, a user manual, or a rule book—and start creating robust object-oriented models.

Walk through a very linear, straightforward set of steps. For instance, given a paragraph or two of specs, start looking through each individual section and start creating classes, properties, operations, and relationships with other classes. Talk about the exact kind of analysis you would do, as well as when you start realizing that a class needs to be broken up into other classes. Inheritance applies when you start seeing repetition in behavior and operations, including the idea of having abstract subtypes. Walk through this one layer at a time and in a thoughtful way, as one step: expand your thinking to the next step.

Here is a clean, linear way to do OOAD from raw material like specs, messy code, manuals, policy docs, or rule books.

The core idea is simple: **do not start by inventing classes.** Start by reading for meaning, then naming concepts, then separating responsibilities, then shaping behavior, then tightening the model.

## Step 1: Read for nouns, verbs, rules, and states

Begin by reading the source material one small section at a time.

For each paragraph, mark four things:

- **Nouns:** candidate objects or concepts
- **Verbs:** candidate operations or responsibilities
- **Rules:** constraints and invariants
- **States:** ways something can change over time

If a paragraph says:

> A customer places an order. An order contains one or more items. Payment must be authorized before shipment. A shipped order cannot be canceled.

Extract immediately:

- **Nouns:** Customer, Order, Item, Payment, Shipment
- **Verbs:** places, contains, authorize, ship, cancel
- **Rules:**
  - Order must have at least one item
  - Payment authorized before shipment
  - Shipped order cannot be canceled
- **States:**
  - Order may move from created → paid → shipped
  - Payment may move from pending → authorized

At this stage, do not worry yet whether every noun becomes a class.

## Step 2: Build a raw candidate list

Next create a rough inventory of possible classes.

Sort candidates into categories:

- **Core domain entities:** durable business things like Order, Customer, Invoice
- **Value-like concepts:** descriptive data like Address, Money, DateRange
- **Processes or transactions:** Payment, Reservation, Enrollment
- **Policies or rules:** DiscountPolicy, EligibilityRule
- **Roles:** Admin, Member, Approver
- **Events or records:** ShipmentNotice, AuditEntry

This is still loose. Some candidates will disappear, merge, or become attributes instead of classes.

A good early question is:

**Does this concept have identity, behavior, lifecycle, or relationships that matter?**

If yes, it is more likely to deserve a class.

## Step 3: Separate “thing” from “data about a thing”

A very common mistake is turning every noun into a full class.

For example:

- Address is often not a major domain actor, but a structured value
- Money is rarely just a decimal field; it usually deserves a small value object
- OrderStatus may be an enum or state abstraction, not a big entity

Ask:

- Does this concept exist independently?
- Can two of them be distinguished by identity?
- Does it own behavior?
- Can it change independently of another object?

If not, it may be better as:

- a property
- a value object
- an enum
- a small helper type

For example:

```
Order
- orderNumber
- customer
- shippingAddress : Address
- total : Money
- status : OrderStatus
```

Here, Order is a class with identity. Address, Money, and OrderStatus may be supporting types.

## Step 4: Write responsibilities before operations

Before writing method names, define what each class is responsible for.

Example:

**Order** — Responsible for:

- holding items
- tracking status
- knowing whether it can be canceled
- coordinating total amount

**Payment** — Responsible for:

- tracking authorization
- recording amount and timing
- exposing whether settlement succeeded

**Shipment** — Responsible for:

- shipment details
- shipment date and carrier
- delivery state

This is important because bad OO models usually happen when classes are created from data structure shape rather than responsibility.

A class should have a reason to exist beyond “the spec mentioned it.”

## Step 5: Add properties and keep them semantically tight

Now add properties.

Do not ask, “What fields are mentioned?”  
Ask, “What information must this object know in order to fulfill its responsibility?”

Example:

**Customer**

- customerId
- name
- email

**Order**

- orderId
- customer
- items
- status
- placedAt

**OrderItem**

- product
- quantity
- unitPrice

**Payment**

- paymentId
- order
- amount
- status
- authorizedAt

Notice something important: choose **OrderItem**, not just Item.

Why? Because the item in this context is not a general thing. It is specifically a product as included in an order, with a quantity and price at that moment.

That is a key OO move: **model the contextual role, not just the vague noun.**

## Step 6: Turn verbs into operations, but only where responsibility belongs

Go back to the verbs and distribute them.

From the earlier example:

- customer places order
- payment authorizes
- order ships
- order cancels

Possible operations:

**Order**

- addItem(product, quantity)
- calculateTotal()
- cancel()
- markPaid()
- ship()

**Payment**

- authorize()
- decline()

**Shipment**

- dispatch()
- markDelivered()

Challenge each one.

For example, should `Order.ship()` exist? Yes, if shipping is part of the order lifecycle.

Should `Customer.placeOrder()` exist? Maybe, but often that is more application-service behavior than core entity behavior. A customer may not need to “know how” to create orders in the domain model.

Keep asking:

**Who truly owns this behavior?**  
Not who mentions it in English, but who is responsible for enforcing it.

## Step 7: Add relationships and cardinality

Define how classes relate.

Example:

- A Customer places many Orders
- An Order contains one or more OrderItems
- An Order may have one Payment
- An Order may result in zero or one Shipment

That becomes:

```
Customer 1 ---- * Order
Order 1 ---- 1..* OrderItem
Order 1 ---- 0..1 Payment
Order 1 ---- 0..1 Shipment
```

This is where structure starts becoming real.

For **plain-text diagrams** (interfaces vs classes, inheritance vs realization, composition vs aggregation, dependency), use the glyphs and tables in **ASCII class diagrams — notation** (later in this skill).

Also decide the strength of containment:

- If OrderItem cannot meaningfully exist without Order, that suggests strong ownership/composition
- If Payment can exist and be referenced independently, it may be an associated entity rather than a contained part

## Step 8: Identify invariants and move them into the model

This is where the object model becomes robust.

From the text:

- An order must contain one or more items
- Payment must be authorized before shipment
- A shipped order cannot be canceled

These are not comments. These are **domain invariants**.

Encode them into class behavior.

- `Order.cancel()` — only allowed if status is not SHIPPED
- `Order.ship()` — only allowed if payment is authorized; only allowed if there is at least one item

This is a major OO principle: **rules belong where they can be enforced**, not in scattered external code.

If rules are only in UI, service code, or documentation, the domain model is weak.

## Step 9: Watch for bloated classes

As you proceed section by section, one of the first danger signals is a class that starts accumulating too much.

**Signs a class needs breaking up:**

- too many properties from unrelated concerns
- methods that operate on different conceptual clusters
- multiple reasons to change
- many if branches based on subtypes or statuses
- class name becomes vague, like Manager, Processor, Handler, SystemData

For example, suppose Order starts to contain:

- item management
- pricing rules
- tax logic
- shipping selection
- payment workflow
- refund logic
- promotion rules
- audit history

That is too much.

Then split by cohesive responsibility:

- Order stays focused on lifecycle and composition
- PricingPolicy or PricingEngine handles price calculation rules
- Payment or PaymentAuthorization handles payment flow
- Shipment handles shipment concerns
- OrderAuditTrail or domain events capture history

A class should feel like **one coherent story.**

## Step 10: Detect when one class is actually several abstractions smashed together

This happens all the time in bad code and prose.

Suppose the source material refers to “user” everywhere, but closer reading shows different roles:

- customer browses and buys
- staff approve refunds
- admins configure rules
- vendors fulfill orders

A single User class may be too blunt.

Ask:

- Are these really the same thing with shared identity and common behavior?
- Or is “user” just a label hiding distinct responsibilities?

Possible outcomes:

- Keep one User plus attached roles
- Create subtypes like Customer, Employee, Vendor
- Separate identity from role assignment

The right choice depends on whether behavior truly differs.

## Step 11: Introduce inheritance only when behavior genuinely generalizes

Do not reach for inheritance early.

Use inheritance when you see:

- repeated structure
- repeated behavior
- true “is-a” semantics
- subtype substitution makes sense

For example:

```
PaymentMethod
+ authorize(amount)
+ capture(amount)

CreditCardPayment
+ authorize(amount)
+ capture(amount)

PayPalPayment
+ authorize(amount)
+ capture(amount)
```

Here, an abstract base type may make sense:

```
abstract PaymentMethod
- methodId
+ authorize(amount)
+ capture(amount)
```

Subtypes:

- CreditCardPayment
- BankTransferPayment
- DigitalWalletPayment

This works if all of them can stand in for the abstract concept cleanly.

**Do not use inheritance just because fields look similar.** Shared fields alone do not justify inheritance.

## Step 12: Use abstract classes or interfaces when the shared contract matters

Start thinking about abstractions when you see common behavior but variant implementation.

Examples:

- PaymentMethod
- DiscountPolicy
- NotificationChannel
- ShipmentStrategy

For example:

```
abstract DiscountPolicy
+ calculateDiscount(order)

SeasonalDiscountPolicy
BulkDiscountPolicy
MemberDiscountPolicy
```

This is useful when the system needs to apply different behaviors interchangeably.

That is often a sign that the domain contains a family of rules or strategies.

A good abstraction appears when the language becomes:

- “any kind of…”
- “different types of…”
- “depending on the policy…”
- “various methods of…”

## Step 13: Prefer composition when behavior varies by part, not by identity

A classic OO improvement is recognizing when inheritance is the wrong tool.

Suppose you start with:

- PremiumCustomer
- StandardCustomer
- GuestCustomer

That may be okay, but often what really varies is pricing, privileges, or access rules.

Then composition is often better:

```
Customer
- membership : MembershipType
- discountPolicy : DiscountPolicy
```

Instead of making a deep subtype tree, keep Customer stable and plug variable behavior into collaborators.

That keeps the model more flexible and less brittle.

## Step 14: Model state transitions explicitly when rules depend on time or sequence

If the document includes rules like:

- submitted requests can be approved or rejected
- approved requests can be fulfilled
- rejected requests cannot be fulfilled
- expired memberships cannot renew automatically

Then state matters.

At that point, often model:

- an explicit status enum for simple cases
- a dedicated state abstraction for more complex cases

**Simple:**

`RequestStatus = Draft, Submitted, Approved, Rejected, Fulfilled`

**Complex:**

```
abstract RequestState
+ submit()
+ approve()
+ reject()
+ fulfill()
```

Use the more elaborate state model only when transitions are numerous and behavior changes materially by state.

## Step 15: Re-read the next section and refine the model, not restart it

This is the “expand thinking one step at a time” part.

Do not try to solve the whole domain in one pass.

Instead:

- read a section
- extract concepts
- update the class model
- test against prior assumptions
- split, merge, or generalize as needed

So the model grows progressively.

For example, an early pass may give:

- Order
- Customer
- Payment

Later, a section on returns may reveal you really need:

- ReturnRequest
- Refund
- ReturnItem
- ReturnPolicy

That does not mean the first pass failed. It means the model is deepening.

**Good OOAD is iterative clarification.**

## Step 16: Use tension as a signal

Certain tensions tell you the model needs adjustment.

**Tension 1: Too many booleans**

If a class has fields like:

- isPaid
- isShipped
- isCanceled
- isReturned
- isArchived

that often means lifecycle is under-modeled. Maybe you need a state model, or separate transaction objects.

**Tension 2: Too many optional fields**

If half the fields are null depending on type, that often means hidden subtypes or separate classes are needed.

**Tension 3: Repeated conditionals**

If code repeatedly checks type, status, or category, there may be missing polymorphism.

**Tension 4: One class talks about several unrelated timelines**

If one object is tracking billing, shipping, auditing, and permissions, it is probably too broad.

## Step 17: Ask “what changes together?”

This is one of the best ways to decide when to split a class.

If two groups of properties and operations tend to change for different business reasons, they probably do not belong in the same class.

Example: Employee might initially include:

- personal details
- payroll settings
- security permissions
- performance reviews

Those often change for different reasons and under different rules.

That may suggest:

- Employee
- PayrollProfile
- AccessProfile
- PerformanceRecord

This is a strong OOAD move because it aligns the model with actual business volatility.

## Step 18: Validate with scenarios, not just diagrams

Once you have a first model, test it against realistic flows.

Example scenarios:

- customer places order
- order is paid
- order is shipped
- shipped order cancel attempted
- refund requested after delivery

Then ask:

- Which object receives each request?
- Which object enforces the rule?
- Which relationships are traversed?
- Is any object doing too much?
- Are any rules orphaned outside the model?

A class diagram can look neat and still be weak. **Scenarios expose weak ownership and misplaced behavior.**

## Step 19: Refine names until the language feels exact

Naming is analysis.

Bad names hide bad modeling.

Push names toward precision:

- Item → OrderItem
- Info → CustomerProfile
- Manager → maybe split into ApprovalPolicy, AssignmentService, WorkflowCoordinator
- Data → almost always a smell

When names improve, responsibilities usually improve too.

## Step 20: Produce the model in layers

By the end, usually express the result in four layers:

1. **Core classes** — The main business entities and value objects
2. **Responsibilities** — What each class owns
3. **Relationships** — Associations, composition, multiplicity
4. **Behavior and rules** — Operations, invariants, state changes, subtype behavior

That gives a model that is readable and testable.

When you communicate structure visually in chat or plain text, **draw class diagrams in ASCII** using the notation below so relationship kinds stay unambiguous.

## ASCII class diagrams — notation

Use **box-and-line** ASCII so readers can tell **classes, abstract classes, interfaces, enums**, and **each UML-style relationship** apart. Prefer **stereotypes** in the top compartment (`<<interface>>`, `<<abstract>>`, `«interface»`) and **consistent line glyphs** for links.

### Classifier boxes (what kind of type)

Put the **name** in the top row; optional **stereotype** above or beside the name. Second compartment: attributes; third: operations (use `+` public, `-` private, `#` protected if useful).

| Kind | How to mark it in ASCII |
|------|-------------------------|
| **Concrete class** | Plain name, or stereotype `«class»` if you need contrast in a busy diagram. |
| **Abstract class** | `<<abstract>>` / `«abstract»` in the header, or prefix name: `*OrderProcessor*` (italic unavailable in plain text). Prefer `<<abstract>> ClassName`. |
| **Interface** | `<<interface>> Name` or `«interface» Name` on its own line in the box header. |
| **Enumeration** | `<<enumeration>> Status` with literals listed (`PENDING`, `OK`, …) or `«enumeration»`. |
| **Value object / datatype** | Optional `<<value object>>` or `<<VO>>` when distinguishing from entities. |

**Example — interface vs concrete class (boxes):**

```
+--------------------------+       +---------------------------+
| <<interface>>            |       | <<abstract>>              |
|    Payable               |       |    Document               |
+--------------------------+       +---------------------------+
| + getAmount(): Money     |       | # id: Id                  |
| + isPaid(): bool         |       | + summary(): String       |
+--------------------------+       +---------------------------+
         ^                                    ^
         |                                    |
         | (see Realization vs Generalization)| (subclasses below)
```

### Relationship lines (edges) — legend

Use these **line shapes** consistently. **Multiplicity** goes at the ends (`1`, `0..1`, `*`, `1..*`, `0..*`). **Role names** go beside the line if needed (`employer`, `items`).

| Meaning | ASCII pattern | Notes |
|--------|----------------|--------|
| **Generalization** (inheritance, **is-a**) | `----\|>` or vertical tree with `^` | Solid line; **hollow triangle** points to **superclass** / base. Child **extends** parent. |
| **Realization** (implements interface) | `..|>` or `-.->` with `|>` | **Dashed** line; hollow triangle points to **interface**. Class **implements** contract. |
| **Association** (knows / links) | `----------` | Plain structural link. Add arrow `------->` if navigation matters one way. |
| **Directed association** | `--------------->` | Clear “uses / navigates to” direction. |
| **Aggregation** (weak whole–part, **shared**) | `o------------` | **Hollow diamond** on the side of the **whole** (“has a”, part can outlive whole). |
| **Composition** (strong whole–part, **not shared**) | `*------------` | **Filled diamond** on the **whole** side; part lifecycle tied to whole. |
| **Dependency** (uses temporarily) | `- - - - ->` or `······>` | **Dashed** arrow; weaker than association (parameter, local, brief use). |

**Triangle direction:** In one-line form, put the **triangle against the target**: `Subclass ----|> Superclass` and `Impl ..|> <<interface>> Service`.

**Quick reference (horizontal):**

```
Realization:        ConcreteCls ..|> <<interface>> IPort
Generalization:     SubClass ----|> BaseClass
Association:        Customer -------- Order
Directed:           Order --------> Payment
Aggregation:        Dept o-------- Employee     (many employees per dept; employee can move)
Composition:        Order *-------- OrderItem    (items belong to one order)
Dependency:         ReportGenerator - - - -> PdfWriter
```

### Vertical layout (when wide diagrams wrap badly)

Stack **supertype above subtype**; use `^` / `|` for inheritance:

```
+-------------------+
| <<interface>>     |
|    Readable       |
+-------------------+
         ^
         |  ..|>   realization
         |
+-------------------+
| <<abstract>>      |
|    Report         |
+-------------------+
         ^
         |  ----|> generalization
         |
+-------------------+
| SalesReport       |
+-------------------+
```

Mix **horizontal** links for peer associations:

```
  Customer                Order
+----------+            +----------+
| +id      |   1    *  | +id      |
+----------+------------+----------+
      \______________/
           places
```

### Same diagram — mixed relationships (worked ASCII)

```
                    <<interface>>
                    DiscountPolicy
                    + calc(o: Order): Money
                          ^
                          | ..|>
          +---------------+---------------+
          |                               |
   SeasonalDiscount                 BulkDiscount
   + rate: Percent                 + threshold: int

   Customer 1 -------- * Order
       |                    |
       |                    | * (composition)
       |                    v
       |              +----------+
       |              | OrderItem|
       |              +----------+
       |                    |
       +--------------------+
            0..1  owns
       (optional account link, etc.)

   Order --------> 1 Payment
   Order - - - -> PricingService   (dependency: looks up quotes)
```

### Rules for the agent

- **Always label** realization (`..|>`) **differently** from generalization (`----|>`) so interfaces are not confused with superclasses.
- Prefer **`<<interface>>`** on the interface box; use **`<<abstract>>`** on abstract classes.
- When multiplicity matters for the domain, **write it** (`1`, `*`, `0..1`) at the ends.
- For **composition vs aggregation**, choose `*` vs `o` on the **whole** side only; keep the diamond on the container.

## A miniature worked example

Take this tiny spec:

> Members can borrow up to five books. Reference books cannot be borrowed. A loan lasts 14 days. Librarians can mark books as lost or removed. Overdue loans incur fines.

### First extraction

**Nouns:** Member, Book, ReferenceBook, Loan, Librarian, Fine

**Verbs:** borrow, mark lost, remove, incur

**Rules:**

- member can borrow up to five books
- reference books cannot be borrowed
- loan lasts 14 days
- overdue loans incur fines

### First candidate model

Member, Book, Loan, Librarian, Fine

### Early relationships

- Member has many Loans
- Loan references one Book
- Loan belongs to one Member
- Loan may produce one Fine

### Properties and operations

**Member**

- memberId
- activeLoans
- canBorrow()
- borrow(book)

**Book**

- bookId
- title
- status
- isBorrowable()

**Loan**

- loanId
- member
- book
- borrowedOn
- dueOn
- isOverdue()
- calculateFine()

**Librarian**

- employeeId
- markLost(book)
- remove(book)

### Refinement

Notice “reference books cannot be borrowed.”

Do you need a ReferenceBook subtype? Maybe.

If borrowability differs by book type, one option is:

```
abstract Book
+ isBorrowable()

CirculatingBook
+ isBorrowable() = true

ReferenceBook
+ isBorrowable() = false
```

That is a reasonable inheritance use because behavior changes by subtype.

But another option is composition:

```
Book
- circulationPolicy
+ isBorrowable()
```

If there are many policy variants, composition may be better.

### Another refinement

Fines may become more complex:

- grace periods
- different rates
- waived fines

Then `Loan.calculateFine()` may become too heavy, and you split out:

- FinePolicy
- Fine

Now the model is growing in a controlled way.

## The practical mindset to use throughout

At every step, keep asking:

- What is the real thing here?
- What responsibility belongs where?
- Is this concept an object, a value, a role, a policy, or a state?
- Is this class cohesive?
- Are these rules enforced inside the model?
- Is inheritance truly justified?
- Would composition keep this simpler?
- Does this model survive real scenarios?

That is the thought process.

**OOAD is less about drawing boxes quickly and more about discovering stable responsibility boundaries.**

If you want, take a short paragraph of specs and demonstrate this exact process live, step by step, turning it into a class model.

### Battle-test example (messy spec)

The repo includes a deliberately **inconsistent, typo-laden ~1–2 page draft** to exercise extraction, naming, and modeling: **`examples/garbled-payments-spec.md`** (payments: local/global, many methods, frontend/redirect fulfillment, idempotency, partial capture/refunds, open questions). Use it to stress-test steps 1–20 and ASCII diagrams.

Each worked example aligns with **abd-maps-models-specs** **continual refinement** ([`domain-model.md`](../abd-maps-models-specs/content/parts/library/domain-model.md)): Steps 1–4 stay pre-notation; from Step 5 onward, add formal **`- <type> property`** / **`operation(...) → return`** lines where helpful, with **`**newly added**`** on lines **first introduced** in that step file. Re-render **`map-model-class-diagram.drawio`** when the promoted **`map-model-spec.json`** changes ([`class-diagram-from-spec.md`](../abd-maps-models-specs/content/parts/library/class-diagram-from-spec.md)).

Each step file ends with **`## Prompt`**: **validate and fix when you find problems** (bloat, boundaries, invariants, drift, conflicts, robustness) — update the model or record explicit debt before moving on.

**Worked examples by step name (not step number)** — same **`garbled-payments-spec.md`** thread:

| Step | File |
|------|------|
| 1 | **`examples/nouns-verbs-rules-and-states.md`** |
| 2 | **`examples/raw-candidate-list.md`** |
| 3 | **`examples/thing-vs-data-about-a-thing.md`** |
| 4 | **`examples/responsibilities-before-operations.md`** |
| 5 | **`examples/add-properties-semantically-tight.md`** |
| 6 | **`examples/turn-verbs-into-operations.md`** |
| 7 | **`examples/relationships-and-cardinality.md`** |
| 8 | **`examples/invariants-in-the-model.md`** |
| 9 | **`examples/watch-for-bloated-classes.md`** |
| 10 | **`examples/smashed-abstractions-and-hidden-roles.md`** |
| 11 | **`examples/inheritance-when-behavior-generalizes.md`** |
| 12 | **`examples/abstract-classes-and-interfaces.md`** |
| 13 | **`examples/prefer-composition.md`** |
| 14 | **`examples/model-state-transitions.md`** |
| 15 | **`examples/iterative-refinement.md`** |
| 16 | **`examples/tension-as-a-signal.md`** |
| 17 | **`examples/what-changes-together.md`** |
| 18 | **`examples/validate-with-scenarios.md`** |
| 19 | **`examples/refine-names.md`** |
| 20 | **`examples/model-in-layers.md`** |
