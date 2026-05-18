---
catalog_garden_tier: practice
catalog_garden_order: 20
name: abd-architecture-blueprint
description: >-
  Produce the second-level architecture document after the outline — a
  blueprint that names each architectural component in a paragraph or two
  (purpose, dependencies, interactions, no internal details), names every
  cross-cutting concern as a typed "architecture mechanism" (security, error
  handling, logging, validation, configuration, etc.), shows the data
  architecture at the model level, captures a common testing strategy, and
  records decisions. Deep internals defer to abd-architecture-template.
---
# abd-architecture-blueprint

## Purpose

The outline shows what a system *is*; the blueprint shows what it is *made of*. A blueprint is the document a tech lead opens to answer "where does the order code live? what does it depend on? how does it talk to the catalogue?" without yet drilling into the implementation patterns. It names every architectural component in a paragraph or two, catalogues every cross-cutting concern as an **architecture mechanism**, shows the data architecture at the model level, captures the common testing strategy, and lists the decisions taken at this level. When the blueprint is in place, the **architecture reference** can go deep on one mechanism at a time without re-explaining the system to its reader.

## When to use this skill

Load this skill when **any** of the following apply:

- An **architecture outline exists** and the team now needs the next level of detail — what components exist, what each one is responsible for, how they relate.
- New engineers can read the outline but still cannot find the **error-handling mechanism**, the **auth pattern**, or the **logging contract** without asking — those belong in the blueprint as mechanisms.
- Code review keeps catching **violations of cross-cutting concerns** (errors thrown across the API boundary, logs that leak PII, validation duplicated in three places) — a named mechanism in the blueprint pulls the rule into the document.
- A **data model question** keeps coming up (where is the canonical Order, can the Catalogue write to the Identity store) — the blueprint's data-architecture section settles it.
- An **architecture review** is approaching and the outline is not enough — reviewers need component-level and mechanism-level material to do their job.

## What is an architecture blueprint?

An **architecture blueprint** is the *system-level reference* that sits between the one-page outline and the deep-dive mechanism reference. It is organised around **components** (1–2 paragraphs each: purpose, dependencies, interactions — no internal structure detail), **architecture mechanisms** (each cross-cutting concern named and described in 1–2 paragraphs as a typed mechanism: Security, Error Handling, Logging, Validation, Configuration, Resilience, etc.), **data architecture** (domain model overview, entity relationships, persistence strategy), **testing architecture** (only the strategy common across components), and **decision records** for blueprint-level choices.

