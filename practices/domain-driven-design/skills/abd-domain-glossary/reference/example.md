
# Core Domain

## Product Catalog

*Product Catalog* is the browsable, searchable collection of pet supplies and the single source of truth for what is for sale. It owns *product* identity, *category* facets for navigation, the *customer review* and rating system, and real-time *stock availability*. No other KA duplicates product identity, stock truth, or review ownership.

### product

- A *product* is a pet supply item (food, toy, bed, leash, grooming product, aquarium gear) available for purchase.
- Every *product* has images, a description, and real-time *stock availability*.

---

### category

- A *category* organizes *product* for browsing — by product type, pet type, or brand.
- Customers narrow the catalog using *category* together with search and filters.

---

### customer review

- A *customer review* is a star rating with optional written text and optional photo attached to a *product*.
- Photo reviews show the pet using the *product*.

---

### stock availability

- *Stock availability* is a real-time indicator of whether a *product* can be purchased.
- Checkout must not proceed when the *product* is backordered.

---
