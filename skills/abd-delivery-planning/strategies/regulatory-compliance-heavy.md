# Strategy: Regulatory / Compliance-Heavy

**When to use:** Regulation, legal, or compliance dominates risk (finance, health, privacy, government programs).

**Typical scope:** Full product, tightest scrutiny on regulated stories.


| Step | Stage                          | Intent                                                                                                            | Scope                          | Checkpoint policy                           | Rationale                              |
| ---- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------ | ------------------------------------------- | -------------------------------------- |
| 1    | Discovery → Prioritization     | **Map compliance surface:** which stories touch regulated data, audit, retention, reporting.                      | Full map                       | Per-epic; checkpoint regulatory touchpoints | Rules matter more than raw tech.       |
| 2    | Exploration → Story Definition | **Make compliance concrete:** AC and scenarios with **real** regulatory values and thresholds — not placeholders. | Compliance-heavy stories first | Per-AC; user validates regulatory accuracy  | Wrong AC = wrong system.               |
| 3    | Acceptance Tests → Engineering | **Encode rules in tests;** code must satisfy them.                                                                | Same compliance stories        | Per-test; cross-role per story              | Tests are the proof bundle.            |
| 4+   | Exploration → Engineering      | **Everything else** by value; tighten only where regulation still applies.                                        | Non-compliance-heavy stories   | Per-slice; per-story when data is regulated | Faster where rules are already proven. |


**Key constraints:**

- Trace rules to sources (law, policy, standard). No invented compliance.
- Use real values in AC/scenarios, not “TBD retention.”
- Post-approval changes to compliance stories need explicit re-approval.
