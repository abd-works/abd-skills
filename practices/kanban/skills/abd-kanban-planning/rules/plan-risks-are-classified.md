---
scanner: plan-shape
---

# Rule: Plan classifies risks against the six named types

**Scanner:** `scanners/plan-shape-scanner.py` — `PlanShapeScanner` (rule id `plan-risks-are-classified`)

The plan must classify context against the six ABD risk types — **value**, **technical**, **delivery**, **domain**, **integration**, **AI-model** — so strategy selection, run ordering, and checkpoint tightness have a basis.

## DO

- Tag at least one risk type in the plan text (e.g. under a `## Risks` or `## Context Assessment` heading, or per-run).
- If multiple risk types apply, list them all; it is common for an engagement to have two or three.
- Prefer the canonical spellings: `value`, `technical`, `delivery`, `domain`, `integration`, `AI-model` (case-insensitive; `ai model` / `ai-model` / `ai_model` all accepted).

## DON'T

- Use vague language like "lots of risk" or "this project is risky" without naming at least one type.
- Invent risk types that are not in the canonical six — if you need a new category, propose extending the planning skill.

## Example (wrong)

```markdown
## Risks
- There is significant risk in this engagement.
- The SSO part is tricky.
```

(No named risk types; "tricky" and "significant risk" are not classifications.)

## Example (correct)

```markdown
## Risks
- **Integration risk** — Acme SSO API has no public documentation.
- **AI-model risk** — proprietary Acme internals; the agent has no training coverage.
- **Domain risk** — billing rules tied to regulated jurisdictions.
```
