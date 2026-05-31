---
state: crc
---

# Module: [PawPlace mini — Increment 2]

Scope: Increment 2 (Click-and-collect) — Sprint 1 (Cart), Sprint 2 (Checkout & pay), and Sprint 3 (Store pickup) integrated below.

**Core terms**:
- shopping cart
- cart line
- cart quantity
- add product to cart
- update cart quantity
- remove product from cart
- guest checkout
- click-and-collect store
- click-and-collect order
- billing address
- payment method
- StripeWave
- order confirmation
- order fulfillment
- fulfillment queue
- prepare click-and-collect orders for pickup
- fulfill click-and-collect order

**Key Abstractions (term grouping)**:
- **Cart**: shopping cart, cart line, cart quantity, add product to cart, update cart quantity, remove product from cart
- **Order**: guest checkout, click-and-collect store, click-and-collect order, billing address, payment method, StripeWave, order confirmation, select click-and-collect store, process card payment via StripeWave, order fulfillment, fulfillment queue, prepare click-and-collect orders for pickup, fulfill click-and-collect order

---

# Core Domain

## Increment 2 — Sprint 1: Cart

Cart specification scope from increment exploration `ubiquitous-language.md` and `acceptance-criteria.md` (Add Product to Cart, Update Cart Quantity, Remove Product from Cart).

## **Cart**

*Cart* holds line items between *catalog* browsing and checkout. Sprint 1 covers line aggregation, quantity changes, and removal before any *guest checkout* flow.

### **Cart**
pre-checkout line aggregation           | Shopping Cart
persist selections while browsing       | Shopping Cart, Cart Lines
                                        |   invariant: a shopping cart must contain at least one line before guest checkout can begin

### **Shopping Cart**
working container for catalog picks     | Cart, Cart Lines
show each line with product identity    | Cart Line, Customer
show editable cart quantity per line    | Cart Line, Cart Quantity, Customer
persist updated counts while browsing   | Cart Lines, Customer
block checkout entry when empty         | Cart Lines, Customer
hand off lines to guest checkout        | Guest Checkout, Click-and-collect Order
clear after successful payment          | Process Card Payment via StripeWave, Guest Checkout
                                        |   invariant: guest checkout is not offered until at least one line exists

### **Cart Line**
product identity on line                | Product
cart quantity on line                   | Cart Quantity
line total from quantity                | Product, Cart Quantity
                                        |   invariant: cart quantity for any line must be a positive whole number while the line remains in the shopping cart

### **Cart Lines**
product lines in shopping cart          | Cart Line, Shopping Cart
merge add into existing product line    | Add Product To Cart, Cart Line, Product
add new product line                    | Add Product To Cart, Cart Line, Product
remove product line from collection     | Remove Product From Cart, Cart Line
apply quantity change on line           | Update Cart Quantity, Cart Line
leave remaining lines unchanged         | Cart Line, Shopping Cart
                                        |   invariant: at most one line per product — no duplicate lines for the same product

### **Cart Quantity**
count for product line                  | Cart Line, Product
editable count on cart view             | Shopping Cart, Customer
                                        |   invariant: cart quantity must be a positive whole number while the line remains in the shopping cart

### **Add Product To Cart**
place product from catalog              | Product, Shopping Cart, Cart Lines, Customer
increase quantity on existing line      | Cart Line, Cart Lines, Cart Quantity
create line with at least one quantity  | Cart Line, Cart Lines, Cart Quantity
prevent unavailable product add         | Stock Availability, Product, Customer
warn before adding unavailable product  | Stock Availability, Customer
                                        |   invariant: respects stock availability at the browsing context — unavailable products are not placed without acknowledgment

### **Update Cart Quantity**
change count on existing line           | Cart Line, Cart Quantity, Customer
save higher count on increase           | Cart Line, Cart Quantity
save lower positive count on decrease   | Cart Line, Cart Quantity
reject zero quantity update             | Customer, Remove Product From Cart
direct customer to remove instead       | Remove Product From Cart, Customer
                                        |   invariant: update cart quantity must not leave a line with zero cart quantity — use remove product from cart instead

