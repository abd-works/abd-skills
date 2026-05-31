# Acceptance Criteria — Increment 2: Click-and-collect

Scope: *Customer* builds a *shopping cart*, completes *guest checkout* (StripeWave), and picks up at a *click-and-collect store*; *store employee* prepares and hands off *click-and-collect orders*. Cart, checkout, and pickup stories only — store discovery and catalog browsing are prerequisites from Increment 1.

Sources: increment `ubiquitous-language.md`, discovery `story-map.md`, `thin-slicing.md` (Increment 2 stories), `information-architecture.md`.

---

## Story: Add Product to Cart

**Story type:** user

### Domain terms

- *Customer* — adds *products* to the *shopping cart* from *catalog*
- *Product* — *catalog* item selected for purchase
- *Shopping cart* — working container for line items before *guest checkout*
- *Add product to cart* — places a *product* into the *shopping cart*
- *Cart quantity* — count on each *shopping cart* line
- *Stock availability* — whether the *product* can be bought at the browsing context now

### Acceptance criteria

1. **WHEN** the *customer* views *product* detail with a *selected store* from Increment 1 and chooses *add product to cart*
   **THEN** the system places the *product* into the *shopping cart*
   **AND** the line shows *cart quantity* of at least one
   **Evidence:** `ubiquitous-language.md` — Cart > *add product to cart*; `story-map.md` — line 19; `information-architecture.md` — Add Product to Cart → Shopping Cart

2. **WHEN** the *customer* *adds product to cart* for a *product* already in the *shopping cart*
   **THEN** the system increases that line's *cart quantity*
   **AND** does not create a duplicate line for the same *product*
   **Evidence:** `ubiquitous-language.md` — Cart > *add product to cart*, "may create a new line or merge into an existing line"

3. **WHEN** *stock availability* shows the *product* as unavailable at the browsing context
   **THEN** the system prevents *add product to cart* or warns the *customer* before adding
   **BUT** does not place unavailable *products* into the *shopping cart* without acknowledgment
   **Evidence:** `ubiquitous-language.md` — Cart > *add product to cart*, "respects *stock availability*"; Increment 1 *stock availability* boundary

4. **WHEN** the *customer* successfully *adds product to cart*
   **THEN** the *customer* can open the *shopping cart* and see the new line with *product* identity and *cart quantity*
   **Evidence:** `information-architecture.md` — Shopping Cart / cart lines; `thin-slicing.md` — Increment 2 cart stories

5. **WHEN** the *shopping cart* is empty
   **THEN** the *customer* can still browse *catalog*
   **BUT** *guest checkout* is not offered until at least one line exists
   **Evidence:** `ubiquitous-language.md` — Cart > *shopping cart* invariant, "must contain at least one line before *guest checkout* can begin"

---

## Story: Update Cart Quantity

**Story type:** user

### Domain terms

- *Customer* — adjusts how many of a *product* they intend to buy
- *Shopping cart* — holds lines the *customer* updates
- *Cart quantity* — count on a *shopping cart* line
- *Update cart quantity* — changes *cart quantity* on an existing line
- *Product* — item whose count changes

### Acceptance criteria

1. **WHEN** the *customer* opens the *shopping cart* with at least one line
   **THEN** the system shows each line's *cart quantity* as editable
   **AND** the *customer* can run *update cart quantity* on any line
   **Evidence:** `ubiquitous-language.md` — Cart > *update cart quantity*; `story-map.md` — line 20; `information-architecture.md` — Update Cart Quantity / cart lines

2. **WHEN** the *customer* increases *cart quantity* on a line
   **THEN** the system saves the higher count
   **AND** the line total reflects the new *cart quantity*
   **Evidence:** `ubiquitous-language.md` — Cart > *update cart quantity*, "increase or decrease how many of a *product*"

3. **WHEN** the *customer* decreases *cart quantity* to a positive whole number greater than zero
   **THEN** the system saves the lower count
   **AND** the line remains in the *shopping cart*
   **Evidence:** `ubiquitous-language.md` — Cart > *cart quantity* invariant, "positive whole number while the line remains"

4. **WHEN** the *customer* attempts *update cart quantity* that would leave a line at zero
   **THEN** the system rejects the update with a clear message
   **BUT** directs the *customer* to *remove product from cart* instead
   **Evidence:** `ubiquitous-language.md` — Cart > *update cart quantity* invariant, "must not leave a line with zero *cart quantity*"

5. **WHEN** the *customer* adjusts *cart quantity* and continues browsing
   **THEN** the *shopping cart* retains the updated counts until *guest checkout* or *remove product from cart*
   **Evidence:** `ubiquitous-language.md` — Cart > *shopping cart*, "persists line items while the *customer* continues browsing"

