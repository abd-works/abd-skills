# Add properties (semantically tight) — payments example

**Skill:** abd-ooad — matches **Step 5: Add properties and keep them semantically tight** in `SKILL.md`.

**Upstream:** `responsibilities-before-operations.md` (Step 4), `garbled-payments-spec.md`.

Ask: **What must this object know to fulfill its responsibility?** — not “what fields appear in the document.”

Use **contextual names** (like **OrderItem** vs **Item**): e.g. **CapturedPortion** or explicit `authorizedAmount` / `capturedAmount` instead of a vague `amount` when partial capture matters.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Payment (aggregate root)

| Property | Why it belongs here |
|----------|---------------------|
| `id` | Identity of **this** payment attempt. |
| `idempotencyKey` | Correlate retries; enforce “no double success” for same client intent. |
| `orderRef` | **OrderId** (external BC) — links checkout to payment **without** duplicating cart lines. |
| `payerRef` | **PayerId** — who pays; sanctions check uses **context**, not a full `Customer` graph. |
| `merchantRef` | **MerchantId** / account — routing and settlement context. |
| `routing` | **RoutingContext** VO — dimensions that pick connector (currency, region, …). |
| `presentmentMoney` | **Money** — what the payer authorizes in **their** currency (name clarifies vs settlement). |
| `settlementMoney` | **Money** — if different from presentment (global); optional **nullable** if same. |
| `feeBreakdown` | **FeeBreakdown** VO — fees **shown/charged for this attempt**, not tax (cart). |
| `fxQuoteRef` | **FxQuoteRef?** — nullable handle for global flows. |
| `methodSelection` | **PaymentMethodSelection** VO — **this attempt’s** chosen method snapshot (kind + safe metadata). |
| `state` | **PaymentState** — lifecycle position. |
| `authorizedMoney` / `capturedMoney` | **Money** (or single progression) — supports **partial capture** and remainder release **without** a vague `amount`. |
| `midRateSnapshot` | **MidRateSnapshot?** — immutable receipt stamp when legal requires; **not** live FX. |
| `connectorRef` | **ConnectorId** or rail handle — **which** integration served this attempt (debugging, capability checks). |
| `redirectContext` | **RedirectContext?** VO — e.g. return/cancel URLs, PSP session id **if** 3DS/redirect — **not** the whole browser. |
| `timestamps` | `createdAt`, `authorizedAt?`, `capturedAt?`, `settledAt?`, `failedAt?` — audit and SLA; **only** those needed for invariants you enforce. |

**Deliberately omitted from Payment** (other BCs or adapters):

- Tax lines, coupon state, cart items — **Order / cart**.
- Full **Merchant** entity — only **merchantRef**.
- PAN, CVV — **never**; tokens live at PSP.
- “Frontend string copy” — **Failure mapping policy**, not properties on Payment.

---

## Refund

| Property | Why it belongs here |
|----------|---------------------|
| `id` | Distinct refund case. |
| `paymentRef` | **PaymentId** — which payment is being undone/partially reversed. |
| `refundMoney` | **Money** — amount **of this refund** (partial or full). |
| `reason` | **ReasonCode** — chargeback prep / compliance. |
| `state` | Refund lifecycle if distinct (requested → processing → completed / failed). |
| `requestedAt`, `completedAt` | Traceability; align with “as fast as rail allows.” |

**Naming note:** use **refundMoney**, not `amount`, if multiple money fields exist on related types — **contextual role** is “portion refunded in this case.”

---

## Dispute (only if aggregate lives in this BC)

| Property | Why |
|----------|-----|
| `id` | Case identity. |
| `paymentRef` / `refundRef` | Links to money movements. |
| `externalCaseId` | PSP or Risk system id. |
| `ownership` | **enum** or tag: `platform` \| `merchantOfRecord` — **data** reflecting policy, not the decision logic. |
| `state` | Open / won / lost / … as your process defines. |

If Dispute is **external**, **Payment** might only hold `disputeIds: DisputeId[]` or nothing.

---

## AuditEntry (immutable row / event payload)

| Property | Why |
|----------|-----|
| `id` | Log line identity (or use event id). |
| `paymentRef` | Which aggregate. |
| `fromState`, `toState` | Transition (or single `eventType` if you prefer events). |
| `actor` | **ActorKind** — `system` \| `user` \| `psp_webhook`. |
| `occurredAt` | Ordering. |
| `payloadRef?` | Optional pointer to raw PSP snippet id — **not** full card data. |

