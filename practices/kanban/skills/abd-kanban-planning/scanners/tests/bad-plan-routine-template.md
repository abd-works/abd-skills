# Agile Delivery Plan — PawPlace (bad template)

## Context inventory

**Provided:** `story/thin-slicing.md` — nine increments.
**Missing:** none.

## Risks

- **Integration risk** — StripeWave in Increment 2.
- **Delivery risk** — nine increments.

## Strategy

Selected: `reference/strategies/new-thin-slice.md`

## Runs summary

| Run | Stages | Scope | Chain policy | Rationale |
| 2 | Exploration ? Specification ? Engineering | Increment 1 | Chain to Run 3 | First vertical slice |
| 3 | Exploration ? Specification ? Engineering | Increment 2 | Chain to Run 4 | Cart + payment |

## Run 2 — Increment 1

| Slot | Phase | Role | Skill(s) | Deliverable |
| 19 | exploration | product-owner | abd-story-acceptance-criteria | Increment 1 AC |
| 20 | exploration | reviewer | — | Review slot 19 |

## Runs 3–10 — Increments 2–9 (routine template)

**Skill pattern per increment** (each row = executor + reviewer pair unless waived):

| Offset | Phase | Role | Skills | Waive when |
| --- | --- | --- | --- | --- |
| +0 | exploration | business-expert | abd-domain-language | no new domain terms |
| +1 | exploration | product-owner | abd-story-acceptance-criteria | never |

### Run slot map (sequential — continues from Run 2)

| Run | Increment | Opens at slot (est.) | Closes at slot (est.) |
| --- | --- | --- | --- |
| 3 | 2 Click-and-collect | 43 | ~68 |
| 4 | 3 Ship to home | ~69 | ~94 |
| 5+ | 4 Returning customers | ~95 | ~120 | Routine delivery |
