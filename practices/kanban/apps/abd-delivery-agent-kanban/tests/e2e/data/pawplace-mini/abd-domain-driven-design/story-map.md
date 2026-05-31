# Story Map — PawPlace mini (outline)

**Product:** PawPlace — online pet store (2 increments: walk-in driver, click-and-collect).  
**Spine:** find store → browse catalog & stock → cart → pay → pickup.

(E) Find a Store
    (S) Customer --> View Store Map
    (S) Customer --> View Store List
    (S) Customer --> Calculate Distance to Store

(E) Browse Catalog & Stock
    (S) Customer --> View Product Details
    (S) System --> Display Real-Time Stock Availability
    (S) Store Employee --> Update Product Stock Levels

(E) Shop & Pay Online
    (E) Shopping Cart
        (S) Customer --> Add Product to Cart
        (S) Customer --> Update Cart Quantity
        (S) Customer --> Remove Product from Cart
    (E) Checkout & Payment
        (S) Customer --> Select Click-and-Collect Store
        (S) Customer --> Check Out as Guest
        (S) Customer --> Enter Billing Address
        (S) Customer --> Select Payment Method
        (S) System --> Process Card Payment via StripeWave
        (S) System --> Confirm Order and Send Confirmation Email
    (E) Store Fulfillment
        (S) Store Employee --> Prepare Click-and-Collect Orders for Pickup
        (S) Store Employee --> Fulfill Click-and-Collect Order
