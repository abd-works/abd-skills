# Mombasa Ferry Service — Thin Slicing

Reference thin-slicing for the `abd-thin-slicing` skill. Used as a quality bar and grill-me scenario. See [`README.md`](./README.md) for domain context and [`story-map.md`](./story-map.md) for the source map.

---

## Delivery increments

### Increment 1 — Foot Passenger Crossing (Cash)

**Outcome:** A passenger can pay a cash fare, board a vessel, cross the channel, and disembark — end to end, no cards, no vehicles.

**Stories (spine):**
- Passenger --> Pay Cash Fare
- Passenger --> Join Boarding Queue
- Ferry Operator --> Open Boarding
- Passenger --> Walk Aboard Vessel
- Ferry Operator --> Close Boarding At Capacity
- Ferry Operator --> Depart Vessel
- Ferry Operator --> Dock Vessel At Far Shore
- Passenger --> Disembark Vessel

**Slicing notes:** Capacity enforcement is in scope — without it the boarding flow has no natural end. Rejection (`Reject Insufficient Balance`) is out of scope for cash (cash is always accepted at face value); it belongs in Increment 3 (Journey Card). Vehicle crossing and turnaround are deferred.

---

### Increment 2 — Vessel Operations (Capacity + Turnaround)

**Outcome:** An operator can assign a vessel to a route, monitor live boarding count, and complete the turnaround cycle between crossings — so the schedule can run continuously.

**Stories (spine):**
- Ferry Operator --> Assign Vessel To Route
- Ferry Operator --> Open Vessel For Boarding
- Ferry Operator --> View Current Boarding Count
- Ferry Operator --> Record Vessel At Full Capacity
- Ferry Operator --> Log Vessel Arrival
- Ferry Operator --> Begin Turnaround Interval
- Ferry Operator --> Re-Open Vessel After Turnaround

**Slicing notes:** Depends on Increment 1 for the core boarding flow. Turnaround is a manual operational cycle for now; automated scheduling is a later enhancement.

---

### Increment 3 — Journey Card (Issue + Board + Recharge)

**Outcome:** A regular passenger can register a Journey Card, load a balance, pay fare at boarding by presenting the card, and recharge when the balance is low.

**Stories (spine):**
- Passenger --> Register New Journey Card
- Passenger --> Load Initial Balance
- Passenger --> Present Journey Card
- Payment Terminal --> Reject Insufficient Balance
- Passenger --> Add Balance To Journey Card
- Payment Terminal --> Confirm Recharge

**Slicing notes:** Depends on Increment 1 (boarding flow). Balance deduction replaces cash payment for card holders; the boarding walk-on flow is unchanged.

---

### Increment 4 — Vehicle Crossing

**Outcome:** A driver can join a vehicle lane queue, get assigned to a lane, drive aboard, cross the channel, and drive off — with the operator enforcing lane capacity and rejecting oversized vehicles.

**Stories (spine):**
- Vehicle Driver --> Join Vehicle Lane Queue
- Ferry Operator --> Assign Vehicle To Lane
- Ferry Operator --> Reject Oversized Vehicle
- Ferry Operator --> Signal Vehicle Lane Boarding Open
- Vehicle Driver --> Drive Vehicle Aboard
- Ferry Operator --> Secure Vehicle Lane At Capacity
- Ferry Operator --> Depart With Vehicles Loaded
- Vehicle Driver --> Drive Vehicle Off Vessel

**Slicing notes:** Depends on Increment 2 for vessel operations. Vehicle fare billing is included in this increment (charged per vehicle at lane assignment). Lane assignment and capacity are enforced by the operator manually in this increment; automated lane routing is a later enhancement.

---

## What to notice

- Each increment delivers a **vertical, demonstrable path** from actor action to observable outcome — not a layer
- Increment names are **stakeholder-visible capabilities**, not tech phases
- Dependencies are made **explicit** in slicing notes, not hidden inside an increment
- Increment 1 is the spine: you can show a completed crossing end-to-end at the end of it
- Quality trade-offs are named: "manually" vs "automated", "operator enforces" vs "system enforces"
