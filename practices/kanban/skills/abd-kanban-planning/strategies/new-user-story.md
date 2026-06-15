# Strategy: New User Story

**When to use:** A small change on an existing solution — new feature, enhancement, or capability within the current architecture. Map, slices, and domain model already exist.

**Typical scope:** 1–3 stories in one backlog increment (or micro-increment).

**Related:** `new-thin-slice.md` (larger scope). `bug-fix.md` (defect, not new capability).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Exploration | story | UL-refresh, acceptance-criteria |
| Specification | story | CRC, spec-by-example, scenario-walkthrough |
| Engineering | story | object-model, ATDD, clean-code |

**No shaping or discovery.** Map, slices, and domain model already exist. Jump directly to exploration at story scope.

---

## Scatter rules

No scatter needed — tickets start and stay at story scope. One ticket per story.

---

## JIT policy

- All stories enter backlog immediately (small total scope)
- No decomposition needed

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per skill | Each story through the full pipeline |
| Per story | Cross-role after each story completes engineering |

---

## Key constraints

- Read the story graph and corrections log first; stay consistent with domain language.
- Surface prior corrections to anyone touching the story.
- If the map itself must be restructured, switch strategy (`new-thin-slice` or `new-initiative-*`).
