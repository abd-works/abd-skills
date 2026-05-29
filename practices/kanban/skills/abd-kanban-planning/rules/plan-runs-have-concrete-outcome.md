---
scanner: plan-shape
---

# Rule: Each run's rationale names a concrete outcome, not only a risk

**Scanner:** `scanners/plan-shape-scanner.py` — `PlanShapeScanner` (rule id `plan-runs-have-concrete-outcome`)

A run's **Rationale** (or **Outcome** / **Why**) column must say what is **true**, **proven**, **delivered**, **mapped**, or **decided** when the run completes. Vague lines like "mitigate technical risk" without what done looks like are not enough.

When the work is constrained by a specific product, runtime, or external system (VTT, ERP, browser, engine, vendor API), the constraint is folded into the same rationale: name the constraint and what this run achieves **there**.

## DO

- Use a concrete verb (prove, map, mitigate X by Y, establish, deliver, wrap, contract, spike, validate, capture, decide, ship, surface, land, refine, define, integrate, test, cover, drain, close).
- Name the thing proven / delivered / mapped — not just a risk category.
- When the run is a learning run (spike, first vertical), say so plainly.

## DON'T

- Leave the rationale blank.
- Write rationales that are only the six risk words with connectors ("mitigate technical risk", "address integration risk").
- Substitute "deliver business value" as the rationale for an early run whose real job is learning a host system.

## Example (wrong)

| Run | Stages | Scope | Checkpoint Policy | Rationale |
| --- | --- | --- | --- | --- |
| 1 | Discovery | SSO surface | Per-story | Mitigate technical risk |
| 2 | Exploration → Engineering | Thin slice 1 | Per-AC | Reduce integration risk |

(Both rationales are risk-only; neither says what is proven or delivered.)

## Example (correct)

| Run | Stages | Scope | Checkpoint Policy | Rationale |
| --- | --- | --- | --- | --- |
| 1 | Discovery | SSO + billing surface | Per-story | Map proprietary integration surface; capture unknowns before any implementation |
| 2 | Exploration → Engineering | Thin slice 1: one SSO story end-to-end | Per-AC / per-test | Prove specification → engineering against Acme SSO; land contract tests for undocumented endpoints |
