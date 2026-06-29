# Architecture Perspective

**Key:** `architecture`

**What it answers:** What is the technology that will implement the solution? Platform, layers, components, cross-cutting concerns, and the principles that govern how code is built.

**Agent:** [Engineer](../../../practices/kanban/agents/engineer/AGENT.md)

**Skills by fidelity:**

| Fidelity | Skill | Mode |
|---|---|---|
| Shaping | `abd-architecture-outline` | system-context |
| Discovery | `abd-architecture-blueprint` | blueprint |
| Exploration | `abd-architecture-specification` | document |
| Specification | `abd-architecture-specification` | template |
| Engineering | `abd-architecture-code` | production-code |

---

## Shared reference (practice level)

| File | Role |
| --- | --- |
| [`validate-checklist.md`](./validate-checklist.md) | Cross-skill validate items |
| [`diagram-workflow.md`](./diagram-workflow.md) | Shared `arch-drawio.ps1` init/export/verify |
| [`architecture-mechanism.md`](./architecture-mechanism.md) | Mechanism definitions (existing) |
| [`common/reference/record-all-architecture-violations.md`](../../../common/reference/record-all-architecture-violations.md) | Violation workflow for existing systems |

---

## Per skill (skill level)

| File | Role |
| --- | --- |
| `reference/input-traps.md` | Pre-flight ambiguity checks — every run, not grill |
| `reference/grill-me.md` | Grill interview questions — grill mode only |
| `reference/generate.md` | Orchestration — element inventory, mechanisms, violations |
| `reference/diagram-workflow.md` | Skill-specific diagram set and verify steps |
| `reference/concepts.md` | Teaching reference (existing on most skills) |

**SKILL.md index sections:** Bootstrap, Read, Input traps, Grill me, Generate, Validate — plus Diagram workflow when applicable. Validate links [`common/reference/rule-checklist.md`](../../../common/reference/rule-checklist.md) (practice items in [`validate-checklist.md`](./validate-checklist.md)).