This skill ships **paired outputs**: a markdown file that humans read, and two `.drawio` sources for the load-bearing blueprint diagrams (`entity-relationships.drawio` and `component-overview.drawio`). The markdown embeds rendered PNGs; the `.drawio` files are the source of truth that architects can open in [draw.io Desktop](https://www.drawio.com/) or [app.diagrams.net](https://app.diagrams.net/). Inline mermaid is fine for **small, walkthrough-style figures** inside a component or mechanism description, but the entity model and the component overview need editable drawio sources because they outlive any single contributor. The CLI helper at `scripts/arch-drawio.ps1` initialises templates, exports PNGs, and verifies pairs.

The blueprint **defers detail down**: anything that needs a code walkthrough, a sequence diagram with multiple participants, or a full mechanism breakdown lives in the **architecture reference** (one file per mechanism, six sections each).

---

## Core concepts

### Components vs systems

The outline catalogues **major systems** (one line each). The blueprint zooms in by **one level**: each major system is described as a small set of **components** — the named building blocks the system is composed of. A component is a self-contained piece of code with one purpose and a stable interface; the blueprint describes it in 1–2 paragraphs and never lists its internal classes, methods, or files.

| Outline level | Blueprint level | Reference level |
|---|---|---|
| "Orders system" (one line) | "Order Service, Order Repository, Order Event Publisher" (paragraph each) | Full `OrderService` walkthrough with code, sequence diagrams, tests |

### Architecture mechanisms

A **cross-cutting concern** is any architectural concern that shows up in many components — authentication, error handling, logging, validation, configuration, caching, resilience, observability. In this skill family they are first-class artefacts called **architecture mechanisms**. The blueprint **names** every mechanism the architecture commits to and describes each one in 1–2 paragraphs: what concern it addresses, which components depend on it, how they interact with it. The **architecture reference** then takes one mechanism at a time and goes deep using `abd-architecture-template`.

The canonical mechanism categories (adapt to the project):

| Mechanism | What it covers |
|---|---|
| **Security** | Authentication, authorization, secret handling, identity propagation |
| **Error Handling & Resilience** | Exception/Result conventions, retry, circuit breaker, fallback, error reporting |
| **Logging & Observability** | Logging library, log shape, trace propagation, metric emission |
| **Validation** | Input validation strategy, business-rule validation, error reporting back to caller |
| **Configuration** | Config source, environment separation, secret management, feature flags |
| **Caching** | Where caches sit, invalidation strategy, consistency model |
| **Communication** | Sync vs async patterns, message bus, API versioning, service discovery |
| **Persistence** | Repository pattern, transaction boundaries, migration strategy |

Add or rename mechanisms as the system demands; the point is *typed, named cross-cutting concerns the codebase commits to*.

### Data architecture

The blueprint shows the **data model** at the entity/aggregate level — names, relationships, ownership boundaries. It does **not** ship schemas, ORM mappings, or indexes (those live with the persistence mechanism reference or the operations runbook). A reader of the data section should be able to draw the dependency graph between domain entities and identify which component owns each one.

### Testing architecture at this level

The outline says "tests exist"; the reference goes deep on testing one mechanism. The blueprint sits between: it names the **test tiers common to the whole system** (the tier vocabulary, the boundary between tiers, the test doubles common across tests). Mechanism-specific testing detail belongs in each mechanism's reference document, not the blueprint.

### Decision records at this level

Blueprint-level decisions are choices visible at this level: how error handling is structured (exceptions vs result objects), the cache strategy (write-through vs cache-aside), the test-tier vocabulary, the message-bus technology. **Outline-level decisions** (platform, architectural style, deployment topology) live with the outline; **reference-level decisions** (the exact retry policy, the exact validator framework) live with the reference. Each blueprint decision is an ADR file using the same template as the outline.

---

## Example

A typical blueprint for a SaaS platform (~250 lines) — markdown plus paired `.drawio` sources:

```
docs/architecture/
├── architecture-blueprint.md                  ← human-readable, embeds the two PNGs
├── architecture-outline.md                    ← produced by abd-architecture-outline
├── diagrams/
│   ├── (the four outline diagrams from abd-architecture-outline)
│   ├── component-overview.drawio              ← source (this skill)
│   ├── component-overview.png                 ← rendered
│   ├── entity-relationships.drawio            ← source (this skill)
│   └── entity-relationships.png               ← rendered
└── decisions/
    ├── ADR-004-result-object-error-handling.md
    ├── ADR-005-write-through-redis-cache.md
    └── ADR-006-outbox-event-publishing.md

architecture-blueprint.md sections:
├── 1. Scope and relationship to outline       ← short link-out
├── 2. Components                              ← one ## per system, 2–4 components each
│   ├── 2.1 Identity components                ← references component-overview.png
│   ├── 2.2 Catalogue components
│   ├── 2.3 Orders components
│   └── 2.4 Notifications components
├── 3. Architecture mechanisms                 ← one ## per mechanism, 1–2 paras
│   ├── 3.1 Security
│   ├── 3.2 Error Handling & Resilience
│   ├── 3.3 Logging & Observability
│   ├── 3.4 Validation
│   ├── 3.5 Configuration
│   ├── 3.6 Caching
│   └── 3.7 Persistence
├── 4. Data architecture                       ← references entity-relationships.png
├── 5. Testing architecture                    ← common tiers, common doubles
├── 6. Extension & evolution (if applicable)   ← only when there are real plug-in points
└── 7. Decision records                        ← table linking to ADRs
```

## The shape of a good blueprint

```
{Title} — Architecture Blueprint

1. Scope
   Linked from the architecture outline. This blueprint adds component-level
   description and mechanism catalogue. Mechanism walkthroughs live in
   architecture-reference.md (one section per mechanism).

2. Components
   2.1 {System} components
       - {Component name}
         {1–2 paragraphs: purpose, dependencies, interactions. No internals.}
       - {Next component …}
   ...

3. Architecture Mechanisms
   3.1 Security
       {1–2 paragraphs: what concern it addresses, which components depend
       on it, how they interact with it. Defer mechanism internals to
       architecture-reference.md.}
   3.2 Error Handling & Resilience
       {1–2 paragraphs}
   ...

4. Data Architecture
   {Entity overview diagram (mermaid classDiagram or ER). Ownership boundary
   table: which component owns which aggregate.}

5. Testing Architecture
   {Common test tiers; common test doubles; framework of record. Mechanism-
   specific testing detail defers to each mechanism's reference section.}

6. Extension & Evolution (if applicable)
   {Only include when the system has real plug-in points: a documented
   adapter contract, a registry-driven extension, a SaaS multi-tenancy
   isolation seam.}

7. Decision Records
   | ID | Decision | One-line consequence |
   |---|---|---|
   | ADR-NNN | ... | ... |
   (each ADR is a separate file under docs/architecture/decisions/)
```

**What the blueprint does NOT contain** (lives in `abd-architecture-template`):
- Code-level walkthroughs of a mechanism
- Sequence diagrams that involve more than three participants
- Full data schemas / DDL / ORM mappings
- Test code examples per tier
- Per-component file structures

**What the blueprint does NOT contain** (lives in `abd-architecture-outline`):
- Platform diagram (the *one* high-level picture)
- Deployment topology
- Guiding principles list
- Technology stack table
- Major systems catalogue (one-liners)

---

## Build

**Goal:** Produce `docs/architecture/architecture-blueprint.md`, two paired `.drawio` sources (+ rendered PNGs) under `docs/architecture/diagrams/`, one ADR file per blueprint-level decision under `docs/architecture/decisions/`, and stub `docs/architecture/architecture-reference.md` (or per-mechanism reference files) for each mechanism named in section 3.

1. **Read the architecture outline first.** The blueprint depends on it: components zoom in on major systems, mechanisms apply to the layered architecture, ADR numbering continues from the outline.

2. **Seed the blueprint diagram templates.** From this skill's folder, run:

   ```powershell
   .\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>
   ```

   This copies `component-overview.drawio` and `entity-relationships.drawio` into `docs/architecture/diagrams/`, skipping any that already exist (use `-Force` to overwrite). These join the four outline diagrams produced by `abd-architecture-outline`.

3. **Write section 1 (Scope).** One paragraph: link back to the outline, link forward to the reference. State explicitly what the blueprint covers and what it defers.

4. **List components per system.** For each major system in the outline's catalogue, write one subsection (`## 2.X {System} components`). Inside, name 2–4 components and write 1–2 paragraphs each: **purpose** (what concern this component owns), **dependencies** (what it imports or is injected with), **interactions** (what calls it and what it calls). **No internal structure** — no class lists, no method tables, no file trees. Open `component-overview.drawio` in draw.io and fill in the real components per system; the diagram captures the same information visually.

5. **Catalogue architecture mechanisms.** For each cross-cutting concern the system commits to, write a subsection (`## 3.X {Mechanism}`). Use the standard mechanism vocabulary (Security, Error Handling & Resilience, Logging & Observability, Validation, Configuration, Caching, Communication, Persistence) and add project-specific ones. Each mechanism is 1–2 paragraphs covering: what concern it addresses, which components depend on it, how they interact with it. Defer the deep walkthrough to the reference. Update the **mechanisms band** at the bottom of `component-overview.drawio` to match.

6. **Sketch the data architecture using the drawio template.** Open `entity-relationships.drawio` and replace the placeholder aggregates (User / Order / LineItem / Product) with the real domain. Keep colour-coded ownership boundaries — each colour maps to the owning component named in section 2. Then add a small markdown table mapping aggregate → owning component. Stop before schemas. (For tiny per-component class diagrams, inline mermaid in the component description is fine; the two **load-bearing** diagrams need drawio sources.)

7. **Export the diagrams to PNG.** Run:

   ```powershell
   .\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>
   ```

   This renders `component-overview.drawio` → `component-overview.png` and `entity-relationships.drawio` → `entity-relationships.png` via the local draw.io Desktop binary. Reference the PNGs from section 2 and section 4.

8. **Capture the common testing strategy.** Name the test tiers the project uses, the boundary between tiers, the common test doubles. Stop before per-mechanism test detail.

9. **Add Extension & Evolution only if applicable.** Skip this section if there is no real plug-in seam, adapter contract, or extension registry. A blueprint with no extension points should not have an Extension section that says "TBD".

10. **Write blueprint-level decision records.** One ADR per decision visible at this level using the `decision-record.md` template (shared with `abd-architecture-outline`). Continue ADR numbering from the outline.

11. **Stub the reference documents.** For each mechanism in section 3, create or update a placeholder section in `architecture-reference.md` (or a per-mechanism file) so that `abd-architecture-template` has a target to fill in.

12. **Verify the paired outputs.** Run:

    ```powershell
    .\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
    ```

    This walks every diagram reference in `architecture-blueprint.md` and confirms a matching `.drawio` source exists. Treat any FAIL line as blocking.

13. **Validate against the rules** bundled at the end of this `SKILL.md`. Walk each rule against the blueprint; fix violations before declaring done.

14. **Bundle this skill's rules into `SKILL.md`** when you have edited any `rules/*.md`:

    ```bash
    python skills/skill-builder/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root skills/architecture-centric-delivery/abd-architecture-blueprint
    ```

---

## Validate

**Goal:** Inspect the produced blueprint the way a reviewer would inspect any architecture document.

- **Who is checking:** Software Architect (does every mechanism appear and does it match what the code does?), Tech Lead (could a new engineer pick the right component for a new feature from this page alone?), Security/Ops (are the security and observability mechanisms named and accurate?).
- **Cross-artifact parity:** Every component in section 2 belongs to a major system named in the outline. Every mechanism in section 3 corresponds to a section (or file) in the architecture reference. Every ADR is a real file.

Checklist for the **produced blueprint**:

- **Section 2 — components in paragraphs, not internals** — every component has 1–2 paragraphs naming purpose, dependencies, interactions; no class lists, no method tables, no file trees.
- **Section 2 ships paired drawio** — `component-overview.drawio` exists, the rendered PNG is embedded, and `.\scripts\arch-drawio.ps1 verify` prints PASS for it.
- **Section 3 — every mechanism is named, typed, and short** — each cross-cutting concern appears as a named mechanism with 1–2 paragraphs; deep walkthroughs are deferred to the reference.
- **Section 4 — data architecture is entity-level** — a relationship diagram and an ownership-boundary table; no schemas, no DDL.
- **Section 4 ships paired drawio** — `entity-relationships.drawio` exists, the rendered PNG is embedded, and `.\scripts\arch-drawio.ps1 verify` prints PASS for it.
- **Section 5 — testing architecture is common-across-the-system** — tiers, boundaries, common doubles only; per-mechanism testing detail is absent.
- **Section 6 — Extension & Evolution is present only when warranted** — no "TBD" placeholder; skip the section if the system has no real extension points.
- **Section 7 — ADRs exist on disk** — every ADR cited has a matching file under `docs/architecture/decisions/`; ADR numbering continues from the outline.
- **No outline-level material in the blueprint** — no platform diagram, no technology-stack table, no major-systems one-liners (those live in the outline).
- **No reference-level material in the blueprint** — no code walkthroughs, no multi-participant sequence diagrams, no test code, no per-mechanism file trees (those live in the reference).
- **References stubbed forward** — for each mechanism, a placeholder section or file exists in `architecture-reference.md` so the reference skill has a target.

---

## Deploy

This skill ships IDE-deployable files under `ide-files/`. Deploy them to any project:

```powershell
.\skills\skill-builder\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath skills/architecture-centric-delivery/abd-architecture-blueprint -ProjectRoot <target-project> -Force
```

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Blueprint defers deep detail to the reference

The blueprint stops at description; the reference owns walkthroughs. The blueprint **must not** contain code-level walkthroughs of a mechanism, multi-participant sequence diagrams, full data schemas/DDL, test code, or per-component file structures — that material belongs in `architecture-reference.md` (one section per mechanism, six parts each). When a reader needs that level of detail, the blueprint must forward-link to the reference rather than inline it. Failing means a single mechanism section runs to multiple pages of code, a class diagram with twenty types ships in the blueprint, or the blueprint duplicates content that already exists in the reference.

#### DO

- Forward-link to the reference whenever a question naturally leads to deeper detail.

  **Example (pass):** "Caching — write-through, keys named `cat:{sku}:v{n}`. *See `architecture-reference.md` section 3.6 for the full key convention, eviction strategy, and consistency guarantees.*"

- Keep diagrams in the blueprint to a single concern (one entity relationship, one ownership boundary, one mechanism overview). Multi-participant sequence diagrams belong in the reference.

  **Example (pass):** Blueprint section 4 has a single classDiagram showing five entities. The reference has a five-participant sequenceDiagram for the order-placement flow.

- When code is genuinely useful to the blueprint reader, prefer a *one-line* contract signature over an implementation.

  **Example (pass):** "Components publish events through `IEventPublisher.publish(event: DomainEvent): Promise<void>`." (signature only, defer the in-process bus implementation to the reference.)

#### DO NOT

- Inline a full method body inside a mechanism subsection.

  **Example (fail):** Section 3.2 (Error Handling) has 40 lines of TypeScript showing the `ErrorTranslator.translate(error)` switch. That is reference content; the blueprint should describe the *role* and link.

- Ship a sequence diagram with more than three participants in the blueprint.

  **Example (fail):** Section 3.1 (Security) has a six-lane sequence diagram covering the full Auth0 PKCE flow. Move it to the reference; the blueprint just names the mechanism.

- Include the database schema or DDL.

  **Example (fail):** Section 4 (Data Architecture) prints the `CREATE TABLE orders (...)` statement with every column and index. The blueprint shows entity relationships and ownership; schemas belong with the persistence mechanism reference.

- Embed a test-suite example.

  **Example (fail):** Section 5 (Testing Architecture) lists ten test methods of `OrderServiceDomainTests`. The blueprint names the tier; per-mechanism tests live in the reference.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); blueprint is description, reference is walkthrough.

