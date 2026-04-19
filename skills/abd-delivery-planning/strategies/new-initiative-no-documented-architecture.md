# Strategy: New Initiative — No Documented Architecture

**When to use:** Greenfield or near-greenfield: no map, no settled architecture. Briefs, interviews, competitors, rough requirements — discover what to build and how.

**Typical scope:** Full product or major area; many stories, many epics.


| Step | Stage                      | Intent                                                                                                                  | Scope                  | Checkpoint policy                                                                          | Rationale                                                      |
| ---- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| 1    | Discovery → Prioritization | **Map the whole surface** and slice by major concern: functional E2E flow, security, data lifecycle, ops, integrations. | Full product surface   | **Per epic** (or major area): stop and confirm **vocabulary and actors** before continuing | See the landscape before committing deep.                      |
| 2    | Exploration → Engineering  | **Spine slice:** simplest flow through all layers (e.g. authenticate → one core action → persist → observe).            | Spine stories only     | Per-story; cross-role per story                                                            | Proves stack and architecture; everything else builds on this. |
| 3    | Exploration → Engineering  | **First cross-cutting concern** (e.g. security: authN/Z, audit) on top of the spine.                                    | That concern’s stories | Per-story; compare corrections to prior row                                                | Layer non-functionals on a proven backbone.                    |
| 4    | Exploration → Engineering  | **Next cross-cutting concern** (e.g. retention, versioning).                                                            | That concern’s stories | Per-story; cross-run review                                                                | Architecture emerges; not big-design-up-front.                 |
| 5+   | Exploration → Engineering  | **Remaining backlog** by business value; cross-cutting work mostly done.                                                | Remaining stories      | Per-slice; per-story only for new integration risk                                         | Faster once model and architecture are stable.                 |


**Key constraints:**

- Do not skip row 1 — mapping forces unknowns visible.
- Spine stays minimal — do not overload the first E2E slice.
- Expect the first map to be wrong in places; revise the plan as you learn.
