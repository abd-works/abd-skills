# Information architecture — PawPlace mini (whole solution)

> **Companion to** `information-architecture.drawio`. Authoritative structured spec; canvas must stay in sync.

## Metadata

| Field | Value |
| --- | --- |
| Scope | Whole solution — increments 1 (walk-in driver) and 2 (click-and-collect) |
| Story map | `docs/end-to-end/discovery/stories/story-graph.json` |
| Domain terms | `docs/end-to-end/discovery/domain/domain-terms.md` |
| Canvas (`.drawio`) | `docs/end-to-end/discovery/ux/information-architecture.drawio` |
| Last canvas update | 2026-05-31 |

## Description

First-pass IA for PawPlace mini: customer journeys to find a *store*, browse *catalog* with *stock availability*, manage a *shopping cart*, complete *guest checkout* for *click-and-collect*, and store-employee surfaces for *product stock levels* and *order fulfillment*. Supports discovery alignment before exploration mockups and acceptance criteria.

---

## Story trace table

| Story | Screen | Region | Action / transition |
| --- | --- | --- | --- |
| View Store Map | Find Store — Map | store map | view map |
| Calculate Distance to Store | Find Store — Map | store map | use location |
| View Store List | Find Store — List | store list | view list |
| Calculate Distance to Store | Find Store — List | store list | sort by distance |
| View Product Details | Browse Catalog | product list | view product → Product Details |
| Display Real-Time Stock Availability | Product Details | product summary | (grouped system) |
| Update Product Stock Levels | Update Stock | stock list | edit levels |
| Add Product to Cart | Product Details | product summary | add to cart → Shopping Cart |
| Update Cart Quantity | Shopping Cart | cart lines | change quantity |
| Remove Product from Cart | Shopping Cart | cart lines | remove line |
| Select Click-and-Collect Store | Checkout — Guest & pickup | pickup store | select store |
| Check Out as Guest | Checkout — Guest & pickup | guest checkout | continue |
| Enter Billing Address | Checkout — Guest & pickup | billing address | enter address |
| Select Payment Method | Checkout — Guest & pickup | payment method | select card |
| Process Card Payment via StripeWave | Order Confirmation | (grouped system) | pay |
| Confirm Order and Send Confirmation Email | Order Confirmation | order summary | (grouped system) |
| Prepare Click-and-Collect Orders for Pickup | Fulfillment — Orders | order queue | mark preparing |
| Fulfill Click-and-Collect Order | Fulfillment — Order | order detail | hand off |

---

## Domain term trace table

| Term | Appears as | Screen | Region |
| --- | --- | --- | --- |
| store | row / map pin | Find Store — Map, List | store map, store list |
| store map | region | Find Store — Map | store map |
| store list | region | Find Store — List | store list |
| distance to store | sort label | Find Store — List | store list |
| catalog | region title | Browse Catalog | product list |
| product | row | Browse Catalog, Product Details | product list, product summary |
| stock availability | field | Product Details | product summary |
| product stock levels | row field | Update Stock | stock list |
| shopping cart | region | Shopping Cart | cart lines |
| cart quantity | field | Shopping Cart | cart lines |
| click-and-collect store | field | Checkout — Guest & pickup | pickup store |
| billing address | fields | Checkout — Guest & pickup | billing address |
| payment method | field | Checkout — Guest & pickup | payment method |
| click-and-collect order | row | Fulfillment — Orders, Order | order queue, order detail |
| order fulfillment | actions | Fulfillment — Order | order detail |

---

## Navigation

### Site map — screens

#### Find Store — Map

