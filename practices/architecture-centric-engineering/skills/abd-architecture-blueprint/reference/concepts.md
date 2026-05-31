# Architecture Blueprint — Concepts

## What is an architecture blueprint?

An **architecture blueprint** is the *system-level reference* that sits between the one-page outline and the deep-dive mechanism reference. It is organised around **components** (1–2 paragraphs each: purpose, dependencies, interactions — no internal structure detail), **architecture mechanisms** (each cross-cutting concern named and described in 1–2 paragraphs as a typed mechanism), **data architecture** (domain model overview, entity relationships, persistence strategy), **testing architecture** (only the strategy common across components), and **decision records** for blueprint-level choices.

This skill ships **paired outputs**: a markdown file that humans read, and two `.drawio` sources for the load-bearing blueprint diagrams (`entity-relationships.drawio` and `component-overview.drawio`). Inline mermaid is fine for **small, walkthrough-style figures** inside a component or mechanism description, but the entity model and the component overview need editable drawio sources because they outlive any single contributor.

The blueprint **defers detail down**: anything that needs a code walkthrough, a sequence diagram with multiple participants, or a full mechanism breakdown lives in the **architecture reference** (one file per mechanism, six sections each).

---

## Components vs systems

The outline catalogues **major systems** (one line each). The blueprint zooms in by **one level**: each major system is described as a small set of **components** — the named building blocks the system is composed of. A component is a self-contained piece of code with one purpose and a stable interface; the blueprint describes it in 1–2 paragraphs and never lists its internal classes, methods, or files.

| Outline level | Blueprint level | Reference level |
|---|---|---|
| "Orders system" (one line) | "Order Service, Order Repository, Order Event Publisher" (paragraph each) | Full `OrderService` walkthrough with code, sequence diagrams, tests |

---

## Architecture mechanisms

**Architecture mechanism** is a family-level concept — see [`reference/architecture-mechanism.md`](../../../reference/architecture-mechanism.md) for the definition and the canonical mechanism categories (Security, Error Handling & Resilience, Logging & Observability, Validation, Configuration, Caching, Communication, Persistence). The blueprint's job is to **name** every mechanism the architecture commits to and describe each one in 1–2 paragraphs: what concern it addresses, which components depend on it, how they interact with it. The **architecture reference** then takes one mechanism at a time and goes deep.

---

## Data architecture

The blueprint shows the **data model** at the entity/aggregate level — names, relationships, ownership boundaries. It does **not** ship schemas, ORM mappings, or indexes. A reader of the data section should be able to draw the dependency graph between domain entities and identify which component owns each one.

---

## Testing architecture at this level

The outline says "tests exist"; the reference goes deep on testing one mechanism. The blueprint sits between: it names the **test tiers common to the whole system** (the tier vocabulary, the boundary between tiers, the test doubles common across tests).

---

## Decision records at this level

Blueprint-level decisions are choices visible at this level: how error handling is structured, the cache strategy, the test-tier vocabulary, the message-bus technology. Each blueprint decision is an ADR file using the same template as the outline.

---

## What the blueprint does NOT contain

**Lives in `abd-architecture-template`:**
- Code-level walkthroughs of a mechanism
- Sequence diagrams that involve more than three participants
- Full data schemas / DDL / ORM mappings
- Test code examples per tier
- Per-component file structures

**Lives in `abd-architecture-outline`:**
- Platform diagram
- Deployment topology
- Guiding principles list
- Technology stack table
- Major systems catalogue (one-liners)
