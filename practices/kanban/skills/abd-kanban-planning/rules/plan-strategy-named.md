---
scanner: plan-shape
---

# Rule: Plan names the selected strategy (or proposes a new one)

**Scanner:** `scanners/plan-shape-scanner.py` — `PlanShapeScanner` (rule id `plan-strategy-named`)

The plan must name the strategy (or strategies) selected from `skills/abd-kanban-planning/strategies/*.md`, OR explicitly mark itself as a custom strategy candidate with a proposed slug.

Naming the strategy locks in the run shape and makes the decision reviewable. If no pre-packaged strategy fits, the plan is still expected to say so rather than silently invent.

## DO

- Reference the strategy file(s) by filename (`new-initiative-proprietary-technology-risk.md`) or by canonical slug.
- When more than one strategy is blended, name each and say how they combine.
- When no strategy fits, include a section like `## Strategy: custom` with a proposed slug for later save under `strategies/`.

## DON'T

- Describe a strategy in prose without a name — reviewers cannot match it to the catalog.
- Copy a strategy's run table without citing the source file.

## Example (wrong)

```markdown
## Strategy
We will start by mapping the risky parts and then spec-test-code each slice.
```

(No file / slug cited; reviewer cannot tell which strategy.)

## Example (correct)

```markdown
## Strategy

Selected: `strategies/new-initiative-proprietary-technology-risk.md`
Blended with: `strategies/new-initiative-business-user-experience-risk.md` (for the second actor path).
```
