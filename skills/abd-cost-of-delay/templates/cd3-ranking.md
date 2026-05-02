# CD3 Ranking

## Instructions

List all scored items ordered by highest CD3 first. Every item in this table must have a completed canvas (or reference prior work). When deviating from pure CD3 order, state the rationale in the Override column.

---

## Context

| Field | Value |
| --- | --- |
| **Portfolio / Team** | |
| **Date** | |
| **Items scored** | |

## Ranked items

| Rank | Feature / Epic | Value Type | Urgency | CoD ($/month) | Duration (months) | CD3 | Override rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | | — |
| 2 | | | | | | | — |
| 3 | | | | | | | — |

## Ordering rationale

State the strategy: pure CD3, or CD3 with stated overrides (expedite items, fixed-date constraints, dependencies).

## Observations

Note any large discrepancies between CoD rank and CD3 rank — these are items where duration (lack of agility) is destroying value and may warrant investigation into sources of delay.

---

## Example (filled)

### Context

| Field | Value |
| --- | --- |
| **Portfolio / Team** | Mobile Payments Portfolio |
| **Date** | 2026-04-30 |
| **Items scored** | 3 |

### Ranked items

| Rank | Feature / Epic | Value Type | Urgency | CoD ($/month) | Duration (months) | CD3 | Override rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Feature B — Online subscription | Increase Revenue | Standard | $16,000 | 1 | 16,000 | — |
| 2 | Feature C — Customer travel notification | Reduce Cost | Standard | $20,000 | 2 | 10,000 | — |
| 3 | Feature A — Dashboard redesign | Intangible | Intangible | $4,000 | 5 | 800 | — |

### Ordering rationale

Pure CD3. Feature C has the highest raw CoD but Feature B's short duration (1 month) gives it the best CD3 score — delivering B first means we start earning C's value only 1 month later than if we did C first, while capturing B's value 2 months earlier.

### Observations

Feature A has high duration relative to value. If the team could thin-slice Feature A into a 2-month first increment, CD3 would rise to 2,000. Worth investigating sources of delay (cross-team handoffs, scope bloat).
