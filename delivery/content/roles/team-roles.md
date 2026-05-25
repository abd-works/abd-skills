# Team roles

Four **executor roles** run delivery slots. Four bootcamp **families** organize skill packages under `skills/`. **Family ≠ role** — the stage file names who executes each skill; that can differ from where the package lives.

**Bootcamp reference:** [Five Families × Five Stages](https://forge.abdworks.net/abd-ai-augmented-bootcamp/#/22/1)

| Family (skill package home) | Default role | Playbook |
| --- | --- | --- |
| **Story-driven delivery** | **Product Owner** | [product-owner.md](product-owner.md) |
| **Domain-driven design** | **Business Expert** | [business-expert.md](business-expert.md) |
| **User experience design** | **UX Designer** | [ux-designer.md](ux-designer.md) |
| **Architecture-centric engineering** (`architecture-centric-engineering/`) | **Engineer** | [engineer.md](engineer.md) |
| **Review (validate only)** | **Reviewer** | [delivery-team-reviewer/AGENT.md](../../agents/delivery-team-reviewer/AGENT.md) |

**Cross-family execution (common):**

| Skill | Package family | Executor role |
| --- | --- | --- |
| `abd-acceptance-test-driven-development` | Story-driven delivery | **Engineer** |
| `abd-object-model` | Domain-driven design | **Engineer** (Business Expert reviews) |

Assign **`team-role`** per slot from [stages/](../stages/) — not from package folder alone.

---

## Skills by executor role (all stages)

What each role **runs** in delivery slots. Package path shown when it differs from the default family.

### Product Owner

| Skill | Stage | Package | Notes |
| --- | --- | --- | --- |
| `abd-opportunity-generation` | Shaping | idea shaping | Optional |
| `abd-story-mapping` (**outline mode**) | Shaping | story-driven delivery | Epics and major flows |
| `abd-story-mapping` (**full mode**) | Discovery | story-driven delivery | Stories decomposed to testable units |
| `abd-thin-slicing` | Discovery | story-driven delivery | **Last** in discovery pass |
| `drawio-story-sync` | Discovery, Exploration | story-driven delivery | After thin-slicing; exploration diagrams |
| `abd-acceptance-criteria` | Exploration | story-driven delivery | After UL refresh |
| `abd-specification-by-example` | Specification | story-driven delivery | After CRC; outline tables use CRC concepts |

Stage detail: [shaping](../stages/shaping.md) · [discovery](../stages/discovery.md) · [exploration](../stages/exploration.md) · [specification](../stages/specification.md)

---

### Business Expert

| Skill | Stage | Package | Notes |
| --- | --- | --- | --- |
| `abd-module-partition` | Shaping | domain-driven design | Module boundaries |
| `abd-bounded-context-map` | Shaping | domain-driven design | When multiple modules |
| `abd-domain-terms` | Discovery | domain-driven design | Before full story map |
| `abd-ubiquitous-language` | Discovery | domain-driven design | Key abstractions |
| `drawio-domain-sync` | Discovery, Exploration | domain-driven design | Optional diagrams |
| `abd-ubiquitous-language` (refresh) | Exploration | domain-driven design | **Before** AC |
| `abd-class-responsibility-collaborator` | Specification | domain-driven design | **Before** spec-by-example |
| `abd-scenario-walkthrough` | Specification | domain-driven design | **After** spec-by-example |
| **`abd-object-model` review** | Engineering | domain-driven design | Checkpoint only — Engineer produces |

Stage detail: [shaping](../stages/shaping.md) · [discovery](../stages/discovery.md) · [exploration](../stages/exploration.md) · [specification](../stages/specification.md) · [engineering](../stages/engineering.md)

---

### UX Designer

| Skill | Stage | Package | Notes |
| --- | --- | --- | --- |
| `abd-impact-mapping` | Shaping | user experience design | Optional |
| `abd-information-architecture` | Discovery | user experience design | Screen inventory, navigation |
| `abd-ux-mockup` | Exploration | user experience design | Lo-fi after IA and AC |
| `abd-interface-design` | Specification | user experience design | **Spec pass** — `interface-design.md` |
| `abd-interface-design` | Engineering | user experience design | **Implementation pass** — runnable UI |

Stage detail: [shaping](../stages/shaping.md) · [discovery](../stages/discovery.md) · [exploration](../stages/exploration.md) · [specification](../stages/specification.md) · [engineering](../stages/engineering.md)

---

### Engineer

| Skill | Stage | Package | Notes |
| --- | --- | --- | --- |
| `abd-architecture-outline` | Shaping | architecture-centric engineering | System context, layering |
| `abd-architecture-blueprint` | Discovery | architecture-centric engineering | Components, mechanisms |
| `abd-service-level-objectives` | Discovery | architecture-centric engineering | NFR/SLO targets |
| `abd-architecture-template` | Exploration | architecture-centric engineering | Mechanism patterns |
| `abd-architecture-reference` | Specification | architecture-centric engineering | Deep reference for code and tests |
| `abd-interface-design` | — | user experience design | **Not Engineer** — UX Designer (implementation pass) |
| `abd-object-model` | Engineering | domain-driven design | Typed domain surface; BE reviews |
| `abd-acceptance-test-driven-development` | Engineering | **story-driven delivery** | Failing tests from scenarios — RED before clean code |
| `abd-clean-code` | Engineering | architecture-centric engineering | Production code to pass tests |
| `mern-technical-architecture`, `hero-vtt-technical-architecture`, … | Engineering | architecture-centric engineering | Stack skill paired with ATDD and clean code |

**Engineering pass order:** `abd-interface-design` impl (UX) → object model → ATDD → clean code (+ stack). Engineer runs steps 2–4.

Stage detail: [engineering](../stages/engineering.md)

---

### Reviewer — validate only

| When | Scope |
| --- | --- |
| After every executor slot | Prior executor artifacts only — run scanners, check stage exit-gate items scoped to that skill; **no new artifacts** |

---

## Default skill order per stage (all roles)

| Stage | Order |
| --- | --- |
| **Shaping** | module partition → context map → story map (outline) → opportunity (opt) → impact map (opt) → architecture outline |
| **Discovery** | domain terms → UL → domain diagram (opt) → story map (full) → IA → blueprint → SLOs (opt) → thin slicing → story diagram |
| **Exploration** | UL refresh → domain diagram (opt) → AC → story diagram (opt) → UX mockup → architecture template |
| **Specification** | CRC → spec-by-example → walkthrough → interface design (spec pass) → architecture reference |
| **Engineering** | interface design (impl, UX) → object model (Engineer) → ATDD (Engineer) → clean code + stack (Engineer) |

Stage index: [stages/README.md](../stages/README.md)

## Common pipeline

All roles use **`story-graph-ops`**, **`execute-skill-using-skills-rules`**, and **`track_task`** when the deliverable touches `story-graph.json`.