---

## Story: Remove Product from Cart

**Story type:** user

### Domain terms

- *Customer* — deletes unwanted lines before checkout
- *Shopping cart* — container lines are removed from
- *Remove product from cart* — deletes a *product* line from the *shopping cart*
- *Cart quantity* — cleared when the line is removed
- *Product* — item removed from the cart

### Acceptance criteria

1. **WHEN** the *customer* views a line in the *shopping cart*
   **THEN** the system offers *remove product from cart* for that line
   **AND** the action is distinct from setting *cart quantity* to zero
   **Evidence:** `ubiquitous-language.md` — Cart > *remove product from cart*; `story-map.md` — line 21; `information-architecture.md` — Remove Product from Cart / remove

2. **WHEN** the *customer* confirms *remove product from cart* on a line
   **THEN** the system deletes that *product* line from the *shopping cart*
   **AND** the line's *cart quantity* no longer counts toward checkout
   **Evidence:** `ubiquitous-language.md` — Cart > *remove product from cart*, "clears the line's *cart quantity*"

3. **WHEN** the *customer* removes the last line from the *shopping cart*
   **THEN** the *shopping cart* is empty
   **BUT** *guest checkout* is not available until the *customer* *adds product to cart* again
   **Evidence:** `ubiquitous-language.md` — Cart > *shopping cart* invariant; `information-architecture.md` — Shopping Cart / checkout trigger requires lines

4. **WHEN** the *customer* removes one line while other lines remain
   **THEN** the remaining lines stay in the *shopping cart* with their *cart quantities* unchanged
   **Evidence:** `ubiquitous-language.md` — Cart > *remove product from cart*, scoped to one line

5. **WHEN** the *customer* removes a line and returns to *catalog*
   **THEN** the *customer* can *add product to cart* again without restoring the removed line
   **Evidence:** `information-architecture.md` — Shopping Cart → Browse Catalog / continue shopping

---

## Story: Select Click-and-Collect Store

**Story type:** user

### Domain terms

- *Customer* — chooses where to pick up the order at checkout
- *Guest checkout* — flow that requires a *click-and-collect store* before payment
- *Click-and-collect store* — *store* selected at checkout for order pickup
- *Store* — retail location record reused from Increment 1
- *Click-and-collect order* — must reference exactly one pickup *store*

### Acceptance criteria

1. **WHEN** the *customer* starts *guest checkout* from a non-empty *shopping cart*
   **THEN** the system presents every eligible *store* as a selectable *click-and-collect store*
   **AND** the *customer* can pick one location for pickup
   **Evidence:** `ubiquitous-language.md` — Order > *click-and-collect store*; `story-map.md` — line 23; `information-architecture.md` — Checkout — Guest & pickup / pickup store

2. **WHEN** the *customer* selects a *click-and-collect store*
   **THEN** the system binds that *store* to the checkout session
   **AND** shows *store* identity and address so the *customer* can confirm pickup location
   **Evidence:** `ubiquitous-language.md` — Order > *click-and-collect store*, "store the *customer* picks at checkout"; `information-architecture.md` — pickup store fields

3. **WHEN** the *customer* has not chosen a *click-and-collect store*
   **THEN** the system blocks payment and *order confirmation*
   **BUT** still allows the *customer* to enter *billing address* or *payment method* only after a *click-and-collect store* is chosen — exploration assumes store-first ordering per checkout form layout
   **Evidence:** `ubiquitous-language.md` — Order > *guest checkout*, "requires a chosen *click-and-collect store* before payment"; `information-architecture.md` — checkout section order

4. **WHEN** the *customer* changes the selected *click-and-collect store* before placing the order
   **THEN** the system updates the checkout binding to the new *store*
   **AND** only one *click-and-collect store* remains selected at a time
   **Evidence:** `ubiquitous-language.md` — Order > *click-and-collect order* invariant, "exactly one *click-and-collect store*"

5. **WHEN** the *customer* completes store selection
   **THEN** the chosen *click-and-collect store* will attach to the placed *click-and-collect order* on successful payment
   **Evidence:** `ubiquitous-language.md` — Order > *order*, "binds … *click-and-collect store* to the placed order"; `thin-slicing.md` — Increment 2 outcome

---

## Story: Check Out as Guest

**Story type:** user

### Domain terms

- *Customer* — pays without an account in this fixture
- *Guest checkout* — checkout capturing billing and payment without sign-in
- *Shopping cart* — must have at least one line before checkout begins
- *Click-and-collect order* — guest-only order produced when payment succeeds
- *Billing address* — collected during *guest checkout*

