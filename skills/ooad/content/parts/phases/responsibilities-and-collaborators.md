# Responsibilities and collaborators

**Skill:** abd-ooad — **Phase-id:** `responsibilities-and-collaborators` (Stage 2 — Model, p4).

**Upstream:** `thing-vs-data-about-a-thing` (p4) — every class has a confirmed stereotype; no `?` carries into this phase.

For each surviving class, write **one sentence** saying what it is responsible for, then name its **collaborators** -- the other classes it calls or depends on. This is a CRC pass: write responsibilities before you name any methods or properties. A type must have a reason to exist beyond "the spec mentioned it."

> **Why this order matters:** Writing the responsibility statement forces higher-order thinking. Those sentences are then refined into first-class operations with return types, parameter types, and supporting properties -- or they reveal that a supposed class is really a property or policy.

---

## CRC pass format

For each class:

```
{{ClassName}}
  Responsible for: {{one sentence}}
  Not responsible for: {{what it deliberately excludes}}
  Collaborators: {{comma-separated class names it needs}}
```

Record each responsibility in `term-registry.md` using Notes labels (see below). If a responsibility is unclear or contested, add a `Tension` note immediately rather than carrying ambiguity forward.

---

## Payments example

### Payment (aggregate root)

**Responsible for:** Representing one payment attempt and enforcing lifecycle transitions from initiation through authorization, capture, settlement, and failure -- including idempotency and invariants that prevent illegal state moves.

**Not responsible for:** Cart and coupon rules; fulfillment; PSP wire protocol; dispute lifecycle end-to-end.

**Collaborators:** RoutingContext, PaymentMethodSelection, FeeBreakdown, ConnectorId, IdempotencyKey

---

### Refund

**Responsible for:** Representing a distinct money-back movement tied to an original payment, tracking its own approval and processing state.

**Not responsible for:** Re-implementing Payment's authorization pipeline.

**Collaborators:** Payment (via PaymentId reference)

---

### Dispute *(only if modelled in this BC)*

**Responsible for:** Tracking dispute identity, status, and links to payment / refund / external case ids.

**Not responsible for:** Merchant-of-record vs platform legal determination -- that is policy input; the model stores ownership role as data.

**Collaborators:** Payment, Refund

---

### AuditEntry

**Responsible for:** Recording one append-only fact -- a state transition with actor and timestamp -- and remaining immutable.

**Not responsible for:** Interpreting business rules; it records outcomes of decisions made elsewhere.

**Collaborators:** Payment (via PaymentId reference)

---

### Value objects (responsibility summary)

| Type | Responsible for |
|------|-----------------|
| **Money** | Invariants on amount + currency pairing. |
| **RoutingContext** | Holding the dimensions that gate connector choice; validating well-formed routing inputs. |
| **FeeBreakdown** | Representing fees shown or charged as a structured snapshot. |
| **PaymentMethodSelection** | Snapshot of what was chosen for this attempt -- kind + safe display metadata. |
| **IdempotencyKey** | Format and equality rules for client key. |

---

### Policies / domain services

| Concept | Responsible for |
|---------|-----------------|
| **ComplianceGate** | Answering whether a payer may proceed to method selection (country / sanctions checks). |
| **ConnectorCapability** | Answering whether partial capture, 3DS, etc. are allowed for this routing + method. |
| **FailureMapping** | Resolving FailureKind to user-visible message + support log category. |

---

## Carry forward to Step 6 (properties and operations)

Each responsibility statement maps directly to either a **property** (data the class must know) or an **operation** (behavior the class must provide). In the next phase, convert these sentences into typed members together -- properties first, then operations that exercise them.

---

## Responsibilities and collaborators -> term-registry.md

> Tag notes on the class model with `[p5]` -- see `templates/domain model template.md` for the full tag table.

Every class whose responsibility is clarified or challenged in this phase gets a row update in `term-registry.md`.

Common Notes labels added at this phase:

- `Classified - {{kind}} {{reason}}` -- when a class's category is confirmed (Entity, ValueObject, Policy, etc.)
- `Tension - **{{TensionName}}** {{what_is_ambiguous_or_conflicting}}` -- when responsibility ownership between classes or layers is unclear
- `Follow-up - {{question_or_action}}` -- deferred responsibility decisions

---

## Action Checklist

- [ ] Does every surviving class have a clear, named responsibility in one sentence?
- [ ] Have you listed collaborators for each class?
- [ ] Have you challenged each responsibility -- does it belong here or in an application service?
- [ ] Have you avoided assigning coordination or orchestration responsibilities to domain objects?
- [ ] Have you updated `term-registry.md` with `Classified` and `Tension` notes for this phase?
- [ ] Have you noted carry-forward items to Step 6 (properties and operations)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model before moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
