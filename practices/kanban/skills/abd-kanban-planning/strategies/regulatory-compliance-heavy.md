# Strategy: Regulatory / Compliance-Heavy

**When to use:** Regulation, legal, or compliance dominates risk (finance, health, privacy, government programs).

**Typical scope:** Full product, tightest scrutiny on regulated stories.

**Related:** `new-initiative-business-user-experience-risk.md` (when domain risk is operational, not regulatory).

---

## System of work

| Stage | Scope | Skills (ordered) |
| --- | --- | --- |
| Shaping | all | story-mapping (tag compliance surface), thin-slicing |
| Discovery | increment | domain-terms, architecture-blueprint |
| Exploration | increment | ubiquitous-language, acceptance-criteria (regulatory values, not placeholders), architecture-template |
| Specification | sprint | CRC, spec-by-example (real regulatory values) |
| Engineering | sprint | object-model (BE), ATDD (PO, tests = proof bundle), clean-code (EN) |

---

## Scatter rules

| Transition | Rule |
| --- | --- |
| Shaping (all) → Discovery (increment) | Order increments by compliance risk: regulated surfaces first. |
| Exploration (increment) → Specification (sprint) | Compliance-heavy stories first, 2-3 per sprint (tighter than default). |

### Increment ordering (compliance-first)

1. **Highest regulatory risk** — stories touching regulated data, audit, retention
2. **Supporting infrastructure** — reporting, logging, compliance tooling
3. **Remaining** — by value once compliance proven

---

## JIT policy

- Scatter all increments after shaping (compliance surface must be visible)
- Scatter sprints tighter (2-3 stories) for compliance increments
- Non-compliance increments can use default 3-4 stories per sprint

---

## Checkpoint policy

| Level | When |
| --- | --- |
| Per AC | Exploration for compliance stories (user validates regulatory accuracy) |
| Per scenario | Specification (real values, not placeholders) |
| Per test | Engineering (tests are the proof bundle) |
| Per sprint | Non-compliance stories after compliance proven |

**Always tight for compliance.** Regulatory accuracy > delivery speed.

---

## Key constraints

- Wrong AC = wrong system in regulated domains.
- Real regulatory values in scenarios (not "X" or "TBD") — concrete rules, thresholds, retention periods.
- Tests are the compliance proof bundle — not documentation, not comments.
- Non-compliance stories get faster treatment after compliance stories prove.
- Audit trail and data retention are first-class stories, not afterthoughts.

---

## AI error rate adjustment

- Compliance stories always at per-AC/per-scenario checkpoints (no relaxation)
- Non-compliance stories: per-sprint after compliance increment passes
- If regulatory errors detected: per-story with domain expert validation
