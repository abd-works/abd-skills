# Lo-fi mockups — Increment 2: Click-and-collect (cart, checkout, pickup)

> **Scope:** Shopping Cart, Checkout — Guest & pickup, Order Confirmation, Fulfillment — Orders, Fulfillment — Order. Companion flow diagram: `click-and-collect-flow.drawio`.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Increment 2 click-and-collect — cart, guest checkout, pickup fulfillment |
| Initial IA | `docs/end-to-end/discovery/ux/information-architecture.md` |
| AC source | `docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md` |
| Domain terms | `docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md` |
| Output folder | `docs/increments/2-click-and-collect/exploration/ux/` |
| Last updated | 2026-05-31 |

## Description

Lo-fi wireframes for the click-and-collect increment: *customer* manages a *shopping cart*, completes *guest checkout* by selecting a *click-and-collect store*, entering *billing address*, and paying via *StripeWave*; receives *order confirmation* with pickup location; *store employee* runs *prepare click-and-collect orders for pickup* and *fulfill click-and-collect order* to complete *order fulfillment*. Store discovery and catalog browsing are prerequisites from Increment 1.

## Screen index

| Screen | State file | Wireframe | Spec |
| --- | --- | --- | --- |
| Shopping Cart | `shopping-cart-state.json` | `shopping-cart.drawio` | `shopping-cart.md` |
| Checkout — Guest & pickup | `checkout-guest-pickup-state.json` | `checkout-guest-pickup.drawio` | `checkout-guest-pickup.md` |
| Order Confirmation | `order-confirmation-state.json` | `order-confirmation.drawio` | `order-confirmation.md` |
| Fulfillment — Orders | `fulfillment-orders-state.json` | `fulfillment-orders.drawio` | `fulfillment-orders.md` |
| Fulfillment — Order | `fulfillment-order-state.json` | `fulfillment-order.drawio` | `fulfillment-order.md` |
| Flow (combined) | `click-and-collect-flow-state.json` | `click-and-collect-flow.drawio` | — |

## Design reference

No production design images in workspace. Layout and regions follow discovery IA (`information-architecture.md`) and increment UL verbatim labels.

| Source | Panel/Region | UX element type | Key observations |
| --- | --- | --- | --- |
| IA — Shopping Cart | cart lines | list | Editable cart quantity per line; remove distinct from zero quantity; checkout primary when lines exist |
| IA — Checkout — Guest & pickup | pickup store | listbox | Selectable click-and-collect store before payment; store-first section order |
| IA — Checkout — Guest & pickup | guest checkout · billing address · payment method | form | Stacked checkout sections; guest-only (email); StripeWave card only |
| IA — Order Confirmation | order summary | form | Order id, pickup store, total, confirmation email sent |
| IA — Fulfillment — Orders | order queue | list | Paid click-and-collect orders scoped to store; mark preparing primary |
| IA — Fulfillment — Order | order detail | form | Order lines, pickup store, fulfill handoff action |

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | Cart, checkout, and pickup screens for Increment 2 exploration |
