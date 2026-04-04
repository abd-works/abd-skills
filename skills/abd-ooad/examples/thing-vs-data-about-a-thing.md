# Thing vs data about a thing — payments example

**Skill:** abd-ooad — matches **Step 3: Separate “thing” from “data about a thing”** in `SKILL.md`.

**Upstream:** `raw-candidate-list.md` (Step 2), `garbled-payments-spec.md`.

For each concept, ask:

- Does it exist **independently**?
- Can two instances be distinguished by **identity**?
- Does it **own behavior** (invariants, lifecycle)?
- Can it **change independently** of another object?

If **no** to most of these → prefer **property**, **value object**, **enum**, or **helper** — not a heavyweight entity.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Likely aggregate / entity (identity + lifecycle + rules)

| Concept | Rationale | Notes |
|---------|-----------|--------|
| **Payment** (or **PaymentIntent** as root name) | One logical “payment attempt” per checkout path; state transitions, audit, idempotency attach here. | **Session** in the spec sounds like the same aggregate with a different label — merge naming in Step 4+. |
| **Refund** | Own lifecycle (full/partial, reason codes); ties to chargeback prep; distinct id from original payment. | May be **entity** under or linked to Payment — decomposition in later steps. |
| **Dispute** | If modeled in this BC: own lifecycle; **who owns it** (platform vs MoR) affects associations, not whether it’s a thing. | If disputes live entirely in Risk’s BC, only a **reference id** here. |
| **AuditEntry** (or event log row) | Append-only record; identity = log id; immutable fact. | Often modeled as **domain event** + store rather than rich entity — still has identity. |

**Order** (checkout order): identity and lifecycle **belong to order/fulfillment BC**. In payments, usually **`orderId` reference + events** — not a second Order aggregate inside payments.

---

## Value objects (no independent lifecycle; equality by value / snapshot)

| Concept | Why VO |
|---------|--------|
| **Money** | Amount + **Currency**; invariants (scale, not negative where inappropriate). Not “just a decimal.” |
| **Currency** | Code (ISO); often VO or enum-backed; comparisons and formatting rules. |
| **FxQuoteRef** | Nullable **FX quote id** on global flows — reference/snapshot handle, not the FX engine. |
| **MidRateSnapshot** | What legal wants **on receipt** — immutable stamp (rate, timestamp, pair?) at settlement/display time. |
| **FeeBreakdown** | “Fees (if any)” before confirm — line items or total; structure TBD but **snapshot** on intent. |
| **ReasonCode** | Enum or small VO for refund/dispute **reason** — not a class per reason. |
| **RoutingContext** (working name) | **Currency + merchant region** (per eng assumption) gates connector — dimensions, not “Local” as a vague noun. Replaces unstable “local vs global” **as a single named VO** once defined. |
| **IdempotencyKey** | Client string + maybe **first-seen instant** — often **embedded in Payment** as VO or string with validation; separate “IdempotencyKey entity” only if keys are reused across payments (rare). |
| **PaymentMethodSelection** | Chosen method **kind** + rail-specific **non-sensitive** metadata (last4, brand) — snapshot on intent; **not** full PAN (token lives at PSP). |

---

## Enums (closed set of states / kinds)

| Concept | Why enum |
|---------|----------|
| **PaymentMethodKind** | Card debit/credit/prepaid, ACH, wallet, wire, crypto, BNPL (when available). |
| **PaymentState** (name TBD) | Created → authorized → captured → settled → failed → … (spec doesn’t enumerate; you will in Step 14+). |
| **CaptureMode** | Full vs partial-capable **for this rail** — may be bool + enum from connector capability. |
| **ActorKind** (audit) | `system` \| `user` \| `psp_webhook` — already in spec. |
| **FailureKind** (for mapping) | Timeout, insufficient funds, issuer decline, … — drives **message + log category** lookup. |

---

## Properties / attributes (hang off aggregate or VO)