### **Remove Product From Cart**
delete product line from shopping cart  | Cart Line, Cart Lines, Shopping Cart
clear line cart quantity on removal     | Cart Line
offer distinct from zero quantity edit  | Update Cart Quantity, Customer
empty cart when last line removed       | Cart Lines, Shopping Cart
                                        |   invariant: removing the last line empties the shopping cart and blocks guest checkout until add product to cart runs again

### references

**Ref — Cart module ubiquitous language**
Source: docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md
Locator: Cart KA, lines 36–84
Extract: partial

```source
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
```

**Ref — Cart stories acceptance criteria**
Source: docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md
Locator: Add Product to Cart, Update Cart Quantity, Remove Product from Cart
Extract: partial

```source
## Story: Add Product to Cart
…
2. **WHEN** the *customer* *adds product to cart* for a *product* already in the *shopping cart*
   **THEN** the system increases that line's *cart quantity*
   **AND** does not create a duplicate line for the same *product*

## Story: Update Cart Quantity
…
4. **WHEN** the *customer* attempts *update cart quantity* that would leave a line at zero
   **THEN** the system rejects the update with a clear message
   **BUT** directs the *customer* to *remove product from cart* instead

## Story: Remove Product from Cart
…
3. **WHEN** the *customer* removes the last line from the *shopping cart*
   **THEN** the *shopping cart* is empty
   **BUT** *guest checkout* is not available until the *customer* *adds product to cart* again
```

### decisions made

- Introduced *Cart Line* as state-carrier — per-line product and quantity state does not belong on *Shopping Cart* alone (state-carrier rule).
- Introduced *Cart Lines* as collection class — merge-on-add, no-duplicate-line, and scoped removal behavior is collection-level (collection-class rule).
- *Add product to cart*, *update cart quantity*, and *remove product from cart* remain named classes — each maps to a distinct customer story with its own responsibilities (typing call from exploration UL).
- Guest checkout and order concepts appear only as boundary invariants on *Shopping Cart* in Sprint 1 — Sprint 2 models *Order* explicitly (scope-fit test).

---

## Increment 2 — Sprint 2: Checkout & pay

Order specification scope from increment exploration `ubiquitous-language.md` and `acceptance-criteria.md` (Select Click-and-Collect Store, Check Out as Guest, Enter Billing Address, Select Payment Method, Process Card Payment via StripeWave, Confirm Order and Send Confirmation Email). Excludes Sprint 3 fulfillment stories.

## **Order**

*Order* converts a non-empty *shopping cart* into a paid *click-and-collect order* through *guest checkout*. Sprint 2 covers *click-and-collect store* selection, *billing address* and *payment method* capture, *StripeWave* card processing, and *order confirmation* — no customer accounts and no store-employee fulfillment in this sprint.

### **Order**
convert shopping cart to paid order       | Shopping Cart, Guest Checkout, Click-and-collect Order
bind billing address to placed order      | Billing Address, Click-and-collect Order
bind payment method to placed order       | Payment Method, Click-and-collect Order
bind click-and-collect store to order     | Click-and-collect Store, Click-and-collect Order
progress payment to confirmation          | StripeWave, Order Confirmation, Guest Checkout
                                        |   invariant: every click-and-collect order in this increment is guest-only — no customer account is created or required

### **Click-and-collect Order**
paid online pickup at chosen store        | Click-and-collect Store, Guest Checkout, Shopping Cart
originate from completed guest checkout   | Guest Checkout, Shopping Cart
reference exactly one pickup store        | Click-and-collect Store
                                        |   invariant: a click-and-collect order must reference exactly one click-and-collect store for pickup

### **Guest Checkout**
pay without account in this fixture       | Customer, Shopping Cart, Click-and-collect Order
collect billing address before payment    | Billing Address, Customer
collect payment method before StripeWave  | Payment Method, StripeWave
require click-and-collect store first     | Click-and-collect Store, Select Click-and-collect Store
block checkout when shopping cart empty   | Shopping Cart, Customer
produce click-and-collect order on success | Click-and-collect Order, Process Card Payment via StripeWave
                                        |   invariant: guest checkout cannot complete without a valid billing address
                                        |   invariant: guest checkout requires a chosen click-and-collect store before payment

