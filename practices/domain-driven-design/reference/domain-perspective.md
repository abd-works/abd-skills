# Domain Perspective

**Key:** `domain`

**What it answers:** What are the concepts, rules, and structure behind the business that the system must enforce?

**Agent:** [Business Expert](../../../practices/kanban/agents/business-expert/AGENT.md)

**Skills by fidelity:**

| Fidelity | Skill | Mode |
|---|---|---|
| Shaping | `abd-domain-glossary` | glossary |
| Discovery | `abd-domain-language` | language |
| Exploration | `abd-domain-model` | conceptual-model |
| Specification | `abd-domain-specification` | typed-model |
| Engineering | `abd-domain-code` | domain-tdd |

**Supporting:** `abd-bounded-context-map`, `abd-ddd-design-building-blocks`, `abd-domain-walk`, `drawio-domain-sync` (tooling — not thin-router migrated).

---

## Shared reference (practice level)

| File | Role |
| --- | --- |
| [`oo-concepts.md`](./oo-concepts.md) | OO fundamentals — read before language, model, specification |
| [`diagram-workflow.md`](./diagram-workflow.md) | Shared `drawio_domain_cli.py` for model and specification diagrams |
| [`validate-checklist.md`](./validate-checklist.md) | Cross-skill validate items |
| [`source-traceability.md`](./source-traceability.md) | Source reference format and coverage rules (glossary, language) |

---

## Per skill (skill level)

| File | Role |
| --- | --- |
| `reference/input-traps.md` | Pre-flight ambiguity checks — every run, not grill |
| `reference/grill-me.md` | Grill interview questions — grill mode only |
| `reference/generate.md` | Orchestration — fidelity branching, pipelines, quality bars |
| `reference/diagram-workflow.md` | Mode + output path — model, specification |
| `reference/output.md` | Non-default output path — glossary (per-module split) |

**SKILL.md index sections:** Bootstrap, Read, Input traps, Grill me, Generate, Validate — plus Diagram workflow / Output when those `reference/` files exist. Bootstrap via [`common/reference/skill-workflow.md`](../../../common/reference/skill-workflow.md) § Bootstrap. Validate links [`common/reference/rule-checklist.md`](../../../common/reference/rule-checklist.md) (practice items in [`validate-checklist.md`](./validate-checklist.md)).
