# Strategy: New Initiative — No Documented Architecture

**When to use:** Greenfield or near-greenfield: no map, no settled architecture. Briefs, interviews, competitors, rough requirements — discover what to build and how.

**Typical scope:** Full product or major area; many stories, many epics.

**Related:** `new-initiative-proprietary-technology-risk.md` (when undocumented APIs dominate). `new-initiative-business-user-experience-risk.md` (when UX/domain risk dominates).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Shaping | all | story-mapping, thin-slicing |
| Discovery | increment | domain-terms, architecture-blueprint, information-architecture |
| Exploration | increment | ubiquitous-language, acceptance-criteria, ux-mockup, architecture-template |
| Specification | sprint | CRC, spec-by-example, interface-design, architecture-reference |
| Engineering | sprint | interface-design, object-model, ATDD, clean-code |

---

## Scatter rules

| Transition | Rule |
| --- | --- |
| Shaping (all) → Discovery (increment) | Thin-slicing produces increments. Order by concern: spine first, then cross-cutting (security, data, ops). |
| Exploration (increment) → Specification (sprint) | First increment: 1 story only (spine proof). Subsequent: 3-4 stories per sprint. |

### Increment ordering (architecture-first)

1. **Spine slice** — simplest E2E flow through all layers (authenticate → core action → persist → observe)
2. **First cross-cutting** — security/authN on top of spine
3. **Next cross-cutting** — retention, versioning, etc.
4. **Remaining** — by business value

---

## JIT policy

- Scatter all increments after shaping (need to see the full landscape)
- Scatter sprints JIT — only current increment's sprints
- After spine slice proves architecture, expand sprint grouping for remaining increments

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per epic | During discovery (confirm vocabulary and actors per epic) |
| Per story | Spine slice through all stages (prove stack and architecture) |
| Per sprint | After spine proves: remaining work at sprint level |
| Per increment | Cross-cutting review after each new concern completes |

---

## Key constraints

- Architecture emerges slice by slice — do not attempt big-upfront design.
- Spine proves the stack; cross-cutting layers non-functionals on proven backbone.
- Vocabulary and actors confirmed per-epic in discovery.
- If corrections from spine affect later increments, revise before proceeding.

---

## AI error rate adjustment

- Spine slice at per-skill checkpoints (architecture decisions are critical)
- If output clean after spine: expand to per-sprint for cross-cutting concerns
- If errors > 10% on architecture: add architecture-template as mandatory in exploration
