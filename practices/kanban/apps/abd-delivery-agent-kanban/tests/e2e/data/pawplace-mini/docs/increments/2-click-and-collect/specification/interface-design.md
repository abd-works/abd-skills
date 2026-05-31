# Interface design — PawPlace mini — Increment 2

> **Companion to** lo-fi mockups under `docs/increments/2-click-and-collect/exploration/ux/` and discovery IA `docs/end-to-end/discovery/ux/information-architecture.md`. Specification-stage spec; implementation and tests land in Engineering (`abd-interface-design` implementation pass → ATDD → clean code). This file is authoritative for Sprint 1 cart screens, Sprint 2 checkout screens, and Sprint 3 store pickup / fulfillment screens.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Increment 2 — Sprint 1 (Cart) + Sprint 2 (Checkout & pay) + Sprint 3 (Store pickup): cart, guest checkout, order confirmation, fulfillment queue, pickup handoff |
| Lo-fi reference | `shopping-cart.md`, `checkout-guest-pickup.md`, `order-confirmation.md`, `fulfillment-orders.md`, `fulfillment-order.md`, `mockups.md` |
| Hi-fi reference | Visual direction below (no separate hi-fi artifact — lo-fi regions + token table) |
| Acceptance criteria | `docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md` |
| Specification by example | `docs/increments/2-click-and-collect/specification/specification-by-example.md` |
| Domain terms | `docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md` |
| CRC | `docs/increments/2-click-and-collect/specification/crc.md` |
| Target framework | React 18 + TypeScript (Vite), Express 4 (per architecture blueprint) |
| Host project root | `C:\dev\agilebydesign-skills\practices\kanban\apps\abd-delivery-agent-kanban\tests\e2e\data\pawplace-mini` (docs); implementation targets `packages/` when Engineering scaffolds |
| Implementation paths (planned) | `packages/app-client` (routes + shell), `packages/cart/client`, `packages/checkout/client`, `packages/payments/client`, `packages/fulfillment/client` |
| Test path (planned) | `tests/` (Vitest + Playwright per architecture blueprint) |
| Last updated | 2026-05-31T04:05:00+00:00 |

## Description

Sprint 1 covers *shopping cart* line management: *customer* runs *add product to cart*, opens **Shopping Cart**, edits *cart quantity*, runs *remove product from cart*, and may *continue shopping*. Sprint 2 adds *guest checkout* from a non-empty cart: *click-and-collect store* selection, contact email, *billing address*, card *payment method* via *StripeWave*, *place order*, and **Order Confirmation** after payment success. Sprint 3 adds *store employee* surfaces: **Fulfillment Queue** for *prepare click-and-collect orders for pickup* and **Fulfillment — Order** detail for *fulfill click-and-collect order* pickup handoff. Labels use ubiquitous-language terms verbatim. Employee routes are role-gated — unavailable to *customer*.


---

## Sprint 1: Cart

Ticket: `2-click-and-collect-sprint-1`. Stories: Add Product to Cart, Update Cart Quantity, Remove Product from Cart.

### Host project conventions (discovered / planned)

- **Folder layout:** domain modules under `packages/<module>/{shared,server,client}`; app shell in `packages/app-client` (per `architecture-blueprint.md`)
- **State management:** React component state + Cart module API clients; server-persisted *shopping cart* keyed to session/customer fixture
- **Styling:** component-scoped CSS; map tokens below until a project-wide token file exists in Engineering
- **Token system:** `packages/shared/layout-tokens.ts` (planned in Engineering — values in § Visual direction)
- **Test framework:** Vitest + React Testing Library (unit/component), Playwright (e2e)
- **Lint / format / type gates:** TypeScript project references; `npm test` from repo root when scaffolded
- **Accessibility check:** axe-core in component tests; manual keyboard pass per screen
- **Performance budget:** no explicit bundle cap declared — cart list must render without blocking on catalog fetch

### Screens (carried from lo-fi and IA)

| Screen | Layout | Route (planned) | Stories |
| --- | --- | --- | --- |
| Product Details | stack | `/catalog/:productId` | Add Product to Cart (entry) |
| Shopping Cart | stack | `/cart` | Add Product to Cart, Update Cart Quantity, Remove Product from Cart |

**Customer chrome (Sprint 1+):** site header with **Find Store** · **catalog** · **Cart** nav links. **Cart** marks current section on Shopping Cart route.

#### Product Details — regions and affordances (add entry only)

