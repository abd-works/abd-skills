---
scanner: plan-shape
---

# Rule: Plan is not a default single-run five-stage waterfall

**Scanner:** `scanners/plan-shape-scanner.py` — `PlanShapeScanner` (rule id `plan-is-not-default-six-stage`)

"Run all five bootcamp stages start to finish in one run" is the **degenerate case** for trivial engagements with no classified risk. Real plans decompose the work into targeted runs that flush out unknowns early, per `abd-kanban-planning` §2a–2c.

This rule flags plans that have **exactly one run** whose stages are the five canonical bootcamp stages (`shaping`, `discovery`, `exploration`, `specification`, `engineering`) in order, **unless** the plan marks itself explicitly as trivial.

## DO

- Break the work into multiple runs that front-load risk.
- Use strategies from `strategies/` as starting points — they decompose the run structure for you.
- If the engagement truly is trivial, mark it with `trivial: true` in the plan's YAML frontmatter, or add a section that states the engagement has no classified risk and explains why a single sweep is appropriate.

## DON'T

- Default to a one-run, five-stage sweep because it feels complete.
- Hide the sweep behind renamed stages — use canonical stage names from `../../../content/stages/README.md`.

## Example (wrong)

```markdown
| Run | Stages |
| 1 | Shaping → Discovery → Exploration → Specification → Engineering |
```

(Single run, canonical five, no trivial flag, non-empty risks. This is the default-sweep shape.)

## Example (correct — non-trivial decomposition)

```markdown
| Run | Stages |
| 1 | Shaping → Discovery |
| 2 | Exploration → Engineering |  (first thin slice)
| 3 | Exploration → Engineering |  (second slice)
| 4 | Discovery          |  (fill-in deferred map)
```

## Example (correct — truly trivial engagement)

```markdown
---
trivial: true
---

# Agile Delivery Plan
Engagement is a five-story internal tool, no classified risks beyond value.

| Run | Stages |
| 1 | Shaping → Discovery → Exploration → Specification → Engineering |
```
