# Strategy: Bug Fix

**When to use:** A defect or regression — something that used to pass or should pass and does not. Often **test- and implementation-led**. Scope stays small until you widen it deliberately.

**Typical scope:** One story or a handful of AC after scope is cut to the **smallest honest repro scope**.

**Related:** `brownfield-current-state.md` (when the bug reveals unmapped behavior). `spike-proof-of-concept.md` (when you need to investigate before fixing).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Exploration | story | abd-story-acceptance-criteria (isolate defect surface) |
| Engineering | story | abd-story-acceptance-test, abd-clean-code |
| Exploration (reverse) | story | abd-story-acceptance-criteria (capture corrected intent), abd-story-specification (optional) |

**No shaping or discovery.** Bug fixes skip to the stage where the defect lives.

---

## Scatter rules

No scatter needed — single ticket at story scope throughout.

---

## JIT policy

- Single ticket, no decomposition
- If the bug exposes a wider gap, escalate to `brownfield-current-state` or `new-thin-slice`

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per skill | User confirms scope before engineering (Step 1 → Step 2 boundary) |
| Per skill | After tests pass (Step 2 complete) |
| Per skill | User reviews captured spec (Step 3 complete) |

---

## Key constraints

- Touch the existing story graph; add/update the defect story; avoid map-wide refactors.
- Forward order (full AC before engineering) is optional when reverse engineering after the fix is faster and more honest.
- If the bug exposed missing written intent, capture it after the fix so the gap does not repeat.
- Scope the ticket to the **smallest reproducible surface** — do not widen until deliberately choosing to.

---

## AI error rate adjustment

Not typically relevant for single-story bug fixes. If the fix attempt fails, tighten scope further (sub-story level) rather than expanding.