### **Click-and-collect Store**
store customer picks at checkout          | Store, Customer, Select Click-and-collect Store
bind to checkout session on selection     | Guest Checkout, Customer
show store identity and address           | Store, Customer
block payment until store chosen          | Guest Checkout, Process Card Payment via StripeWave
replace binding when customer changes store | Select Click-and-collect Store, Guest Checkout
attach to placed order on success         | Click-and-collect Order, Process Card Payment via StripeWave
                                        |   invariant: only one click-and-collect store may be selected on a checkout session at a time

### **Billing Address**
payment contact on guest checkout         | Guest Checkout, Customer
name and postal fields for receipt        | (name, street, city, postal code, country)
save on checkout session when valid       | Guest Checkout, Customer
reject incomplete or invalid submission   | Guest Checkout, Customer
replace prior values before payment       | Guest Checkout
attach to click-and-collect order on pay  | Click-and-collect Order, Process Card Payment via StripeWave
                                        |   invariant: guest checkout cannot complete without a valid billing address

### **Payment Method**
card via StripeWave in this fixture       | StripeWave, Guest Checkout
present as only option at payment step    | Guest Checkout, Customer
record card choice on checkout session    | Guest Checkout
block StripeWave until method selected    | Process Card Payment via StripeWave, Guest Checkout
pass details to StripeWave on place order | Process Card Payment via StripeWave, StripeWave
                                        |   invariant: only card payment via StripeWave is supported in this fixture

### **StripeWave**
process card charge for order             | Payment Method, Process Card Payment via StripeWave
return success or failure to guest checkout | Guest Checkout, Click-and-collect Order
withhold order confirmation on failure    | Order Confirmation, Click-and-collect Order
                                        |   invariant: a click-and-collect order is not confirmed until StripeWave reports payment success

### **Order Confirmation**
acknowledge placed click-and-collect order | Click-and-collect Order, Process Card Payment via StripeWave
send confirmation email after success     | Customer, Click-and-collect Store
show order summary on confirmation screen | Click-and-collect Order, Click-and-collect Store, Customer
expose order to fulfillment queue         | Click-and-collect Store
                                        |   invariant: order confirmation follows successful StripeWave payment only

### **Select Click-and-collect Store**
present eligible stores at checkout start | Store, Guest Checkout, Customer
let customer pick one pickup location     | Click-and-collect Store, Customer
bind selection to checkout session        | Click-and-collect Store, Guest Checkout
update binding when customer changes store | Click-and-collect Store, Guest Checkout
                                        |   invariant: select click-and-collect store must complete before payment and order confirmation

### **Enter Billing Address**
present billing address fields at billing step | Guest Checkout, Customer
save valid billing address on session     | Billing Address, Guest Checkout
reject incomplete or invalid submission   | Customer, Billing Address
replace prior values on revision          | Billing Address, Guest Checkout
attach billing address to placed order    | Click-and-collect Order, Process Card Payment via StripeWave
block StripeWave on invalid billing       | Process Card Payment via StripeWave

### **Select Payment Method**
present card as only payment method option | Payment Method, Guest Checkout, StripeWave
enable place order after method selection | Process Card Payment via StripeWave, Guest Checkout
record card choice on checkout session    | Payment Method, Guest Checkout
block StripeWave without method selection | Process Card Payment via StripeWave
reject non-card payment alternatives      | Customer, Payment Method

### **Process Card Payment via StripeWave**
invoke StripeWave when prerequisites met  | StripeWave, Payment Method, Guest Checkout, Billing Address, Click-and-collect Store
create paid order on processor success      | Click-and-collect Order, Shopping Cart, Guest Checkout
clear shopping cart after successful pay    | Shopping Cart, Guest Checkout
show failure without creating order         | Customer, Guest Checkout, Order Confirmation
prevent duplicate payment submission      | Guest Checkout, Customer
withhold confirmation until success       | Order Confirmation, StripeWave
                                        |   invariant: no click-and-collect order is created until StripeWave reports payment success

### references

**Ref — Order module ubiquitous language**
Source: docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md
Locator: Order KA, lines 105–177
Extract: partial

