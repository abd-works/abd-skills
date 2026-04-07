# Raw candidate list — payments example

**Skill:** abd-ooad — matches **Step 2: Build a raw candidate list** in `SKILL.md`.

**Upstream:** `nouns-verbs-rules-and-states.md` (Step 1) and `garbled-payments-spec.md`.

This is still **loose**. Candidates may merge, split, or become attributes in later steps.

> **Continual refinement:** Full notation is in **[Domain model Markdown](../library/domain-model.md)** (*Domain concept* template; class definition and diagram refined together). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Worked example — from nouns-verbs to this step

**Upstream:** Step 1 (`nouns-verbs-rules-and-states.md`) produces **`domain-noun-verb.md`** (in the workspace `abd-ooad/` folder) — nouns, verbs, rules, and states, often grouped **by anchor** (same headings as `strategy.md`). Step 2 **does not** paste that file wholesale; you **re-sort** the same terms into the buckets below (entities, value-like concepts, processes, policies, roles, events) and add **why** each row might matter.

**Term registry:** As you promote terms to candidates here, keep **`Anchor`** in `term-registry.md` aligned: e.g. `S1=Check` for anything first evidenced under a **Check** heading in slice 1’s `domain-noun-verb.md` (see the **Term registry ↔ slice mapping** section in the nouns-verbs phase).

### Mini excerpt (hypothetical “rules” slice — one anchor)

Imagine one anchor section **Check** in `domain-noun-verb.md`:

| Kind | Extraction (illustrative) |
| ---- | ------------------------- |
| **Nouns** | Character, Check, DC, bonus, penalty, Condition, trait, die roll |
| **Verbs** | roll, compare, apply, succeed, fail, stack |
| **Rules** | Compare total vs DC; some bonuses don’t stack; Conditions can impose advantage/disadvantage |
| **States** | Check pending → resolved (success / failure / critical); Condition active vs cleared |

### Roll-up into Step 2 buckets (same terms, new shape)

| Step 1 term(s) | Likely Step 2 bucket | Notes |
| -------------- | -------------------- | ----- |
| Character, Check | **Core domain entities** | Durable “things” — may merge later (e.g. Check as operation vs aggregate). |
| DC, bonus, penalty | **Value-like concepts** | Often numbers + rules; may become VO / struct / enum. |
| “roll → compare → resolve” | **Processes or transactions** | End-to-end flow with a start/end. |
| stacking, advantage/disadvantage | **Policies or rules** | Eligibility and modifiers — may stay policy objects or plain rules. |
| player, GM (if in source) | **Roles** | Actors; may merge with user accounts later. |
| “Check resolved”, Condition applied | **Events or records** | Audit / history if the product cares about replay. |

### What you add in Step 2 that Step 1 didn’t require

- **Separation** — entity vs value vs process vs policy (Step 1 only *marked* candidates).
- **Tensions** — e.g. “Is **Check** a noun (object) or only a verb-shaped process?” — carry forward to `thing-vs-data-about-a-thing` / later steps.
- **Watch list** — terms that might collapse (e.g. “die roll” as part of Check, not its own class).

Use the **payments** tables below as a full-size reference thread; use this mini example when your domain is not payments but you still need a **template** for nouns-verbs → raw candidate list.

---

## Core domain entities (durable “things” in the problem space)


| Candidate                             | Why it might be an entity                                                              |
| ------------------------------------- | -------------------------------------------------------------------------------------- |
| **Payer** / **Buyer**                 | Initiates payment; may be blocked (sanctions).                                         |
| **Merchant** / **Seller**             | Receives funds; merchant account, region, legal entity.                                |
| **Order** (checkout context)          | Physical vs digital fulfillment hooks; not “owned” by payments but coupled via events. |
| **Payment** (aggregate root name TBD) | Money movement, lifecycle, ties to rails.                                              |
| **PaymentIntent** *or* **Session**    | Spec names both — **one concept, two labels**; holds amount, method choice, state.     |
| **Marketplace**                       | Partial capture, hold auth — marketplace-style semantics mentioned.                    |
| **PSP connector** (per rail/region)   | “Which connector runs” for local/global.                                               |
| **Refund** (case)                     | Full/partial, reason codes, chargeback prep.                                           |
| **Dispute**                           | Open question who owns lifecycle — still a domain concern.                             |


---

## Value-like concepts (descriptive, may be VO / enum / struct)


| Candidate                      | Notes                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------ |
| **Money** / **Amount**         | Always paired with currency.                                                   |
| **Currency**                   | Storefront vs settlement; local/global gates.                                  |
| **FX quote id**                | Nullable on “intent” for global.                                               |
| **Mid rate snapshot**          | Receipt display — may be value stamped on receipt.                             |
| **Fees**                       | Shown pre-confirm; structure unspecified.                                      |
| **Idempotency key**            | Client-supplied; TTL disputed (24h vs 72h).                                    |
| **Reason code**                | Refunds / chargeback prep.                                                     |
| **Country** / **jurisdiction** | Sanctions, region gates.                                                       |
| **Payment method kind**        | Card variants, ACH, wallet, wire, crypto — may be enum + metadata.             |
| **Local vs Global**            | **Unstable** in spec — might be computed classification, not a stored “thing.” |


