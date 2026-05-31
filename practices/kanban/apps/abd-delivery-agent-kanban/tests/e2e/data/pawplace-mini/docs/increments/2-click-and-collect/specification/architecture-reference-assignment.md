---
ticket: 2-click-and-collect-sprint-1
skill: abd-architecture-reference
scope: Increment 2 Sprint 1 — Cart
---

# Architecture Reference Assignment — Increment 2 Sprint 1 (Cart)

**Ticket:** `2-click-and-collect-sprint-1`  
**Mode:** Docs-only E2E fixture — assign-only; no `architecture-reference.md` or `src/` generation at specification.

## Mechanisms in scope

| Mechanism / component | In sprint scope |
| --- | --- |
| Cart (CartService, CartApi, CartRepository) | Yes |
| Catalog read surface (ICatalogClient stock/product lookup) | Yes — validation only |
| App Shell (AppClientShell cart views) | Yes — presentation only |
| Security | Yes — guest session / cart token at edge |
| Error Handling & Resilience | Yes |
| Validation | Yes |
| Persistence (`cart_*`) | Yes |
| Communication (REST `/api/v1`) | Yes |
| Configuration | Yes |
| Logging & Observability | Yes |
| Order, Payment, Notification | No — later sprints |

## Assignment table

| Mechanism | Reference | Code | Paths |
| --- | --- | --- | --- |
| Cart lifecycle | **assign** | **n/a** | [`docs/end-to-end/discovery/architecture/architecture-blueprint.md`](../../../end-to-end/discovery/architecture/architecture-blueprint.md) § 2.4 Cart components |
| Catalog client (stock read) | **assign** | **n/a** | Blueprint § 2.3 Catalog components (read path for add-to-cart validation) |
| Security | **assign** | **n/a** | Blueprint § 3.1 Security |
| Error Handling & Resilience | **assign** | **n/a** | Blueprint § 3.2 |
| Validation | **assign** | **n/a** | Blueprint § 3.4 |
| Persistence | **assign** | **n/a** | Blueprint § 3.6; data ownership § 4.2 (`Cart`) |
| Communication | **assign** | **n/a** | Blueprint § 3.7 |
| Configuration | **assign** | **n/a** | Blueprint § 3.5 |
| Logging & Observability | **assign** | **n/a** | Blueprint § 3.3 |

### Exploration & specification context (assign)

- CRC: [`crc.md`](./crc.md)
- Spec by example: [`specification-by-example.md`](./specification-by-example.md)
- Interface design: [`interface-design.md`](./interface-design.md)
- Ubiquitous language: [`../exploration/domain/ubiquitous-language.md`](../exploration/domain/ubiquitous-language.md)
- Acceptance criteria: [`../exploration/stories/acceptance-criteria.md`](../exploration/stories/acceptance-criteria.md)
- UX mockups: [`../exploration/ux/shopping-cart.md`](../exploration/ux/shopping-cart.md)

**Deferred to engineering:** Runnable reference sections (`architecture-reference.md`), File Structure, and production code under `src/` — created by `abd-object-model`, `abd-acceptance-test-driven-development`, and `abd-clean-code` on the engineering ticket.

---

---
ticket: 2-click-and-collect-sprint-2
skill: abd-architecture-reference
scope: Increment 2 Sprint 2 — Checkout & pay
---

# Architecture Reference Assignment — Increment 2 Sprint 2 (Checkout & pay)

**Ticket:** `2-click-and-collect-sprint-2`  
**Mode:** Docs-only E2E fixture — assign-only; checkout and payment mechanisms already covered in discovery blueprint. No `architecture-reference.md` or `packages/` generation at specification.

## Mechanisms in scope