### Rule: Components described in paragraphs, not internals

A component in the blueprint is described in **one to two short paragraphs** covering **purpose**, **dependencies**, and **interactions** — no internal class lists, no method tables, no file trees, no code snippets. The blueprint sits between the outline (one-liner) and the reference (full walkthrough); internal structure belongs in the reference, not here. Failing means a component description bullets out every class in the package, lists every public method, embeds a file tree, or runs to multiple pages.

#### DO

- Write each component as 1–2 paragraphs with the three named subheadings (Purpose, Dependencies, Interactions) or three sentence-shaped beats in a single paragraph.

  **Example (pass):**

  > #### OrderService
  >
  > **Purpose.** Owns the order lifecycle from cart to fulfilment; canonical source of revenue events.
  >
  > **Dependencies.** `IOrderRepository`, `ICatalogueClient`, `IEventPublisher`, `IClock`.
  >
  > **Interactions.** Called from the orders API; calls into the Catalogue system on validation; emits domain events consumed by Notifications.

- Name dependencies as interface symbols, not implementation classes. The component's job in the blueprint is what it *uses*, not what it *contains*.

  **Example (pass):** "Depends on `IPaymentProvider`" rather than "uses `StripePaymentProvider`".

- Defer "how does it do X?" to the architecture reference by explicit forward link when the question naturally arises.

  **Example (pass):** "Implements the outbox pattern for cross-component event delivery — see the Persistence mechanism in `architecture-reference.md` for the full transactional shape."

