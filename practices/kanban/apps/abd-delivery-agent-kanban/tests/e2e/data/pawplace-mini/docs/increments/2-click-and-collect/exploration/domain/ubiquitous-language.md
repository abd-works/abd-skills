---
state: ubiquitous-language
---

# Module: [PawPlace mini — Increment 2]

_Concept sketch for the click-and-collect increment: build a shopping cart, pay online as a guest via StripeWave, and pick up at the chosen store — store discovery and catalog browsing are prerequisites from Increment 1._

Scope: Increment 2 (click-and-collect) — shopping cart, guest checkout, StripeWave payment, click-and-collect store selection, order confirmation, and store-employee fulfillment. Excludes walk-in-only store discovery mechanics beyond what checkout requires. Guest checkout only — no customer accounts in this fixture.

**Terms**:
- **Cart**
  - **shopping cart** — aggregates selected products and quantities before order placement
  - **cart quantity** — count of a product line in the shopping cart
  - **update cart quantity** — changes the count of a product line in the shopping cart
  - **add product to cart** — places a product into the shopping cart from catalog
  - **remove product from cart** — deletes a line from the shopping cart
- **Order**
  - **click-and-collect order** — paid online and picked up at the selected click-and-collect store
  - **guest checkout** — checkout without an account, capturing billing and payment details
  - **click-and-collect store** — the store the customer picks at checkout for order pickup
  - **billing address** — payment contact information captured during guest checkout
  - **payment method** — how the customer pays (card via StripeWave in this fixture)
  - **StripeWave** — external card payment processor for click-and-collect orders
  - **order confirmation** — acknowledgment of a placed click-and-collect order (email in this fixture)
  - **order fulfillment** — store-employee preparation and handoff of a click-and-collect order
  - **prepare click-and-collect orders for pickup** — store employee stages paid orders for customer collection
  - **fulfill click-and-collect order** — store employee hands a prepared order to the customer at pickup

_A *customer* adds *products* to a *shopping cart*, adjusts *cart quantity*, and proceeds through *guest checkout* by choosing a *click-and-collect store*, entering a *billing address*, and paying with a *payment method* processed by *StripeWave*. On success the system issues *order confirmation* for a *click-and-collect order*. A *store employee* runs *prepare click-and-collect orders for pickup* then *fulfill click-and-collect order* to complete *order fulfillment*. No customer accounts appear in this increment._

---

# Core Domain

## Cart

*Cart* holds line items between *catalog* browsing and *guest checkout*. The *customer* uses *add product to cart*, adjusts *cart quantity*, or *remove product from cart*; the *shopping cart* persists selections until checkout converts them into a *click-and-collect order*.

### cart

- aggregates selected *products* and *cart quantities* before *order* placement
- persists line items while the *customer* continues browsing or moves to *guest checkout*
- **Invariant:** a *shopping cart* must contain at least one line before *guest checkout* can begin

### shopping cart

- is the working container the *customer* fills from *catalog*
- holds one or more *product* lines each with a *cart quantity*
- hands off its contents to *guest checkout*, producing a *click-and-collect order* when payment succeeds

### cart quantity

- is the count of a *product* line in the *shopping cart*
- changes when the *customer* runs *update cart quantity*
- **Invariant:** *cart quantity* for any line must be a positive whole number while the line remains in the *shopping cart*

### update cart quantity

- changes the *cart quantity* on an existing *shopping cart* line
- lets the *customer* increase or decrease how many of a *product* they intend to buy
- **Invariant:** *update cart quantity* must not leave a line with zero *cart quantity* — use *remove product from cart* instead

### add product to cart

- places a *product* from *catalog* into the *shopping cart*, producing or increasing a line with *cart quantity*
- respects *stock availability* at the browsing context — the *customer* should not add unavailable *products*
- may create a new line or merge into an existing line for the same *product*

### remove product from cart

- deletes a *product* line from the *shopping cart*
- clears the line's *cart quantity* so the item no longer counts toward checkout

### product *(boundary)*

- is the *catalog* item the *customer* selects when running *add product to cart*
- supplies identity and detail for each *shopping cart* line

#### Decisions made

- *Cart* owns pre-checkout line aggregation; *Order* owns payment and pickup (independence test).
- *Add product to cart*, *remove product from cart*, and *update cart quantity* are named as concepts because each is a distinct customer action with its own story (typing call).
- Store discovery and catalog browsing from Increment 1 are boundary dependencies — not re-modeled here (scope-fit test).

#### References

**Ref — Manage Cart sub-epic**
Source: docs/end-to-end/discovery/stories/story-map.md
Locator: lines 18–21
Extract: partial

**Ref — Increment 2 cart stories**
Source: docs/end-to-end/discovery/stories/thin-slicing.md
Locator: Increment 2 stories (Add/Update/Remove cart)
Extract: partial

**Ref — Cart module terms**
Source: docs/end-to-end/discovery/domain/domain-terms.md
Locator: Module Cart section
Extract: partial

---

## Order

*Order* covers *guest checkout*, payment via *StripeWave*, *order confirmation*, and *click-and-collect order* *fulfillment* at the chosen *click-and-collect store*. Guest-only — no accounts in this fixture. *Order* owns the paid commitment and pickup lifecycle; *Cart* supplies line items and *Store* supplies the pickup location.

### order

- converts a *shopping cart* into a paid *click-and-collect order* through *guest checkout*
- binds *billing address*, *payment method*, and *click-and-collect store* to the placed order
- progresses from payment to *order confirmation* to *order fulfillment*
- **Invariant:** every *click-and-collect order* in this increment is guest-only — no customer account is created or required

### click-and-collect order

