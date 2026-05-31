# Specification by Example — PawPlace mini — Increment 2

**Sources / context:** `docs/increments/2-click-and-collect/specification/crc.md`, `docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md`, `docs/increments/2-click-and-collect/exploration/ux/shopping-cart.md`, `docs/increments/2-click-and-collect/exploration/ux/checkout-guest-pickup.md`, `docs/increments/2-click-and-collect/exploration/ux/order-confirmation.md`, `docs/increments/2-click-and-collect/exploration/ux/fulfillment-orders.md`, `docs/increments/2-click-and-collect/exploration/ux/fulfillment-order.md`

Scope: Sprint 1 (Cart) — Add Product to Cart, Update Cart Quantity, Remove Product from Cart. Sprint 2 (Checkout & pay) — Select Click-and-Collect Store through Confirm Order and Send Confirmation Email. Sprint 3 (Store pickup) — Prepare Click-and-Collect Orders for Pickup, Fulfill Click-and-Collect Order.

---

## Background

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Shopping Cart** for **Customer** *Alex Rivera* has no **Cart Lines**

---

## Story: Add Product to Cart

**Story type:** user

**Sources / context:** CRC — Add Product To Cart, Shopping Cart, Cart Lines, Cart Line, Cart Quantity, Stock Availability; AC Add Product to Cart

---

## Scenarios

### Scenario 1: Product from catalog detail lands in shopping cart with cart quantity

Given **Product** *Premium Salmon Kibble* is in *catalog* scoped to **Selected Store** *Downtown PawPlace*
  And **Stock Availability** for **Product** *Premium Salmon Kibble* at **Selected Store** *Downtown PawPlace* is *available*
When **Customer** *Alex Rivera* views **Product** *Premium Salmon Kibble* detail and runs **Add Product To Cart**
Then **Cart Lines** in **Shopping Cart** include one **Cart Line** for **Product** *Premium Salmon Kibble*
  And that **Cart Line** shows **Cart Quantity** *1*
  And **Cart Line** line total reflects **Cart Quantity** *1* at unit price *$24.99*

### Scenario 2: Repeat add merges into existing line without duplicate

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1*
When **Customer** *Alex Rivera* runs **Add Product To Cart** for **Product** *Premium Salmon Kibble* again
Then **Cart Lines** still has exactly one **Cart Line** for **Product** *Premium Salmon Kibble*
  And that **Cart Line** shows **Cart Quantity** *2*
  And **Cart Lines** does not create a second line for the same **Product**

### Scenario 3: Unavailable product is blocked from shopping cart without acknowledgment

Given **Product** *Limited Edition Cat Tree* is in *catalog* scoped to **Selected Store** *Downtown PawPlace*
  And **Stock Availability** for **Product** *Limited Edition Cat Tree* at **Selected Store** *Downtown PawPlace* is *unavailable*
When **Customer** *Alex Rivera* attempts **Add Product To Cart** for **Product** *Limited Edition Cat Tree*
Then **Add Product To Cart** prevents placing **Product** *Limited Edition Cat Tree* into **Shopping Cart**
  And **Cart Lines** has no **Cart Line** for **Product** *Limited Edition Cat Tree*
  And **Customer** *Alex Rivera* sees a clear warning that *stock availability* is *unavailable* before any line is created

### Scenario 4: Shopping cart shows product identity and cart quantity after add

Given **Customer** *Alex Rivera* successfully ran **Add Product To Cart** for **Product** *Reflective Dog Leash*
When **Customer** *Alex Rivera* opens **Shopping Cart**
Then **Shopping Cart** shows **Cart Line** for **Product** *Reflective Dog Leash* with catalog identity *Reflective Dog Leash*
  And that **Cart Line** shows **Cart Quantity** *1*
  And **Shopping Cart** shows editable **Cart Quantity** for that **Cart Line**

### Scenario 5: Empty shopping cart allows catalog browse but not guest checkout

Given **Shopping Cart** for **Customer** *Alex Rivera* has no **Cart Lines**
When **Customer** *Alex Rivera* browses *catalog* scoped to **Selected Store** *Downtown PawPlace*
Then **Customer** *Alex Rivera* can view **Product** listings
  And *guest checkout* is not offered from **Shopping Cart**
  And **Shopping Cart** blocks checkout entry until at least one **Cart Line** exists

---

## Story: Update Cart Quantity

**Story type:** user

**Sources / context:** CRC — Update Cart Quantity, Cart Line, Cart Quantity, Shopping Cart; AC Update Cart Quantity

---

## Scenarios

### Scenario 1: Each cart line shows editable cart quantity on shopping cart

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1*
  And **Shopping Cart** has **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *2*