#### DO NOT

- List every public method or property of the component.

  **Example (fail):**
  > **OrderService methods:** `createCart()`, `addLineItem()`, `removeLineItem()`, `applyDiscount()`, `submit()`, `cancel()`, `fulfil()`, `refund()`, `archive()`.

  The method list is reference-level content and changes every sprint; in the blueprint it adds noise without adding clarity.

- Embed code or pseudo-code inside a component description.

  **Example (fail):** A `OrderService` paragraph followed by a 30-line TypeScript snippet showing the `createCart` implementation. That is reference content.

- Drop a file tree under each component.

  **Example (fail):**
  > **OrderService files:**
  > ```
  > packages/orders/
  > ├── order-service.ts
  > ├── order-repository.ts
  > ├── order-event-publisher.ts
  > └── ...
  > ```
  > File structure of a component is reference-level content (the reference's File Structure section). Keep the blueprint at paragraphs.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); blueprint is "components in paragraphs", reference owns internals.

### Rule: Cross-cutting concerns are named as typed architecture mechanisms

Every cross-cutting concern the system commits to appears in the blueprint as a **typed, named architecture mechanism** with its own subsection under section 3. The standard mechanism vocabulary covers Security, Error Handling & Resilience, Logging & Observability, Validation, Configuration, Caching, Communication, and Persistence; projects may add or rename mechanisms as needed but each must be a named subsection. Failing means a cross-cutting concern exists in code but has no blueprint section, two unrelated concerns are merged into one subsection, or a section title is generic ("Other patterns", "Implementation notes") instead of naming the mechanism.

#### DO

- Give every committed cross-cutting concern its own `### 3.X {Mechanism Name}` subsection inside section 3.

  **Example (pass):**

  ```
  ## 3. Architecture Mechanisms
  ### 3.1 Security
  ### 3.2 Error Handling & Resilience
  ### 3.3 Logging & Observability
  ### 3.4 Validation
  ### 3.5 Configuration
  ### 3.6 Caching
  ### 3.7 Persistence
  ```

- Describe each mechanism in 1–2 paragraphs: what concern it addresses, which components depend on it, how they interact with it; then explicitly defer deep walkthroughs to the reference.

  **Example (pass):** "Caching — Catalogue data is cached in Redis with a write-through pattern; admin writes invalidate the keys they touch. Identity data is cached at the API edge with a 60-second TTL. *See `architecture-reference.md` for the full cache-key convention and invalidation strategy.*"

- Add project-specific mechanisms when the canonical list does not cover something material (e.g. **Multi-tenancy Isolation**, **Game Bridge Seam**, **GPU Workload Dispatch**).

  **Example (pass):** A WPF/COH project blueprint with a `### 3.8 COH Game Bridge Seam` subsection — same shape as the standard ones.

#### DO NOT

- Fold security and validation together under a single "Cross-cutting" heading.

  **Example (fail):** Section 3 has one subsection called "Cross-cutting concerns" with five paragraphs that drift across auth, error handling, logging, and validation. Readers cannot find the security mechanism without scanning.

- Use a generic subsection title like "Patterns" or "Implementation notes" instead of naming the mechanism.

  **Example (fail):** `### 3.4 Implementation patterns` with content that is in fact about logging and observability. Rename to `### 3.4 Logging & Observability`.

- Drop a mechanism into the document as a single sentence because "we'll fill it in later".

  **Example (fail):** "### 3.5 Configuration. TBD." Either describe the mechanism in 1–2 paragraphs, omit the section because the concern is not yet a real commitment, or call out the deferral in writing with a reason.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); mechanisms map one-to-one to architecture-reference sections.

