
---

# Core Domain

## Product Catalog

### product catalog

- owns the browsable, searchable collection of pet supplies and is the single source of truth for what is available for sale
- provides filtering and search so customers can narrow results by *category*, pet type, or brand
- owns the *customer review* and rating system — reviews attach social proof directly to *product*
- collaborates with *Order* by supplying current *product* prices at purchase time and with *Customer Account* through *wishlist* links back to *product*
- **Invariant:** no other abstraction may duplicate *product* identity, *stock availability* truth, or *customer review* ownership

### product

- is a pet supply item (food, toy, bed, leash, grooming product, aquarium gear) available for purchase through the online store
- carries multiple *product images*, a description, and weight and dimensions where relevant
- belongs to at least one *category* and may belong to several simultaneously
- exposes real-time *stock availability* so checkout never surprises the customer with a backorder
- accumulates *customer reviews* that contribute to an aggregate star rating
- **Invariant:** must always belong to at least one *category*; must always expose current *stock availability*

### product image

- is a visual asset attached to a *product*, carrying a source file reference, alt text, and a display order
- composes under a single *product*, ideally covering multiple angles
- presents on the *product* detail page to support purchase decisions

### category

- organizes *product* into browsable groups — by product type, pet type, or brand
- allows a *product* to belong to multiple *category* simultaneously; *category* assignments are not exclusive
- acts as a filter facet enabling customers to narrow catalog results without scrolling through irrelevant items

### customer review

- attaches a one-to-five star rating, optional written text, and optional photo to a *product*
- aggregates with other *customer reviews* into the *product*'s star rating and review count
- shows photo reviews where a customer's pet uses the *product*, adding social proof
- **Invariant:** must be attached to exactly one *product*; only one *customer review* per *customer account* per *product*

### stock availability

- is a real-time indicator of whether a *product* is purchasable and how much quantity is available to sell at a given *store*
- computes from *stock level* at each *store* (quantity on hand minus reserved quantity)
- displays on the *product page* per *store* so a walk-in customer knows where to find the item
- gates the purchase path — a *product* that is out of stock at all stores must not offer *add to cart* (Increment 2: *cart item* quantity reflects *stock availability* at render time; checkout blocked when unavailable)
- reserves quantity when an *order* is confirmed so concurrent shoppers cannot oversell the same *stock level*
- updates immediately when *store employee* changes *stock level* via the *admin dashboard*
- **Invariant:** must always be current; stale availability that permits checkout of an unavailable *product* is a domain failure

### stock level

- *(property on stock availability)* — numeric quantity of a *product* held at a given *store*
- is edited by *store employee* through the *admin dashboard* stock form
- drives the customer-visible *stock availability* status for that *store* and *product* pair

### product page

- *(presentation surface)* — detail view for a single *product* showing name, *description*, *product images*, *category* membership, and per-store *stock availability*
- in Increment 2 exposes *add to cart* when *stock availability* permits at least one *store*; defers *customer review* and keyword search
- is reachable from *product catalog* category browsing and from the *shopping cart* for quantity review

### restocking

- is the replenishment of *stock availability* when a *returned items* passes inspection and the item is placed back into sellable inventory
- updates *stock level* at the *store* where the item was originally sourced or the designated *return* warehouse
- fires asynchronously after *return status* transitions to "inspected" — does not block the *refund* path
- **Invariant:** *stock level* increase must match returned quantity only after inspection confirms sellable condition

#