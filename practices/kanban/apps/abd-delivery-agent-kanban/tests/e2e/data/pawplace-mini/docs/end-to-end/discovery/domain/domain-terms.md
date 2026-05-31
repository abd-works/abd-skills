---
state: domain-terms
---

# Module: [PawPlace mini]

Scope: Whole-solution vocabulary for PawPlace mini — 2 increments (walk-in driver, click-and-collect). Source: shaping module partition and story map.

**Key Abstractions (term grouping)**:
- **Store**: store, store map, store list, distance to store, click-and-collect store
- **Catalog**: product, catalog, real-time stock, stock availability, product stock levels
- **Cart**: shopping cart, cart quantity, add product to cart, remove product from cart
- **Order**: guest checkout, billing address, payment method, StripeWave, order confirmation, click-and-collect order, order fulfillment

---

# Core Domain

# Module: [Store]

## Store

*Store* is the physical PawPlace retail location a *customer* discovers via *store map*, *store list*, or *distance to store*, and later selects as the *click-and-collect store* for online orders. It owns location identity and selection; *catalog* and *order* depend on a chosen *store* but do not define it.

### store

- A *store* is a PawPlace retail location where customers browse *catalog* and collect orders.

**Ref — Find a Store epic**
Source: docs/end-to-end/shaping/story-map.md
Locator: lines 6–9
Extract: partial

### store map

- The *store map* shows *store* locations for the *customer* to choose where to shop.

**Ref — View Store Map**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 7
Extract: partial

### store list

- The *store list* presents *store* names and details as an alternative to the *store map*.

**Ref — View Store List**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 8
Extract: partial

### distance to store

- *Distance to store* ranks *stores* by proximity to the *customer*.

**Ref — Calculate Distance to Store**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 9
Extract: partial

### click-and-collect store

- The *click-and-collect store* is the *store* the *customer* picks at checkout for order pickup.

**Ref — Select Click-and-Collect Store**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 22
Extract: partial

---

# Module: [Catalog]

## Catalog

*Catalog* is the product assortment and per-*store* inventory view. *Customers* see *product* details and *real-time stock* / *stock availability*; *store employees* update *product stock levels*.

### product

- A *product* is an item in the PawPlace *catalog* offered at a *store*.

**Ref — View Product Details**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 12
Extract: partial

### catalog

- The *catalog* is the browsable set of *products* available through PawPlace.

**Ref — Browse Catalog & Stock epic**
Source: docs/end-to-end/shaping/story-map.md
Locator: lines 11–14
Extract: partial

### real-time stock

- *Real-time stock* reflects current on-hand quantity at the selected *store*.

**Ref — Display Real-Time Stock Availability**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 13
Extract: partial

### stock availability

- *Stock availability* tells the *customer* whether a *product* can be bought at a *store* now.

**Ref — Display Real-Time Stock Availability**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 13
Extract: partial

### product stock levels

- *Product stock levels* are on-hand counts a *store employee* maintains for each *product* at a *store*.

**Ref — Update Product Stock Levels**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 14
Extract: partial

---

# Module: [Cart]

## Cart

*Cart* holds line items before *guest checkout*. The *customer* uses *add product to cart*, adjusts *cart quantity*, or *remove product from cart*; the *shopping cart* persists selections until checkout.

### shopping cart

- The *shopping cart* aggregates selected *products* and quantities before *order* placement.

**Ref — Shopping Cart sub-epic**
Source: docs/end-to-end/shaping/story-map.md
Locator: lines 17–20
Extract: partial

### cart quantity

- *Cart quantity* is the count of a *product* line in the *shopping cart*.

**Ref — Update Cart Quantity**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 19
Extract: partial

### add product to cart

- *Add product to cart* places a *product* into the *shopping cart* from *catalog*.

**Ref — Add Product to Cart**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 18
Extract: partial

### remove product from cart

- *Remove product from cart* deletes a line from the *shopping cart*.

**Ref — Remove Product from Cart**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 20
Extract: partial

---

# Module: [Order]

## Order

*Order* covers *guest checkout*, payment via *StripeWave*, *order confirmation*, and *click-and-collect order* *fulfillment* at the chosen *store*. Guest-only — no accounts in this fixture.

### guest checkout

- *Guest checkout* lets a *customer* pay without an account, entering *billing address* and *payment method*.

**Ref — Check Out as Guest**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 23
Extract: partial

### billing address

- *Billing address* is payment contact information captured during *guest checkout*.

**Ref — Enter Billing Address**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 24
Extract: partial

### payment method

- *Payment method* is how the *customer* pays (card via *StripeWave* in this fixture).

**Ref — Select Payment Method**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 25
Extract: partial

### StripeWave

- *StripeWave* processes card payment for a *click-and-collect order*.

**Ref — Process Card Payment via StripeWave**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 26
Extract: partial

### order confirmation

- *Order confirmation* acknowledges a placed *click-and-collect order* (email in this fixture).

**Ref — Confirm Order and Send Confirmation Email**
Source: docs/end-to-end/shaping/story-map.md
Locator: line 27
Extract: partial

### click-and-collect order

- A *click-and-collect order* is paid online and picked up at the selected *click-and-collect store*.

**Ref — Checkout & Payment sub-epic**
Source: docs/end-to-end/shaping/story-map.md
Locator: lines 21–27
Extract: partial

### order fulfillment

- *Order fulfillment* is *store employee* preparation and handoff of a *click-and-collect order*.

**Ref — Store Fulfillment sub-epic**
Source: docs/end-to-end/shaping/story-map.md
Locator: lines 28–30
Extract: partial
