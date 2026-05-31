# Thin slicing — PawPlace mini (2 increments)

## Product / context

**Product:** PawPlace — online pet store. This fixture stops after increment 2 (click-and-collect).

**Spine:** catalog → store → stock visibility → cart → pay → pickup.

## Increments

### Increment 1: `Walk-in driver — find the store, see what's in stock`

**Outcome:** Customer finds a *store*, browses *catalog*, sees *real-time stock* at that store, walks in to buy in person (no checkout in system).

**Stories:**

- *View Store Map*
- *View Store List*
- *Calculate Distance to Store*
- *View Product Details*
- *Display Real-Time Stock Availability*
- *Update Product Stock Levels* (store employee)

**Folder:** `docs/increments/1-walk-in-driver/`

---

### Increment 2: `Click-and-collect — buy online, pick up at the store`

**Outcome:** Customer uses *shopping cart*, pays online (StripeWave), picks up at chosen *store*. Guest checkout only.

**Stories:**

- *Add Product to Cart*
- *Update Cart Quantity*
- *Remove Product from Cart*
- *Select Click-and-Collect Store*
- *Check Out as Guest*
- *Enter Billing Address*
- *Select Payment Method*
- *Process Card Payment via StripeWave*
- *Confirm Order and Send Confirmation Email*
- *Prepare Click-and-Collect Orders for Pickup* (store employee)
- *Fulfill Click-and-Collect Order* (store employee)

**Folder:** `docs/increments/2-click-and-collect/`

---

## Sprint grouping (for scatter at specification/engineering)

See `sprint-groupings.md` for ticket labels kanban-lead uses when scattering increment → sprint.
