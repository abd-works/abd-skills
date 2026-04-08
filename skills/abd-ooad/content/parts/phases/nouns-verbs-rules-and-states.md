# Nouns, verbs, rules, and states

**Skill:** abd-ooad — matches **Step 1: Read for nouns, verbs, rules, and states** in `SKILL.md`.

**What you produce:** **domain-noun-verb.md** on disk (one per source slice): structured extraction by anchor — one **## [AnchorName module]** per backbone anchor; **Candidate …** lists; **full** class boxes (`+` / **opt** / **Invariant:**) or pared **`### … : << … >>`** where the source supports it; **#### Note :** when useful.

Use **## Cross-anchor notes** for unsettled or cross-cutting hooks. The slice file is **domain content only** — do not paste skill paths, template filenames, or process-only labels into the artifact.

**Focus here:** candidates and tensions; which nouns become classes is decided in later steps.

For the full anchor definition and the three-part anchor test — see `anchors` in this library.

---

## Phase 2 deliverable — `domain-noun-verb.md` (normative)

**One file per slice:** **domain-noun-verb.md** in the **slice folder** (e.g. `abd-ooad/1 - basics-checks-conditions/`). Canonical Phase 2 extraction for that slice.

| Item | Rule |
|------|------|
| **Path** | `<workspace>/<slice-folder>/domain-noun-verb.md` |
| **H1** | `# <SliceLabel>: Noun Verb Domain` — **SliceLabel** from the slice plan or folder slug. |
| **Structure** | Per anchor: **## [Anchor module]** → **### Note :** → **Candidate …** lists → class boxes (**full** `+` / **opt** / **Invariant:** or pared **`### … : << … >>`**). Optional **## Cross-anchor notes**. |
| **Artifact body** | Domain content only — no skill paths, template filenames, or process meta in the file. |
| **Elsewhere** | Methodology and plans stay in **strategy.md** / **term-registry.md** / phase docs — not in the slice artifact. |
| **Phase 3 in the same file** | Optional: append bucket roll-up, watch list, and tensions to **domain-noun-verb.md** (see **raw-candidate-list** phase) instead of a second markdown file. |


Align **term-registry.md** **Anchor** cells (`S1=<heading>`) with the **`## [… module]`** headings in **domain-noun-verb.md**.


| Artifact                                 | Role                                                                                                                                                  |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **term-registry.md**                   | SCAN **type** decisions: Classification, Confidence, Status, Notes — sparse.                                                                          |
| **domain-noun-verb.md** (slice folder) | Phase 2 **evidence**: candidates and **full** class boxes **by anchor** (pared-down only in Cross-anchor / boundary notes), structured as above. |


**Anchor column** (single cell per term in the registry table) — one code cell per term, **slice-keyed**:

- **S1=<heading>** — primary anchor where this term is evidenced in **slice 1**, matching the **## [… module]** label in **domain-noun-verb.md** (e.g. `Character`, `Check`). Use **S1=—** if no hook in slice 1.
- **Optional suffix** on the same `S1=` value when evidence is thin: **(partial)**, **(gaps)**, or **Character+Effect** when the text spans anchors.
- **S2=…** — add when slice 2 exists; keep **`S2=—`** out of the registry until slice 2 is in play.

**Traceability:** the registry states **what** you claim; **domain-noun-verb.md** holds **what the source said**. Rows should be defensible from `S1=` (and later `S2=`) where not `—`.

---

## Anchor boundaries under test

Step 1 is the first time anchors are tested by the full vocabulary of the source. As you extract nouns and verbs, actively watch for:

- **Evidence that supports an anchor** — terms that clearly belong inside an anchor's module frame (future supporting classes or properties of the core class)
- **Evidence that challenges an anchor** — a term that is referenced independently by multiple other concepts, suggesting it may need to be elevated to its own anchor
- **Evidence that an anchor should be split** — the core class is doing two different things and the nouns in this pass separate cleanly into two groups

Keep the anchor set stable for this step. Record boundary questions in the term registry (`Status: Ambiguous`, note the challenge); resolve at **`candidate-list` (CANDS)**.

**At the end of Step 1, re-apply the anchor test** (from `anchors.md`) to any anchor whose boundary was challenged. Promote, demote, or split if the test now fails. Update the term registry and diagram accordingly before proceeding.

---

## Worked example — payments spec

> **Continual refinement:** Fictional payments thread. **newly added** = line first appears in this step’s file. Steps 1–4 stay informal; typed members start later.

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
- p95 initiate < 300ms excluding network — **measurement point undefined.**

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

- **Delta:** **pre-notation** — nouns, verbs, rules, states, tensions; typed members in later steps.

---

## Action Checklist

- Have you created **domain-noun-verb.md** in the slice folder with H1 `# <SliceLabel>: Noun Verb Domain`, anchors, Candidate lists, and class boxes — with methodology outside the slice file?
- Have you extracted candidate nouns from every major section of the source material?
- Have you extracted domain verbs (actions, operations, state changes)?
- Have you identified at least three domain rules or constraints?
- Have you recorded lifecycle states for at least the key candidate classes?
- Have you noted synonyms, naming conflicts, and scope boundary noise for later steps?
- Have you updated the term registry with all new terms found in this step?
- Have you set each row’s **Anchor** cell (`S1=…`; add **S2=…** only after slice 2 exists) to point at the right **slice** anchor in the slice’s **domain-noun-verb.md**?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.

