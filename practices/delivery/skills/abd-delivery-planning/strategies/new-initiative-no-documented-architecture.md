# Strategy: New Initiative — No Documented Architecture

**When to use:** Greenfield or near-greenfield: no map, no settled architecture. Briefs, interviews, competitors, rough requirements — discover what to build and how.

**Typical scope:** Full product or major area; many stories, many epics.


| Step | Stage | Intent | Scope | Checkpoint policy | Rationale |
| ---- | ----- | ------ | ----- | ----------------- | --------- |
| 1 | Shaping → Discovery | **Map the whole surface** and **thin-slice last** by major concern: E2E flow, security, data lifecycle, ops, integrations | Full product surface | **Per epic**: confirm **vocabulary and actors** before continuing | Landscape before deep build |
| 2 | Exploration → Specification → Engineering | **Spine slice:** simplest flow through all layers (e.g. authenticate → one core action → persist → observe) | Spine stories only | Per-story; cross-role per story | Proves stack and architecture |
| 3 | Exploration → Specification → Engineering | **First cross-cutting concern** (e.g. security: authN/Z, audit) on top of the spine | That concern’s stories | Per-story; compare corrections to prior row | Layer non-functionals on a proven backbone |
| 4 | Exploration → Specification → Engineering | **Next cross-cutting concern** (e.g. retention, versioning) | That concern’s stories | Per-story; cross-run review | Architecture emerges incrementally |
| 5+ | Exploration → Specification → Engineering | **Remaining backlog** by business value | Remaining stories | Per-slice; per-story only for new integration risk | Faster once model and architecture are stable |


**Key constraints:**

- Do not skip row 1 — shaping + discovery forces unknowns visible.
- Spine stays minimal — do not overload the first E2E slice.
- Expect the first map to be wrong in places; revise the plan as you learn.