| Mechanism / component | In sprint scope |
| --- | --- |
| Order (OrderService, OrderApi, OrderRepository) | Yes |
| Payment (PaymentGatewayAdapter, `IPaymentProvider` / StripeWave) | Yes |
| Notification (order confirmation email) | Yes |
| Store read surface (`IStoreClient` — pickup store selection) | Yes — read path only |
| Cart read surface (`ICartClient` — checkout conversion) | Yes — read path only |
| Catalog read surface (`ICatalogClient` — stock/price at placement) | Yes — validation only |
| App Shell (checkout + order confirmation views) | Yes — presentation only |
| Security | Yes — guest checkout, idempotency key at edge |
| Error Handling & Resilience | Yes — payment declined, idempotent submit |
| Validation | Yes |
| Persistence (`order_*`, idempotency records) | Yes |
| Communication (REST `/api/v1`) | Yes |
| Configuration | Yes — StripeWave + email provider |
| Logging & Observability | Yes — checkout spine tracing |
| Employee fulfillment status updates | No — Sprint 3 |

## Assignment table

| Mechanism | Reference | Code | Paths |
| --- | --- | --- | --- |
| Order lifecycle (guest checkout, placement, confirmation) | **assign** | **n/a** | [`docs/end-to-end/discovery/architecture/architecture-blueprint.md`](../../../end-to-end/discovery/architecture/architecture-blueprint.md) § 2.5 Order components |
| Payment capture (StripeWave adapter) | **assign** | **n/a** | Blueprint § 2.5 PaymentGatewayAdapter |
| Order confirmation email | **assign** | **n/a** | Blueprint § 2.5 NotificationAdapter |
| Store client (pickup store) | **assign** | **n/a** | Blueprint § 2.2 Store components (read path) |
| Cart client (checkout read) | **assign** | **n/a** | Blueprint § 2.4 Cart components (read at checkout) |
| Catalog client (stock/price validation) | **assign** | **n/a** | Blueprint § 2.3 Catalog components (read path) |
| Security | **assign** | **n/a** | Blueprint § 3.1 Security |
| Error Handling & Resilience | **assign** | **n/a** | Blueprint § 3.2 (checkout, payment, idempotency) |
| Validation | **assign** | **n/a** | Blueprint § 3.4 |
| Persistence | **assign** | **n/a** | Blueprint § 3.6; data ownership § 4.2 (`Order`, line snapshots) |
| Communication | **assign** | **n/a** | Blueprint § 3.7 |
| Configuration | **assign** | **n/a** | Blueprint § 3.5 |
| Logging & Observability | **assign** | **n/a** | Blueprint § 3.3 (checkout spine) |

### Exploration & specification context (assign)

- CRC (Sprint 2): [`crc.md`](./crc.md) — Increment 2 — Sprint 2: Checkout & pay
- Spec by example (Sprint 2): [`specification-by-example.md`](./specification-by-example.md)
- Interface design (Sprint 2): [`interface-design.md`](./interface-design.md) — Checkout & pay, Order Confirmation
- Ubiquitous language: [`../exploration/domain/ubiquitous-language.md`](../exploration/domain/ubiquitous-language.md)
- Acceptance criteria: [`../exploration/stories/acceptance-criteria.md`](../exploration/stories/acceptance-criteria.md)
- UX mockups: [`../exploration/ux/checkout-guest-pickup.md`](../exploration/ux/checkout-guest-pickup.md), [`../exploration/ux/order-confirmation.md`](../exploration/ux/order-confirmation.md)

**Skipped — all mechanisms assign:** No reference sections or code files missing for Sprint 2 scope; blueprint § 2.5 and § 3.x satisfy checkout/payment/notification. Runnable `architecture-reference.md` and `packages/checkout`, `packages/payments`, `packages/order` deferred to engineering (`abd-object-model`, ATDD, `abd-clean-code`).

---

---
ticket: 2-click-and-collect-sprint-3
skill: abd-architecture-reference
scope: Increment 2 Sprint 3 — Store pickup
---

# Architecture Reference Assignment — Increment 2 Sprint 3 (Store pickup)

