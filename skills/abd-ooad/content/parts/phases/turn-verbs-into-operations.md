# Turn verbs into operations — payments example

**Skill:** abd-ooad — **Step 6:** distribute verbs to types that **own** the behavior.

**Upstream:** `add-properties-semantically-tight.md`, `nouns-verbs-rules-and-states.md`.

> **Continual refinement:** Aligns with **abd-maps-models-specs** [`domain-model.md`](../../abd-maps-models-specs/content/parts/library/domain-model.md) (*Domain concept* template, *Continual refinement — class definition + diagram*). In this payments thread, **`**newly added**`** marks a property or operation line **first introduced in this step file** (Steps 1–4 stay pre-notation; formal `- <type> property` / `operation(...) → return` lines begin at Step 5).

---

## Verbs → candidate operations (challenged)

| Verb (from spec) | First guess | Who **should** own it? |
|-------------------|-------------|-------------------------|
| take / charge money | `Payment.authorize()`, `Payment.capture()` | **Payment** — lifecycle. |
| block sanctioned payer | `ComplianceGate.canProceed(payerContext)` or `Payment` precondition | **Policy** before UI; **Payment** refuses `initiate` if illegal. |
| pick method / confirm | N/A as entity method | **Application service** orchestrates UI; **Payment.recordMethodSelection()`, `confirm()`** if state on aggregate. |
| open redirect / 3DS | `RedirectSession.start()` | **Application** + infra; domain: **`Payment.markAwaitingRedirect()`** fact. |
| emit `payment.settled` | internal + domain event | **`Payment.settle()`** or domain event raised when state hits settled — **not** Warehouse. |
| refund | `Refund.initiate()`, `Payment.attachRefund?` | **Refund** aggregate or **Payment.requestRefund** if refunds are always subordinate. |
| expire idempotency key | `IdempotencyRegistry.expire?` | **Policy/config** + time; **Payment** rejects replay if key expired for **this** intent. |

---

## Payment — operations (domain)

- `initiate(idempotencyKey, orderRef, payerRef, merchantRef, routing)` — creates attempt or returns same for key.
- `recordMethodSelection(selection)` — snapshot VO when user picks method.
- `recordFees(feeBreakdown)` — after quote.
- `authorize(...)` / `markAuthorized(result)` — PSP outcome applied.
- `capture(amount)` / `markCaptured` — partial or full per rail rules.
- `settle()` / `markSettled` — emit domain fact; enforce ordering invariants.
- `fail(reason)` — terminal failure with **FailureKind**.
- `recordPspCallback(payloadRef)` — transition from webhook **via** application mapping.

**Not** on Payment: `renderCheckoutPage()` (UI), `callStripeHttp()` (adapter).

---

## Refund

- `request(amount, reason)` — valid vs original captured amounts.
- `complete()` / `fail()` — rail outcomes.

---

## Application / use-case layer (English verbs land here)

- **Place payment** / **Run happy path** — coordinates cart lock, Payment aggregate, PSP adapter, redirect URLs.
- **Interpret webhook** — maps to `Payment.record...` commands.

**Challenge:** Should `Payer.pay()` exist? Usually **no** — payer is identity; **InitiatePayment** use case uses **Payment** factory or repository.

---

## Formal domain operations (Step 6)

**`- <type> operation(...) → …`** lines first introduced in this step; each marked **`**newly added`**.

### **Payment**

- initiate(IdempotencyKey, OrderId, PayerId, MerchantId, RoutingContext) → Payment **newly added**
- recordMethodSelection(PaymentMethodSelection) → void **newly added**
- recordFees(FeeBreakdown) → void **newly added**
- authorize(AuthorizationResult) → void **newly added**
- capture(Money) → void **newly added**
- settle() → void **newly added**
- fail(FailureKind) → void **newly added**
- recordPspCallback(String payloadRef) → void **newly added**

### **Refund**

- request(Money, ReasonCode) → Refund **newly added**
- complete() → void **newly added**
- fail() → void **newly added**

*(Application-layer use cases — Place payment, Interpret webhook — stay outside aggregate operation lists; reference them in **Interactions** on the spec when you promote.)*

---

## Carry forward → Step 7

Add **relationships and cardinality** between Payment, Refund, Order (ref), external catalogs.

---

## Continual refinement (this step)

- **Delta:** core **operations** on **Payment** and **Refund** with **`**newly added**`**; verb-to-owner table above remains the rationale.
- **Diagram:** update class diagram / spec when these operations are stable in **`map-model-spec.json`**.

---

## Action Checklist

- [ ] Have you mapped each domain verb from Step 1 to an owning class?
- [ ] Have you challenged application-layer verbs — do they belong in a service, not a domain object?
- [ ] Does every surviving operation appear on the class as a formal method signature?
- [ ] Have you updated the class diagram / `map-model-spec.json` with the new operations?
- [ ] Have you noted carry-forward items to Step 7 (relationships)?

---

## Prompt

> **Validate and fix when you find problems.** This step may surface bloat, unclear boundaries, missing invariants, naming drift, spec conflicts, or other robustness gaps. When you notice any of that in your work, **validate** and **fix** the model (or **map-model-spec.json** / class diagram) **before** moving on; record **explicit debt** only when you cannot fix yet, with a clear follow-up.
