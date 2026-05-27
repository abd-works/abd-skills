# Rule: Every SLO row has target × volume × percentage

Every Service Level Objective in the matrix must specify three numbers: a **target value** (the threshold being met), a **volume** (the conditions under which the target is claimed), and a **percentage** (how often the target must be met over a measurement window). Without all three, the row is a wish, not an objective — a "fast API" can be made true or false by the next reader, but "p99 < 300 ms at 10 000 req/day at 99.9% over 28 days" cannot. Failing means a row missing the volume condition, a percentage of 100% on an availability claim where incidents are inevitable, or a target stated only in adjectives ("highly available", "fast", "secure").

## DO

- Write every SLO as `{target value} at {volume} at {percentage}` (or as three filled cells in a table that compose to the same shape).

  **Example (pass):** "p99 < 300 ms on `POST /orders` at 10 000 req/day at 99.9% over a 28-day rolling window."

- Choose a percentage less than 100% for anything subject to real-world failure (availability, latency, success rate). 100% is appropriate only for absolute requirements (zero data loss, zero unauthorized writes, encryption coverage).

  **Example (pass):** "Order durability: zero data loss at any volume at 100% within the commit window" — correct because data loss is a hard requirement.

  **Example (pass):** "API uptime: < 0.1% error rate at production traffic at 99.9% over 28 days" — correct because perfect availability is impossible and 99.9% has a real error budget.

- Make the volume realistic and named. "Peak hour", "10 000 req/day", "during business hours", "across both regions concurrently" all qualify.

  **Example (pass):** "Cache hit rate ≥ 95% at all reads at 99% over a 24-hour window." (Volume = "all reads", time window stated.)

## DO NOT

- Ship a row with no volume condition.

  **Example (fail):** "API latency < 300 ms at 99.9%." — at what request rate? Cold start? Peak load? The row is unmeasurable in practice.

- Claim 100% on a probabilistic dimension.

  **Example (fail):** "API uptime 100% over a 28-day window." — incidents are inevitable; the team will burn out chasing a target it cannot hit, or pretend the target was met when it was not.

- State an objective in adjectives.

  **Example (fail):** "The system must be highly available, performant, and secure." — none of the three is decidable.

- Use a SLI that is not actually being measured today, without naming the planned tool and owner.

  **Example (fail):** SLI column reads "user-perceived latency" with no measurement column entry. If the tool does not exist yet, the row should name the tool that will measure it and the owner who will land it; otherwise the objective is unsupported.

**Source:** Practice-skill authoring convention (abd-service-level-objectives); the target-volume-percentage shape is the central discipline of this skill.