### Rule: Every diagram ships paired markdown reference and drawio source

Every diagram referenced from `architecture-blueprint.md` must have a matching `.drawio` source file on disk under `docs/architecture/diagrams/`. The markdown is what readers see; the `.drawio` is what the team edits. Without the source file, the next person who needs to update the diagram has to redraw it from scratch, and the architecture document drifts from the running system within a release. The two blueprint-level diagrams this skill ships templates for are `entity-relationships.drawio` (the data model overview in section 4) and `component-overview.drawio` (the component-per-system overview that complements section 2). The CLI helper at `scripts/arch-drawio.ps1` initialises templates, exports PNGs, and verifies the pairs. Failing means a diagram appears in the markdown as a PNG with no `.drawio` source, or a `.drawio` source exists for a diagram that the markdown never references.

#### DO

- Place every blueprint-level diagram source as `docs/architecture/diagrams/<name>.drawio` and reference either the rendered `<name>.png` or the `<name>.drawio` file directly from the markdown.

  **Example (pass):** `architecture-blueprint.md` section 4 contains `![Entity relationships](./diagrams/entity-relationships.png)`. The file `docs/architecture/diagrams/entity-relationships.drawio` exists. Running `.\scripts\arch-drawio.ps1 verify` prints `[verify] OK   diagrams/entity-relationships.png -> entity-relationships.drawio exists`.

