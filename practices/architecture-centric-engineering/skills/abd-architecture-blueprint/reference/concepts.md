# Architecture Blueprint — Concepts

## What is an architecture blueprint?

An **architecture blueprint** is the system-level reference that sits between the one-page outline and the deep-dive architecture specifications. It adds three things the outline deliberately defers:

1. **Platform runtime** — the full platform diagram showing what processes actually run, how they connect, and what technology each uses.
2. **Mechanisms as code shapes** — each mechanism from the outline is described in prose: what technology it uses and, critically, what code shape every module must adopt to implement it.
3. **Module catalogue** — the major domain and infrastructure areas described in 1–2 sentences each, with their mechanisms and dependencies named.

The blueprint also carries the testing architecture (tier vocabulary, what each tier exercises, what it fakes) and blueprint-level decision records.

This skill ships **paired outputs**: a markdown file that humans read, and `.drawio` sources for each diagram (`platform-architecture.drawio`, `architecture-flow.drawio`, `module-overview.drawio`, `testing-flow.drawio`).

The blueprint **defers deep mechanism detail**: code walkthroughs, multi-participant sequence diagrams, and per-file structures live in **architecture specifications** (one per mechanism scope).

---

## Platform architecture 

The outline's system-context diagram shows what the system is and who uses it. The blueprint adds the **platform runtime view**: the actual client apps, backend services, data stores, and third-party integrations — showing how they connect and what technology each runs on.

| Outline level | Blueprint level |
|---|---|
| "Retail Platform connects to Stripe over HTTPS/REST" | "Orders API (Node.js/Fastify) calls `stripe.paymentIntents.create()` via the Stripe SDK; response and webhook events both arrive at the Orders API" |

---

## Mechanisms as code shapes

The outline states each mechanism's technology choice and NFR justification. The blueprint goes further: for each mechanism it describes **the code shape every module must adopt** — what pattern, base class, hook, or convention a developer follows when writing a module that participates in that mechanism.

| Dimension | Outline | Blueprint |
|---|---|---|
| Technology choice | Named | Named (retained from outline) |
| NFR justification | One sentence | Retained from outline |
| Code shape | Not present | How every module implements or extends the mechanism — what to extend, inject, or follow |
| Module interactions | Not present | Which modules call into the mechanism and what they pass |

**New mechanisms discovered during blueprint work go back into the outline first.** When blueprinting surfaces a mechanism not yet recorded, add it to the outline (technology choice + NFR justification + ADR), then deepen it in the blueprint. The outline remains the single source of mechanism technology decisions.

### Mechanism-modules

Some mechanisms also have a **concrete module surface** — a deployable or importable unit with its own API. Security (→ Identity module), App Server (→ Bootstrap module), and similar are both a mechanism *and* a module. They are described in the mechanisms section for their code-shape constraint, and in the modules section for their functional surface.

**Unified Domain Logic** is an example of a pure mechanism (no module): it constrains the shape of routes, views, and DB layers to follow domain naming and structure, but there is no single class or API to import. Every module that handles domain objects participates in it.

---

## Modules

Modules are the major domain and infrastructure areas. Front and back are **not** different modules — a module spans the full stack for its domain area. Each module description has:

- **Business scope** — 1–2 sentences on what domain responsibility this module owns.
- **Mechanisms used** — universal mechanisms (used by all modules) go in a legend; module-specific ones are listed per module.
- **Dependencies** — which other modules this one calls or depends on.

The module overview diagram shows inter-module dependencies with a functional scope one-liner and the mechanism list per module.

---

## Architecture flow diagram

The architecture flow diagram shows the **mechanisms active at each layer** for a typical request. It is not an exhaustive sequence diagram — it shows which mechanism governs each layer crossing (e.g. App Server at the entry point, Identity at the auth boundary, Unified Domain Logic at the service and DB layers). More than one diagram is acceptable when different mechanism combinations apply to meaningfully different flows.

---

## Testing architecture at this level

The outline says "tests exist"; specifications go deep on testing one mechanism. The blueprint sits between: it names the **test tiers common to the whole system** — their scope, what each tier treats as real vs faked, and the entry point for each.

The testing flow diagram shows this visually: each tier as a column, each stack layer as a row, coloured by whether that layer is real (green), faked (yellow), the test entry point (blue), or not reached (grey).

---

## Decision records at this level

Blueprint-level decisions are choices visible at this level: module boundaries, test-tier vocabulary, data ownership patterns, extension seam contracts. Mechanism technology choices have their ADRs in the outline and are not re-recorded here.

---

## What the blueprint does NOT contain

**Lives in `abd-architecture-specification`:**
- Code-level walkthroughs of a mechanism
- Sequence diagrams that involve more than three participants
- Per-module file structures
- Test code examples per tier

**Lives in `abd-architecture-outline`:**
- Layered architecture diagram
- System context diagram (functions + tech per system, protocols)
- Mechanisms catalogue (technology choice + NFR justification)
- Guiding principles list
- Technology stack table
- Major systems catalogue (one-liners)
- Mechanism-choice ADRs
