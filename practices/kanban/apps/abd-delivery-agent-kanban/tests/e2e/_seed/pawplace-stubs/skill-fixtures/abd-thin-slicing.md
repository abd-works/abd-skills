# Thin slicing — PawPlace (stub)

**Product:** PawPlace — kanban E2E fixture with **three modules** and **multiple increments** per module (trimmed from abd-pet-store-demo).

Scatter reads `## Module N:` sections when a **partition** ticket completes discovery; increment tickets use `### Increment N:` under the matching module.

## Module 1: Product Catalog

### Increment 1: Find products and check store stock

**Outcome:** A shopper can search the catalog, open a product page, and confirm stock at a store.

**Stories in this increment:**

- Search Products by Keyword
- View Product Detail Page
- Confirm Product Stock at Store

### Increment 2: Browse categories and filters

**Outcome:** A shopper can browse by category and filter results without keyword search.

**Stories in this increment:**

- Browse Products by Category
- Filter Products by Price Range

## Module 2: Store Operations

### Increment 1: Staff maintain store stock

**Outcome:** Store employees can update stock levels for their location.

**Stories in this increment:**

- Update Product Stock Levels
- View Low Stock Alerts

## Module 3: Checkout and Fulfillment

### Increment 1: Click-and-collect checkout

**Outcome:** A guest can add items to cart, pay online, and pick up at a chosen store.

**Stories in this increment:**

- Add Product to Cart
- Check Out as Guest
- Select Click-and-Collect Store
