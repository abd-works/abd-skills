# Decision Record (DR)

> **Universal across all practices.** Any skill — architecture, domain, story, UX — can write a DR when a decision meets the criteria below. DRs are not limited to architecture. The ADR concept is an instance of this pattern.

---

## What gets a DR

Write a DR when **both** of the following are true:

1. **It is a real decision** — a choice between at least two alternatives, not an observation of fact.
2. **It is major** — it meets at least one of:
   - You had to ask the user to resolve it (they could not be assumed from context)
   - It establishes a model, boundary, or constraint that other decisions will depend on
   - Getting it wrong would require significant rework to undo
   - It deviates from an obvious default or a previously stated principle

**Examples — write a DR:**
- "Should we model the domain concept as `Account` or as `Onboarding`?" — needed user input, shapes the domain model.
- "Should the onboarding aggregate track `sessionState` directly or delegate to a `ProgressTracker`?" — architectural coupling decision.
- "Should we use optimistic UI or wait for server confirmation on voucher redemption?" — UX/reliability trade-off with rework cost.
- "Live with the pattern deviation in `catalog.service.ts` or plan a refactor?" — explicit architectural choice.

**Examples — do NOT write a DR:**
- "Does a customer have an account?" — a fact, not a decision.
- "Should we use a `const` or `let` here?" — trivial, no significant rework risk.
- "Should the filename be `catalog.service.ts` or `catalogService.ts`?" — style convention, not an architectural decision.
- "Should we add a comment to this function?" — not a decision about the system.

---

## DR folder convention

DRs live in a `dr/` subfolder within the relevant context. Common locations:

| Context | DR folder |
|---|---|
| Architecture decisions | `docs/architecture/decisions/` |
| Domain decisions | `docs/domain/decisions/` |
| Story / delivery decisions | `docs/stories/decisions/` |
| Session / delivery decisions | `docs/sessions/<session>/decisions/` |
| Project-wide | `docs/decisions/` |

**Numbering:** Each DR is numbered sequentially within its folder. Find the highest existing number and increment. Numbers do not reset per folder — if `decisions/` already has DR-001 through DR-010, the next DR is DR-011 regardless of context.

**File naming:** `DR-{NNN}-{short-slug}.md` — e.g. `DR-011-account-vs-onboarding-model.md`.

---

## DR template

```markdown
# DR-{NNN}: {the decision in five words or fewer}

> **Status:** Proposed | Accepted | Superseded by DR-NNN | Deprecated
> **Date:** YYYY-MM-DD
> **Practice context:** {Architecture | Domain | Story | UX | Delivery | Cross-cutting}
> **Deciders:** {names or roles — who made the call}
> **Trigger:** {User input required | Critical constraint | Deviation from default | Violation deferral}

## Context

{One to three paragraphs. What situation prompted this decision? What alternatives were visible? What constraints or forces shaped the choice? Write so a future reader who was not present understands why the decision was necessary.}

## Decision

We will {chosen option in plain language}. {One additional sentence on the specific scope or condition.}

## Options considered

| Option | Pros | Cons | Why rejected (or chosen) |
|---|---|---|---|
| **{Option A — chosen}** | … | … | **Chosen because** … |
| Option B | … | … | Rejected because … |

## Consequences

**Positive:** {What this enables or simplifies.}

**Negative / trade-offs:** {What this constrains or complicates.}

## Trigger for revisit

{A specific event, milestone, or condition that would cause this decision to be re-evaluated. Not "when we have time."}

## Compliance / verification

{How will the team know this decision is being followed? If there is no automated check, say so explicitly.}
```

---

## DRs vs notes vs observations

| When | Use |
|---|---|
| Real decision, major | Write a DR |
| Observation, risk, or concern — not yet a decision | Note it in the document as a `> **Note:**` blockquote |
| Violation of current-state architecture | Follow `../common/record-all-architecture-violations.md` which produces a Violation DR |
| Accepted standard (no real alternative considered) | Skip — no DR needed |

---

## Referencing DRs from other documents

When a document references a DR, use inline notation: `(→ DR-NNN)` after the relevant statement. Example:

```markdown
The domain aggregate is `Account`, not `Onboarding` (→ DR-003).
```

This lets a reader find the record without leaving the current document.