When **Customer** *Alex Rivera* opens **Shopping Cart**
Then **Shopping Cart** shows **Cart Quantity** *1* as editable on the **Cart Line** for **Product** *Premium Salmon Kibble*
  And **Shopping Cart** shows **Cart Quantity** *2* as editable on the **Cart Line** for **Product** *Reflective Dog Leash*
  And **Customer** *Alex Rivera* can run **Update Cart Quantity** on any **Cart Line**

### Scenario 2: Increased cart quantity saves higher count and updates line total

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1* at unit price *$24.99*
When **Customer** *Alex Rivera* runs **Update Cart Quantity** on that **Cart Line** to **Cart Quantity** *3*
Then **Cart Line** for **Product** *Premium Salmon Kibble* persists **Cart Quantity** *3*
  And **Cart Line** line total is *$74.97*
  And **Cart Line** remains in **Shopping Cart**

### Scenario 3: Decrease to a positive whole number saves lower count and keeps line

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *4* at unit price *$18.50*
When **Customer** *Alex Rivera* runs **Update Cart Quantity** on that **Cart Line** to **Cart Quantity** *2*
Then **Cart Line** for **Product** *Reflective Dog Leash* persists **Cart Quantity** *2*
  And **Cart Line** line total is *$37.00*
  And **Cart Line** remains in **Shopping Cart**

### Scenario 4: Zero cart quantity update is rejected and directs to remove product from cart

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *2*
When **Customer** *Alex Rivera* attempts **Update Cart Quantity** on that **Cart Line** to **Cart Quantity** *0*
Then **Update Cart Quantity** rejects the change with a clear message
  And **Cart Line** for **Product** *Premium Salmon Kibble* still has **Cart Quantity** *2*
  And **Customer** *Alex Rivera* is directed to run **Remove Product From Cart** instead of setting **Cart Quantity** to zero

### Scenario 5: Updated cart quantities persist while customer continues browsing

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1*
When **Customer** *Alex Rivera* runs **Update Cart Quantity** on that **Cart Line** to **Cart Quantity** *3*
  And **Customer** *Alex Rivera* returns to *catalog* scoped to **Selected Store** *Downtown PawPlace*
  And **Customer** *Alex Rivera* opens **Shopping Cart** again
Then **Cart Line** for **Product** *Premium Salmon Kibble* still shows **Cart Quantity** *3*
  And **Shopping Cart** retained the updated counts until **Remove Product From Cart** or *guest checkout*

---

## Story: Remove Product from Cart

**Story type:** user

**Sources / context:** CRC — Remove Product From Cart, Cart Lines, Cart Line, Shopping Cart; AC Remove Product from Cart

---

## Scenarios

### Scenario 1: Remove product from cart is offered distinctly from zero quantity edit

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *2*
When **Customer** *Alex Rivera* views that **Cart Line** on **Shopping Cart**
Then **Shopping Cart** offers **Remove Product From Cart** for **Product** *Reflective Dog Leash*
  And **Remove Product From Cart** is distinct from running **Update Cart Quantity** to **Cart Quantity** *0*

### Scenario 2: Confirmed remove deletes product line from shopping cart

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *3*
  And **Shopping Cart** has **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *1*
When **Customer** *Alex Rivera* confirms **Remove Product From Cart** for **Product** *Premium Salmon Kibble*
Then **Cart Lines** has no **Cart Line** for **Product** *Premium Salmon Kibble*
  And removed **Cart Line** **Cart Quantity** no longer counts toward checkout
  And **Cart Line** for **Product** *Reflective Dog Leash* remains with **Cart Quantity** *1*

### Scenario 3: Removing last line empties shopping cart and blocks guest checkout

Given **Shopping Cart** for **Customer** *Alex Rivera* has only **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *1*
When **Customer** *Alex Rivera* confirms **Remove Product From Cart** for **Product** *Reflective Dog Leash*
Then **Shopping Cart** has no **Cart Lines**
  And *guest checkout* is not available
  And **Shopping Cart** blocks checkout entry until **Customer** *Alex Rivera* runs **Add Product To Cart** again

### Scenario 4: Removing one line leaves remaining lines and cart quantities unchanged

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *2*
  And **Shopping Cart** has **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *3*
When **Customer** *Alex Rivera* confirms **Remove Product From Cart** for **Product** *Premium Salmon Kibble*
Then **Cart Lines** has no **Cart Line** for **Product** *Premium Salmon Kibble*
  And **Cart Line** for **Product** *Reflective Dog Leash* still has **Cart Quantity** *3*
  And **Cart Lines** leave remaining **Cart Line** entries unchanged

### Scenario 5: Customer can add product again after remove without restoring removed line

