# Mombasa Ferry Service — Story Map

Reference story map for the `abd-story-mapping` skill. Used as a quality bar and grill-me scenario. See [`README.md`](./README.md) for domain context.

---

## Story map

(E) Manage Passenger Crossing
    (SE) Pay Fare
        (S) Passenger --> Present Journey Card
        (S) Passenger --> Pay Cash Fare
        (S) Payment Terminal --> Reject Insufficient Balance
    (SE) Board Vessel
        (S) Passenger --> Join Boarding Queue
        (S) Ferry Operator --> Open Boarding
        (S) Passenger --> Walk Aboard Vessel
        (S) Ferry Operator --> Close Boarding At Capacity
    (SE) Complete Crossing
        (S) Ferry Operator --> Depart Vessel
        (S) Ferry Operator --> Dock Vessel At Far Shore
        (S) Passenger --> Disembark Vessel

(E) Manage Vehicle Crossing
    (SE) Register Vehicle For Crossing
        (S) Vehicle Driver --> Join Vehicle Lane Queue
        (S) Ferry Operator --> Assign Vehicle To Lane
        (S) Ferry Operator --> Reject Oversized Vehicle
    (SE) Load Vehicle Onto Vessel
        (S) Ferry Operator --> Signal Vehicle Lane Boarding Open
        (S) Vehicle Driver --> Drive Vehicle Aboard
        (S) Ferry Operator --> Secure Vehicle Lane At Capacity
    (SE) Complete Vehicle Crossing
        (S) Ferry Operator --> Depart With Vehicles Loaded
        (S) Vehicle Driver --> Drive Vehicle Off Vessel

(E) Manage Journey Card
    (SE) Issue Journey Card
        (S) Passenger --> Register New Journey Card
        (S) Passenger --> Load Initial Balance
    (SE) Recharge Journey Card
        (S) Passenger --> Add Balance To Journey Card
        (S) Payment Terminal --> Confirm Recharge

(E) Operate Vessel
    (SE) Start Vessel Service
        (S) Ferry Operator --> Assign Vessel To Route
        (S) Ferry Operator --> Open Vessel For Boarding
    (SE) Monitor Capacity
        (S) Ferry Operator --> View Current Boarding Count
        (S) Ferry Operator --> Record Vessel At Full Capacity
    (SE) Complete Turnaround
        (S) Ferry Operator --> Log Vessel Arrival
        (S) Ferry Operator --> Begin Turnaround Interval
        (S) Ferry Operator --> Re-Open Vessel After Turnaround

---

## What to notice

- Actor before `-->`, not in the story name — `Ferry Operator --> Open Boarding`, not `Open Boarding by Operator`
- Each sub-epic is a coherent **flow**, not a feature category
- Stories are **observable behaviors**, not implementation tasks — `Reject Insufficient Balance` not `Validate balance check`
- System actors (`Payment Terminal`) appear only when the system is the initiating party
- Capacity and turnaround are in the map because they are real operational behaviors, not implementation detail