---

## Value objects — internal shape (properties are the VO’s fields)

### Money

- `amount` (scaled integer or decimal with scale)
- `currency` — **Currency** code VO or ISO string with validation

### RoutingContext

- `storefrontCurrency` or `chargeCurrency`
- `merchantRegion` (or legal entity id) — **whatever engineering uses to gate** connector per spec assumption

### FeeBreakdown

- `lines: FeeLine[]` or single `total: Money` — **minimum** structure to match “fees if any” on confirm

### PaymentMethodSelection (contextual snapshot)

- `kind: PaymentMethodKind`
- `displayLabel` / `last4` / `brand` — **non-sensitive** display only

### IdempotencyKey (if VO)

- `value: string`
- optionally `firstSeenAt` — if TTL policy applies to **this** key

### FxQuoteRef

- `opaqueId: string` (or URI) — **no** FX math here

### MidRateSnapshot

- `rate`, `pair`, `asOf` — **frozen** for receipt

### RedirectContext (optional)

- `returnUrl`, `cancelUrl`, `pspSessionId` — **whatever** your redirect flow needs to correlate callbacks

---

## Contextual naming (payments)

| Vague noun | Tighter name in this context |
|------------|------------------------------|
| Amount | `authorizedMoney`, `capturedMoney`, `refundMoney`, `presentmentMoney` |
| Item | N/A — if you model line-level charges, use **PaymentLine** or **CaptureLine** with explicit role |
| Session | Prefer **`Payment`** as aggregate name; **Session** in spec → alias in docs only |
| User | **`payerRef`** / **PayerId** — role in this flow |

---

## Formal domain concepts (Step 5)

First typed **`- <type> property`** lines for core aggregates (see [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md). Every line below is **`**newly added**`** at this step in the payments thread.

### **Payment**

- UniqueID id **newly added**
- String idempotencyKey **newly added**
- OrderId orderRef **newly added**
- PayerId payerRef **newly added**
- MerchantId merchantRef **newly added**
- RoutingContext routing **newly added**
- Money presentmentMoney **newly added**
- Money settlementMoney **newly added**
- FeeBreakdown feeBreakdown **newly added**
- FxQuoteRef fxQuoteRef **newly added**
- PaymentMethodSelection methodSelection **newly added**
- PaymentState state **newly added**
- Money authorizedMoney **newly added**
- Money capturedMoney **newly added**
- MidRateSnapshot midRateSnapshot **newly added**
- ConnectorId connectorRef **newly added**
- RedirectContext redirectContext **newly added**
- PaymentTimestamps timestamps **newly added** (`createdAt`, `authorizedAt`, …)

### **Refund**

- UniqueID id **newly added**
- PaymentId paymentRef **newly added**
- Money refundMoney **newly added**
- ReasonCode reason **newly added**
- RefundState state **newly added**
- Instant requestedAt **newly added**
- Instant completedAt **newly added**

### **Dispute** (only if aggregate lives in this BC)

- UniqueID id **newly added**
- PaymentId paymentRef **newly added**
- RefundId refundRef **newly added**
- String externalCaseId **newly added**
- DisputeOwnership ownership **newly added**
- DisputeState state **newly added**

### **AuditEntry**

- UniqueID id **newly added**
- PaymentId paymentRef **newly added**
- PaymentState fromState **newly added**
- PaymentState toState **newly added**
- ActorKind actor **newly added**
- Instant occurredAt **newly added**
- String payloadRef **newly added**

VO shapes (**Money**, **RoutingContext**, **FeeBreakdown**, etc.) stay under the tables above; add typed property lines in **map-model-spec** / diagram when you promote those value objects.

---

## Carry forward to Step 6 (operations)

Next: map **verbs** from Step 1 and spec to **operations** on **Payment**, **Refund**, policies — and **challenge** each (e.g. does `Payer.placePayment()` belong here or in an application service?).

---

## Continual refinement (this step)

- **Delta:** semantically tight **properties** for **Payment**, **Refund**, optional **Dispute**, **AuditEntry**, plus VO lists — all as **`- <type> property`** lines with **`**newly added**`** (first formal notation in this thread).
- **Diagram:** when maintaining **`map-model-spec.json`**, re-run **`render_map_model_class_diagram.py`** so the class diagram stays the visual twin (see [class-diagram-from-spec.md](../../abd-maps-models-specs/content/parts/library/class-diagram-from-spec.md).

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