- **Description:** Customer discovers PawPlace *stores* on a map and sees proximity.
- **Source:** [Find a Store](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `stack` — site header + map body

```
[ Find Store — Map ]                               stack
  ┌─────────────────────────────────────────────┐
  │ site header · Find Store · Catalog · Cart   │
  ├─────────────────────────────────────────────┤
  │ [ Map ] [ List ]                            │  ← tab bar (List inactive/greyed)
  ├─────────────────────────────────────────────┤
  │ store map                                   │
  │   pin · store name · address                │
  │   pin · store name · address                │
  │ use my location · select store              │
  └─────────────────────────────────────────────┘
```

- **Inactive tabs (greyed):** List
- **Chrome (shared regions — named only):** site header
- **From (incoming transitions):**
  - from app entry — trigger: open PawPlace
  - from Find Store — List — trigger: selects Map tab
  - from Browse Catalog — trigger: Find Store (header)
- **To (outgoing transitions):**
  - to Find Store — List — trigger: selects List tab
  - to Browse Catalog — trigger: select store · continue to catalog
- **Content regions**
  - **store map**
    - Row fields: `pin · store name · address · distance`
    - Actions: `use my location · select store`
- **In-scope user stories (~4 max):**
  - View Store Map — maps to: store map / view map
  - Calculate Distance to Store — maps to: store map / use my location
- **Domain terms (visible only):** store, store map, distance to store

#### Find Store — List

- **Description:** Customer browses *stores* as a list ranked by proximity.
- **Source:** [Find a Store](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `stack` — site header + list body

```
[ Find Store — List ]                              stack
  ┌─────────────────────────────────────────────┐
  │ site header                                 │
  ├─────────────────────────────────────────────┤
  │ [ Map ] [ List ]                            │  ← Map inactive/greyed
  ├─────────────────────────────────────────────┤
  │ store list                                  │
  │   store name · address · distance           │
  │   store name · address · distance           │
  │ use my location · select store              │
  └─────────────────────────────────────────────┘
```

- **Inactive tabs (greyed):** Map
- **Chrome:** same as Find Store — Map
- **From (incoming transitions):**
  - from Find Store — Map — trigger: selects List tab
- **To (outgoing transitions):**
  - to Find Store — Map — trigger: selects Map tab
  - to Browse Catalog — trigger: select store
- **Content regions**
  - **store list**
    - Row fields: `store name · address · distance to store`
    - Actions: `use my location · select store`
- **In-scope user stories (~4 max):**
  - View Store List — maps to: store list / view list
  - Calculate Distance to Store — maps to: store list / use my location
- **Domain terms (visible only):** store, store list, distance to store

#### Browse Catalog

- **Description:** Customer browses the *catalog* for the chosen *store* and opens a *product*.
- **Source:** [Browse Catalog & Stock](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `sidebar` — selected store panel + product list body

```
[ Browse Catalog ]                                 sidebar
  ┌──────────────┬──────────────────────────────┐
  │ selected     │ product list                 │
  │ store        │   product · price · badge    │
  │ (panel)      │   product · price · badge    │
  │              │ view product                 │
  └──────────────┴──────────────────────────────┘
```

- **Chrome:** site header
- **From (incoming transitions):**
  - from Find Store — Map — trigger: select store
  - from Find Store — List — trigger: select store
  - from Product Details — trigger: back to catalog
  - from Shopping Cart — trigger: continue shopping (header)
- **To (outgoing transitions):**
  - to Product Details — trigger: view product
  - to Shopping Cart — trigger: Cart (header)
  - to Find Store — Map — trigger: Find Store (header)
  - to Update Stock — trigger: employee menu (staff only)
- **Content regions**
  - **selected store**
    - Row fields: `store name · address`
    - Actions: `change store`
  - **product list**
    - Row fields: `product name · price · in stock badge`
    - Actions: `view product`
- **In-scope user stories (~4 max):**
  - View Product Details — maps to: product list / view product → Product Details
- **Domain terms (visible only):** catalog, product, store

#### Product Details

- **Description:** Customer inspects a *product* and sees *stock availability* at the store.
- **Source:** [Browse Catalog & Stock](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `stack`

```
[ Product Details ]                                stack
  ┌─────────────────────────────────────────────┐
  │ site header                                 │
  ├─────────────────────────────────────────────┤
  │ product summary                             │
  │   product name · price · description        │
  │   stock availability · quantity at store    │
  │ add to cart · back to catalog               │
  └─────────────────────────────────────────────┘
```

- **Chrome:** site header
- **From (incoming transitions):**
  - from Browse Catalog — trigger: view product
- **To (outgoing transitions):**
  - to Browse Catalog — trigger: back to catalog
  - to Shopping Cart — trigger: add to cart
- **Content regions**
  - **product summary**
    - Row fields: `product name · price · description · stock availability`
    - Actions: `add to cart · back to catalog`
- **In-scope user stories (~4 max):**
  - View Product Details — maps to: product summary / view
- **Groups system stories:**
  - Display Real-Time Stock Availability
- **Domain terms (visible only):** product, stock availability

#### Update Stock

- **Description:** *Store employee* maintains *product stock levels* for the active store.
- **Source:** [Browse Catalog & Stock](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `sidebar` — store context panel + stock list body

```
[ Update Stock ]                                   sidebar
  ┌──────────────┬──────────────────────────────┐
  │ store        │ stock list                   │
  │ (panel)      │   product · on-hand count    │
  │              │   product · on-hand count    │
  │              │ save levels                  │
  └──────────────┴──────────────────────────────┘
```

- **Chrome:** employee header (store name · Fulfillment · Sign out)
- **From (incoming transitions):**
  - from Browse Catalog — trigger: employee menu
  - from Fulfillment — Orders — trigger: Update stock (employee nav)
- **To (outgoing transitions):**
  - to Browse Catalog — trigger: customer view (employee nav)
  - to Fulfillment — Orders — trigger: Fulfillment (employee nav)
- **Content regions**
  - **stock list**
    - Row fields: `product · product stock levels`
    - Actions: `edit level · save levels`
- **In-scope user stories (~4 max):**
  - Update Product Stock Levels — maps to: stock list / edit level
- **Domain terms (visible only):** product, product stock levels

#### Shopping Cart

- **Description:** Customer reviews *shopping cart* lines before checkout.
- **Source:** [Shopping Cart](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `stack`

```
[ Shopping Cart ]                                  stack
  ┌─────────────────────────────────────────────┐
  │ site header                                 │
  ├─────────────────────────────────────────────┤
  │ cart lines                                  │
  │   product · cart quantity · line total      │
  │   product · cart quantity · line total      │
  │ update quantity · remove · checkout         │
  └─────────────────────────────────────────────┘
```

- **Chrome:** site header
- **From (incoming transitions):**
  - from Product Details — trigger: add to cart
  - from Checkout — Guest & pickup — trigger: back to cart
  - from site header — trigger: Cart
- **To (outgoing transitions):**
  - to Checkout — Guest & pickup — trigger: checkout
  - to Browse Catalog — trigger: continue shopping
- **Content regions**
  - **cart lines**
    - Row fields: `product · cart quantity · line total`
    - Actions: `update quantity · remove · checkout`
- **In-scope user stories (~4 max):**
  - Add Product to Cart — maps to: (incoming) Product Details / add to cart
  - Update Cart Quantity — maps to: cart lines / update quantity
  - Remove Product from Cart — maps to: cart lines / remove
- **Domain terms (visible only):** shopping cart, product, cart quantity

#### Checkout — Guest & pickup

- **Description:** Guest selects *click-and-collect store*, enters *billing address*, and chooses *payment method*.
- **Source:** [Checkout & Payment](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `form` — stacked checkout sections

```
[ Checkout — Guest & pickup ]                      form
  ┌─────────────────────────────────────────────┐
  │ site header                                 │
  ├─────────────────────────────────────────────┤
  │ pickup store                                │
  │   click-and-collect store · store address   │
  │ guest checkout                              │
  │ billing address                             │
  │   name · street · city · postal · country   │
  │ payment method                              │
  │   card · StripeWave                         │
  │ place order                                 │
  └─────────────────────────────────────────────┘
```

- **Chrome:** site header
- **From (incoming transitions):**
  - from Shopping Cart — trigger: checkout
- **To (outgoing transitions):**
  - to Order Confirmation — trigger: place order
  - to Shopping Cart — trigger: back to cart
- **Content regions**
  - **pickup store**
    - Row fields: `click-and-collect store · store address`
    - Actions: `change store`
  - **guest checkout**
    - Row fields: `email · phone`
    - Actions: `continue`
  - **billing address**
    - Row fields: `name · street · city · postal code · country`
    - Actions: `continue`
  - **payment method**
    - Row fields: `card last four · StripeWave`
    - Actions: `place order`
- **In-scope user stories (~4 max):**
  - Select Click-and-Collect Store — maps to: pickup store / change store
  - Check Out as Guest — maps to: guest checkout / continue
  - Enter Billing Address — maps to: billing address / continue
  - Select Payment Method — maps to: payment method / place order
- **Domain terms (visible only):** click-and-collect store, billing address, payment method, guest checkout

#### Order Confirmation

- **Description:** Customer sees placed *click-and-collect order* after payment and email confirmation.
- **Source:** [Checkout & Payment](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `stack`

```
[ Order Confirmation ]                             stack
  ┌─────────────────────────────────────────────┐
  │ site header                                 │
  ├─────────────────────────────────────────────┤
  │ order summary                               │
  │   order id · pickup store · total           │
  │   confirmation sent · continue shopping   │
  └─────────────────────────────────────────────┘
```

- **Chrome:** site header
- **From (incoming transitions):**
  - from Checkout — Guest & pickup — trigger: place order
- **To (outgoing transitions):**
  - to Browse Catalog — trigger: continue shopping
- **Content regions**
  - **order summary**
    - Row fields: `order id · click-and-collect store · total · confirmation email`
    - Actions: `continue shopping`
- **In-scope user stories:** *(none — system-only surface)*
- **Groups system stories:**
  - Process Card Payment via StripeWave
  - Confirm Order and Send Confirmation Email
- **Domain terms (visible only):** click-and-collect order, order confirmation

#### Fulfillment — Orders

- **Description:** *Store employee* sees *click-and-collect orders* awaiting preparation.
- **Source:** [Store Fulfillment](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `stack`

```
[ Fulfillment — Orders ]                           stack
  ┌─────────────────────────────────────────────┐
  │ employee header                             │
  ├─────────────────────────────────────────────┤
  │ order queue                                 │
  │   order id · customer · status · pickup time│
  │   order id · customer · status · pickup time│
  │ open order · mark preparing                 │
  └─────────────────────────────────────────────┘
```

- **Chrome:** employee header
- **From (incoming transitions):**
  - from Update Stock — trigger: Fulfillment (employee nav)
  - from Fulfillment — Order — trigger: back to queue
- **To (outgoing transitions):**
  - to Fulfillment — Order — trigger: open order
  - to Update Stock — trigger: Update stock (employee nav)
- **Content regions**
  - **order queue**
    - Row fields: `order id · customer name · status · pickup time`
    - Actions: `open order · mark preparing`
- **In-scope user stories (~4 max):**
  - Prepare Click-and-Collect Orders for Pickup — maps to: order queue / mark preparing
- **Domain terms (visible only):** click-and-collect order

#### Fulfillment — Order

- **Description:** *Store employee* completes *order fulfillment* for one pickup order.
- **Source:** [Store Fulfillment](docs/end-to-end/discovery/stories/story-graph.json)
- **Layout:** `stack`

```
[ Fulfillment — Order ]                            stack
  ┌─────────────────────────────────────────────┐
  │ employee header                             │
  ├─────────────────────────────────────────────┤
  │ order detail                                │
  │   order id · lines · pickup store · status  │
  │ fulfill order · back to queue               │
  └─────────────────────────────────────────────┘
```

- **Chrome:** employee header
- **From (incoming transitions):**
  - from Fulfillment — Orders — trigger: open order
- **To (outgoing transitions):**
  - to Fulfillment — Orders — trigger: back to queue · fulfill order
- **Content regions**
  - **order detail**
    - Row fields: `order id · product lines · click-and-collect store · status`
    - Actions: `fulfill order · back to queue`
- **In-scope user stories (~4 max):**
  - Fulfill Click-and-Collect Order — maps to: order detail / fulfill order
- **Domain terms (visible only):** click-and-collect order, order fulfillment

---

### Navigational components

#### Site header (global chrome)

- **Appears on:** Find Store — Map, Find Store — List, Browse Catalog, Product Details, Shopping Cart, Checkout — Guest & pickup, Order Confirmation
- **Links to:** Find Store — Map, Browse Catalog, Shopping Cart
- **Notes:** Primary customer navigation; no cart badge detail at IA level.

#### Find Store tab bar

- **Appears on:** Find Store — Map, Find Store — List
- **Links to:** Find Store — Map, Find Store — List
- **Notes:** Map/List are sibling tab-state screens, not sub-regions.

#### Employee header (staff chrome)

- **Appears on:** Update Stock, Fulfillment — Orders, Fulfillment — Order
- **Links to:** Update Stock, Fulfillment — Orders, Browse Catalog (customer view)
- **Notes:** Separates store-employee flows from customer header.

---

## Content types (shared across screens)

#### Store

- **Source:** [Store](docs/end-to-end/discovery/domain/domain-terms.md)
- **Used on:** Find Store — Map, Find Store — List, Browse Catalog, Checkout — Guest & pickup, Fulfillment — Order
- **Hierarchy / collections:** store selected once per session context; list/map are collections
- **Key actions:** select store, change store, use my location

#### Product

- **Source:** [product](docs/end-to-end/discovery/domain/domain-terms.md)
- **Used on:** Browse Catalog, Product Details, Shopping Cart, Update Stock
- **Hierarchy / collections:** belongs to catalog at a store
- **Key actions:** view product, add to cart, edit stock level

#### Click-and-collect order

- **Source:** [click-and-collect order](docs/end-to-end/discovery/domain/domain-terms.md)
- **Used on:** Order Confirmation, Fulfillment — Orders, Fulfillment — Order
- **Hierarchy / collections:** queue of orders per store
- **Key actions:** place order, mark preparing, fulfill order, open order

---

## Change log

| Date | Direction | Summary |
| --- | --- | --- |
| 2026-05-31 | initial | Discovery IA for PawPlace mini — 10 screens, customer + employee flows. |