Sprint 1 implements only the *add product to cart* affordance on the existing Product Details shell from Increment 1 catalog browsing. Other Product Details regions (name, price, *stock availability*) remain as Increment 1 — Sprint 1 adds cart integration only.

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| site header · Find Store · catalog · Cart | chrome | Find Store · catalog · Cart | Nav links |
| product summary | form | product name · price · description · stock availability | Read-only product identity |
| product summary actions | toolbar | add to cart · back to catalog | add to cart (primary) → *add product to cart* API → optional toast → `/cart` or stay; back to catalog → `/catalog` |

**Conditional states:**
- *stock availability* unavailable: add to cart disabled; inline warning with `role="alert"` before any line is created (AC Add Product #3)
- *stock availability* available: add to cart enabled
- Repeat add to cart for same *product*: merges into existing *cart line* (no duplicate row) — server-side merge; UI may show confirmation without duplicate lines on cart view

#### Shopping Cart — regions and affordances

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| site header · Find Store · catalog · Cart | chrome | Find Store · catalog · Cart | Cart active on this route |
| cart lines | list | columns: product · cart quantity · line total | Each row: product identity, editable *cart quantity* input/stepper, computed line total |
| cart lines actions | list actions | update quantity · remove · continue shopping · checkout | update quantity commits *update cart quantity*; remove confirms *remove product from cart*; continue shopping → `/catalog`; checkout primary when lines exist → `/checkout` (Sprint 2); disabled when empty |
| empty cart message | chrome | browse catalog prompt | Shown when no *cart lines*; checkout hidden/disabled |

**Conditional states:**
- Non-empty cart: checkout button visible, enabled styling per lo-fi (engineering may wire navigation in Sprint 2); lines show product identity and editable *cart quantity*
- Empty cart: checkout disabled/hidden; browse catalog prompt with link to *catalog*
- Zero-quantity edit attempt: validation message directs to *remove product from cart* instead of *update cart quantity* to zero
- Partial remove: remaining *cart lines* and their *cart quantities* unchanged

### Visual direction (specification hi-fi)

No production design images in workspace. Engineering implements these roles as CSS variables / theme tokens. Align with Increment 1 store locator palette for customer chrome continuity.

| Role | Typography / colour | Usage |
| --- | --- | --- |
| display | sans-serif, 24/32, weight 600, `#1A1A2E` | Page title: Shopping Cart |
| body | sans-serif, 16/24, weight 400, `#2D2D2D` | Product names, line totals |
| label | sans-serif, 14/20, weight 500, `#5C5C5C` | Column headers: product · cart quantity · line total |
| accent | `#B85C38` | Primary: add to cart, checkout (when enabled), update quantity confirm |
| surface | `#FFFFFF` | Screen background |
| surface-muted | `#F5F5F0` | Cart row hover / focus |
| danger | `#C0392B` | Remove confirm destructive action |
| focus | 2px solid `#B85C38`, offset 2px | Keyboard focus ring — never removed |
| spacing scale | 4 · 8 · 16 · 24 · 32 px | Region padding and list row gaps |

*Cart quantity* control: numeric input with `min="1"` and adjacent stepper buttons, or native number input with validation — must expose programmatic label "cart quantity" tied to product name.

### Implementation targets (planned — Engineering)

| Screen / concern | Primary component(s) | Server module |
| --- | --- | --- |
| Shopping Cart | `ShoppingCartView.tsx`, `CartLineRow.tsx` | `packages/cart/server/cart.service.ts`, `CartApi` |
| Product Details add | `ProductDetailsView.tsx` (extend), `AddToCartButton.tsx` | same Cart module |
| Customer header | `CustomerNav.tsx` | — |
| Cart persistence | `useShoppingCart.ts` hook | `GET/POST/PATCH/DELETE /api/v1/cart/...` |
| Empty / validation | `EmptyCartMessage.tsx`, `CartQuantityField.tsx` | validation in cart.service |

---

## Sprint 2: Checkout & pay

Ticket: `2-click-and-collect-sprint-2`. Stories: Select Click-and-Collect Store · Check Out as Guest · Enter Billing Address · Select Payment Method · Process Card Payment via StripeWave (system) · Confirm Order and Send Confirmation Email (system).

### Host project conventions (discovered / planned)

Same as Sprint 1 unless noted:

- **Folder layout:** add `packages/checkout/{shared,server,client}` and `packages/payments/{shared,server}` beside Cart module
- **State management:** `CheckoutSessionProvider` holds *click-and-collect store*, contact email, *billing address*, *payment method*, processing flags; survives step navigation within `/checkout`
- **Checkout flow:** single-page stacked form (store-first per lo-fi) — not a wizard with separate routes per step in this fixture
- **Payment boundary:** `StripeWaveClient` adapter in `packages/payments`; UI never calls StripeWave directly from presentational components
- **Post-payment:** redirect to `/order-confirmation/:orderId` only after *StripeWave* success

### Screens (carried from lo-fi and IA)

| Screen | Layout | Route (planned) | Stories |
| --- | --- | --- | --- |
| Shopping Cart (checkout entry) | stack | `/cart` | Check Out as Guest (entry) |
| Checkout — Guest & pickup | form | `/checkout` | Select Click-and-Collect Store · Check Out as Guest · Enter Billing Address · Select Payment Method · Process Card Payment via StripeWave |
| Order Confirmation | stack | `/order-confirmation/:orderId` | Confirm Order and Send Confirmation Email · Process Card Payment via StripeWave (success path) |

**Customer chrome (Sprint 2):** site header with **Find Store** · **catalog** · **Cart** on all customer routes.

**Shopping Cart checkout affordance (Sprint 2 update):** when *cart lines* exist, **checkout** primary navigates to `/checkout` and starts *guest checkout* without sign-in. Empty cart: checkout disabled; blocks entry per AC Check Out as Guest #3.

#### Checkout — Guest & pickup — regions and affordances

Lo-fi: `checkout-guest-pickup.md` · `checkout-guest-pickup.drawio`

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| site header · Find Store · catalog · Cart | chrome | Find Store · catalog · Cart | Customer navigation |
| pickup store | body | listbox: click-and-collect store · store address | Single-select list of every eligible *store*; shows retail location identity and geographic placement per row |
| pickup store actions | body | toolbar | change store | Replaces checkout binding; only one *click-and-collect store* selected |
| guest checkout | body | form | email · phone · guest-only label | Collects contact for *order confirmation*; no login or registration |
| billing address | body | form | name · street · city · postal code · country | *Enter billing address* with field-level validation before payment step |
| payment method | body | form | payment method · StripeWave | Card only; labels processor *StripeWave* |
| payment method actions | body | form buttons | back to cart · place order | place order primary; invokes *process card payment via StripeWave* |
| validation error area | body | chrome | field-level messages | Billing, store, and payment errors; `role="alert"` on submit failures |

**Section order (store-first):** pickup store → guest checkout (email) → billing address → payment method → place order.

**Conditional states:**
- No *click-and-collect store* selected: place order disabled; *StripeWave* not invoked (AC Select Click-and-Collect Store #3)
- Invalid or incomplete *billing address*: field errors in validation error area; *StripeWave* not invoked (AC Enter Billing Address #3)
- No *payment method* selected: place order disabled (AC Select Payment Method #3)
- Processing payment: place order disabled; processing indicator; duplicate submit blocked (AC Process Card Payment #4)
- Payment failure: validation error area shows failure message; *back to cart* preserves recoverable *shopping cart* (AC Process Card Payment #3, #5)
- Payment success: navigate to Order Confirmation; *shopping cart* cleared server-side (AC Process Card Payment #2)

#### Order Confirmation — regions and affordances

Lo-fi: `order-confirmation.md` · `order-confirmation.drawio`

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| site header · Find Store · catalog · Cart | chrome | Find Store · catalog · Cart | Customer navigation |
| order summary | body | form (read-only) | order id · click-and-collect store · total · order confirmation | Displays placed *click-and-collect order*; indicates email sent |
| order summary actions | body | form button | continue shopping | Returns to `/catalog` scoped to *selected store*; placed order not editable via cart |

**Conditional states:**
- Route guard: only reachable after *StripeWave* payment success — otherwise redirect to checkout or cart (AC Confirm Order #3)
- Empty cart after success: Cart nav shows empty state on next visit

### Visual direction (Sprint 2 — reuse Sprint 1 tokens)

Reuse Sprint 1 customer token table. Checkout-specific usage:

| Role | Usage |
| --- | --- |
| display | Page title: Checkout — Guest & pickup · Order Confirmation |
| accent | Primary: place order · continue shopping |
| surface-muted | Selected *click-and-collect store* row highlight |
| danger | Payment failure and billing validation messages |
| focus | 2px solid accent focus ring on listbox, inputs, place order |

*click-and-collect store* listbox: `role="listbox"` with `role="option"` rows; selected state announced via `aria-selected`. Store identity and address visible in each option.

*place order* processing: `aria-busy="true"` on form during *StripeWave* wait; button `aria-disabled` when prerequisites incomplete.

### Implementation targets (planned — Engineering)

| Screen / concern | Primary component(s) | Server module |
| --- | --- | --- |
| Checkout shell | `GuestCheckoutView.tsx`, `CheckoutSection.tsx` | `packages/checkout/server/checkout.service.ts`, `CheckoutApi` |
| Store selection | `PickupStoreList.tsx`, `PickupStoreOption.tsx` | `GET /api/v1/stores` (reuse Store module) |
| Guest contact | `GuestContactFields.tsx` | checkout session |
| Billing | `BillingAddressForm.tsx` | `PATCH /api/v1/checkout/session/billing` |
| Payment | `PaymentMethodForm.tsx`, `PlaceOrderButton.tsx` | `packages/payments/server/stripewave.adapter.ts` |
| Order confirmation | `OrderConfirmationView.tsx` | `GET /api/v1/orders/:orderId` |
| Cart → checkout | `ShoppingCartView.tsx` (extend checkout nav) | `POST /api/v1/checkout/session` from cart |
| Email (system) | — | `OrderConfirmationService` (server-only; AC Confirm Order #1) |

---

## Sprint 3: Store pickup

Ticket: `2-click-and-collect-sprint-3`. Stories: Prepare Click-and-Collect Orders for Pickup · Fulfill Click-and-Collect Order.

### Host project conventions (discovered / planned)

Same React/Express stack as Sprint 1–2 unless noted:

- **Folder layout:** add `packages/fulfillment/{shared,server,client}` beside checkout and payments modules
- **State management:** employee session binds *store employee* to *click-and-collect store*; queue and order detail fetch scoped APIs
- **Route guard:** fulfillment routes require *store employee* role — *customer* receives 403 or redirect to customer shell (AC Prepare #5)
- **Queue scope:** API and UI filter by employee-bound *click-and-collect store* — no cross-store mixing (AC Prepare #4)
- **Status lifecycle:** *order fulfillment* progresses `awaiting preparation` → `ready for collection` → `complete` (or `collected` / `closed` after handoff)

### Screens (carried from lo-fi and IA)

| Screen | Layout | Route (planned) | Stories |
| --- | --- | --- | --- |
| Fulfillment — Orders | stack | `/employee/fulfillment/orders` | Prepare Click-and-Collect Orders for Pickup |
| Fulfillment — Order | stack | `/employee/fulfillment/orders/:orderId` | Fulfill Click-and-Collect Order |

**Employee chrome (Sprint 3):** employee header with bound *click-and-collect store* name · **Fulfillment** (active on fulfillment routes) · **Update stock** · **Sign out**. Distinct from customer header — no Find Store · catalog · Cart nav.

#### Fulfillment — Orders — regions and affordances

Lo-fi: `fulfillment-orders.md` · `fulfillment-orders.drawio`

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| employee header · store · Fulfillment · Sign out | chrome | store · Fulfillment · Sign out | Employee-only navigation; Fulfillment marks current section |
| order queue | list | columns: order id · customer · status · pickup time | Each row: paid *click-and-collect order* scoped to employee *click-and-collect store* |
| order queue actions | list actions | open order · mark preparing | open order → `/employee/fulfillment/orders/:orderId`; mark preparing primary → updates *order fulfillment* to *ready for collection* |

**Conditional states:**
- Paid confirmed orders only: unpaid or failed-checkout orders excluded from queue (AC Prepare #3)
- Store scoped: orders for other *stores* not listed (AC Prepare #4)
- *Customer* role: fulfillment queue route unavailable — 403 or redirect (AC Prepare #5)
- Empty queue: order queue shows empty state; mark preparing and open order hidden until rows exist
- After mark preparing: row status updates to *ready for collection*; order remains in queue until handoff completes (AC Prepare #2)

#### Fulfillment — Order — regions and affordances

Lo-fi: `fulfillment-order.md` · `fulfillment-order.drawio`

| Region | Type | Controls (verbatim labels) | Interaction |
| --- | --- | --- | --- |
| employee header · store · Fulfillment · Sign out | chrome | store · Fulfillment · Sign out | Same employee chrome as queue screen |
| order detail | body | form (read-only) | order id · product · click-and-collect store · order fulfillment | Shows *cart line* products with *cart quantity*, bound *click-and-collect store*, current *order fulfillment* status |
| order detail actions | body | form buttons | back to queue · fulfill click-and-collect order | fulfill click-and-collect order primary when *ready for collection*; back to queue → `/employee/fulfillment/orders` |

**Conditional states:**
- *Order fulfillment* *ready for collection*: fulfill click-and-collect order enabled (AC Fulfill #1)
- *awaiting preparation*: fulfill click-and-collect order disabled; warning that preparation is incomplete (AC Fulfill #4)
- After successful fulfill: *order fulfillment* *complete*; order removed from active queue; status shows *collected* or *closed* (AC Fulfill #2, #5)
- Repeat fulfill attempt on completed order: action blocked; no second handoff (AC Fulfill #5)
- back to queue: returns without completing handoff (AC Fulfill #1 navigation)

### Visual direction (Sprint 3 — employee chrome)

Reuse Sprint 1 token scale with employee-specific roles. Align with Increment 1 employee surfaces (Update Stock) for header continuity.

| Role | Typography / colour | Usage |
| --- | --- | --- |
| display | sans-serif, 24/32, weight 600, `#1A1A2E` | Page title: Fulfillment — Orders · Fulfillment — Order |
| body | sans-serif, 16/24, weight 400, `#2D2D2D` | Order rows, product lines, customer contact |
| label | sans-serif, 14/20, weight 500, `#5C5C5C` | Column headers: order id · customer · status · pickup time |
| accent | `#2E6B4A` | Primary: mark preparing · fulfill click-and-collect order (employee actions — distinct from customer accent) |
| surface | `#FFFFFF` | Screen background |
| surface-muted | `#F0F4F1` | Queue row hover / selected order highlight |
| warning | `#D68910` | Preparation-incomplete handoff warning |
| danger | `#C0392B` | Access denied messaging for unauthorized roles |
| focus | 2px solid `#2E6B4A`, offset 2px | Keyboard focus ring on queue actions and fulfill button |
| spacing scale | 4 · 8 · 16 · 24 · 32 px | Region padding and list row gaps |

*order fulfillment* status badges: text label plus icon — not colour-only. States: *awaiting preparation*, *ready for collection*, *complete* / *collected* / *closed*.

### Implementation targets (planned — Engineering)

| Screen / concern | Primary component(s) | Server module |
| --- | --- | --- |
| Fulfillment queue | `FulfillmentOrdersView.tsx`, `FulfillmentQueueRow.tsx` | `packages/fulfillment/server/fulfillment-queue.service.ts`, `FulfillmentApi` |
| Mark preparing | `MarkPreparingButton.tsx` | `POST /api/v1/fulfillment/orders/:orderId/prepare` |
| Order detail | `FulfillmentOrderView.tsx`, `OrderLineList.tsx` | `GET /api/v1/fulfillment/orders/:orderId` |
| Fulfill handoff | `FulfillOrderButton.tsx` | `POST /api/v1/fulfillment/orders/:orderId/fulfill` |
| Employee header | `EmployeeNav.tsx` | employee session / store binding |
| Role guard | `RequireStoreEmployee.tsx` route wrapper | auth middleware — blocks *customer* |
| Queue filter | — | server enforces *click-and-collect store* scope and paid-only filter |

---

## AC → behaviour → test mapping

One row per AC clause for Sprint 1, Sprint 2, and Sprint 3 stories. Status **pending (Engineering)** until implementation pass.

### Add Product to Cart

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Add Product to Cart | 1 | add to cart on Product Details places *product* into *shopping cart* with *cart quantity* ≥ 1 | `Add Product to Cart — AC 1: product placed with cart quantity` | pending |
| Add Product to Cart | 2 | Repeat add to cart increases *cart quantity* on existing line; no duplicate line | `Add Product to Cart — AC 2: merge increases quantity no duplicate` | pending |
| Add Product to Cart | 3 | Unavailable *stock availability* blocks add; warning shown; no line created | `Add Product to Cart — AC 3: unavailable blocked with warning` | pending |
| Add Product to Cart | 4 | Opening Shopping Cart shows new line with product identity and editable *cart quantity* | `Add Product to Cart — AC 4: cart shows identity and quantity` | pending |
| Add Product to Cart | 5 | Empty cart allows catalog browse; checkout not offered until at least one line | `Add Product to Cart — AC 5: empty cart no checkout browse ok` | pending |

### Update Cart Quantity

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Update Cart Quantity | 1 | Each *cart line* shows editable *cart quantity*; customer can run update quantity | `Update Cart Quantity — AC 1: editable cart quantity per line` | pending |
| Update Cart Quantity | 2 | Increase saves higher count; line total reflects new *cart quantity* | `Update Cart Quantity — AC 2: increase saves line total` | pending |
| Update Cart Quantity | 3 | Decrease to positive whole number saves lower count; line remains | `Update Cart Quantity — AC 3: decrease positive keeps line` | pending |
| Update Cart Quantity | 4 | Zero quantity rejected with message directing to remove | `Update Cart Quantity — AC 4: zero rejected directs remove` | pending |
| Update Cart Quantity | 5 | Updated counts persist after return to catalog and reopen cart | `Update Cart Quantity — AC 5: counts persist across browse` | pending |

### Remove Product from Cart

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Remove Product from Cart | 1 | remove offered per line; distinct from setting *cart quantity* to zero | `Remove Product from Cart — AC 1: remove distinct from zero edit` | pending |
| Remove Product from Cart | 2 | Confirmed remove deletes line; quantity no longer counts toward checkout | `Remove Product from Cart — AC 2: confirmed remove deletes line` | pending |
| Remove Product from Cart | 3 | Removing last line empties cart; guest checkout unavailable | `Remove Product from Cart — AC 3: last remove empties blocks checkout` | pending |
| Remove Product from Cart | 4 | Removing one line leaves remaining lines and quantities unchanged | `Remove Product from Cart — AC 4: partial remove unchanged remainder` | pending |
| Remove Product from Cart | 5 | After remove, add product again does not restore removed line | `Remove Product from Cart — AC 5: re-add does not restore removed` | pending |

### Select Click-and-Collect Store

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Select Click-and-Collect Store | 1 | checkout from non-empty cart lists every eligible *store* as selectable *click-and-collect store* | `Select Click-and-Collect Store — AC 1: all stores selectable` | pending |
| Select Click-and-Collect Store | 2 | selecting *store* binds *click-and-collect store*; shows identity and address | `Select Click-and-Collect Store — AC 2: bind shows identity address` | pending |
| Select Click-and-Collect Store | 3 | no *click-and-collect store*: place order disabled; no *order confirmation* | `Select Click-and-Collect Store — AC 3: payment blocked without store` | pending |
| Select Click-and-Collect Store | 4 | change store replaces binding; only one *click-and-collect store* on session | `Select Click-and-Collect Store — AC 4: change replaces single binding` | pending |
| Select Click-and-Collect Store | 5 | chosen *click-and-collect store* attaches to placed order on payment success | `Select Click-and-Collect Store — AC 5: store on paid order` | pending |

### Check Out as Guest

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Check Out as Guest | 1 | checkout from cart with lines starts *guest checkout* without sign-in; guest-only label | `Check Out as Guest — AC 1: guest checkout no sign-in` | pending |
| Check Out as Guest | 2 | collects email for *order confirmation*; no registration or login | `Check Out as Guest — AC 2: email no registration` | pending |
| Check Out as Guest | 3 | empty cart blocks checkout; directs to catalog or cart | `Check Out as Guest — AC 3: empty cart blocked` | pending |
| Check Out as Guest | 4 | sections advance store → billing → payment toward place order | `Check Out as Guest — AC 4: store billing payment order` | pending |
| Check Out as Guest | 5 | success creates *click-and-collect order* without customer account | `Check Out as Guest — AC 5: order without account` | pending |

### Enter Billing Address

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Enter Billing Address | 1 | billing step shows name · street · city · postal code · country fields | `Enter Billing Address — AC 1: billing fields presented` | pending |
| Enter Billing Address | 2 | valid submit saves *billing address* on session; unlocks payment step | `Enter Billing Address — AC 2: valid saves unlocks payment` | pending |
| Enter Billing Address | 3 | incomplete submit shows field errors; no *StripeWave* | `Enter Billing Address — AC 3: incomplete rejects no stripewave` | pending |
| Enter Billing Address | 4 | revised address replaces prior values on session | `Enter Billing Address — AC 4: revise replaces prior` | pending |
| Enter Billing Address | 5 | paid order includes captured *billing address* | `Enter Billing Address — AC 5: address on paid order` | pending |

### Select Payment Method

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Select Payment Method | 1 | payment step shows card only; processor labeled *StripeWave* | `Select Payment Method — AC 1: card stripewave only` | pending |
| Select Payment Method | 2 | selecting card enables place order; records *payment method* on session | `Select Payment Method — AC 2: card enables place order` | pending |
| Select Payment Method | 3 | no *payment method*: blocks *StripeWave*; can fix prior steps | `Select Payment Method — AC 3: blocked without method` | pending |
| Select Payment Method | 4 | no cash wallet or BNPL alternatives offered | `Select Payment Method — AC 4: no alternative methods` | pending |
| Select Payment Method | 5 | place order passes card details to *StripeWave* | `Select Payment Method — AC 5: details to stripewave` | pending |

### Process Card Payment via StripeWave

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Process Card Payment via StripeWave | 1 | place order invokes *StripeWave*; waits for success or failure | `Process Card Payment via StripeWave — AC 1: invokes waits response` | pending |
| Process Card Payment via StripeWave | 2 | success creates paid *click-and-collect order*; clears *shopping cart* | `Process Card Payment via StripeWave — AC 2: success order clears cart` | pending |
| Process Card Payment via StripeWave | 3 | failure shows message; no order or confirmation | `Process Card Payment via StripeWave — AC 3: failure no order` | pending |
| Process Card Payment via StripeWave | 4 | processing prevents duplicate payment submit | `Process Card Payment via StripeWave — AC 4: duplicate blocked` | pending |
| Process Card Payment via StripeWave | 5 | failure leaves recoverable *shopping cart* for retry | `Process Card Payment via StripeWave — AC 5: cart recoverable on failure` | pending |

### Confirm Order and Send Confirmation Email

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Confirm Order and Send Confirmation Email | 1 | success sends *order confirmation* email with order id and *click-and-collect store* | `Confirm Order and Send Confirmation Email — AC 1: email with store` | pending |
| Confirm Order and Send Confirmation Email | 2 | confirmation screen shows order id · *click-and-collect store* · total · email sent | `Confirm Order and Send Confirmation Email — AC 2: summary on screen` | pending |
| Confirm Order and Send Confirmation Email | 3 | no confirmation until *StripeWave* success; no premature route | `Confirm Order and Send Confirmation Email — AC 3: withheld until success` | pending |
| Confirm Order and Send Confirmation Email | 4 | paid order visible in fulfillment queue for *click-and-collect store* (server) | `Confirm Order and Send Confirmation Email — AC 4: queue visibility` | pending |
| Confirm Order and Send Confirmation Email | 5 | continue shopping → catalog; order not editable via cart | `Confirm Order and Send Confirmation Email — AC 5: continue shopping committed` | pending |

### Prepare Click-and-Collect Orders for Pickup

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Prepare Click-and-Collect Orders for Pickup | 1 | Fulfillment Queue lists paid *click-and-collect orders* with order id, customer contact, status, pickup context | `Prepare Click-and-Collect Orders for Pickup — AC 1: queue lists paid orders` | pending |
| Prepare Click-and-Collect Orders for Pickup | 2 | mark preparing updates *order fulfillment* to *ready for collection*; store scope unchanged | `Prepare Click-and-Collect Orders for Pickup — AC 2: mark preparing ready for collection` | pending |
| Prepare Click-and-Collect Orders for Pickup | 3 | unpaid or unconfirmed orders excluded from queue | `Prepare Click-and-Collect Orders for Pickup — AC 3: unpaid excluded` | pending |
| Prepare Click-and-Collect Orders for Pickup | 4 | queue shows only orders for employee *click-and-collect store* | `Prepare Click-and-Collect Orders for Pickup — AC 4: store scoped queue` | pending |
| Prepare Click-and-Collect Orders for Pickup | 5 | *customer* cannot access queue or preparation actions | `Prepare Click-and-Collect Orders for Pickup — AC 5: customer blocked` | pending |

### Fulfill Click-and-Collect Order

| Story | Clause | Behaviour | Test name | Status |
| --- | --- | --- | --- | --- |
| Fulfill Click-and-Collect Order | 1 | order detail shows lines, *click-and-collect store*, status; offers fulfill when ready | `Fulfill Click-and-Collect Order — AC 1: detail shows lines and fulfill offer` | pending |
| Fulfill Click-and-Collect Order | 2 | confirm fulfill marks *order fulfillment* complete; removes from active queue | `Fulfill Click-and-Collect Order — AC 2: fulfill complete removes queue` | pending |
| Fulfill Click-and-Collect Order | 3 | employee matches order proof; *customer* receives products at store | `Fulfill Click-and-Collect Order — AC 3: handoff at store` | pending |
| Fulfill Click-and-Collect Order | 4 | not-yet-prepared order blocks fulfill with warning; status not complete | `Fulfill Click-and-Collect Order — AC 4: unprepared blocked` | pending |
| Fulfill Click-and-Collect Order | 5 | completed order shows collected/closed; repeat fulfill blocked | `Fulfill Click-and-Collect Order — AC 5: collected no repeat fulfill` | pending |

---

## Accessibility implementation (planned)

| Check | Status | Notes |
| --- | --- | --- |
| Every input has a programmatic label | planned | *cart quantity* inputs use `<label>` or `aria-label` including product name |
| Focus order matches reading order | planned | header nav → cart lines (product → quantity → remove) → continue shopping → checkout |
| Focus is visible | planned | accent focus ring per Visual direction table |
| Errors are programmatically associated | planned | Zero-quantity and unavailable-add messages use `role="alert"` + `aria-describedby` on quantity field |
| State cues are not colour-only | planned | Disabled checkout: `aria-disabled` + visible muted styling; unavailable stock: text + icon |
| Keyboard reachable | planned | Tab through lines; Enter on remove opens confirm dialog; quantity steppers keyboard-operable |
| Axe passes | planned | No rules silenced |

**Sprint 2 checkout (planned):**

| Check | Status | Notes |
| --- | --- | --- |
| Pickup store listbox | planned | `role="listbox"` / `role="option"`; `aria-selected` on chosen *click-and-collect store* |
| Billing fields labeled | planned | Each of name · street · city · postal code · country has `<label>` or `aria-labelledby` |
| Error association | planned | validation error area linked via `aria-describedby` on invalid billing fields |
| place order disabled state | planned | `aria-disabled` + visible styling when store/billing/payment incomplete — not colour-only |
| Processing state | planned | `aria-busy` during *StripeWave*; duplicate submit prevented |
| Order confirmation read-only | planned | Summary fields not focus-trapped inputs; continue shopping is primary action |

**Sprint 3 fulfillment (planned):**

| Check | Status | Notes |
| --- | --- | --- |
| Employee route guard | planned | *customer* blocked from `/employee/fulfillment/*`; programmatic access-denied message |
| Queue list semantics | planned | order queue uses `<table>` or `role="grid"` with column headers matching lo-fi labels |
| Status badges accessible | planned | *order fulfillment* status announced via text + icon — not colour-only |
| mark preparing / fulfill buttons | planned | Primary actions keyboard-reachable; disabled state uses `aria-disabled` when blocked |
| Preparation warning | planned | Unprepared fulfill attempt: `role="alert"` warning linked via `aria-describedby` |
| Focus order | planned | employee header → queue rows (open order · mark preparing) or order detail → back to queue → fulfill |
| Axe passes | planned | No rules silenced on employee fulfillment routes |

---

## Performance constraints

| Constraint | Budget | Current | Notes |
| --- | --- | --- | --- |
| Cart screen bundle | baseline TBD | — | Lazy-load cart module route if code-split |
| Initial paint | no regression vs shell | — | Render empty state or skeleton without blocking on cart API |
| Cart API round-trip | async, non-blocking | — | Optimistic UI optional; must reconcile on error |
| Animation | ≤16 ms/frame | — | Line remove: opacity transition; respect prefers-reduced-motion |
| Checkout submit | no double-charge UX | — | Disable place order until *StripeWave* responds; idempotent server token |
| Order confirmation route | lazy-load | — | Split checkout bundle from confirmation view |
| Fulfillment queue route | lazy-load | — | Split employee fulfillment module from customer bundle |
| Queue refresh | non-blocking poll optional | — | mark preparing / fulfill update row without full page reload |
| Employee auth check | server-first | — | UI guard mirrors API 403 — do not rely on client-only hiding |

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | Sprint 1 shopping cart + Product Details add entry from exploration lo-fi + AC + spec-by-example |
| 2026-05-31 | extend | Sprint 2 checkout — Guest & pickup + Order Confirmation; 6 stories, 30 AC rows; lo-fi checkout-guest-pickup + order-confirmation |
| 2026-05-31 | engineering | Sprint 1–3 engineering impl: packages/cart, checkout, fulfillment client modules; 6+8+8 client tests GREEN |