- Use mermaid inside the blueprint markdown only for **small, walkthrough-style figures** that fit on one screen and benefit from being in-page (e.g. a tiny sequence sketch in a component description). The two **load-bearing** blueprint diagrams (entity-relationships and component-overview) need drawio sources because architects and reviewers edit them outside the codebase.

  **Example (pass):** Section 4 uses a drawio-sourced PNG for the entity overview; an inline mermaid `classDiagram` appears in a component description showing a single class — fine, that one does not need a paired drawio.

- Run `.\scripts\arch-drawio.ps1 init -ProjectRoot <path>` to seed templates without overwriting existing diagrams (unless `-Force`).

  **Example (pass):** Project gets two new `.drawio` files in `diagrams/`; existing diagrams are not touched.

#### DO NOT

- Embed a screenshot or PNG of an entity diagram with no `.drawio` source.

  **Example (fail):** `architecture-blueprint.md` shows `./diagrams/entity-relationships.png` but `diagrams/` has no matching `.drawio`. The diagram becomes write-only.

- Use only inline mermaid for the entity overview when the blueprint promises a drawio-sourced diagram in its template.

  **Example (fail):** Section 4 has a 30-line mermaid `classDiagram` and no drawio source. Once the entity model grows past 5 aggregates, the mermaid block becomes unreadable in source view and the team cannot edit it visually.