```source
## Order

*Order* covers *guest checkout*, payment via *StripeWave*, *order confirmation*, and *click-and-collect order* … at the chosen *click-and-collect store*. Guest-only — no accounts in this fixture.

### guest checkout

- lets a *customer* pay without an account
- collects *billing address* and *payment method* before invoking *StripeWave*
- requires a chosen *click-and-collect store* before payment
- produces a *click-and-collect order* when payment succeeds

### click-and-collect order

- is paid online and picked up at the selected *click-and-collect store*
- originates from a *shopping cart* completed through *guest checkout*
- **Invariant:** a *click-and-collect order* must reference exactly one *click-and-collect store* for pickup

### StripeWave

- processes card payment for a *click-and-collect order*
- **Invariant:** a *click-and-collect order* is not confirmed until *StripeWave* reports payment success
```

**Ref — Checkout and payment acceptance criteria**
Source: docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md
Locator: Select Click-and-Collect Store through Confirm Order and Send Confirmation Email
Extract: partial

```source
## Story: Select Click-and-Collect Store
…
3. **WHEN** the *customer* has not chosen a *click-and-collect store*
   **THEN** the system blocks payment and *order confirmation*

## Story: Process Card Payment via StripeWave
…
2. **WHEN** *StripeWave* reports payment success
   **THEN** the system creates a paid *click-and-collect order* from the *shopping cart* contents
   **AND** clears or closes the checkout *shopping cart* for that session

## Story: Confirm Order and Send Confirmation Email
…
1. **WHEN** *StripeWave* reports payment success …
   **THEN** the system sends *order confirmation* to the email captured in *guest checkout*
```

### decisions made

- *Order* owns checkout, payment, and confirmation; *Cart* owns pre-payment lines — handoff at successful *process card payment via StripeWave* (independence test).
- *Click-and-collect Store* is a distinct class from Increment 1 *selected store* — checkout pickup commitment, not browse context (scope-fit test).
- *Select click-and-collect store*, *enter billing address*, *select payment method*, and *process card payment via StripeWave* are named operation classes — each maps to a distinct story (typing call).
- *StripeWave* is an external payment port — responsibilities stay thin; domain owns when to invoke and how to interpret success (boundary port pattern).
- Sprint 3 *prepare click-and-collect orders for pickup* and *fulfill click-and-collect order* appear only on *order confirmation* queue exposure — not modeled in Sprint 2 CRC (scope-fit test).

---

## Increment 2 — Sprint 3: Store pickup

Fulfillment specification scope from increment exploration `ubiquitous-language.md` and `acceptance-criteria.md` (Prepare Click-and-Collect Orders for Pickup, Fulfill Click-and-Collect Order). Builds on paid *click-and-collect orders* exposed by *order confirmation*; excludes Sprint 1–2 cart and checkout modeling already integrated above.

## **Order** *(Sprint 3 fulfillment extension)*

*Order fulfillment* spans *store employee* preparation and pickup handoff at the *click-and-collect store*. Sprint 3 models the fulfillment queue, preparation staging, and handoff completion — not guest checkout or payment.

### **Order**
progress fulfillment after confirmation     | Order Confirmation, Order Fulfillment, Click-and-collect Order
scope preparation and handoff to store      | Click-and-collect Store, Fulfillment Queue
                                        |   invariant: order fulfillment begins only after order confirmation for a paid click-and-collect order

### **Click-and-collect Order**
fulfillment status on placed order          | Order Fulfillment, Fulfillment Queue
await preparation after confirmation        | Order Confirmation, Fulfillment Queue
transition to ready for collection          | Prepare Click-and-collect Orders for Pickup, Order Fulfillment
block handoff until preparation complete    | Fulfill Click-and-collect Order, Order Fulfillment
mark collected or closed after handoff      | Fulfill Click-and-collect Order, Order Fulfillment
exclude unpaid orders from fulfillment queue | Order Confirmation, Fulfillment Queue
                                        |   invariant: a click-and-collect order in the fulfillment queue must have successful payment and order confirmation
                                        |   invariant: fulfill click-and-collect order must not complete until preparation marks the order ready for collection

