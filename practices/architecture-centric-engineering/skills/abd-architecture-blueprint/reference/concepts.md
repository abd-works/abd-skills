# Architecture Blueprint — Concepts

## What is an architecture blueprint?

An **architecture blueprint** is the *system-level reference* that sits between the one-page outline and the deep-dive mechanism reference. It adds three things the outline deliberately defers:

1. **Platform runtime and deployment topology** — the full platform diagram (client apps, backend services, data stores, CDN, third-party integrations) and the deployment diagram (environments, infrastructure nodes, container instances, OS image per node type, network relationships).
2. **Component-level descriptions** — each major system from the outline is decomposed into 2–4 named components (1–2 paragraphs each: purpose, dependencies, interactions with other components and with mechanisms).
3. **Deeper mechanism descriptions** — every mechanism from the outline is repeated here with the component interactions spelled out, the platform and deployment specifics that shape the mechanism, and the runtime behaviour described end-to-end.

The blueprint also carries the data architecture (entity/aggregate relationships and ownership boundaries), the common testing strategy, and blueprint-level decision records.

This skill ships **paired outputs**: a markdown file that humans read, and `.drawio` sources for each load-bearing diagram (`platform-architecture.drawio`, `deployment-architecture.drawio`, `component-overview.drawio`, `entity-relationships.drawio`). Inline mermaid is fine for small walkthrough-style figures inside a component or mechanism description, but the platform, deployment, component, and entity diagrams need editable drawio sources because they outlive any single contributor.

The blueprint **defers deep mechanism detail down**: code walkthroughs, multi-participant sequence diagrams, and full mechanism breakdowns live in the **architecture reference** (one file per mechanism).

---

## Platform architecture (new at this level)

The outline's system-context diagram shows what the system is and who uses it. The blueprint adds the **platform runtime view**: the actual client apps, backend services, data stores, CDN/edge layer, background workers, and third-party integrations, showing how they connect and what technology each runs on.

This is the document a new engineer opens to understand "what processes actually run and how do they talk to each other?" before drilling into any component.

| Outline level | Blueprint level |
|---|---|
| System context: "Retail Platform connects to Stripe over HTTPS/REST" | Platform: "Orders API (Node.js/Fastify in ECS) calls `stripe.paymentIntents.create()` via the Stripe SDK; response and webhook events both arrive at the Orders API" |

---

## Deployment topology (new at this level)

The blueprint also adds the **deployment diagram**: environments (Production, Staging, Preview), deployment nodes (cloud regions, VPCs, AZs, managed services), infrastructure nodes (load balancers, CDN, API gateway), and container instances (which service runs in which node at what replica count).

When more than one operating system image is in use (e.g. API containers on Alpine, GPU workers on Ubuntu), the deployment section names the OS per node type and explains the reason.

---

## Components vs systems

The outline catalogues **major systems** (one line each). The blueprint zooms in one level: each major system is described as a small set of **components** — the named building blocks the system is composed of. A component is a self-contained piece of code with one purpose and a stable interface.

| Outline level | Blueprint level | Reference level |
|---|---|---|
| "Orders system" (one line) | "OrderService, OrderRepository, OutboxPublisher" (paragraph each) | Full `OrderService` walkthrough with code, sequence diagrams, tests |

Each component description names the **mechanisms it participates in**: which resilience pattern wraps its external calls, which logging pattern it uses, which persistence helper it delegates to. This links the component picture to the mechanism picture.

---

## Architecture mechanisms — deeper than the outline

The outline states the mechanism technology choice and the NFR justification in 1–2 paragraphs. The blueprint repeats every mechanism but goes three levels deeper:

| Dimension | Outline | Blueprint |
|---|---|---|
| Technology choice | Named | Named + referenced to platform/deployment specifics |
| NFR justification | One sentence | Retained from outline |
| Component interactions | Not present | Named: which components call into the mechanism, what they pass, what they receive |
| Platform / deployment detail | Not present | How the mechanism is configured in the running platform — e.g. secrets store ARN, Redis TLS config, broker endpoint, OS-level sidecar |
| Runtime behaviour | Not present | Step-by-step description of the mechanism in steady state and under failure |

**The blueprint must not invent a new mechanism** not present in the outline. Mechanism technology choices and their ADRs belong to the outline. Blueprint ADRs cover: component boundaries, test-tier vocabulary, data ownership patterns, extension contracts.

---

## Data architecture

The blueprint shows the **data model** at the entity/aggregate level — names, relationships, ownership boundaries. It does **not** ship schemas, ORM mappings, or indexes. A reader of the data section should be able to draw the dependency graph between domain entities and identify which component owns each one.

---

## Testing architecture at this level

The outline says "tests exist"; the reference goes deep on testing one mechanism. The blueprint sits between: it names the **test tiers common to the whole system** (the tier vocabulary, the boundary between tiers, the test doubles common across tests).

---

## Decision records at this level

Blueprint-level decisions are choices visible at this level: component boundaries, test-tier vocabulary, data ownership patterns, extension seam contracts. Mechanism technology choices have their ADRs in the outline and are not re-recorded here.

---

## What the blueprint does NOT contain

**Lives in `abd-architecture-specification`:**
- Code-level walkthroughs of a mechanism
- Sequence diagrams that involve more than three participants
- Full data schemas / DDL / ORM mappings
- Test code examples per tier
- Per-component file structures

**Lives in `abd-architecture-outline`:**
- Layered architecture diagram
- System context diagram (functions + tech per system, protocols)
- Mechanisms catalogue (technology choice + NFR justification — the *what and why*)
- Guiding principles list
- Technology stack table
- Major systems catalogue (one-liners)
- Mechanism-choice ADRs