Given **Shopping Cart** for **Customer** *Alex Rivera* had **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *2*
  And **Customer** *Alex Rivera* confirmed **Remove Product From Cart** for **Product** *Premium Salmon Kibble*
When **Customer** *Alex Rivera* returns to *catalog* scoped to **Selected Store** *Downtown PawPlace*
  And **Customer** *Alex Rivera* runs **Add Product To Cart** for **Product** *Reflective Dog Leash*
Then **Cart Lines** has **Cart Line** for **Product** *Reflective Dog Leash*
  And **Cart Lines** has no restored **Cart Line** for **Product** *Premium Salmon Kibble*

---

## Background — Sprint 2

Given **Customer** *Alex Rivera* has **Selected Store** *Downtown PawPlace*
  And **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1* at unit price *$24.99*
  And **Shopping Cart** has **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *1* at unit price *$18.50*
  And **Store** *Downtown PawPlace* has retail location identity *Downtown PawPlace* at geographic placement *123 Main St*
  And **Store** *Westside PawPlace* has retail location identity *Westside PawPlace* at geographic placement *456 Oak Ave*
  And **Store** *Uptown PawPlace* has retail location identity *Uptown PawPlace* at geographic placement *789 Pine Rd*

---

## Story: Select Click-and-Collect Store

**Story type:** user

**Sources / context:** CRC — Select Click-and-collect Store, Click-and-collect Store, Guest Checkout, Store; AC Select Click-and-Collect Store

---

## Scenarios

### Scenario 1: Guest checkout presents every eligible store as click-and-collect store

Given **Shopping Cart** for **Customer** *Alex Rivera* has at least one **Cart Line**
When **Customer** *Alex Rivera* starts **Guest Checkout** from **Shopping Cart**
Then **Guest Checkout** presents **Store** *Downtown PawPlace*, **Store** *Westside PawPlace*, and **Store** *Uptown PawPlace* as selectable **Click-and-collect Store** options
  And **Customer** *Alex Rivera* can run **Select Click-and-collect Store** for one pickup location

### Scenario 2: Store selection binds click-and-collect store with identity and address

Given **Customer** *Alex Rivera* is in **Guest Checkout**
When **Customer** *Alex Rivera* runs **Select Click-and-collect Store** for **Store** *Downtown PawPlace*
Then **Click-and-collect Store** on the checkout session is **Store** *Downtown PawPlace*
  And **Guest Checkout** shows retail location identity *Downtown PawPlace* and geographic placement *123 Main St*
  And **Customer** *Alex Rivera* can confirm the pickup location before payment

### Scenario 3: Payment blocked until click-and-collect store is chosen

Given **Customer** *Alex Rivera* is in **Guest Checkout**
  And **Guest Checkout** has no **Click-and-collect Store** selected
When **Customer** *Alex Rivera* attempts **Process Card Payment via StripeWave**
Then **Guest Checkout** blocks **Process Card Payment via StripeWave**
  And **Order Confirmation** is not offered
  And **Customer** *Alex Rivera* must run **Select Click-and-collect Store** before payment

### Scenario 4: Changing click-and-collect store replaces prior binding with one store

Given **Guest Checkout** for **Customer** *Alex Rivera* has **Click-and-collect Store** **Store** *Downtown PawPlace*
When **Customer** *Alex Rivera* runs **Select Click-and-collect Store** for **Store** *Westside PawPlace* instead
Then **Click-and-collect Store** on the checkout session is **Store** *Westside PawPlace*
  And **Guest Checkout** shows retail location identity *Westside PawPlace* and geographic placement *456 Oak Ave*
  And only one **Click-and-collect Store** remains selected on the checkout session

### Scenario 5: Chosen click-and-collect store attaches to placed order on payment success

Given **Guest Checkout** for **Customer** *Alex Rivera* has **Click-and-collect Store** **Store** *Uptown PawPlace*
  And **Billing Address** on the checkout session is valid
  And **Payment Method** card via **StripeWave** is selected
When **Customer** *Alex Rivera* runs **Process Card Payment via StripeWave** and **StripeWave** reports payment success
Then **Click-and-collect Order** references **Click-and-collect Store** **Store** *Uptown PawPlace* for pickup
  And **Click-and-collect Order** references exactly one **Click-and-collect Store**

---

## Story: Check Out as Guest

**Story type:** user

**Sources / context:** CRC — Guest Checkout, Shopping Cart, Click-and-collect Order, Customer; AC Check Out as Guest

---

## Scenarios

### Scenario 1: Non-empty shopping cart starts guest checkout without sign-in

