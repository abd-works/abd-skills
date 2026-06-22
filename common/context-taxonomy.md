# Context Taxonomy

Definitions of the two dimensions the delivery model operates on: **context perspective** (which lens) and **context fidelity** (how deep).

---

## Context perspectives

Each perspective is a different window on the same fact. A single business reality — "an Account has many Customers" — appears as a domain model relationship, a story ("Add Account to Customer"), a UX surface ("Browse Account List on Customer Page"), and an architecture decision ("Customer Service is the source of all Customer and Account info"). The perspectives don't duplicate facts — they view the same fact through different lenses.

**You must read every perspective file** listed below before starting a session. You cannot assess what exists or what's missing without understanding what each perspective articulates.

| Perspective | Key | Definition |
|---|---|---|
| **Domain** | `domain` | [domain-perspective.md](../../../practices/domain-driven-design/reference/domain-perspective.md) |
| **Stories** | `stories` | [stories-perspective.md](../../../practices/story-driven-delivery/reference/stories-perspective.md) |
| **User Experience** | `ux` | [ux-perspective.md](../../../practices/user-experience-design/reference/ux-perspective.md) |
| **Architecture** | `architecture` | [architecture-perspective.md](../../../practices/architecture-centric-engineering/reference/architecture-perspective.md) |
| **Stage** | `stage` | Cross-cutting concerns that belong to a fidelity level but aren't owned by a single perspective (e.g., code research, clean code, secure code). |

### Default perspective order

**domain → stories → ux → architecture**

This is the default, not a constraint. Route based on what the interview reveals (see `common/grill-me-with-practice-skill.md`).

---

## Context fidelity

Each fidelity level represents a scope and depth of work. Earlier levels are wider and shallower; later levels are narrower and deeper.

**You must read the stage definition for the fidelity level you are working at.** Each definition lists the practice skills, entry/exit conditions, expected outputs, and handoff to the next level.

| Fidelity | Key | Scope | Depth | What it produces | Definition |
|---|---|---|---|---|---|
| **Shaping** | `shaping` | Whole solution | Wide / shallow | Outcomes, scope, boundaries — the full solution view | [stages/shaping.md](common/stages/shaping.md) |
| **Discovery** | `discovery` | Whole solution | Medium | Interactions, experience, structure — complete product definition | [stages/discovery.md](common/stages/discovery.md) |
| **Exploration** | `exploration` | Increment | Medium | Solution tests, business logic, user experience, tech design for a slice | [stages/exploration.md](common/stages/exploration.md) |
| **Specification** | `specification` | Sprint | Narrow / deeper | Behaviour, design, logic — typed models, concrete scenarios, hi-fi prototypes | [stages/specification.md](common/stages/specification.md) |
| **Engineering** | `engineering` | Story | Narrowest / deep | Tests, code, interface — working software | [stages/engineering.md](common/stages/engineering.md) |

### Never skip specification

A piece of work always passes through specification. Earlier fidelity levels can be skipped (with the user's explicit permission) when existing context is sufficient, but specification is where context becomes executable.

### Size heuristics (guidance, not rules)

- **Massive** — new business line, core system replacement → shaping
- **Large** — new product, new application → discovery
- **Medium** — new feature in existing product → exploration
- **Small** — change to existing feature, fix, tweak → specification

These are starting intuitions the grill refines — not gates.

---

## Front matter schema

Every practice skill declares its position in the taxonomy via YAML front matter.

### Practice skills

```yaml
context-perspective: domain          # one of: domain, stories, ux, architecture
context-fidelity:
  - level: shaping                   # one of: shaping, discovery, exploration, specification, engineering
    mode: glossary                   # skill-specific label for what it does at this level
  - level: discovery
    mode: language
```

### Stage skills

```yaml
context-perspective: stage
context-fidelity:
  - level: engineering
    mode: quality-gate
```

### Field definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `context-perspective` | string | yes | Which lens this skill looks through. One of `domain`, `stories`, `ux`, `architecture`, `stage`. |
| `context-fidelity` | array of objects | yes | Which fidelity levels this skill operates at. |
| `context-fidelity[].level` | string | yes | The fidelity level. One of `shaping`, `discovery`, `exploration`, `specification`, `engineering`. |
| `context-fidelity[].mode` | string | yes | A short label describing what the skill does at this fidelity level. Skill-specific — not from a fixed list. |
