# `docs/` — long-lived documentation

Put **durable** reference material here: pipeline analysis, architecture rationale, operator guides—content that should remain useful after the v2 build is “done.”

**Contrast:** `plan/` holds **working** plans you may **discard** after milestones; `docs/` is what you expect the next maintainer (or you in six months) to read.

## Contents

| Document | Purpose |
| -------- | ------- |
| [`why-story-mapping-first.md`](why-story-mapping-first.md) | **Why** story mapping (behavior) comes before sparse domain types—user context and AI steer; complements Phase 3 in `plan/PROCESS-PLAN.md`. |
| [`modeling_kind_sidecar_v1.md`](modeling_kind_sidecar_v1.md) | **`modeling_kind` sidecar** (v1 payload, **v2** body TOC heuristics) — promotion gate helper; golden regression + JSON Schema under `docs/schemas/`. |
| [`orchestrator.md`](orchestrator.md) | **Autonomous loop** — planner / runner / MM3 domain critic; `scripts/orchestrator_loop.py` (10–20 runs, optional `ORCHESTRATOR_AGENT_URL`). |
