### Rule: Reference includes Instantiating the Domain

Every `architecture-specification.md` produced or extended by this skill must contain a `## Instantiating the Domain` section before `## Mechanisms`. This section is **common to all architecture specs** — it defines how domain classes and operations from the domain model become code. It has four named sub-sections: **Principles**, **Architecture Flow**, **Module Layout**, and **Participants**. Mechanism sections differ by tech stack; Instantiating the Domain does not.

Passing means the section explains domain-to-code mapping with all four sub-sections present. Failing means domain rules are scattered across mechanism sections, buried in Overview prose, or Architecture Flow is a standalone top-level section instead of a sub-section here.

#### DO

- Place `## Instantiating the Domain` before `## Mechanisms` and give it four sub-sections: Principles, Architecture Flow, Module Layout, Participants.

  **Example (pass):** MERN spec has `## Instantiating the Domain` → `### Principles` (naming rules, layer qualifiers) → `### Architecture Flow` (diagram + table) → `### Module Layout` (folder tree) → `### Participants` (class diagram), then `## Mechanisms`.

- Put Architecture Flow as a sub-section of Instantiating the Domain — not as a standalone `## Architecture Flow`.

  **Example (pass):** `### Architecture Flow` inside `## Instantiating the Domain`.

- Include a Participants class diagram showing inheritance (`--|>`), interface implementation (`..|>`), and delegation (`-->`) across shared, client, and server tiers.

  **Example (pass):** Mermaid classDiagram with `<<Entity>>Client --|> <<Entity>>`, `<<Entity>>sServer --|> <<Entity>>s`, `<<Entity>>RepositoryServer ..|> <<Entity>>Repository`.

- State that every code artifact instantiates from a domain class and/or operation.

  **Example (pass):** "`useRecipients.ts` is named for `<<Entity>>`; exposes `<<operation>>()` as a callable method."

- Include module layout and a naming contract table.

  **Example (pass):** Module tree under `packages/<domain>/` plus a table mapping tier → qualifier → example.

#### DO NOT

- Make Architecture Flow a standalone top-level `## Architecture Flow` section.

  **Example (fail):** Document TOC lists `## Overview`, `## Architecture Flow`, `## Instantiating the Domain` as separate H2 entries.

- Fold domain orientation, shared logic, or cross-layer alignment into separate mechanism sections when they belong in Instantiating the Domain.

  **Example (fail):** Three mechanisms named Domain-First Module Structure, Shared Domain Logic, Cross-Layer Alignment — these are one Instantiating the Domain section, not mechanisms.

- Skip Instantiating the Domain and jump straight to Mechanisms.

  **Example (fail):** Document has Overview → Mechanisms with no domain-to-code mapping section.

- Use generic tech names in Instantiating the Domain without tying them to domain placeholders or concrete domain terms.

  **Example (fail):** "Put business logic in the service layer" with no `<<Entity>>`, `<<operation>>`, or shared-core location.

**Source:** Practice-skill authoring convention (abd-architecture-specification); aligned with `specs/mern/architecture-specification.md`.
