---
state: domain-terms
---

# Module: PawPlace

Scope: Online pet store — product catalog, multi-store stock, walk-in driver slice.

**Key Abstractions:**
- **Product Catalog**: product catalog, product, category, stock availability
- **Store**: store, store locator

---

# Core Domain

## Product Catalog

*Product Catalog* is the browsable collection of pet supplies — single source of truth for *product* identity and *stock availability*.

### product

- A *product* is a pet supply item with name, SKU, price, and description.
- Invariant: SKU is unique across the catalog.

### stock availability

- *Stock availability* shows whether a *product* is available at a given *store*.
- Invariant: must reflect current quantity; stale stock misleads shoppers.

## Store

### store

- A *store* is a physical retail location with address and geo-coordinates.

### store locator

- *Store locator* lets shoppers discover *stores* on a map or list.