### Acceptance criteria

1. **WHEN** the *customer* opens checkout from a *shopping cart* with at least one line
   **THEN** the system starts *guest checkout* without requiring sign-in or account creation
   **AND** the flow is labeled as guest-only
   **Evidence:** `ubiquitous-language.md` — Order > *guest checkout*; `story-map.md` — line 24; scope note, "Guest checkout only"

2. **WHEN** the *customer* is in *guest checkout*
   **THEN** the system collects contact fields needed for *order confirmation* (email in this fixture)
   **AND** does not offer account registration or login
   **Evidence:** `information-architecture.md` — guest checkout / email · phone; `ubiquitous-language.md` — Order > *click-and-collect order* invariant, guest-only

3. **WHEN** the *customer* attempts checkout with an empty *shopping cart*
   **THEN** the system blocks *guest checkout*
   **BUT** directs the *customer* back to *catalog* or cart to *add product to cart*
   **Evidence:** `ubiquitous-language.md` — Cart > *shopping cart* invariant; `ubiquitous-language.md` — Order > *guest checkout* requires cart contents

4. **WHEN** the *customer* proceeds through *guest checkout* steps in order
   **THEN** the system advances from *click-and-collect store* selection through *billing address* and *payment method* toward payment
   **Evidence:** `information-architecture.md` — Checkout — Guest & pickup transitions; `story-map.md` — Complete Guest Checkout epic sequence

5. **WHEN** *guest checkout* completes successfully
   **THEN** the system creates a *click-and-collect order* without a customer account record
   **AND** no persistent customer profile is stored in this increment
   **Evidence:** `ubiquitous-language.md` — Order > *order* invariant, "guest-only — no customer account is created or required"

---

## Story: Enter Billing Address

**Story type:** user

### Domain terms

- *Customer* — supplies payment contact information during checkout
- *Billing address* — name and postal fields captured in *guest checkout*
- *Guest checkout* — cannot complete without valid *billing address*
- *Click-and-collect order* — receives the saved *billing address*

### Acceptance criteria

1. **WHEN** the *customer* reaches the billing step in *guest checkout*
   **THEN** the system presents fields for *billing address* (name, street, city, postal code, country)
   **AND** the *customer* can enter values before continuing
   **Evidence:** `ubiquitous-language.md` — Order > *billing address*; `story-map.md` — line 25; `information-architecture.md` — billing address fields

2. **WHEN** the *customer* submits a complete valid *billing address*
   **THEN** the system saves the *billing address* on the checkout session
   **AND** allows the *customer* to continue to *payment method* selection
   **Evidence:** `ubiquitous-language.md` — Order > *billing address*, "attaches to the *click-and-collect order*"

3. **WHEN** the *customer* submits an incomplete or invalid *billing address*
   **THEN** the system rejects the submission with field-level messages
   **BUT** does not invoke *StripeWave* or place an order
   **Evidence:** `ubiquitous-language.md` — Order > *billing address* invariant, "cannot complete without a valid *billing address*"

4. **WHEN** the *customer* revises *billing address* before payment
   **THEN** the system replaces the prior values on the checkout session
   **AND** the latest *billing address* is what will attach to the placed order
   **Evidence:** `ubiquitous-language.md` — Order > *billing address*, payment contact for receipt and verification

5. **WHEN** payment succeeds
   **THEN** the placed *click-and-collect order* includes the captured *billing address*
   **Evidence:** `ubiquitous-language.md` — Order > *order*, "binds *billing address* … to the placed order"

---

## Story: Select Payment Method

**Story type:** user

### Domain terms

- *Customer* — chooses how to pay during *guest checkout*
- *Payment method* — card via *StripeWave* in this fixture
- *StripeWave* — external processor invoked after method selection
- *Guest checkout* — collects *payment method* before card processing

### Acceptance criteria

1. **WHEN** the *customer* reaches the payment step in *guest checkout* with *billing address* captured
   **THEN** the system presents card payment as the only *payment method* option
   **AND** labels the processor as *StripeWave*
   **Evidence:** `ubiquitous-language.md` — Order > *payment method*, "card via *StripeWave*"; `story-map.md` — line 26

2. **WHEN** the *customer* selects the card *payment method*
   **THEN** the system enables *place order* (or equivalent) to invoke payment
   **AND** records card as the chosen *payment method* on the checkout session
   **Evidence:** `information-architecture.md` — payment method / card · StripeWave; `ubiquitous-language.md` — Order > *payment method*

