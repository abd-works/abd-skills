# Nouns, verbs, rules, and states — payments example

**Skill:** abd-ooad — matches **Step 1: Read for nouns, verbs, rules, and states** in `SKILL.md`.

**Source:** `garbled-payments-spec.md` (battle-test input).

At this stage we do **not** decide which nouns become classes—only mark candidates and tensions.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Section: What we need (high level)

### Nouns (candidates)

Buyer, seller, money, float, compliance, locality (local / global), country, rails, merchant account, FX, cross-border, mid rate snapshot, receipt, product matrix, payment types, card, debit, credit, prepaid, ACH, bank pull, wallet (instant push), wire, B2B, crypto pilot, region, admin checkbox, BNPL, Partner X, coming soon screen, frontend, happy path, user, method, fees, success, failure, PSP, redirect, 3DS, bank login, browser, in-app webview, fulfillment, order, digital goods, physical SKUs, warehouse, download link, Ops, event `payment.settled`, payments team.

### Verbs (candidates)

Take (money), get (money to sellers), hold (float), apply (FX), show (mid rate on receipt), route (BNPL), pick (method), see (fees), confirm, fulfill (happy path), open (browser/webview), complete (auth), emit (event), pick (warehouse) …

### Rules (constraints / invariants — as stated or implied)

- Do not hold float longer than compliance allows (vague threshold).
- Local vs global affects rails and whether FX applies; legal wants mid rate on receipts (conflicts with earlier “FX is someone else’s problem”).
- Crypto only where admin allows region.
- Do not promise BNPL until Partner X signs; until then show “coming soon.”
- For physical SKUs: emit `payment.settled` before warehouse picks (ordering constraint).
- For digital: sometimes emit before download link — **conflicting** guidance.
- Cart: if payment fails after tax shown, must not double-apply coupons (cross-team rule touching checkout).

### States (lifecycle / change over time)

- Payment / money movement: implied flow from initiation → authorization/capture → settlement; partial capture with remainder release mentioned.
- Checkout UX: method selection → fee display → confirmation → success or failure.
- Redirect flows: user may abandon 3DS / webview.
- “Local” definition unstable: currency-based vs merchant-entity-based (conceptual state of the **classification** itself).

---

## Section: Rules that came up in meetings (unordered)

### Nouns

Idempotency key, client, server, charge, card rails, marketplace, auth, capture, remainder, refund, reason code, chargeback, sanctioned country list, payer, method selection UI, subscription, webhook, billing, events.

### Verbs

Retry, send (`Idempotency-Key` header), double-charge (forbidden), expire (keys — duration disputed), hold, capture, release, refund (full/partial), block (sanctioned users), subscribe (billing, later).

### Rules

- Server must not double-charge for same idempotency intent.
- Idempotency key TTL: **24h vs 72h — unresolved.**
- Partial capture only on card rails that support it; else full capture only.
- Refunds need reason codes for chargeback prep.
- Block sanctioned payers **before** method selection, not after.
- Subscriptions out of scope but webhook shape must stay stable for future billing.

### States

- Idempotency key: valid → expired? (timeline unclear)
- Capture: authorized → partially captured → remainder released?
- Refund: full vs partial paths

---

## Section: Local vs global (still fuzzy)

### Nouns

Currency, storefront, merchant legal entity, engineering assumption, PSP connector, FX quote id, intent object, tax, checkout, cart, coupon.

### Verbs

Gate (connector), run (connector), display (tax).

### Rules

- Global: FX quote id on intent (nullable).
- Tax displayed on checkout; payments does not compute tax.

### States / tension

- “Local” is **not** one stable notion — slides used two definitions.

---

## Section: Failure modes (fragmentary)

### Nouns

Timeout, webview, funds, issuer, fraud score, velocity limit, billing zip, 3DS, user-visible message, log category, support.

### Verbs

Close (webview), decline, block, abandon (friction).

### Rules

- Each failure type should map to user-visible message + support log category — **not all mapped.**

### States

- User journey: in redirect → abandoned vs returned.

---

## Section: Non-functional / misc

### Nouns

Audit log, PaymentIntent, Session (naming TBD), state transition, actor (`system` | `user` | `psp_webhook`), performance, pilot demo, sample flow list (browse → pay → fail → retry).

### Verbs

Append (audit), measure (p95 initiate).

### Rules

- Every PaymentIntent (or Session) state transition → append-only audit with actor.
- p95 initiate &lt; 300ms excluding network — **measurement point undefined.**

### States

- PaymentIntent / Session: arbitrary transition graph referenced but not enumerated in spec.

---

## Section: Open questions

### Nouns

Dispute lifecycle, merchant of record, platform, offline payment, cash, partner location, MVP, schema field.

### Verbs

Own (dispute), remove, hide (field).

### Rules / tension

- Dispute ownership: Risk vs eng — **unresolved.**
- Offline payments: out of MVP scope but field in schema — remove or hide?

---

## Cross-cutting observations (still Step 1 only)

- **Synonym pile:** paymnts system, PSP, rails, connector, Intent vs Session — naming debt.
- **Boundary noise:** payments vs cart vs warehouse vs digital fulfillment — verbs span teams.
- **Conflicts:** idempotency TTL; digital emit timing; local definition; dispute owner — good fuel for later steps (classes, responsibilities).

---

## Continual refinement (this step)

- **Delta:** **pre-notation** — nouns, verbs, rules, states, tensions extracted from spec; no **`- <type> property`** lines yet (aligns with **Terms & mechanisms** / **shaped story map** in [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md).

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