Given **Shopping Cart** for **Customer** *Alex Rivera* has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1*
When **Customer** *Alex Rivera* opens checkout from **Shopping Cart**
Then **Guest Checkout** starts without sign-in or account creation
  And the flow is labeled as *guest-only*
  And **Customer** *Alex Rivera* can proceed toward **Click-and-collect Store** selection

### Scenario 2: Guest checkout collects contact email without registration offer

Given **Customer** *Alex Rivera* is in **Guest Checkout**
When **Customer** *Alex Rivera* reaches the contact step
Then **Guest Checkout** collects email *alex.rivera@example.com* for **Order Confirmation**
  And **Guest Checkout** does not offer account registration or login
  And no persistent customer profile is created in this fixture

### Scenario 3: Empty shopping cart blocks guest checkout entry

Given **Shopping Cart** for **Customer** *Alex Rivera* has no **Cart Lines**
When **Customer** *Alex Rivera* attempts to open checkout from **Shopping Cart**
Then **Guest Checkout** is blocked
  And **Customer** *Alex Rivera* is directed back to *catalog* or **Shopping Cart** to run **Add Product To Cart**
  And **Click-and-collect Order** is not created

### Scenario 4: Guest checkout advances store then billing then payment in order

Given **Customer** *Alex Rivera* is in **Guest Checkout** with **Click-and-collect Store** **Store** *Downtown PawPlace* selected
When **Customer** *Alex Rivera* completes **Enter Billing Address** with valid **Billing Address**
  And **Customer** *Alex Rivera* runs **Select Payment Method** for card via **StripeWave**
Then **Guest Checkout** enables **Process Card Payment via StripeWave**
  And checkout steps progressed from **Select Click-and-collect Store** through **Billing Address** and **Payment Method** toward payment

### Scenario 5: Successful guest checkout creates click-and-collect order without customer account

Given **Guest Checkout** for **Customer** *Alex Rivera* has **Click-and-collect Store**, valid **Billing Address**, and card **Payment Method** selected
When **Customer** *Alex Rivera* runs **Process Card Payment via StripeWave** and **StripeWave** reports payment success
Then **Guest Checkout** produces **Click-and-collect Order** *CNC-1042*
  And no customer account record is created or required
  And **Click-and-collect Order** *CNC-1042* is *guest-only*

---

## Story: Enter Billing Address

**Story type:** user

**Sources / context:** CRC — Enter Billing Address, Billing Address, Guest Checkout; AC Enter Billing Address

---

## Scenarios

### Scenario 1: Billing step presents name and postal fields before payment

Given **Customer** *Alex Rivera* is in **Guest Checkout** with **Click-and-collect Store** **Store** *Downtown PawPlace* selected
When **Customer** *Alex Rivera* reaches the billing step
Then **Guest Checkout** presents **Billing Address** fields for name, street, city, postal code, and country
  And **Customer** *Alex Rivera* can run **Enter Billing Address** before continuing to **Payment Method**

### Scenario 2: Valid billing address saves on checkout session and unlocks payment step

Given **Customer** *Alex Rivera* is on the billing step in **Guest Checkout**
When **Customer** *Alex Rivera* runs **Enter Billing Address** with name *Alex Rivera*, street *42 Maple Lane*, city *Toronto*, postal code *M5V 1A1*, country *Canada*
Then **Billing Address** on the checkout session is saved with name *Alex Rivera*, street *42 Maple Lane*, city *Toronto*, postal code *M5V 1A1*, country *Canada*
  And **Guest Checkout** allows **Customer** *Alex Rivera* to continue to **Select Payment Method**

### Scenario 3: Incomplete billing address is rejected without StripeWave invocation

Given **Customer** *Alex Rivera* is on the billing step in **Guest Checkout**
When **Customer** *Alex Rivera* submits **Enter Billing Address** with street *42 Maple Lane* but missing postal code
Then **Enter Billing Address** rejects the submission with field-level messages
  And **StripeWave** is not invoked
  And no **Click-and-collect Order** is placed

### Scenario 4: Revised billing address replaces prior values before payment

Given **Billing Address** on the checkout session is name *Alex Rivera*, street *42 Maple Lane*, city *Toronto*, postal code *M5V 1A1*, country *Canada*
When **Customer** *Alex Rivera* runs **Enter Billing Address** again with street *88 Cedar Court* and postal code *M5V 2B2*
Then **Billing Address** on the checkout session is name *Alex Rivera*, street *88 Cedar Court*, city *Toronto*, postal code *M5V 2B2*, country *Canada*
  And the prior street *42 Maple Lane* is no longer the saved **Billing Address**
  And the latest **Billing Address** is what will attach to the placed order

### Scenario 5: Paid click-and-collect order includes captured billing address

