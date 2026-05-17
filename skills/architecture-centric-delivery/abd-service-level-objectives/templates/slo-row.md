# SLO row template

Use this template when adding a single SLO row outside the main matrix — e.g. as part of acceptance criteria on a high-criticality story, or in an ADR that introduces a new measurable target. The fields are identical to a row in `service-level-objectives.md` but presented one-per-block for readability inside a story or ADR.

---

## SLO: {one-sentence outcome}

| Field | Value |
|---|---|
| **Scope** | system / parent epic: {name} / epic: {name} / story: {name} |
| **Category** | Performance & Scalability / Availability & Reliability / Security & Compliance / Usability & Accessibility / Maintainability & Supportability / Interoperability & Compatibility |
| **Criticality** | mission-critical / business-important / best-effort |
| **SLI (what we measure)** | {a ratio or a quantity over a time window, e.g. "p99 latency on POST /orders"} |
| **Target value** | {threshold being met, e.g. "< 300 ms", "≥ 99.9%", "zero loss"} |
| **Volume** | {conditions, e.g. "at 10 000 req/day during business hours"} |
| **Percentage** | {how often the target must hold over the window, e.g. "99.9% of the time over a 28-day rolling window"} |
| **Measurement** | {tool that produces the SLI, e.g. "Datadog APM", "axe-core CI", "Auth0 audit log"} |
| **Owner** | {team / role} |
| **Error budget action at < 25% remaining** | {what the team does} |
| **Linked SLA** | {customer commitment, or "none — internal only"} |

---

## Example (filled)

## SLO: Order placement latency

| Field | Value |
|---|---|
| **Scope** | parent epic: Orders |
| **Category** | Performance & Scalability |
| **Criticality** | mission-critical |
| **SLI** | p99 server-side latency on `POST /orders` |
| **Target value** | < 300 ms |
| **Volume** | at 10 000 req/day at peak hour load |
| **Percentage** | 99.9% over a 28-day rolling window |
| **Measurement** | Datadog APM trace span `http.server.duration{route=POST /orders}` p99 |
| **Owner** | Orders team |
| **Error budget action at < 25% remaining** | Pause non-essential migrations; prioritise latency fixes (DB index review, N+1 hunt, payload reduction). |
| **Linked SLA** | None — internal target. (Public commitment is "fast checkout"; no contractual latency clause.) |
