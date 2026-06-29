# Story Mapping — Example

## Example story map

(E) Manage Customer Orders
    (E) Place New Order
        (S) Customer --> Browse Product Catalog
        (S) Customer --> Add Item To Cart
        (S) Customer --> Enter Shipping Address
        (S) Customer --> Select Delivery Option
        (S) Customer --> Submit Order
    (E) Track Order Status
        (S) Customer --> View Current Order Status
        (S) System --> Send Shipment Notification
    (E) Cancel Order
        (S) Customer --> Request Order Cancellation
        (S) System --> Process Cancellation Refund

## What to notice

- Epic names are **verb–noun**, no actor in the name
- Actor goes before `-->`, not in the story name
- Each story is one observable behavior — not a task or feature
- Sub-epics group stories into coherent flows

---

## Cross-skill example domain — Mombasa Ferry Service

A second worked domain for grill-me sessions and quality benchmarks: the **Mombasa-Likoni Ferry Service** (Kenya Ferry Services). Richer domain constraints (capacity, vehicle lanes, Journey Card balance), two distinct actor types (Passenger, Vehicle Driver), and a real system with regulatory and operational invariants.

See [`../../../reference/mombasa-ferry/story-map.md`](../../../reference/mombasa-ferry/story-map.md) for the full story map in this domain, and [`../../../reference/mombasa-ferry/README.md`](../../../reference/mombasa-ferry/README.md) for domain context.
