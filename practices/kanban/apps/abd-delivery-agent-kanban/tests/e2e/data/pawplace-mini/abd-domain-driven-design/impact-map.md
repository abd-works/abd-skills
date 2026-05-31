# Impact map — PawPlace mini (2 increments)

```text
GOAL: Grow omnichannel revenue at PawPlace pet stores
GOAL: Increase converted store visits and click-and-collect orders
  METRIC: Combined in-store plus click-and-collect revenue +15% vs baseline this planning slice (economic)
  METRIC: Guest checkout completion rate 70%+ among carts that reach payment (conversion)
  NOTE: Inc1-Inc2 below = delivery increments in thin-slicing.md
  ASSUMPTION: Real-time stock at the selected store stays accurate within five minutes when walk-in and pickup demand overlap at peak hours.

  ACTOR: Local pet shoppers (planning an in-store visit)
    IMPACT: Find a nearby store and confirm stock before visiting
      METRIC: % of store-detail views followed by visit within 48 hours; target 25%+
      DELIVERABLE: View Store Map
      DELIVERABLE: View Store List
      DELIVERABLE: Calculate Distance to Store
      DELIVERABLE: View Product Details
      DELIVERABLE: Display Real-Time Stock Availability
    IMPACT: Buy in person when stock is visible at the chosen store
      METRIC: Walk-in purchases where customer checked stock online first; target 60%+ of qualifying visits
      DELIVERABLE: Display Real-Time Stock Availability (store-scoped)

  ACTOR: Online guest shoppers (click-and-collect intent)
    IMPACT: Build a cart and check out without creating an account
      METRIC: Guest checkout completion among carts reaching billing; target 70%+
      DELIVERABLE: Add Product to Cart
      DELIVERABLE: Update Cart Quantity
      DELIVERABLE: Remove Product from Cart
      DELIVERABLE: Check Out as Guest
      DELIVERABLE: Enter Billing Address
      DELIVERABLE: Select Payment Method
      DELIVERABLE: Process Card Payment via StripeWave
      DELIVERABLE: Confirm Order and Send Confirmation Email
    IMPACT: Pick up paid orders at the chosen store
      METRIC: Click-and-collect orders marked ready within promised window; target 90%+
      DELIVERABLE: Select Click-and-Collect Store

  ACTOR: Store employees (stock and pickup desk)
    IMPACT: Keep shelf stock levels current for customer-facing availability
      METRIC: Stock level updates within 15 minutes of physical change; target 95%+
      DELIVERABLE: Update Product Stock Levels
    IMPACT: Prepare click-and-collect orders for customer pickup
      METRIC: Orders moved to ready-for-pickup status within SLA; target 90%+
      DELIVERABLE: Prepare Click-and-Collect Orders for Pickup
      DELIVERABLE: Fulfill Click-and-Collect Order
```

| Phase | Feature | Actor / impact |
| --- | --- | --- |
| Inc1 | View Store Map | Local pet shoppers / Find a nearby store and confirm stock before visiting |
| Inc1 | View Store List | Local pet shoppers / Find a nearby store and confirm stock before visiting |
| Inc1 | Calculate Distance to Store | Local pet shoppers / Find a nearby store and confirm stock before visiting |
| Inc1 | View Product Details | Local pet shoppers / Find a nearby store and confirm stock before visiting |
| Inc1 | Display Real-Time Stock Availability | Local pet shoppers / Find a nearby store and confirm stock before visiting |
| Inc1 | Update Product Stock Levels | Store employees / Keep shelf stock levels current for customer-facing availability |
| Inc2 | Add Product to Cart | Online guest shoppers / Build a cart and check out without creating an account |
| Inc2 | Check Out as Guest | Online guest shoppers / Build a cart and check out without creating an account |
| Inc2 | Process Card Payment via StripeWave | Online guest shoppers / Build a cart and check out without creating an account |
| Inc2 | Select Click-and-Collect Store | Online guest shoppers / Pick up paid orders at the chosen store |
| Inc2 | Prepare Click-and-Collect Orders for Pickup | Store employees / Prepare click-and-collect orders for customer pickup |
| Inc2 | Fulfill Click-and-Collect Order | Store employees / Prepare click-and-collect orders for customer pickup |
