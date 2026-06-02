# Acceptance Criteria — Increment 1 (stub)

Scope: Find products and check store stock.

---

## Story: Search Products by Keyword

**Story type:** user

### Acceptance criteria

1. **WHEN** the shopper enters a keyword in the *search bar* and submits
   **THEN** the *search results* show matching *products*
   **Evidence:** abd-pet-store-demo requirements — search and filter

2. **WHEN** the keyword matches no products
   **THEN** the system shows a "no results" message

---

## Story: View Product Detail Page

**Story type:** user

### Acceptance criteria

1. **WHEN** the shopper selects a *product* from the catalog
   **THEN** the *product detail page* shows name, price, images, and description

---

## Story: Confirm Product Stock at Store

**Story type:** user

### Acceptance criteria

1. **WHEN** the shopper views the *product detail page*
   **THEN** the system displays *stock availability* per *store*
   **AND** quantities reflect current *stock level*

2. **WHEN** the *product* is out of stock at all stores
   **THEN** the system clearly indicates unavailability