- Leave orphan `.drawio` files in `diagrams/` that the blueprint never references.

  **Example (fail):** `diagrams/component-overview-old.drawio` and `diagrams/component-overview-v2.drawio` both exist; the blueprint links only to the v2 PNG. Delete the orphan or update the markdown to make its purpose clear.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); paired markdown + drawio keeps load-bearing diagrams editable.

### Rule: Extension & Evolution section appears only when there is a real extension point

Section 6 of the blueprint (Extension & Evolution) is included **only** when the system has a *real, documented* extension seam: a named adapter contract, an extension registry, a documented plug-in mechanism, a multi-tenancy isolation boundary, or a similar concrete plug-in point. A blueprint with no such seams should **omit** the section entirely. A "TBD" or "not applicable yet" placeholder is the failing case — empty sections create noise and signal documentation drift. Failing means shipping the section with no content, listing speculative future extension ideas, or describing a feature that is not actually pluggable.

#### DO

- Include section 6 only when at least one extension point exists in code, with a named contract and a registration mechanism.

  **Example (pass):** "The architecture has one documented extension seam: notification channels. New channels implement `INotificationChannel` and register through `ChannelRegistry.register()` at startup."

- Describe each extension point in one paragraph naming the contract, the registration mechanism, and where the contract is documented in detail.

  **Example (pass):** "Theme plug-ins — load JSON theme manifests at startup through `IThemeProvider`; the contract is in `architecture-reference.md` section 5.4."

- Omit the section entirely when there are no real extension points. State explicitly in the Build/Validate step that section 6 was omitted because nothing is pluggable; reviewers know it was a considered decision.

  **Example (pass):** A blueprint with sections 1–5 and 7 (no 6). The Validate step note: "Extension & Evolution omitted; no extension seams exist in the current architecture."

#### DO NOT

- Ship the section with "TBD" or "To be defined" as content.

  **Example (fail):** "### 6. Extension & Evolution\nTBD — we'll define plug-in points once the system grows."

- Use the section to list speculative future ideas that are not implemented.

  **Example (fail):** "Future plug-in points may include theme packs, alternative payment providers, and custom reporting. Architecture support to be added."

- Describe a feature as "pluggable" when it is hard-coded in source.

  **Example (fail):** "Payment providers are pluggable" when the codebase has a `switch(provider)` statement enumerating Stripe and PayPal with no contract or registry. Either the seam is real (named contract + registry) or the section omits payment providers.

**Source:** Practice-skill authoring convention (abd-architecture-blueprint); empty sections are documentation rot.
<!-- execute_rules:bundle_rules:end -->