Given **Guest Checkout** for **Customer** *Alex Rivera* has **Billing Address** name *Alex Rivera*, street *88 Cedar Court*, city *Toronto*, postal code *M5V 2B2*, country *Canada*
  And **Click-and-collect Store** **Store** *Downtown PawPlace* and card **Payment Method** are selected
When **Customer** *Alex Rivera* runs **Process Card Payment via StripeWave** and **StripeWave** reports payment success
Then **Click-and-collect Order** includes **Billing Address** name *Alex Rivera*, street *88 Cedar Court*, city *Toronto*, postal code *M5V 2B2*, country *Canada*

---

## Story: Select Payment Method

**Story type:** user

**Sources / context:** CRC — Select Payment Method, Payment Method, StripeWave, Guest Checkout; AC Select Payment Method

---

## Scenarios

### Scenario 1: Payment step presents card via StripeWave as only payment method

Given **Customer** *Alex Rivera* is in **Guest Checkout** with valid **Billing Address** captured
When **Customer** *Alex Rivera* reaches the payment step
Then **Guest Checkout** presents card as the only **Payment Method** option
  And the processor is labeled **StripeWave**
  And no alternative **Payment Method** types are offered in this fixture

### Scenario 2: Card selection enables place order and records payment method on session

Given **Customer** *Alex Rivera* is on the payment step with **Click-and-collect Store** **Store** *Downtown PawPlace* selected
When **Customer** *Alex Rivera* runs **Select Payment Method** for card via **StripeWave**
Then **Payment Method** on the checkout session is card via **StripeWave**
  And **Guest Checkout** enables **Process Card Payment via StripeWave**
  And **Customer** *Alex Rivera* can submit payment

### Scenario 3: StripeWave blocked until payment method is selected

Given **Guest Checkout** for **Customer** *Alex Rivera* has valid **Billing Address** and **Click-and-collect Store** **Store** *Downtown PawPlace*
  And no **Payment Method** is selected on the checkout session
When **Customer** *Alex Rivera* attempts **Process Card Payment via StripeWave**
Then **Guest Checkout** blocks **StripeWave** processing
  And **Customer** *Alex Rivera* can return to run **Select Payment Method** or complete prior checkout steps first

### Scenario 4: Non-card payment alternatives are not offered in this fixture

Given **Customer** *Alex Rivera* is on the payment step in **Guest Checkout**
When **Customer** *Alex Rivera* looks for alternative **Payment Method** options
Then **Guest Checkout** does not offer cash, wallet, or buy-now-pay-later methods
  And only card via **StripeWave** is supported
  And **Select Payment Method** rejects non-card alternatives if attempted

### Scenario 5: Selected payment method passes card details to StripeWave on place order

Given **Payment Method** card via **StripeWave** is selected on the checkout session
  And **Guest Checkout** prerequisites include **Click-and-collect Store** and valid **Billing Address**
When **Customer** *Alex Rivera* confirms payment with the selected **Payment Method**
Then **Process Card Payment via StripeWave** passes **Payment Method** card details to **StripeWave**
  And **StripeWave** receives the charge request for **Shopping Cart** total *$43.49*

---

## Story: Process Card Payment via StripeWave

**Story type:** system

**Sources / context:** CRC — Process Card Payment via StripeWave, StripeWave, Click-and-collect Order, Guest Checkout, Order Confirmation; AC Process Card Payment via StripeWave

---

## Scenarios

### Scenario 1: Valid prerequisites invoke StripeWave and wait for processor response

Given **Guest Checkout** for **Customer** *Alex Rivera* has **Click-and-collect Store** **Store** *Downtown PawPlace*, valid **Billing Address**, and card **Payment Method** selected
When **Customer** *Alex Rivera* submits **Process Card Payment via StripeWave**
Then **StripeWave** receives the card charge for **Shopping Cart** total *$43.49*
  And **Guest Checkout** waits for **StripeWave** success or failure response
  And **Order Confirmation** is withheld until **StripeWave** responds

### Scenario 2: StripeWave success creates paid order and clears shopping cart

Given **Guest Checkout** for **Customer** *Alex Rivera* has **Cart Lines** for **Product** *Premium Salmon Kibble* and **Product** *Reflective Dog Leash*
When **Customer** *Alex Rivera* runs **Process Card Payment via StripeWave**
  And **StripeWave** reports payment success
Then **Guest Checkout** creates paid **Click-and-collect Order** *CNC-1042* from **Shopping Cart** contents
  And **Click-and-collect Order** *CNC-1042* references **Click-and-collect Store** **Store** *Downtown PawPlace*
  And **Shopping Cart** for **Customer** *Alex Rivera* has no **Cart Lines** after successful payment

### Scenario 3: StripeWave failure shows message without order or confirmation

