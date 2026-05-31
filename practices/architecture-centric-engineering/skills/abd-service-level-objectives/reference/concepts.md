# Service Level Objectives — Concepts

## What is a Service Level Indicator / Objective / Agreement?

| Term | Definition | Example |
|---|---|---|
| **SLI** (Indicator) | The *thing being measured*. Always a ratio or a quantity over a time window. | "p99 response time for `POST /orders`" |
| **SLO** (Objective) | The *internal target* on the SLI, expressed as **a target value at a volume at a percentage**. | "< 300 ms p99, sustained over 10 000 requests/day, met 99.9% of the time over a 28-day window" |
| **SLA** (Agreement) | The *external commitment* (usually contractual), looser than the SLO so internal teams have headroom. | "99.5% monthly availability on the Orders API, with credits below threshold" |

---

## Six NFR categories

| Category | What it covers |
|---|---|
| **Performance & Scalability** | Speed, throughput, capacity, growth headroom. |
| **Availability & Reliability** | Uptime, fault tolerance, mean time between failures, recovery objectives. |
| **Security & Compliance** | Data protection, authorization correctness, encryption, regulatory adherence. |
| **Usability & Accessibility** | UX quality, accessibility standards, learnability. |
| **Maintainability & Supportability** | Ease of change, debuggability, deployment without downtime, MTTR. |
| **Interoperability & Compatibility** | Integration, browser/device compatibility, API contract stability. |

---

## Scope: where the SLO lives in the story map

| Scope | When to set NFRs here |
|---|---|
| **System** | An NFR that genuinely applies to the whole product. |
| **Parent epic** | An NFR that applies to a coherent group of features. |
| **Epic** | An NFR that applies to one epic but not its siblings. |
| **Story** | An NFR specific to a single user-visible scenario. |

---

## The target-volume-percentage shape

Every well-formed SLO has three numbers:

```
{target value}  at  {volume}  at  {percentage}
```

- **Target value** — the threshold being met (e.g. 300 ms, 99.9% uptime).
- **Volume** — the conditions under which the target is claimed (e.g. "at 10 000 req/day").
- **Percentage** — how often the target must be met over the measurement window (e.g. "99.9% over 28 days").

---

## Error budgets and burn rates

Every SLO with a percentage less than 100% has an **error budget** equal to `1 − target`. The skill's template ships a section for error-budget policy: what the team does when the budget is at 50% remaining, 25%, 0%.
