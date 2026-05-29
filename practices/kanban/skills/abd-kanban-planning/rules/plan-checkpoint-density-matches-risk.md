---
scanner: plan-shape
---

# Rule: Checkpoint density matches the classified risk

**Scanner:** `scanners/plan-shape-scanner.py` — `PlanShapeScanner` (rule id `plan-checkpoint-density-matches-risk`)

When the plan classifies **integration risk** or **AI-model risk**, at least one run must use a **tight checkpoint policy** — per-story, per-AC, or per-test. Looser-only policies (per-slice, per-epic, across-team only) are insufficient when the model is expected to struggle against proprietary or undocumented surfaces.

When risks are only **value** or **domain** (context is documented, the question is what to build), looser checkpoint policies are acceptable.

## DO

- Tighten checkpoints for the first run against a risky surface (typically per-AC or per-test).
- Loosen later, once the corrections log and the graph have stabilized the domain for the agent.
- State the granularity level explicitly using ABD vocabulary: `per-story`, `per-AC`, `per-test`, `per-slice`, `per-epic`, `across-team`, `across-runs`.

## DON'T

- Write `per-slice` on every run when integration or AI-model risk is classified.
- Use an informal phrase like "we'll check in as needed" — the checkpoint policy must be explicit.

## Example (wrong)

```markdown
## Risks
- **Integration risk** — Acme SSO API, undocumented.
- **AI-model risk** — proprietary Acme internals.

| Run | Stages | Checkpoint Policy |
| 1 | Discovery | Per-slice |
| 2 | Exploration → Engineering | Per-slice |
| 3 | Exploration → Engineering | Per-slice |
```

(Integration + AI-model risk classified, but no run uses per-story / per-AC / per-test.)

## Example (correct)

```markdown
## Risks
- **Integration risk** — Acme SSO API, undocumented.

| Run | Stages | Checkpoint Policy |
| 1 | Discovery | Per-story |
| 2 | Exploration → Engineering | Per-AC / per-test (first slice through SSO) |
| 3 | Exploration → Engineering | Per-slice (subsequent slices once pattern is proven) |
```
