---
state: domain-model
increment_scope: Increment 1 — Find products and check store stock
---

# Module: PawPlace

## Product Catalog

### ProductCatalog << Entity >>

+ findProduct(sku: String): Product
+ search(keyword: String): List<Product>

### Product << Entity >>

+ sku: String
+ name: String
+ price: Money

### StockAvailability << Entity >>

+ availableToSellQuantity: Integer
+ store: Store

## Store

### Store << Entity >>

+ storeCode: String
+ name: String
