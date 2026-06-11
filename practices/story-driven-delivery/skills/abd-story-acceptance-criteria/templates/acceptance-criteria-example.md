# Acceptance criteria (exploration) — example

Filled example for the **Manage Customer Orders** story map (`abd-story-mapping` reference). Use as the quality bar when authoring `acceptance-criteria.md` from `templates/acceptance-criteria.md`.

---

## Story: Browse Product Catalog

**Story type:** user

### Domain terms

- *Product Catalog* — browsable list of products available to order
- *Category* — grouping used to narrow what the customer sees
- *Product Detail* — name, description, price, and image for one product
- *Out Of Stock* — product not available to add to an order right now

### Acceptance criteria

1. **WHEN** the customer opens the *Product Catalog*
   **THEN** the system displays available products grouped by *Category*
   **AND** each row shows at least product name and price
   **Evidence:** Order Management Workshop — whiteboard “Place order” flow, 2026-03-15, sticky “browse by category”

2. **WHEN** the customer selects a *Category*
   **THEN** the *Product Catalog* lists only products in that *Category*
   **Evidence:** Order Management Workshop — same session, “filter catalog by category”

3. **WHEN** the customer selects a product from the *Product Catalog*
   **THEN** the system shows *Product Detail* for that product
   **Evidence:** Order Management Workshop — “click through to product detail”

4. **WHEN** a product is *Out Of Stock*
   **THEN** the *Product Catalog* and *Product Detail* show that the product cannot be added to an order
   **BUT** the customer can still browse other products
   **Evidence:** Order Management Workshop — “don’t block browsing when one SKU is gone”

---

## Story: Add Item To Cart

**Story type:** user

### Domain terms

- *Cart* — holding area for products the customer intends to order
- *Cart Line* — one product and quantity in the *Cart*
- *Product Detail* — surface where the customer chooses quantity
- *Quantity* — number of units of one product
- *Out Of Stock* — cannot add or increase quantity beyond available supply

### Acceptance criteria

1. **WHEN** the customer adds a product from *Product Detail*
   **THEN** the system creates or updates a *Cart Line* with the chosen *Quantity*
   **AND** the *Cart* shows the updated line total
   **Evidence:** Order Management Workshop — “add to cart from detail page”

2. **WHEN** the customer changes *Quantity* on an existing *Cart Line*
   **THEN** the *Cart* updates the line total immediately
   **Evidence:** Order Management Workshop — “edit qty in cart”

3. **WHEN** the customer adds the same product again
   **THEN** the system increases *Quantity* on the existing *Cart Line*
   **BUT** does not create a duplicate *Cart Line* for the same product
   **Evidence:** Order Management Workshop — “one line per SKU”

4. **WHEN** the product is *Out Of Stock* for the requested *Quantity*
   **THEN** the system rejects the add or increase
   **AND** the customer sees which *Quantity* is available
   **BUT** other *Cart Line* items are unchanged
   **Evidence:** Order Management Workshop — “cap qty to stock”

---

## Story: Submit Order

**Story type:** user

### Domain terms

- *Cart* — must contain at least one *Cart Line* before submit
- *Shipping Address* — delivery destination captured earlier in the flow
- *Delivery Option* — shipping speed or method the customer selected
- *Order* — confirmed request to fulfill and ship
- *Order Confirmation* — reference and summary shown after successful submit
- *Payment Authorization* — funds check with the payment provider before the *Order* is accepted

### Acceptance criteria

1. **WHEN** the customer submits with a non-empty *Cart*, a valid *Shipping Address*, and a selected *Delivery Option*
   **THEN** the system requests *Payment Authorization*
   **AND** on success creates an *Order* from the *Cart*
   **Evidence:** Order Management Workshop — “submit only when cart + address + delivery ready”

2. **WHEN** *Payment Authorization* succeeds
   **THEN** the customer sees *Order Confirmation* with order reference and line summary
   **AND** the *Cart* is cleared
   **Evidence:** Order Management Workshop — “confirmation screen + empty cart”

3. **WHEN** *Payment Authorization* fails
   **THEN** the customer sees that payment failed and can retry or change payment method
   **BUT** no *Order* is created and the *Cart* is unchanged
   **Evidence:** Order Management Workshop — “failed pay ≠ order placed”

4. **WHEN** the customer submits with an empty *Cart*
   **THEN** the system blocks submit
   **AND** prompts the customer to add products first
   **Evidence:** Order Management Workshop — “no empty submit”

5. **WHEN** the customer submits without a *Shipping Address* or *Delivery Option*
   **THEN** the system blocks submit
   **AND** directs the customer to complete the missing step
   **Evidence:** Order Management Workshop — “gate on address and delivery”