3. **WHEN** the *customer* has not selected a *payment method*
   **THEN** the system blocks *StripeWave* processing
   **BUT** allows the *customer* to return and complete *billing address* or *click-and-collect store* steps first
   **Evidence:** `ubiquitous-language.md` — Order > *payment method*, "selected during *guest checkout* before card processing runs"

4. **WHEN** the *customer* attempts to choose a non-card *payment method*
   **THEN** the system does not offer alternative methods in this fixture
   **BUT** only card via *StripeWave* is supported
   **Evidence:** `ubiquitous-language.md` — Order > *payment method* invariant, "only card payment via *StripeWave*"

5. **WHEN** the *customer* confirms payment with the selected *payment method*
   **THEN** the system passes *payment method* details to *StripeWave* for processing
   **Evidence:** `ubiquitous-language.md` — Order > *StripeWave*, "receives *payment method* details from *guest checkout*"

---

## Story: Process Card Payment via StripeWave

**Story type:** system

### Domain terms

- *StripeWave* — external card payment processor
- *Payment method* — card details sent for processing
- *Click-and-collect order* — created only after payment success
- *Guest checkout* — invokes *StripeWave* at place order
- *Order confirmation* — withheld until payment succeeds

### Acceptance criteria

1. **WHEN** the *customer* submits payment with valid *payment method* and checkout prerequisites complete
   **THEN** the system invokes *StripeWave* to process the card charge
   **AND** waits for a success or failure response
   **Evidence:** `ubiquitous-language.md` — Order > *StripeWave*; `story-map.md` — line 27; `information-architecture.md` — Process Card Payment via StripeWave

2. **WHEN** *StripeWave* reports payment success
   **THEN** the system creates a paid *click-and-collect order* from the *shopping cart* contents
   **AND** clears or closes the checkout *shopping cart* for that session
   **Evidence:** `ubiquitous-language.md` — Order > *guest checkout*, "produces a *click-and-collect order* when payment succeeds"; Cart handoff

3. **WHEN** *StripeWave* reports payment failure or decline
   **THEN** the system shows a clear failure message to the *customer*
   **BUT** does not create a *click-and-collect order* or send *order confirmation*
   **Evidence:** `ubiquitous-language.md` — Order > *StripeWave*, "returns success or failure"; invariant on confirmation

4. **WHEN** payment is still processing
   **THEN** the system prevents duplicate submission of the same checkout payment
   **AND** the *customer* sees a processing state until *StripeWave* responds
   **Evidence:** `ubiquitous-language.md` — Order > *StripeWave* processing rules; ADR-007 idempotent placement (discovery architecture) — idempotency assumed for duplicate submit

5. **WHEN** *StripeWave* has not reported success
   **THEN** no *order confirmation* is issued
   **BUT** the *shopping cart* remains recoverable for retry where payment failed
   **Evidence:** `ubiquitous-language.md` — Order > *StripeWave* invariant, "not confirmed until *StripeWave* reports payment success"

---

## Story: Confirm Order and Send Confirmation Email

**Story type:** system

### Domain terms

- *Order confirmation* — acknowledgment after successful payment (email in this fixture)
- *Click-and-collect order* — subject of confirmation
- *Click-and-collect store* — pickup location shown on confirmation
- *StripeWave* — payment must succeed before confirmation
- *Customer* — receives confirmation and summary on screen

### Acceptance criteria

1. **WHEN** *StripeWave* reports payment success for a placed *click-and-collect order*
   **THEN** the system sends *order confirmation* to the email captured in *guest checkout*
   **AND** the message identifies the order and *click-and-collect store* for pickup
   **Evidence:** `ubiquitous-language.md` — Order > *order confirmation*; `story-map.md` — line 28; `information-architecture.md` — Order Confirmation / confirmation email

2. **WHEN** the *customer* lands on the order confirmation screen
   **THEN** the system displays order summary with order id, *click-and-collect store*, and total
   **AND** indicates that confirmation was sent by email
   **Evidence:** `information-architecture.md` — Order Confirmation / order summary fields

3. **WHEN** payment has not succeeded
   **THEN** the system does not send *order confirmation*
   **BUT** keeps the *customer* on checkout or payment error surfaces
   **Evidence:** `ubiquitous-language.md` — Order > *order confirmation*, "follows successful *StripeWave* payment"

4. **WHEN** *order confirmation* is sent
   **THEN** the *click-and-collect order* is visible to *store employees* in the fulfillment queue for that *click-and-collect store*
   **Evidence:** `ubiquitous-language.md` — Order > *prepare click-and-collect orders for pickup*, "after *order confirmation*"; `information-architecture.md` — Fulfillment — Orders