**Ticket:** `2-click-and-collect-sprint-3`  
**Mode:** Docs-only E2E fixture — assign-only; fulfillment mechanisms already covered in discovery blueprint § 2.5 and § 3.1. No `architecture-reference.md` or `packages/fulfillment/` generation at specification.

## Mechanisms in scope

| Mechanism / component | In sprint scope |
| --- | --- |
| OrderService (fulfillment status transitions) | Yes |
| OrderApi (employee fulfillment endpoints) | Yes |
| OrderRepository (fulfillment status on orders) | Yes |
| Fulfillment Queue / Order Fulfillment (domain) | Yes — via OrderService |
| Store Employee boundary (role-gated routes) | Yes |
| App Shell (Fulfillment Queue + Order detail views) | Yes — presentation only |
| Security | Yes — staff token / basic auth on fulfillment routes |
| Error Handling & Resilience | Yes |
| Validation | Yes |
| Persistence (`order_*` fulfillment status fields) | Yes |
| Communication (REST `/api/v1` fulfillment) | Yes |
| Configuration | Yes |
| Logging & Observability | Yes |
| Cart, checkout, payment | No — Sprint 1–2 |

## Assignment table

| Mechanism | Reference | Code | Paths |
| --- | --- | --- | --- |
| Order fulfillment lifecycle (prepare, ready, handoff) | **assign** | **n/a** | [`docs/end-to-end/discovery/architecture/architecture-blueprint.md`](../../../end-to-end/discovery/architecture/architecture-blueprint.md) § 2.5 OrderService — fulfillment status transitions |
| Employee fulfillment HTTP endpoints | **assign** | **n/a** | Blueprint § 2.5 OrderApi — employee fulfillment endpoints |
| Order persistence (fulfillment status) | **assign** | **n/a** | Blueprint § 2.5 OrderRepository |
| Store employee route security | **assign** | **n/a** | Blueprint § 3.1 Security — staff token on fulfillment routes |
| Error Handling & Resilience | **assign** | **n/a** | Blueprint § 3.2 |
| Validation | **assign** | **n/a** | Blueprint § 3.4 |
| Persistence | **assign** | **n/a** | Blueprint § 3.6; data ownership § 4.2 (`Order` fulfillment status) |
| Communication | **assign** | **n/a** | Blueprint § 3.7 |
| Configuration | **assign** | **n/a** | Blueprint § 3.5 |
| Logging & Observability | **assign** | **n/a** | Blueprint § 3.3 |
| Fulfillment client surfaces | **assign** | **n/a** | Blueprint § 2.5 OrderApi interactions — AppClientShell fulfillment flows; interface-design § Sprint 3 planned `packages/fulfillment/client` |

### Exploration & specification context (assign)

- CRC (Sprint 3): [`crc.md`](./crc.md) — Increment 2 — Sprint 3: Store pickup
- Spec by example (Sprint 3): [`specification-by-example.md`](./specification-by-example.md)
- Interface design (Sprint 3): [`interface-design.md`](./interface-design.md) — Fulfillment Queue, Fulfillment — Order
- Ubiquitous language: [`../exploration/domain/ubiquitous-language.md`](../exploration/domain/ubiquitous-language.md)
- Acceptance criteria: [`../exploration/stories/acceptance-criteria.md`](../exploration/stories/acceptance-criteria.md)
- UX mockups: [`../exploration/ux/fulfillment-orders.md`](../exploration/ux/fulfillment-orders.md), [`../exploration/ux/fulfillment-order.md`](../exploration/ux/fulfillment-order.md)

**Skipped — all mechanisms assign:** No reference sections or code files missing for Sprint 3 scope; blueprint § 2.5 OrderService/OrderApi and § 3.1 staff-route security satisfy fulfillment queue, preparation, and handoff. Runnable `architecture-reference.md` and `packages/fulfillment` deferred to engineering (`abd-object-model`, ATDD, `abd-clean-code`).