---

## Processes or transactions (flows with a start/end)


| Candidate                                          | Notes                                                                |
| -------------------------------------------------- | -------------------------------------------------------------------- |
| **Authorization → capture** (possibly **partial**) | Remainder release; card-rail-dependent.                              |
| **Settlement**                                     | `payment.settled` event — ordering vs warehouse / digital.           |
| **Refund**                                         | Full vs partial paths.                                               |
| **Redirect / 3DS / bank login**                    | Browser or webview session; abandon vs complete.                     |
| **Webhook handling**                               | PSP → platform; idempotent processing implied.                       |
| **Checkout attempt**                               | Method pick → fees → confirm → outcome (ties frontend “happy path”). |


---

## Policies or rules (eligibility, gates, capabilities)


| Candidate                        | Notes                                             |
| -------------------------------- | ------------------------------------------------- |
| **Sanctions / blocklist policy** | Block **before** method UI.                       |
| **BNPL availability**            | Partner X gate; “coming soon” route.              |
| **Crypto region gate**           | Admin checkbox per region.                        |
| **Partial capture capability**   | Per rail / card network — “only where supported.” |
| **Idempotency policy**           | No double-charge; key expiry **unresolved**.      |
| **Compliance / float limit**     | Vague — may become policy + clock on holds.       |


---

## Roles (actors in the domain or org)


| Candidate    | Notes                                                             |
| ------------ | ----------------------------------------------------------------- |
| **Payer**    | Same as buyer in retail story.                                    |
| **Merchant** | Receives payout; MoR question in disputes.                        |
| **Platform** | Assumed owner of some flows; **conflicts** with Risk on disputes. |
| **Admin**    | Region checkbox for crypto, product matrix.                       |
| **Support**  | Maps failures to messages + log categories.                       |
| **Ops**      | Conflicting email on digital vs physical **emit** ordering.       |


*(Roles may stay as actors only, or merge with user accounts — Step 3+.)*

---

## Events or records (things that happened / audit)


| Candidate                              | Notes                                                                                  |
| -------------------------------------- | -------------------------------------------------------------------------------------- |
| `**payment.settled`**                  | Domain event; consumers: warehouse, digital fulfillment.                               |
| **Audit entry**                        | Append-only; actor `system` | `user` | `psp_webhook`; every intent/session transition. |
| **Webhook payload** / **delivery log** | Billing wants stable shape for future subscriptions.                                   |
| **Chargeback / dispute record**        | Reason codes on refund; lifecycle owner TBD.                                           |


---

## Early “does it deserve a class?” (identity / behavior / lifecycle / relationships)

Ask for each hot candidate:


| Candidate               | Identity?                 | Behavior / lifecycle?  | Relationships?                                       | Tentative                            |
| ----------------------- | ------------------------- | ---------------------- | ---------------------------------------------------- | ------------------------------------ |
| PaymentIntent / Session | Yes — one per attempt     | Strong — state machine | Payer, merchant, order?, connector                   | **Likely core**                      |
| Idempotency key         | Yes — dedupe              | TTL, expiry            | Tied to intent                                       | **Likely** (or sub-object of intent) |
| PSP connector           | Yes — configured instance | Routes, capabilities   | Region, method                                       | **Likely**                           |
| Receipt                 | Yes for customer          | Immutable snapshot?    | Payment, rates                                       | **Maybe**                            |
| Failure mapping         | Cross-cutting             | Lookup                 | Failure kind → message + log code                    | **Policy** or **registry**           |
| Cart / coupon           | Mentioned                 | **Cart team**          | **Boundary** — may be **external** to payments model | Integrate, don’t duplicate           |


---

## Candidates likely to collapse or stay non-classes (watch list)

- **“Rails”** — might be attribute of connector or rail **type**, not a class per se.
- **“Frontend”** — presentation; behaviors surface as use cases, not a domain class.
- **“Ops / Cart team”** — organizational, not types.
- **Offline cash field** — schema smell; might be removed or hidden (flag), not a full entity in MVP.

---

## Tensions to carry into Step 3+

1. **PaymentIntent vs Session** — rename to one aggregate or two bounded contexts?
2. **Local** (currency vs legal entity) — one enum, two dimensions, or a **RoutingContext** value object?
3. **Dispute** — platform vs merchant of record affects where **Dispute** lives and associations.
4. **Digital vs physical** settlement ordering — may force **FulfillmentChannel** or events only (no class in payments).

---

## Continual refinement (this step)

- **Delta:** **pre-notation** — candidate entities, value-ish things, policies, and watch-list; **`**newly added**`** not used on formal lines until Step 5.

---

## Action Checklist

- [ ] Have you rolled up Step 1 nouns-verbs (per slice / anchor) into this step’s buckets (entities, values, processes, policies, roles, events)?
- [ ] Have you produced a raw candidate list with at least three entities and at least one value object?
- [ ] Have you separated entities from value objects (mutability, identity)?
- [ ] Have you flagged watch-list candidates (possible classes that need further evidence)?
- [ ] Have you noted tensions from the candidate list to carry into Step 3+?
- [ ] Have you updated the term registry with all candidate names?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
