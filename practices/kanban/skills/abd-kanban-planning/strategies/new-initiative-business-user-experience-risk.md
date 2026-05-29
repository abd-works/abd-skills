# Strategy: New Initiative — Business / User Experience Risk

**When to use:** The main uncertainty is whether the **product is right** for people and operations — not primarily whether the tech integrates. Signals: new user experience, unclear domain language, risky operational flows, data that must be correct in meaning.

**Typical scope:** Riskiest thin slices first; prove experience, domain, operations, and data correctness.

**Related:** `new-initiative-proprietary-technology-risk.md` (tech risk dominant). `new-initiative-no-documented-architecture.md` (architecture risk dominant).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Shaping | all | story-mapping, thin-slicing |
| Discovery | increment | domain-terms, UL, architecture-blueprint, information-architecture |
| Exploration | increment | UL-refresh, acceptance-criteria, ux-mockup, architecture-template |
| Specification | sprint | CRC, spec-by-example, scenario-walkthrough, interface-design, architecture-reference |
| Engineering | sprint | interface-design, object-model, ATDD, clean-code |

---

## Scatter rules

| Transition | Rule |
| --- | --- |
| Shaping (all) → Discovery (increment) | Order increments by UX/domain risk: most-unclear user journeys first. |
| Exploration (increment) → Specification (sprint) | First increment: 1-2 stories (prove domain + UX). Then 3-4 per sprint. |

### Increment ordering (UX/domain-first)

1. **Highest UX uncertainty** — user journeys with most unclear flows
2. **Highest domain uncertainty** — business rules with ambiguous terms
3. **Remaining** — by value once domain language is stable

---

## JIT policy

- Scatter increments after shaping
- Scatter sprints JIT — only current increment
- After first increment validates domain: scatter broader (2 increments ahead)
- **Outcome assessment** after first increment completes engineering: is the product right?

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per skill | Exploration (UL, AC, mockup — domain correctness is critical) |
| Per story | First increment through spec + engineering |
| Per increment | Outcome assessment after first increment ships |
| Per sprint | After domain stabilizes: remaining work |

---

## Key constraints

- UX and domain language correctness outweigh technical elegance.
- User validates domain terms and AC meaning, not just format.
- If the domain model is wrong after first increment, revisit discovery before continuing.
- Outcome assessment runs after engineering (not mid-pipeline).

---

## AI error rate adjustment

- Domain terms and AC are the highest-risk outputs: per-skill checkpoints mandatory
- If domain corrections accumulate (>3 in first increment): shrink scope to per-story
- If domain is stable after first increment: expand to per-sprint for remaining
