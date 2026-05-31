# Architecture Outline — Concepts

## What is an architecture outline?

An **architecture outline** is the *one-page* answer to "what is this system?". It is built around a small set of diagrams — platform, layered architecture, system context, deployment topology — supplemented by a consolidated list of guiding principles, the technology stack, and a one-line description of every major system or subsystem. It is **deliberately shallow**: it shows the system's silhouette and neighbours but explicitly defers internal mechanisms, component contracts, data models, and patterns to the **blueprint** and **reference** skills that come after it.

This skill ships **paired outputs**: a markdown file that humans read, and four `.drawio` sources that the team edits. The markdown embeds rendered PNGs (or links the `.drawio` files directly); the `.drawio` files are the source of truth that anyone can open in [draw.io Desktop](https://www.drawio.com/) or [app.diagrams.net](https://app.diagrams.net/) without checking out the repository. The CLI helper at `scripts/arch-drawio.ps1` initialises the four templates, exports PNGs, and verifies that every diagram in the markdown has a matching `.drawio` source.

The outline carries **decision records** for the choices visible at this level (chosen platform, chosen architectural style, chosen deployment model). Decisions below this level — how error handling works, which caching pattern, which test tier owns what — live with the blueprint or reference document that introduces them.

---

## The four diagrams

Every architecture outline contains four diagrams. Each one answers a different question and a reviewer should be able to point at the answer without reading prose.

| Diagram | Question it answers | Notation |
|---|---|---|
| **Platform diagram** | What kind of system is this? (web app, mobile + API, desktop client, embedded device, distributed pipeline, etc.) | Block diagram or simple grouping; logo-level technology badges acceptable |
| **Layered architecture diagram** | What are the logical layers and what is the dependency direction between them? | Stacked-boxes diagram; arrows always point one way |
| **System context diagram** | Who and what does the system talk to? | C4 System Context, or a simple actor + neighbouring-system box diagram |
| **Deployment topology diagram** | Where does each part run, and what runtime container hosts it? | C4 Deployment, or boxes-inside-boxes (environment → host → process) |

---

## Guiding principles

A **guiding principle** is a one-sentence stance the system takes that constrains future decisions. Good principles are **decidable**, **directional**, and **traceable to a real trade-off** the team has accepted. They are pulled together in the outline so that everyone working on the system can see them in one place — even if the principles originate in deeper documents (the reference, the blueprint, or an ADR).

---

## Major systems catalogue

The outline names every **major system or subsystem** the architecture distinguishes and gives each one a single line of description. Internal organisation, components, interfaces, and patterns are *not* in scope here — they belong in the blueprint and reference. The catalogue exists so a reader can map any feature request, bug, or operations alert to a named owner-system within minutes.

---

## Decision records

A **decision record (ADR)** captures *why* a choice was made — context, options considered, consequences. The outline carries ADRs for choices visible at the outline level: platform, architectural style, deployment model, major external integrations. Decisions about internals (which caching pattern, which test tier) live with the document that introduces them.

---

## What the outline does NOT contain

These live in `abd-architecture-blueprint` and `abd-architecture-template`:

- Component-by-component descriptions
- Cross-cutting concern implementations (auth, error handling, logging — those are [*architecture mechanisms*](../../../reference/architecture-mechanism.md))
- Data models or entity relationships
- Code-level patterns
- Detailed testing strategy beyond a one-liner stating where tests live
