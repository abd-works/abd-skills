# Specification by Example — Increment 1 (stub)

## Story: Search Products by Keyword

### Scenario 1: Keyword returns matching products

Given the **ProductCatalog** contains **Product** *Kitten Food* with **sku** *PET-FOD-001*
When the shopper searches for *kitten*
Then the **Search Results** include **Product** *Kitten Food*

### Scenario 2: No matches

Given the **ProductCatalog** has no product matching *xyznone*
When the shopper searches for *xyznone*
Then the system displays a no-results message

---

## Story: Confirm Product Stock at Store

### Scenario Outline: Stock shown per store

Given **StockAvailability** for **Product** *{product_sku}* at **Store** *{store_code}* has **availableToSellQuantity** *{qty}*
When the shopper views the product detail page for **Product** *{product_name}*
Then the page shows **Store** *{store_code}* with quantity *{qty}*

| product_name | product_sku | store_code | qty |
| --- | --- | --- | --- |
| Kitten Food | PET-FOD-001 | STR-001 | 12 |
