# Mombasa Ferry Service — Cross-Skill Reference Domain

## What this is

A shared reference domain used across all story-driven-delivery skills for worked examples, grill-me scenarios, and quality benchmarks. All story-driven-delivery `reference/examples.md` files that use this domain point here for the source-of-truth context.

## Domain overview

The **Mombasa-Likoni Ferry Service** connects Mombasa Island to the Likoni mainland across the Kilindini Harbour channel. It is operated by the **Kenya Ferry Services (KFS)**, carrying passengers on foot and vehicles. The service runs continuously across the day, with vessels departing on-demand when capacity allows.

### Key actors

| Actor | Role |
|---|---|
| **Passenger** | A person travelling on foot across the channel |
| **Vehicle Driver** | A driver bringing a vehicle (matatu, car, lorry) aboard |
| **Ferry Operator** | KFS staff who manages boarding, capacity, and departure |
| **Vessel** | A physical ferry that carries passengers and vehicles across |
| **Payment Terminal** | A self-service or staffed point for fare payment |

### Core domain concepts

| Concept | Meaning |
|---|---|
| **Crossing** | One trip of a *Vessel* from one shore to the other |
| **Boarding Queue** | The queue of passengers or vehicles waiting for the next *Crossing* |
| **Vehicle Lane** | A designated lane on the vehicle deck; each *Vessel* has a fixed number |
| **Fare** | The fee for a single passenger or vehicle *Crossing* |
| **Journey Card** | A rechargeable travel card used by regular passengers |
| **Capacity** | Maximum passengers or vehicles a *Vessel* can carry per *Crossing* |
| **Departure** | The moment a *Vessel* leaves the quay; *Boarding Queue* closes |
| **Turnaround** | The interval between a *Vessel* arriving and re-opening for boarding |

### Domain constraints (invariants)

- A *Vessel* may not depart with **more** passengers or vehicles than its *Capacity*.
- A *Crossing* becomes **Full** the moment *Capacity* is reached — no further boarding.
- A *Journey Card* fare is **deducted at boarding**, not at departure.
- Cash *Fare* is **non-refundable** once a *Crossing* begins.
- Vehicle *Fare* is charged **per vehicle**, regardless of the number of passengers inside it.
- A *Vehicle Lane* assigned to a lorry may not be re-assigned mid-boarding.

---

## Story map (for abd-story-mapping examples)

See [`story-map.md`](./story-map.md).

## Thin slicing (for abd-thin-slicing examples)

See [`thin-slicing.md`](./thin-slicing.md).

## Acceptance criteria (for abd-story-acceptance-criteria examples)

See [`acceptance-criteria.md`](./acceptance-criteria.md).

## Specification by example (for abd-story-specification examples)

See [`specification-by-example.md`](./specification-by-example.md).
