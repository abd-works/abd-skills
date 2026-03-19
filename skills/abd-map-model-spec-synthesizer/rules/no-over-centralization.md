---
rule_id: no-over-centralization
phases: [step6]
order: 25
impact: MEDIUM
---

## Distribute Responsibility — No Central Manager

A single "manager", "service", or "controller" concept that does everything is an anti-pattern. Responsibility should be distributed to the concepts that own the decisions.

There is no scanner for this rule. It requires design judgment — the AI assesses whether operations are over-centralized.

**DO** assign operations to the concepts that own the decisions. Prefer composition — concepts collaborate; no single concept orchestrates everything.

**DO NOT** create a central concept that holds most operations while other concepts are anemic. Spread operations to the concepts that naturally own them.

- Right: Check has roll(); DifficultyClass has value; Result has degree. Each owns its part.
- Wrong: CheckResolver has resolveCheck(), getDC(), computeDegree() — one concept does it all
