# Nouns, verbs, rules, and states

**Skill:** abd-ooad — matches **Step 1: Read for nouns, verbs, rules, and states** in `SKILL.md`.

At this stage we do **not** decide which nouns become classes — only mark candidates and tensions.

For the full anchor definition and the three-part anchor test — see `anchors` in this library.

---

## Anchor boundaries under test

Step 1 is the first time anchors are tested by the full vocabulary of the source. As you extract nouns and verbs, actively watch for:

- **Evidence that supports an anchor** — terms that clearly belong inside an anchor's module frame (future supporting classes or properties of the core class)
- **Evidence that challenges an anchor** — a term that is referenced independently by multiple other concepts, suggesting it may need to be elevated to its own anchor
- **Evidence that an anchor should be split** — the core class is doing two different things and the nouns in this pass separate cleanly into two groups

Do not restructure anchors mid-step. Record any anchor boundary questions in the term registry (`Status: Ambiguous`, note the challenge). Evaluate at the `candidate-list` (CANDS) step.

**At the end of Step 1, re-apply the anchor test** (from `anchors.md`) to any anchor whose boundary was challenged. Promote, demote, or split if the test now fails. Update the term registry and diagram accordingly before proceeding.

---

## Term registry ↔ slice mapping (`Anchor` column)

After (or while) you produce **domain noun–verb** extraction per **slice** (e.g. S1 = first strategy section / chapter folder), write it to **`domain-noun-verb.md`** in the active workspace’s `abd-ooad/` folder (one file per workspace; use slice subfolders if you split by source slice). Align each **`term-registry.md`** row with the evidence file:

| Artifact | Role |
|----------|------|
| **`term-registry.md`** | SCAN **type** decisions: Classification, Confidence, Status, Notes — sparse. |
| **`…/domain-noun-verb.md` (per workspace or per slice folder)** | Phase-2 **evidence**: candidate nouns, verbs, rules, states. Prefer grouping **by anchor** (same headings as `strategy.md`). |

**`Anchor` column (single HTML column in the registry table)** — one code cell per term, **slice-keyed**:

- **`S1=<heading>`** — primary heading in **slice 1**’s `domain-noun-verb.md` where this term is evidenced (`Character`, `Check`, `Condition`, `Effect`, or your anchor names). Use **`S1=—`** if that term has **no** hook in slice 1.
- **Optional suffix** on the same `S1=` value when evidence is thin: **`(partial)`**, **`(gaps)`**, or combine anchors as **`Character+Effect`** when the text really spans both.
- **`S2=…`** — add **only when slice 2 exists** (second slice’s evidence file, or a second `domain-noun-verb.md` in another slice folder). Same pattern, e.g. `S1=Character; S2=Check` in one cell, or keep `S1=…` only until S2 is done. **Do not** add empty `S2=—` placeholders before slice 2.

**Traceability:** registry states **what** you claim; each slice’s `domain-noun-verb.md` holds **what the source said**. Rows should be defensible from `S1=` (and later `S2=`) where not `—`.

---

## Worked example — payments spec

> **Continual refinement:** This payments example uses the same "grow the model as you go" approach described in **[Domain model Markdown](../library/domain-model.md)**. **Tag:** **newly added** means this property or operation line appears for the **first time** in *this* step's file (so you can see the delta from the previous step). **Notation:** Steps 1–4 stay informal—bullets and prose only. Typed members start at **Step 5** (`- <type> property`, `operation(...) → return`).

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

- **Delta:** **pre-notation** — nouns, verbs, rules, states, tensions extracted from spec; no **`- <type> property`** lines yet (aligns with **Terms & mechanisms** / **shaped story map** in [Domain model Markdown](../library/domain-model.md).

---

## Action Checklist

- [ ] Have you extracted candidate nouns from every major section of the source material?
- [ ] Have you extracted domain verbs (actions, operations, state changes)?
- [ ] Have you identified at least three domain rules or constraints?
- [ ] Have you recorded lifecycle states for at least the key candidate classes?
- [ ] Have you noted synonyms, naming conflicts, and scope boundary noise for later steps?
- [ ] Have you updated the term registry with all new terms found in this step?
- [ ] Have you set each row’s **`Anchor`** cell (`S1=…`; add **`S2=…`** only after slice 2 exists) to point at the right section heading in **`domain-noun-verb.md`**?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