### **Click-and-collect Store**
scope fulfillment queue to one location     | Fulfillment Queue, Click-and-collect Order
filter queue to orders for this store only  | Fulfillment Queue, Store Employee
bind employee context to store at login     | Store Employee, Fulfillment Queue
                                        |   invariant: fulfillment queue lists only click-and-collect orders for the employee click-and-collect store context

### **Order Fulfillment**
employee preparation through handoff        | Click-and-collect Order, Store Employee
span prepare through fulfill operations     | Prepare Click-and-collect Orders for Pickup, Fulfill Click-and-collect Order
complete when customer collects at store    | Fulfill Click-and-collect Order, Customer
block premature completion before prepare     | Prepare Click-and-collect Orders for Pickup, Fulfill Click-and-collect Order
                                        |   invariant: order fulfillment completes only after fulfill click-and-collect order succeeds for a prepared order

### **Fulfillment Queue**
paid orders awaiting preparation per store  | Click-and-collect Order, Click-and-collect Store, Order Confirmation
list order id contact status pickup context | Click-and-collect Order, Store Employee
exclude unpaid or unconfirmed sessions      | Order Confirmation, Click-and-collect Order
remove order from active queue on fulfill   | Fulfill Click-and-collect Order, Click-and-collect Order
open order detail for handoff prep          | Fulfill Click-and-collect Order, Store Employee
                                        |   invariant: only store employees may access the fulfillment queue and its actions

### **Prepare Click-and-collect Orders for Pickup**
open queue for click-and-collect store      | Fulfillment Queue, Store Employee, Click-and-collect Store
list paid orders awaiting preparation       | Fulfillment Queue, Click-and-collect Order
mark order preparing or staging equivalent  | Click-and-collect Order, Order Fulfillment
update status to ready for collection       | Order Fulfillment, Click-and-collect Order
keep order scoped to its click-and-collect store | Click-and-collect Store, Click-and-collect Order
                                        |   invariant: prepare click-and-collect orders for pickup runs only after order confirmation for that order

### **Fulfill Click-and-collect Order**
open prepared order from queue              | Fulfillment Queue, Click-and-collect Order, Store Employee
show lines store and fulfillment status     | Click-and-collect Order, Click-and-collect Store, Order Fulfillment
enable handoff when preparation complete    | Order Fulfillment, Store Employee
block handoff when preparation incomplete   | Order Fulfillment, Prepare Click-and-collect Orders for Pickup
mark order fulfillment complete on confirm    | Order Fulfillment, Click-and-collect Order
remove order from active preparation queue  | Fulfillment Queue, Click-and-collect Order
close order against repeat pickup actions     | Click-and-collect Order, Customer
                                        |   invariant: fulfill click-and-collect order completes order fulfillment for that click-and-collect order exactly once

### references

**Ref — Order fulfillment and employee operations**
Source: docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md
Locator: Order KA — order fulfillment, prepare click-and-collect orders for pickup, fulfill click-and-collect order; boundary store employee
Extract: partial

```source
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
```

**Ref — Fulfillment stories acceptance criteria**
Source: docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md
Locator: Prepare Click-and-Collect Orders for Pickup, Fulfill Click-and-Collect Order
Extract: partial

```source
## Story: Prepare Click-and-Collect Orders for Pickup
…
1. **WHEN** the *store employee* opens the fulfillment queue for a *click-and-collect store*
   **THEN** the system lists paid *click-and-collect orders* awaiting preparation

2. **WHEN** the *store employee* marks an order as preparing …
   **THEN** the system updates that *click-and-collect order* status to ready for customer collection

## Story: Fulfill Click-and-Collect Order
…
2. **WHEN** the *store employee* confirms *fulfill click-and-collect order* at pickup
   **THEN** the system marks *order fulfillment* complete for that order
   **AND** removes the order from the active preparation queue

4. **WHEN** the *store employee* attempts to fulfill an order not yet prepared
   **THEN** the system blocks handoff …
   **BUT** does not mark *order fulfillment* complete prematurely
```

### decisions made

