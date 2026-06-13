# Architecture Outline — Concepts

## What is an architecture outline?

An **architecture outline** is the *one-page* answer to "what is this system?". It is built around a system context diagram supplemented by an architecture mechanisms catalogue, guiding principles, and the technology stack. It is **deliberately at the right altitude**: it names every system's functions and platform technology, commits to the mechanisms that address cross-cutting concerns, and records the decisions behind those choices — but explicitly defers runtime platform detail, deployment topology, component contracts, data models, and deep mechanism walkthroughs to the **blueprint** and **reference** skills that follow.

This skill ships **two layers of output for the diagram**: an element-inventory markdown that lists and describes every element, and a `.drawio` source populated from that inventory. The element file is written first; the diagram is built from it. The CLI helper at `scripts/arch-drawio.ps1` initialises the `.drawio` template, exports PNGs, and verifies that the diagram in the markdown has a matching `.drawio` source.

The outline carries **decision records** for all choices visible at this level: chosen platform, chosen architectural style, and every mechanism technology choice. Decisions below this level — component boundaries, internal patterns, test-tier vocabulary — live with the blueprint or reference document that introduces them.

---

## System context

The outline is centred on one diagram that answers a single question.

| **System context diagram** | What systems are in scope (with their major functions and platform technology), who uses them, what external systems connect, and over which protocols? |

---

## Diagram element inventory

Before the diagram is drawn, the outline skill produces a **`system-context-elements.md`** file. This file lists every element the diagram will show and gives each one a 1–2 sentence description. The inventory is the team's agreement on what belongs in the diagram; the `.drawio` source is populated *from* the inventory.

The file lives in `docs/architecture/diagrams/`:

| `system-context-elements.md` | All in-scope systems (functions + platform technology), persons (actors/roles), external systems, and relationships with protocols |

Every element in the diagram must have a matching entry in its inventory file, and every entry in the inventory must appear in the diagram.

---

## System context detail

For each **owned system**, the element inventory records:

- **Major functions** — the capabilities the system provides
- **Platform technology** — app stack (runtime, framework, key libraries), persistence (database and role), tools and infrastructure libs

For each **relationship**, the inventory records the **protocol** (HTTP/REST, gRPC, AMQP, WebSocket, etc.) alongside the functional description of what crosses the boundary.

The outline describes every system in terms of its functions and tech.

---

## Architecture mechanisms catalogue

The outline names every **architecture mechanism** the system commits to and gives each one a brief description: the **technology or platform choice**, **one or two paragraphs** on how the mechanism works at this level, and the **key non-functional requirement or justification** that drove the choice.

The standard set of mechanisms covers:

| Mechanism | Concern addressed |
|---|---|
| Security | Identity, authentication, authorisation, secrets |
| Error Handling & Resilience | Failure representation, propagation, circuit breaking, retry |
| Logging & Observability | Structured logging, tracing, metrics, correlation |
| Validation | Input validation at the edge and business rules in the domain |
| Configuration & Secrets | Startup config, secret injection, rotation |
| Caching | Cache technology, pattern, invalidation, staleness guarantees |
| Persistence | Data ownership, cross-aggregate consistency, migration policy |
| Communication | Synchronous protocols (REST/gRPC), async messaging, contracts |

Additional **bespoke mechanisms** — concerns unique to this system's context that the standard set does not cover — are included as additional subsections. The skill must derive these from the problem domain, not default to an empty list.

**Decision records for mechanism choices happen at the outline level**, not the blueprint level. If the choice of Redis over Memcached or gRPC over REST warranted a decision, that ADR lives here.

---

## Guiding principles

A **guiding principle** is a one-sentence stance the system takes that constrains future decisions. Good principles are **decidable**, **directional**, and **traceable to a real trade-off** the team has accepted.

---

## Decision records

A **decision record (ADR)** captures *why* a choice was made — context, options considered, consequences. The outline carries ADRs for:

- Platform and architectural-style choices
- Major external integration choices
- Every mechanism technology choice (which auth provider, which cache, which message bus, etc.)

Decisions about internals — component boundaries, test-tier vocabulary, specific code patterns — live with the document that introduces them.

---

## What the outline does NOT contain

These live in `abd-architecture-blueprint` and `abd-architecture-specification`:

- Layered architecture diagram
- Platform runtime diagram (client apps, backend services, data stores, CDN)
- Deployment topology diagram (environments, infrastructure nodes, container instances)
- Component-by-component descriptions
- Deep mechanism walkthroughs (code, sequence diagrams with multiple participants)
- Data models or entity relationships
- Testing strategy beyond a one-liner stating where tests live