5. **WHEN** the *customer* finishes reading confirmation
   **THEN** the *customer* can return to *catalog* via continue shopping
   **BUT** cannot edit the placed *click-and-collect order* through the *shopping cart*
   **Evidence:** `information-architecture.md` — Order Confirmation → Browse Catalog; guest order is committed after payment

---

## Story: Prepare Click-and-Collect Orders for Pickup

**Story type:** user

### Domain terms

- *Store employee* — stages paid orders for collection
- *Prepare click-and-collect orders for pickup* — makes orders ready at the *click-and-collect store*
- *Click-and-collect order* — paid order awaiting preparation
- *Click-and-collect store* — scopes the fulfillment queue
- *Order confirmation* — precedes preparation work

### Acceptance criteria

1. **WHEN** the *store employee* opens the fulfillment queue for a *click-and-collect store*
   **THEN** the system lists paid *click-and-collect orders* awaiting preparation
   **AND** each row shows order id, customer contact, status, and pickup context
   **Evidence:** `ubiquitous-language.md` — Order > *prepare click-and-collect orders for pickup*; `story-map.md` — line 30; `information-architecture.md` — Fulfillment — Orders / order queue

2. **WHEN** the *store employee* marks an order as preparing (or equivalent staging action)
   **THEN** the system updates that *click-and-collect order* status to ready for customer collection
   **AND** the order remains scoped to its *click-and-collect store*
   **Evidence:** `information-architecture.md` — order queue / mark preparing; `ubiquitous-language.md` — Order > *prepare click-and-collect orders for pickup*

3. **WHEN** a *click-and-collect order* has not received payment success and *order confirmation*
   **THEN** the order does not appear in the preparation queue
   **BUT** unpaid or failed-checkout sessions are excluded
   **Evidence:** `ubiquitous-language.md` — Order > *prepare click-and-collect orders for pickup*, "after *order confirmation*"

4. **WHEN** the *store employee* views the queue
   **THEN** only orders for that employee's *click-and-collect store* (or selected store context) appear
   **BUT** orders for other *stores* are not mixed in one queue
   **Evidence:** `ubiquitous-language.md` — Order > *click-and-collect store*, scopes preparation and handoff

5. **WHEN** the *customer* is not a *store employee*
   **THEN** the fulfillment queue and preparation actions are unavailable
   **Evidence:** `ubiquitous-language.md` — boundary *store employee*; Increment 1 pattern for employee-only surfaces

---

## Story: Fulfill Click-and-Collect Order

**Story type:** user

### Domain terms

- *Store employee* — hands prepared orders to the *customer*
- *Fulfill click-and-collect order* — pickup handoff completing *order fulfillment*
- *Click-and-collect order* — prepared order the *customer* collects
- *Click-and-collect store* — location where handoff occurs
- *Order fulfillment* — spans preparation through handoff

### Acceptance criteria

1. **WHEN** the *store employee* opens a prepared *click-and-collect order* from the queue
   **THEN** the system shows order lines, *click-and-collect store*, and current fulfillment status
   **AND** offers *fulfill click-and-collect order* when staging is complete
   **Evidence:** `ubiquitous-language.md` — Order > *fulfill click-and-collect order*; `story-map.md` — line 31; `information-architecture.md` — Fulfillment — Order / order detail

2. **WHEN** the *store employee* confirms *fulfill click-and-collect order* at pickup
   **THEN** the system marks *order fulfillment* complete for that order
   **AND** removes the order from the active preparation queue
   **Evidence:** `ubiquitous-language.md` — Order > *fulfill click-and-collect order*, "completes *order fulfillment*"; `ubiquitous-language.md` — Order > *order fulfillment*

3. **WHEN** the *customer* arrives at the *click-and-collect store* with proof of order
   **THEN** the *store employee* can match the order and complete handoff
   **AND** the *customer* receives the *products* from the placed order
   **Evidence:** `ubiquitous-language.md` — Order > *order fulfillment*, "completes when the *customer* collects"; `thin-slicing.md` — Increment 2 outcome

4. **WHEN** the *store employee* attempts to fulfill an order not yet prepared
   **THEN** the system blocks handoff or warns that preparation is incomplete
   **BUT** does not mark *order fulfillment* complete prematurely
   **Evidence:** `ubiquitous-language.md` — Order > *order fulfillment* spans prepare then fulfill; sequential epic in `story-map.md`

5. **WHEN** *fulfill click-and-collect order* completes
   **THEN** the *click-and-collect order* shows as collected or closed
   **BUT** the *customer* cannot re-open the same order for another pickup through fulfillment actions
   **Evidence:** `ubiquitous-language.md` — Order > *fulfill click-and-collect order*, handoff completes lifecycle; exploration closure of pickup journey
