---
state: domain-model
increment_scope: Increment 1 — Find products and check store stock
---

# Module: PawPlace

## Product Catalog

| Class | Responsibilities | Collaborators |
| --- | --- | --- |
| **ProductCatalog** | Browse, search products; enforce catalog invariants | Product, Category |
| **Product** | Hold identity (SKU), price, description | ProductImage, StockAvailability |
| **StockAvailability** | Track quantity per store | Product, Store |

## Store

| Class | Responsibilities | Collaborators |
| --- | --- | --- |
| **Store** | Address, geo-coordinates, hours | StockAvailability |
| **StoreLocator** | Map/list discovery | Store |

Invariants: one SKU per product; stock quantity ≥ 0.
