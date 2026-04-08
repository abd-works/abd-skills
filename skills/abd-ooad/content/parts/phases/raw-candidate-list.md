# Raw candidate list

**Skill:** abd-ooad — Phase 3.

**What this phase does:** Sort vocabulary into **candidate kinds** — **entities**, **value objects**, **processes**, **policies**, **roles**, **events** — record **why** each candidate matters, early class smell, watch list, and tensions.

**Focus:** Separation and tensions. Value-object candidates may stay `<< ValueObject >>` / enum / struct until later phases.

---

## Deliverables — pick a shape (do not duplicate bucket tables twice)

**Two views of the same Phase 3 work:**

1. **Bucket tables (tabular pass)** — **`raw-candidate-list.md`** *or* the same sections **appended** to **`domain-noun-verb.md`**. Use **`templates/raw-candidate-list-template.md`**. Tables group rows under: entities, value objects, processes, policies, roles, events (+ early “deserves a class?”, watch list, tensions).

2. **Integrated class model (optional, separate file)** — **`domain-raw-candidates.md`**. Use **`templates/domain-raw-candidates-template.md`**. Here you **do not** repeat those bucket tables. Every candidate is a **`### Name : << Entity >>`** (or `<< ValueObject >>`, `<< Process >>`, `<< Policy >>`, `<< Role >>`, `<< Event >>`, or `<< >>`) under **`## [Anchor module]`**, with members and **`#### Note :`**. Material that does not fit one class goes in **`## Cross-anchor`** or **`## Appendix …`**.

**Rule:** If both **`raw-candidate-list.md`** and **`domain-raw-candidates.md`** exist, the **tables live in one place only** (usually **`raw-candidate-list.md`**). The integrated file **links** to it if needed; it does **not** re-paste bucket tables (“Entities”, “Value objects”, …).

**Artifact body:** Domain content only. **Do not** put **`Source:`** / **`Slice:`** / **`OOAD phase:`** / registry **`Step`** / **`Upstream:`** / **`Pre-notation:`** / **`Integrated model:`** boilerplate in slice files.

---

## Illustrative shape

Re-sort **Candidate …** material from the slice’s Phase 2 file into the buckets used in the worked examples below.

### Mini excerpt (hypothetical “rules” slice — one anchor)

Imagine one anchor section **Check** in the slice’s **domain-noun-verb.md**:

| Kind      | Extraction (illustrative)                                                                 |
| --------- | ----------------------------------------------------------------------------------------- |
| **Nouns** | Character, Check, DC, bonus, penalty, Condition, trait, die roll                          |
| **Verbs** | roll, compare, apply, succeed, fail, stack                                                |
| **Rules** | Compare total vs DC; some bonuses don’t stack; Conditions can impose advantage/disadvantage |
| **States** | Check pending → resolved (success / failure / critical); Condition active vs cleared        |

### Roll-up into Step 2 buckets (same terms, new shape)

| Step 1 term(s)                       | Likely Step 2 bucket   | Notes                                                                 |
| ------------------------------------ | ---------------------- | --------------------------------------------------------------------- |
| Character, Check                   | **Entities**           | Durable “things” — may merge later (e.g. Check as operation vs aggregate). |
| DC, bonus, penalty                   | **Value objects**      | Often numbers + rules; may become VO / struct / enum.                 |
| “roll → compare → resolve”           | **Processes**          | End-to-end flow with a start/end.                                     |
| stacking, advantage/disadvantage     | **Policies**           | Eligibility and modifiers — may stay policy objects or plain rules.   |
| player, GM (if in source)            | **Roles**              | Actors; may merge with user accounts later.                           |
| “Check resolved”, Condition applied | **Events**             | Audit / history if the product cares about replay.                    |

### What you add in Step 2 that Step 1 did not require

- **Separation** — entity vs value vs process vs policy (Step 1 *lists* candidates; Step 2 *sorts* them).
- **Tensions** — e.g. “Is **Check** a noun (object) or only a verb-shaped process?” — carry forward to **thing-vs-data-about-a-thing** and later steps.
- **Watch list** — terms that might collapse (e.g. “die roll” as part of Check, not its own class).

Use the **payments** tables below as a full-size reference thread; use this mini example when your domain is not payments but you still need a **shape** for nouns-verbs → raw candidate list.

---

## Worked example — payments spec

> **Continual refinement:** Fictional payments thread. **newly added** = line first appears in this step’s file. Steps 1–4 stay informal; typed members start later.

This thread still uses **garbled-payments-spec.md** as the fictional source alongside Step 1; it is **loose**. Candidates may merge, split, or become attributes in later steps.

---

## Entities (durable “things” in the problem space)


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

## Value objects (descriptive, may be VO / enum / struct)


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

## Processes (flows with a start/end)


| Candidate                                          | Notes                                                                |
| -------------------------------------------------- | -------------------------------------------------------------------- |
| **Authorization → capture** (possibly **partial**) | Remainder release; card-rail-dependent.                              |
| **Settlement**                                     | `payment.settled` event — ordering vs warehouse / digital.           |
| **Refund**                                         | Full vs partial paths.                                               |
| **Redirect / 3DS / bank login**                    | Browser or webview session; abandon vs complete.                     |
| **Webhook handling**                               | PSP → platform; idempotent processing implied.                       |
| **Checkout attempt**                               | Method pick → fees → confirm → outcome (ties frontend “happy path”). |


---

## Policies (eligibility, gates, capabilities)


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


*(Roles may stay as actors only, or merge with user accounts — later steps.)*

---

## Events (things that happened / audit)


| Candidate                              | Notes                                                                                  |
| -------------------------------------- | -------------------------------------------------------------------------------------- |
| **`payment.settled`**                  | Domain event; consumers: warehouse, digital fulfillment.                             |
| **Audit entry**                        | Append-only; actor `system` \| `user` \| `psp_webhook`; every intent/session transition. |
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
| Cart / coupon           | Mentioned                 | **Cart team**          | **Boundary** — may be **external** to payments model | Integrate at boundaries; avoid duplicating cart inside payments |


---

## Candidates likely to collapse or stay non-classes (watch list)

- **“Rails”** — might be attribute of connector or rail **type**, not a class per se.
- **“Frontend”** — presentation; behaviors surface as use cases, not a domain class.
- **“Ops / Cart team”** — organizational, not types.
- **Offline cash field** — schema smell; might be removed or hidden (flag), not a full entity in MVP.

---

## Tensions to carry into later steps

1. **PaymentIntent vs Session** — rename to one aggregate or two bounded contexts?
2. **Local** (currency vs legal entity) — one enum, two dimensions, or a **RoutingContext** value object?
3. **Dispute** — platform vs merchant of record affects where **Dispute** lives and associations.
4. **Digital vs physical** settlement ordering — may force **FulfillmentChannel** or events only (no class in payments).

---

## Continual refinement (this step)

- **Delta:** **pre-notation** — candidate entities, value-ish things, policies, watch list; **newly added** tags informal lines; typed members arrive in later steps.

---

## Action Checklist

- Have you rolled vocabulary into buckets (entities, value objects, processes, policies, roles, events)?
- Is that roll-up **appended to `domain-noun-verb.md`** *or* in a separate **`raw-candidate-list.md`** (not redundant copies without reason)?
- Early class smell, watch list, and tensions recorded?
- Have you separated entity-like vs value-object hypotheses where it matters?
- Tensions noted for later phases?

---

## Prompt

> When this step surfaces bloat, unclear boundaries, missing invariants, naming drift, or spec conflicts, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) while you work; record **explicit debt** with a clear follow-up only when you cannot fix yet.
