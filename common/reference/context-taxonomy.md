# Context Taxonomy

Every practice skill sits at the intersection of two dimensions: a **context perspective** (which lens the skill looks through) and a **context fidelity** (how granular / deep the skill works). Together these two axes locate every skill in the taxonomy and determine what context it reads, what it produces, and where its output feeds next.

---

## Context perspectives
Every practice skill frames context through exactly one perspective. Each perspective provides a different window on the same context. A single business reality — "an Account has many Customers" — appears as a domain model relationship, a story ("Add Account to Customer"), a UX surface ("Browse Account List on Customer Page"), and an architecture decision ("Customer Service is the source of all Customer and Account info"). The perspectives don't duplicate facts — they view the same facts within a context through different lenses. A skill's `context-perspective` front-matter field declares which window it looks through, and that declaration determines what upstream context the skill consumes and what downstream skills can use its output.

**You must read every perspective file** listed below before starting a session. You cannot assess what exists or what's missing without understanding what each perspective articulates. Each perspective file also lists the practice skills that belong to it, so reading them tells you both the lens and the toolbox available.

| Perspective | Key | Definition |
|---|---|---|
| **Domain** | `domain` | [domain-perspective.md](../../../practices/domain-driven-design/reference/domain-perspective.md) |
| **Stories** | `stories` | [stories-perspective.md](../../../practices/story-driven-delivery/reference/stories-perspective.md) |
| **User Experience** | `ux` | [ux-perspective.md](../../../practices/user-experience-design/reference/ux-perspective.md) |
| **Architecture** | `architecture` | [architecture-perspective.md](../../../practices/architecture-centric-engineering/reference/architecture-perspective.md) |
| **Stage** | `stage` | Cross-cutting concerns that belong to a fidelity level but aren't owned by a single perspective. Stage skills (e.g., code research, clean code, secure code) serve any perspective — they provide quality gates or utilities rather than a domain/story/UX/architecture view. |

### Default perspective order

**domain → stories → ux → architecture**

This is the default, not a constraint. The grill interview (see `common/reference/grill-me-with-practice-skill.md`) determines which perspective — and therefore which practice skill — to run first. When context is already rich in one perspective, the next skill in sequence can start from that output instead of beginning from scratch.

---

## Context fidelity

Each fidelity level represents a scope and depth of work. Earlier levels are wider and shallower; later levels are narrower and deeper. A practice skill's `context-fidelity` front-matter array declares which levels it can operate at and what mode it runs in at each level — the same skill may behave differently at discovery than at specification.

**You must read the stage definition for the fidelity level you are working at.** Each definition lists the practice skills available at that level, entry/exit conditions, expected outputs, and handoff to the next level. The stage definition is how you know which skills to offer and in what order.

| Fidelity | Key | Scope | Depth | What it produces | Definition |
|---|---|---|---|---|---|
| **Context** | `context` | All sources | Unstructured | Indexed, searchable workspace memory — raw material before generation | [stages/context.md](./stages/context.md) |
| **Shaping** | `shaping` | Whole solution | Wide / shallow | Outcomes, scope, boundaries — the full solution view | [stages/shaping.md](./stages/shaping.md) |
| **Discovery** | `discovery` | Whole solution | Medium | Interactions, experience, structure — complete product definition | [stages/discovery.md](./stages/discovery.md) |
| **Exploration** | `exploration` | Increment | Medium | Solution tests, business logic, user experience, tech design for a slice | [stages/exploration.md](./stages/exploration.md) |
| **Specification** | `specification` | Sprint | Narrow / deeper | Behaviour, design, logic — typed models, concrete scenarios, hi-fi prototypes | [stages/specification.md](./stages/specification.md) |
| **Engineering** | `engineering` | Story | Narrowest / deep | Tests, code, interface — working software | [stages/engineering.md](./stages/engineering.md) |

### Never skip specification

A piece of work always passes through specification. Earlier fidelity levels can be skipped (with the user's explicit permission) when existing context is sufficient, but specification is where context becomes executable. In practice this means at least one specification-level skill per perspective must run before any engineering-level skill can start — specification skills produce the typed, scenario-level context that engineering skills consume.

### Size heuristics (guidance, not rules)

- **Massive** — new business line, core system replacement → shaping
- **Large** — new product, new application → discovery
- **Medium** — new feature in existing product → exploration
- **Small** — change to existing feature, fix, tweak → specification

These are starting intuitions the grill refines — not gates. The heuristic tells you which fidelity level to enter at; the stage definition at that level tells you which practice skills are available and in what order to run them.

---

## Front matter schema

Every practice skill declares its position in the taxonomy via YAML front matter. This metadata is what lets tooling, stage definitions, and other skills discover where a skill sits — which perspective it belongs to and at which fidelity levels it operates.

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
| `context-fidelity[].level` | string | yes | The fidelity level. One of `context`, `shaping`, `discovery`, `exploration`, `specification`, `engineering`. |
| `context-fidelity[].mode` | string | yes | A short label describing what the skill does at this fidelity level. Skill-specific — not from a fixed list. |
