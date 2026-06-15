# Strategy: New Initiative — Proprietary Technology Risk

**When to use:** Heavy proprietary APIs, internal systems, or custom protocols with little public documentation; high AI-model risk. Greenfield or brownfield.

**Typical scope:** Riskiest thin slices first; prove each slice before moving on.

**Related:** `new-initiative-no-documented-architecture.md` (greenfield without tech risk). `brownfield-current-state.md` (when the proprietary system is the one being mapped).

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
| Shaping (all) → Discovery (increment) | Order increments by integration risk: proprietary surfaces first. |
| Exploration (increment) → Specification (sprint) | First increment: 1-2 stories only (prove integration). Then 3-4 per sprint. |

### Increment ordering (risk-first)

1. **Riskiest integration** — stories touching most-undocumented APIs
2. **Second integration** — next proprietary surface
3. **Remaining** — by value once integrations proven

---

## JIT policy

- Scatter increments after shaping (need risk ordering)
- **Scatter only current increment into sprints** — do not look ahead until integration proven
- After first increment proves integration: scatter next 2 increments

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per skill | All stages for first increment (high model risk) |
| Per story | First integration slice end-to-end |
| Per sprint | After first increment proves: remaining at sprint level |

**Tighten aggressively** — proprietary APIs cause hallucination. Every skill gets checked until confidence builds.

---

## Key constraints

- Prove proprietary integration before breadth.
- Accept per-skill checkpoint overhead for first increment — speed comes after trust.
- Document API quirks and undocumented behaviors in corrections log.
- If integration is impossible (API doesn't do what brief assumes), escalate immediately.

---

## AI error rate adjustment

- Start at per-skill (expect high error rate with proprietary surfaces)
- If first increment passes cleanly: expand to per-sprint for subsequent increments
- If errors persist: shrink to per-story scope and add spike strategy for the integration