- is paid online and picked up at the selected *click-and-collect store*
- originates from a *shopping cart* completed through *guest checkout*
- moves through preparation and handoff via *order fulfillment*
- **Invariant:** a *click-and-collect order* must reference exactly one *click-and-collect store* for pickup

### guest checkout

- lets a *customer* pay without an account
- collects *billing address* and *payment method* before invoking *StripeWave*
- requires a chosen *click-and-collect store* before payment
- produces a *click-and-collect order* when payment succeeds

### click-and-collect store

- is the *store* the *customer* picks at checkout for order pickup
- differs from Increment 1 *selected store* — chosen for fulfillment, not just browsing context
- scopes *prepare click-and-collect orders for pickup* and *fulfill click-and-collect order* to one retail location

### billing address

- is payment contact information captured during *guest checkout*
- attaches to the *click-and-collect order* for receipt and payment verification
- **Invariant:** *guest checkout* cannot complete without a valid *billing address*

### payment method

- is how the *customer* pays — card via *StripeWave* in this fixture
- is selected during *guest checkout* before card processing runs
- **Invariant:** only card payment via *StripeWave* is supported in this fixture

### StripeWave

- processes card payment for a *click-and-collect order*
- receives *payment method* details from *guest checkout*
- returns success or failure, determining whether *order confirmation* is issued
- **Invariant:** a *click-and-collect order* is not confirmed until *StripeWave* reports payment success

### order confirmation

- acknowledges a placed *click-and-collect order* — email in this fixture
- follows successful *StripeWave* payment
- tells the *customer* the order is accepted and where to pick up

### order fulfillment

- is *store employee* preparation and handoff of a *click-and-collect order*
- spans *prepare click-and-collect orders for pickup* through *fulfill click-and-collect order*
- completes when the *customer* collects the order at the *click-and-collect store*

### prepare click-and-collect orders for pickup

- is work a *store employee* performs to stage paid *click-and-collect orders* for collection
- runs at the *click-and-collect store* after *order confirmation*
- makes orders ready for the *customer* to collect

### fulfill click-and-collect order

- is the handoff when a *store employee* gives a prepared *click-and-collect order* to the *customer*
- completes *order fulfillment* for that order
- occurs at the *click-and-collect store* during pickup

### customer *(boundary)*

- builds a *shopping cart* and runs *guest checkout*
- selects *click-and-collect store*, enters *billing address*, and pays via *StripeWave*
- collects the order after *fulfill click-and-collect order*

### store employee *(boundary)*

- runs *prepare click-and-collect orders for pickup* for paid orders at a *store*
- runs *fulfill click-and-collect order* when the *customer* arrives

#### Decisions made

- *Order* owns checkout, payment, confirmation, and fulfillment; *Cart* owns pre-payment lines (independence test).
- *Click-and-collect store* is modeled here, not under Store — Increment 2 selection is for pickup commitment, not browse context (scope-fit test).
- *Prepare click-and-collect orders for pickup* and *fulfill click-and-collect order* are separate concepts — distinct employee stories with different outcomes (typing call).
- *StripeWave* is an external payment port — named as a concept because it has its own processing rules and invariants (typing call).

#### References

**Ref — Complete Guest Checkout sub-epic**
Source: docs/end-to-end/discovery/stories/story-map.md
Locator: lines 22–28
Extract: partial

**Ref — Fulfill Click-and-Collect Orders sub-epic**
Source: docs/end-to-end/discovery/stories/story-map.md
Locator: lines 29–31
Extract: partial

**Ref — Increment 2 outcome and stories**
Source: docs/end-to-end/discovery/stories/thin-slicing.md
Locator: Increment 2 section
Extract: partial

**Ref — Order module terms**
Source: docs/end-to-end/discovery/domain/domain-terms.md
Locator: Module Order section
Extract: partial

---

# Boundary Domain

## Product

Owned by: Catalog

- is the item the *customer* adds to the *shopping cart*
- was browsed in Increment 1; Increment 2 depends on *product* identity for cart lines only

#### Decisions made

- *Product* remains owned by Catalog — Cart references it without redefining assortment (scope-fit test).

#### References

**Ref — View Product Details**
Source: docs/end-to-end/discovery/stories/story-map.md
Locator: line 13
Extract: partial

---

## Store

Owned by: Store

- supplies retail locations; Increment 2 uses *store* identity when the *customer* selects a *click-and-collect store*
- discovery views (*store map*, *store list*) are Increment 1 scope — checkout reuses *store* records only

#### Decisions made

- *Store* module owns location identity; *Order* owns *click-and-collect store* selection semantics at checkout (independence test).

#### References

**Ref — Select Click-and-Collect Store**
Source: docs/end-to-end/discovery/stories/story-map.md
Locator: line 23
Extract: partial

---

## Customer

Owned by: Order

- builds and adjusts a *shopping cart*, completes *guest checkout*, and collects the *click-and-collect order*
- has no account in this fixture — guest identity only through *billing address* and confirmation email

#### Decisions made

- *Customer* boundary spans Cart and Order behaviors in Increment 2 — single actor across shop, pay, and pickup (scope-fit test).

#### References

**Ref — Click-and-collect outcome**
Source: docs/end-to-end/discovery/stories/thin-slicing.md
Locator: Increment 2 outcome
Extract: partial

---

## Store employee

Owned by: Order

- prepares and fulfills *click-and-collect orders* at a *click-and-collect store*
- may also maintain *product stock levels* from Increment 1 — stock updates are out of scope for this increment's fulfillment stories

#### Decisions made

- Fulfillment stories own *store employee* behavior for Increment 2; stock maintenance stays Increment 1 (scope-fit test).

#### References

**Ref — Prepare and Fulfill stories**
Source: docs/end-to-end/discovery/stories/thin-slicing.md
Locator: Increment 2 store employee stories
Extract: partial