Given **Guest Checkout** for **Customer** *Alex Rivera* has all checkout prerequisites complete
When **Customer** *Alex Rivera* runs **Process Card Payment via StripeWave**
  And **StripeWave** reports payment failure *card declined*
Then **Guest Checkout** shows a clear failure message to **Customer** *Alex Rivera*
  And no **Click-and-collect Order** is created
  And **Order Confirmation** is not sent

### Scenario 4: Processing state prevents duplicate payment submission

Given **Customer** *Alex Rivera* submitted **Process Card Payment via StripeWave**
  And **StripeWave** has not yet responded
When **Customer** *Alex Rivera* attempts to submit payment again
Then **Guest Checkout** prevents duplicate submission of the same checkout payment
  And **Customer** *Alex Rivera* sees a processing state until **StripeWave** responds

### Scenario 5: Failed payment leaves shopping cart recoverable for retry

Given **Guest Checkout** for **Customer** *Alex Rivera* has **Cart Lines** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1*
When **Customer** *Alex Rivera* runs **Process Card Payment via StripeWave**
  And **StripeWave** reports payment failure *card declined*
Then **Order Confirmation** is not issued
  And **Shopping Cart** for **Customer** *Alex Rivera* still has **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1*
  And **Customer** *Alex Rivera* can return from **Guest Checkout** to retry payment

---

## Story: Confirm Order and Send Confirmation Email

**Story type:** system

**Sources / context:** CRC — Order Confirmation, Click-and-collect Order, StripeWave, Click-and-collect Store; AC Confirm Order and Send Confirmation Email

---

## Scenarios

### Scenario 1: Payment success sends order confirmation email with pickup store

Given **Guest Checkout** captured email *alex.rivera@example.com* for **Customer** *Alex Rivera*
  And **Process Card Payment via StripeWave** completed with **StripeWave** payment success for **Click-and-collect Order** *CNC-1042*
  And **Click-and-collect Order** *CNC-1042* references **Click-and-collect Store** **Store** *Downtown PawPlace*
When **Order Confirmation** runs after payment success
Then **Order Confirmation** sends email to *alex.rivera@example.com*
  And the message identifies **Click-and-collect Order** *CNC-1042* and **Click-and-collect Store** *Downtown PawPlace* for pickup

### Scenario 2: Confirmation screen shows order summary with store and total

Given **StripeWave** reported payment success for **Click-and-collect Order** *CNC-1042* at total *$43.49*
  And **Click-and-collect Order** *CNC-1042* references **Click-and-collect Store** **Store** *Downtown PawPlace*
When **Customer** *Alex Rivera* lands on the order confirmation screen
Then the screen displays **Click-and-collect Order** id *CNC-1042*
  And the screen displays **Click-and-collect Store** *Downtown PawPlace* and total *$43.49*
  And the screen indicates **Order Confirmation** was sent by email

### Scenario 3: Order confirmation withheld until StripeWave reports success

Given **Customer** *Alex Rivera* is in **Guest Checkout** with payment still pending or failed
When **StripeWave** has not reported payment success
Then **Order Confirmation** is not sent
  And **Customer** *Alex Rivera* remains on checkout or payment error surfaces
  And no order confirmation screen is shown prematurely

### Scenario 4: Confirmed order exposes click-and-collect order to store fulfillment queue

Given **StripeWave** reported payment success for **Click-and-collect Order** *CNC-1042*
  And **Click-and-collect Order** *CNC-1042* references **Click-and-collect Store** **Store** *Downtown PawPlace*
When **Order Confirmation** completes
Then **Click-and-collect Order** *CNC-1042* is visible in the fulfillment queue for **Click-and-collect Store** **Store** *Downtown PawPlace*
  And unpaid or failed-checkout sessions are excluded from the queue

### Scenario 5: Customer continues shopping without editing placed order via cart

Given **Customer** *Alex Rivera* finished reading **Order Confirmation** for **Click-and-collect Order** *CNC-1042*
When **Customer** *Alex Rivera* chooses continue shopping
Then **Customer** *Alex Rivera* returns to *catalog* scoped to **Selected Store** *Downtown PawPlace*
  And **Click-and-collect Order** *CNC-1042* cannot be edited through **Shopping Cart**
  And the placed order remains committed after payment

---

## Background — Sprint 3