| Concept | Placement |
|---------|-----------|
| **Merchant account id**, **region**, **storefront id** | On Payment or **RoutingContext** / merchant ref — not re-modeling full **Merchant** if identity lives elsewhere. |
| **BNPL “coming soon”** | Feature flag or **ProductMatrix** config — not a domain class named BNPL. |
| **Crypto allowed for region** | Config row or admin flag — **policy input**, could be `RegionPolicy` VO or table. |
| **Sanctioned country** | List **outside** aggregate or **CountryCode** VO + **ComplianceGate** policy — block list is **data + rule**, not a “SanctionedCountry” entity per country. |

---

## Policy / registry objects (behavior without classic entity lifecycle)

| Concept | Shape |
|---------|--------|
| **Sanctions / eligibility gate** | **Policy** or **domain service**: `canSelectPaymentMethod(payerContext)` — **not** a “Sanction class.” |
| **Partial capture allowed** | Capability on **Rail** or **Connector** config — `supportsPartialCapture: bool`. |
| **Failure → user message + log code** | **Registry** or strategy map: `FailureKind` → `UserMessage` + `SupportCategory`. |
| **Idempotency TTL** | **24h vs 72h** — **configuration** until spec aligns; not a class. |

---

## Not classes in the core domain model (boundaries / org / UI)

| Concept | Treatment |
|---------|-----------|
| **Frontend**, **browser**, **webview** | **Adapters** / application layer; **RedirectSession** might be a **VO** (id, return URL) if you need to track abandon vs complete. |
| **PSP** (as company) | **Connector** is often **configuration + adapter**; domain names **PaymentRail** or **ConnectorId** + capabilities. |
| **Ops**, **Cart team**, **Support** | **Actors** in use cases; **Support** failure mapping is **policy/registry**, not a `Support` class. |
| **Platform vs Risk** | **Organizational ownership** of disputes — affects **which BC** owns **Dispute**, not a `Platform` entity in payments. |
| **Offline cash** field | **Remove or boolean flag** on order/checkout — **not** MVP payment method class. |

---

## Sketch: one aggregate with supporting types (analogous to Order in the skill)

Working names only — refine in Step 4+.

```
Payment   <<aggregate root>>
- id
- idempotencyKey : IdempotencyKey   (or string with VO rules)
- orderRef : OrderId                (external BC)
- payerRef : PayerId
- merchantRef : MerchantId
- routing : RoutingContext          (VO: currency, region, …)
- amounts : Money
- fees : FeeBreakdown
- fxQuoteRef : FxQuoteRef?          (nullable)
- method : PaymentMethodSelection
- state : PaymentState
- receiptSnapshot : MidRateSnapshot?  (when legal requires)
- audit : AuditEntry*               (or events projected)

Refund
- id
- paymentRef : PaymentId
- amount : Money
- reason : ReasonCode
- state : …
```

**Value objects** embedded: `Money`, `RoutingContext`, `FeeBreakdown`, `FxQuoteRef`, `MidRateSnapshot`, `PaymentMethodSelection`, `IdempotencyKey`.

**Enums**: `PaymentState`, `ReasonCode` (or subset), `PaymentMethodKind`, `FailureKind` (for mapping).

---

## Tensions resolved or deferred

| Tension | Step 3 stance |
|---------|----------------|
| PaymentIntent vs Session | **One aggregate**; two names in spec = **rename**, not two roots. |
| Local vs global | **Not** an entity “LocalGlobal” — use **RoutingContext** VO + rules. |
| Cart / coupons | **Outside** payments aggregate; **invariant** enforced via integration test or saga, not `Cart` class here. |
| Digital vs physical emit order | **Domain event** `payment.settled` + **consumers** decide order — may stay **event-only** in payments BC. |

---

## Carry forward to Step 4 (responsibilities)

Next: assign **what each remaining aggregate/VO/policy owns** before naming operations.

---

## Continual refinement (this step)

- **Delta:** **pre-notation** — entity vs VO vs policy split (**Payment**, **Refund**, embedded **Money**, **RoutingContext**, etc.); sketches stay narrative until Step 5 formal properties.
---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
