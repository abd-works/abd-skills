# Responsibilities before operations — payments example

**Skill:** abd-ooad — matches **Step 4: Write responsibilities before operations** in `SKILL.md`.

**Upstream:** `thing-vs-data-about-a-thing.md` (Step 3), `garbled-payments-spec.md`.

Define **what each type is for** before naming methods. A type should have a reason to exist beyond “the spec mentioned it.”

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Payment (aggregate root)

**Responsible for:**

- Representing **one payment attempt** for a checkout (identity, idempotency correlation).
- **Tracking lifecycle** from initiation through authorization, capture, settlement, or failure — and refusing illegal transitions.
- **Recording** committed amounts, currency, routing context, chosen method snapshot, fees, and optional FX references **as known to this bounded context**.
- **Enforcing** payments-domain invariants: e.g. no double-settlement, capture rules consistent with rail capability, settlement only when business rules say so.
- **Emitting or staging domain facts** other systems need (e.g. `payment.settled`) at the right point in **this** model — without owning warehouse picking or digital download UX.
- **Coordinating** with idempotency: same client key must not create two distinct successful charges for the same intent.

**Not responsible for:**

- **Cart, tax, coupons** — other BCs; payments may **assume** prerequisites or react to failure signals, not own coupon rules.
- **Fulfillment** (warehouse, digital asset delivery) — **consumers** of events; payments does not pick SKUs or issue download links.
- **PSP wire protocol** — lives in infrastructure adapters; domain **decides** what must happen, adapters **call** PSPs.
- **Dispute lifecycle end-to-end** — unless this BC is chosen as owner; then only **that** slice (see Dispute).

---

## Refund

**Responsible for:**

- Representing a **distinct money-back movement** tied to an original payment (full or partial).
- **Recording** reason codes needed for chargeback / compliance **as required by policy**.
- **Tracking its own** approval / processing / completion or failure state **if** the business differentiates these from payment state.

**Not responsible for:**

- Re-implementing **Payment**’s authorization pipeline; it **references** the original payment and amounts.

---

## Dispute (only if modeled in this BC)

**Responsible for:**

- **Tracking** dispute identity, status, and links to payment / refund / external case ids **if** Risk and product agree this BC holds the aggregate.
- **Exposing** what downstream **needs** for customer service and reporting **without** duplicating full Risk analytics.

**Not responsible for:**

- **Merchant-of-record vs platform** legal determination — that is **policy/org** input; the model **stores** ownership role as data if needed, not **decides** it in code alone.

*If Dispute lives entirely in another BC, this BC only holds **external references** — no Dispute aggregate here.*

---

## AuditEntry (or equivalent immutable log row)

**Responsible for:**

- **Recording** one **append-only** fact: state transition (or domain event) with **actor** (`system` \| `user` \| `psp_webhook`) and timestamp.
- **Remaining immutable** — corrections are new entries or compensating events, not edits.

**Not responsible for:**

- **Interpreting** business rules; it **records** outcomes of decisions made elsewhere.

---

## Value objects (contract of what they “guard”)

| Type | Responsible for |
|------|-----------------|
| **Money** | Invariants on amount + currency pairing (scale, no mixed-currency math without conversion rules). |
| **RoutingContext** | Holding the **dimensions** that gate connector choice (e.g. currency + merchant region); validating **well-formed** routing inputs. |
| **FeeBreakdown** | Representing **fees shown or charged** as a structured snapshot (line items or totals), not recomputing tax. |
| **FxQuoteRef** / **MidRateSnapshot** | Holding **opaque** quote handle vs **immutable** receipt display snapshot — not sourcing live FX rates. |
| **PaymentMethodSelection** | Snapshot of **what** was chosen for this attempt (kind + safe display metadata), not storing secrets. |
| **IdempotencyKey** (if VO) | Format / equality rules for client key; may participate in “same attempt” logic. |

---

## Policies / domain services (behavior without owning payment row)

| Concept | Responsible for |
|---------|-----------------|
| **Compliance / sanctions gate** | Answering **whether** a payer may proceed to method selection **before** UI exposes rails (country / list checks). |
| **Rail / connector capability** | Answering **whether** partial capture, 3DS, etc. are allowed for this **routing + method** (from config). |
| **Failure mapping** | Resolving **FailureKind** → user-visible message + support log category (registry or policy). |
| **Webhook interpretation** (application service) | Mapping PSP payloads → domain commands / facts — **not** a god object; split by integration if large. |

---

## Boundary clarity (who owns “fulfill happy path”)

The spec says the **frontend** walks pick method → fees → confirm → success/failure. In OO terms:

- **Application / use-case layer** orchestrates **screens and adapters**.
- **Payment** aggregate still **owns** whether a transition is allowed and **what** gets recorded when the user confirms or when the PSP callback arrives.

So: **“fulfill happy path”** is a **scenario** cutting across UI + Payment + PSP; **responsibility** for **truth** of payment state stays in **Payment**, not in a class named `Frontend`.

---

## Carry forward to Step 5 (properties)

Next: list **properties per aggregate/entity** using **semantic tightness** — only what the object must know to fulfill these responsibilities, not every field the spec ever mentioned.

---

## Continual refinement (this step)

- **Delta:** **pre-notation** — responsibility paragraphs for **Payment**, **Refund**, **AuditEntry**, VOs, policies; formal **`- <type> property`** / **operation** lines start in Steps 5–6.

---

## Action Checklist

- [ ] Does every surviving class have a clear, named responsibility in plain English?
- [ ] Have you challenged each responsibility — does it belong here or in an application service?
- [ ] Have you avoided assigning responsibilities that are really coordination or orchestration to domain objects?
- [ ] Have you noted carry-forward items to Step 5 (properties)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