Given **Store Employee** *Jordan Kim* is bound to **Click-and-collect Store** **Store** *Downtown PawPlace*
  And **Click-and-collect Order** *CNC-1042* for **Customer** *Alex Rivera* at contact *alex.rivera@example.com* has **Order Confirmation** completed with **StripeWave** payment success
  And **Click-and-collect Order** *CNC-1042* references **Click-and-collect Store** **Store** *Downtown PawPlace*
  And **Click-and-collect Order** *CNC-1042* includes **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1*
  And **Click-and-collect Order** *CNC-1042* includes **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *1*
  And **Click-and-collect Order** *CNC-1043* for **Customer** *Sam Patel* at contact *sam.patel@example.com* has **Order Confirmation** completed with **StripeWave** payment success
  And **Click-and-collect Order** *CNC-1043* references **Click-and-collect Store** **Store** *Westside PawPlace*
  And **Click-and-collect Order** *CNC-1044* for **Customer** *Lee Chen* at contact *lee.chen@example.com* has unpaid checkout session without **Order Confirmation**

---

## Story: Prepare Click-and-Collect Orders for Pickup

**Story type:** user

**Sources / context:** CRC — Prepare Click-and-collect Orders for Pickup, Fulfillment Queue, Click-and-collect Order, Click-and-collect Store, Order Confirmation, Store Employee; AC Prepare Click-and-Collect Orders for Pickup; UX `fulfillment-orders.md`

---

## Scenarios

### Scenario 1: Fulfillment queue lists paid click-and-collect orders awaiting preparation

Given **Click-and-collect Order** *CNC-1042* awaits preparation at **Click-and-collect Store** **Store** *Downtown PawPlace*
  And **Order Fulfillment** for **Click-and-collect Order** *CNC-1042* is *awaiting preparation*
When **Store Employee** *Jordan Kim* runs **Prepare Click-and-collect Orders for Pickup** and opens **Fulfillment Queue** for **Click-and-collect Store** **Store** *Downtown PawPlace*
Then **Fulfillment Queue** lists **Click-and-collect Order** *CNC-1042*
  And the queue row shows order id *CNC-1042*, customer contact *alex.rivera@example.com*, fulfillment status *awaiting preparation*, and pickup context **Click-and-collect Store** *Downtown PawPlace*
  And **Store Employee** *Jordan Kim* can open **Click-and-collect Order** *CNC-1042* from the queue

### Scenario 2: Mark preparing updates click-and-collect order to ready for collection

Given **Fulfillment Queue** for **Click-and-collect Store** **Store** *Downtown PawPlace* lists **Click-and-collect Order** *CNC-1042* with **Order Fulfillment** status *awaiting preparation*
When **Store Employee** *Jordan Kim* marks **Click-and-collect Order** *CNC-1042* as preparing through **Prepare Click-and-collect Orders for Pickup**
Then **Click-and-collect Order** *CNC-1042* **Order Fulfillment** status becomes *ready for collection*
  And **Click-and-collect Order** *CNC-1042* remains scoped to **Click-and-collect Store** **Store** *Downtown PawPlace*
  And **Prepare Click-and-collect Orders for Pickup** does not reassign the order to another **Store**

### Scenario 3: Unpaid orders without order confirmation are excluded from preparation queue

Given **Click-and-collect Order** *CNC-1044* has no **StripeWave** payment success
  And **Order Confirmation** has not completed for **Click-and-collect Order** *CNC-1044*
When **Store Employee** *Jordan Kim* opens **Fulfillment Queue** for **Click-and-collect Store** **Store** *Downtown PawPlace*
Then **Fulfillment Queue** does not list **Click-and-collect Order** *CNC-1044*
  And unpaid or failed-checkout sessions are excluded from **Prepare Click-and-collect Orders for Pickup**
  And only paid **Click-and-collect Order** entries with **Order Confirmation** appear in the queue

### Scenario 4: Fulfillment queue shows only orders for employee click-and-collect store

Given **Click-and-collect Order** *CNC-1042* references **Click-and-collect Store** **Store** *Downtown PawPlace*
  And **Click-and-collect Order** *CNC-1043* references **Click-and-collect Store** **Store** *Westside PawPlace*
When **Store Employee** *Jordan Kim* opens **Fulfillment Queue** scoped to **Click-and-collect Store** **Store** *Downtown PawPlace*
Then **Fulfillment Queue** lists **Click-and-collect Order** *CNC-1042*
  And **Fulfillment Queue** does not list **Click-and-collect Order** *CNC-1043*
  And orders for other **Store** locations are not mixed into one queue

### Scenario 5: Customer cannot access fulfillment queue or preparation actions

Given **Customer** *Alex Rivera* is not a **Store Employee**
When **Customer** *Alex Rivera* attempts to open **Fulfillment Queue** or run **Prepare Click-and-collect Orders for Pickup**
Then **Fulfillment Queue** and preparation actions are unavailable to **Customer** *Alex Rivera*
  And only **Store Employee** roles can access **Prepare Click-and-collect Orders for Pickup**
  And **Store Employee** *Jordan Kim* can still open **Fulfillment Queue** for **Click-and-collect Store** **Store** *Downtown PawPlace*