- Introduced *Fulfillment Queue* as collection class — store-scoped listing, exclusion rules, and queue removal on fulfill are collection-level (collection-class rule).
- *Order Fulfillment* is lifecycle carrier on *Click-and-collect Order* — preparation and handoff states do not belong on checkout classes alone (state-carrier rule).
- *Prepare click-and-collect orders for pickup* and *fulfill click-and-collect order* remain separate named operation classes — distinct employee stories with sequential invariants (typing call).
- Sprint 2 *Order Confirmation* queue exposure is boundary only in Sprint 2; Sprint 3 models queue, preparation, and handoff explicitly (scope-fit test).
- *Store Employee* is boundary actor — queue access and fulfillment actions are not *Customer* responsibilities (receiver-not-responsible-for-receiving).

---

# Boundary Domain

### **Customer**
add product to cart from catalog       | Add Product To Cart, Product, Shopping Cart
open shopping cart to view lines       | Shopping Cart, Cart Line
update cart quantity on line           | Update Cart Quantity, Cart Line
remove product from cart on line       | Remove Product From Cart, Cart Line
continue browsing with persisted cart  | Shopping Cart, Cart Lines
browse catalog with empty cart         | Shopping Cart
start guest checkout from cart         | Guest Checkout, Shopping Cart
select click-and-collect store         | Select Click-and-collect Store, Click-and-collect Store
enter billing address at checkout      | Billing Address, Guest Checkout
select payment method at checkout      | Payment Method, Guest Checkout
submit payment via StripeWave          | Process Card Payment via StripeWave, Guest Checkout
read order confirmation summary        | Order Confirmation, Click-and-collect Order
collect click-and-collect order at store | Fulfill Click-and-collect Order, Click-and-collect Store

### **Store Employee**
open fulfillment queue for store       | Fulfillment Queue, Click-and-collect Store
mark orders preparing for pickup       | Prepare Click-and-collect Orders for Pickup, Click-and-collect Order
open prepared order from queue         | Fulfillment Queue, Fulfill Click-and-collect Order
confirm fulfill click-and-collect order | Fulfill Click-and-collect Order, Click-and-collect Order, Customer
                                        |   invariant: store employee fulfillment actions are unavailable to customer role

### **Store**
retail location record for pickup       | Click-and-collect Store, Select Click-and-collect Store
supply identity and address at checkout | Click-and-collect Store, Customer
                                        |   invariant: store discovery views remain Increment 1 scope — checkout reuses store records only

### **Product**
catalog item identity for cart line    | Cart Line, Add Product To Cart

### **Stock Availability**
availability at browsing context       | Product, Add Product To Cart
block or warn on unavailable add       | Add Product To Cart, Customer

### **Selected Store**
browsing context for product detail add | Product, Add Product To Cart, Customer

### references

**Ref — Cart boundary concepts**
Source: docs/increments/2-click-and-collect/exploration/domain/ubiquitous-language.md
Locator: Boundary Domain — Product, Customer; Cart > product (boundary)
Extract: partial

```source
### product *(boundary)*

- is the *catalog* item the *customer* selects when running *add product to cart*
- supplies identity and detail for each *shopping cart* line

### customer *(boundary)*

- builds a *shopping cart* and runs *guest checkout*
- selects *click-and-collect store*, enters *billing address*, and pays via *StripeWave*
```

**Ref — Increment 1 selected store prerequisite**
Source: docs/increments/2-click-and-collect/exploration/stories/acceptance-criteria.md
Locator: Add Product to Cart AC 1
Extract: partial

```source
1. **WHEN** the *customer* views *product* detail with a *selected store* from Increment 1 and chooses *add product to cart*
   **THEN** the system places the *product* into the *shopping cart*
```

### decisions made

- *Product* and *Stock Availability* remain Catalog and Increment 1 boundaries — Cart references them without redefining assortment or inventory (scope-fit test).
- *Customer* owns cart actions; *Shopping Cart* and operation classes own container and line rules — receiver-not-responsible-for-receiving (CRC rule).
- Sprint 2 extends *Customer* checkout actions; *Store* supplies pickup location identity — *Click-and-collect Store* owns checkout binding semantics.
- Sprint 3 extends boundary with *Store Employee* fulfillment actions; *Customer* collects after *fulfill click-and-collect order*.