---

## Story: Fulfill Click-and-Collect Order

**Story type:** user

**Sources / context:** CRC — Fulfill Click-and-collect Order, Order Fulfillment, Fulfillment Queue, Click-and-collect Order, Click-and-collect Store, Store Employee, Customer; AC Fulfill Click-and-Collect Order; UX `fulfillment-order.md`

---

## Scenarios

### Scenario 1: Prepared order detail shows lines store and fulfillment status with handoff action

Given **Click-and-collect Order** *CNC-1042* has **Order Fulfillment** status *ready for collection*
  And **Fulfillment Queue** for **Click-and-collect Store** **Store** *Downtown PawPlace* lists **Click-and-collect Order** *CNC-1042*
When **Store Employee** *Jordan Kim* opens **Click-and-collect Order** *CNC-1042* from **Fulfillment Queue** through **Fulfill Click-and-collect Order**
Then the order detail shows **Cart Line** for **Product** *Premium Salmon Kibble* with **Cart Quantity** *1*
  And the order detail shows **Cart Line** for **Product** *Reflective Dog Leash* with **Cart Quantity** *1*
  And the order detail shows **Click-and-collect Store** *Downtown PawPlace* and **Order Fulfillment** status *ready for collection*
  And **Fulfill Click-and-collect Order** is offered because preparation is complete

### Scenario 2: Confirming fulfill marks order fulfillment complete and removes order from queue

Given **Click-and-collect Order** *CNC-1042* has **Order Fulfillment** status *ready for collection*
  And **Customer** *Alex Rivera* arrives at **Click-and-collect Store** **Store** *Downtown PawPlace* with proof of **Click-and-collect Order** *CNC-1042*
When **Store Employee** *Jordan Kim* confirms **Fulfill Click-and-collect Order** at pickup
Then **Order Fulfillment** for **Click-and-collect Order** *CNC-1042* is *complete*
  And **Fulfillment Queue** removes **Click-and-collect Order** *CNC-1042* from the active preparation queue
  And **Customer** *Alex Rivera* receives **Product** *Premium Salmon Kibble* and **Product** *Reflective Dog Leash* from the placed order

### Scenario 3: Store employee matches order proof and completes handoff at click-and-collect store

Given **Click-and-collect Order** *CNC-1042* has **Order Fulfillment** status *ready for collection*
  And **Customer** *Alex Rivera* presents order id *CNC-1042* at **Click-and-collect Store** **Store** *Downtown PawPlace*
When **Store Employee** *Jordan Kim* verifies **Click-and-collect Order** *CNC-1042* matches the customer proof
  And **Store Employee** *Jordan Kim* confirms **Fulfill Click-and-collect Order**
Then **Customer** *Alex Rivera* collects the order lines at **Click-and-collect Store** **Store** *Downtown PawPlace*
  And **Order Fulfillment** completes when the **Customer** collects the order at the **Click-and-collect Store**

### Scenario 4: Handoff blocked when click-and-collect order is not yet prepared

Given **Click-and-collect Order** *CNC-1042* has **Order Fulfillment** status *awaiting preparation*
  And **Prepare Click-and-collect Orders for Pickup** has not marked **Click-and-collect Order** *CNC-1042* *ready for collection*
When **Store Employee** *Jordan Kim* opens **Click-and-collect Order** *CNC-1042* and attempts **Fulfill Click-and-collect Order**
Then **Fulfill Click-and-collect Order** blocks handoff with a warning that preparation is incomplete
  And **Order Fulfillment** for **Click-and-collect Order** *CNC-1042* is not marked *complete*
  And **Fulfillment Queue** still lists **Click-and-collect Order** *CNC-1042* in the active preparation queue

### Scenario 5: Completed fulfill closes order against repeat pickup actions

Given **Store Employee** *Jordan Kim* confirmed **Fulfill Click-and-collect Order** for **Click-and-collect Order** *CNC-1042*
  And **Order Fulfillment** for **Click-and-collect Order** *CNC-1042* is *complete*
When **Customer** *Alex Rivera* or **Store Employee** *Jordan Kim* attempts **Fulfill Click-and-collect Order** again for **Click-and-collect Order** *CNC-1042*
Then **Click-and-collect Order** *CNC-1042* shows as *collected* or *closed*
  And **Fulfill Click-and-collect Order** does not complete **Order Fulfillment** a second time for the same **Click-and-collect Order**
  And the **Customer** cannot re-open **Click-and-collect Order** *CNC-1042* for another pickup through fulfillment actions

