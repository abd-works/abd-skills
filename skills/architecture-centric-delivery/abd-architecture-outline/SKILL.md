---
name: abd-architecture-outline
description: >-
  Produce the first architecture artifact for a new or unfamiliar system —
  a mostly-diagrams document that fixes platform, layering, system context,
  deployment topology, guiding principles, technology stack, and a brief
  catalogue of major systems with decision records. The outline answers
  "what is this thing made of and what does it sit next to?" before any
  deeper architecture work begins.
---
# abd-architecture-outline

## Purpose

A team that cannot draw its system on one page also cannot agree on what to build next. Outlines fix that. This skill produces the first architecture artifact for a system — short on prose, heavy on diagrams — so engineers, product, and stakeholders share a single picture of the platform, the layers, the neighbours, the deployment topology, and the principles in force. When the outline is in place, deeper architecture work (blueprint, reference, mechanisms) can start without re-litigating what the system *is*.

## When to use this skill

Load this skill when **any** of the following apply:

- A new project is **kicking off** and there is no architecture document at all — start with the outline before deeper work.
- An existing project has **no canonical picture** of itself and onboarding new people takes weeks because everyone redraws the system from memory.
- A team is choosing a **platform or major technology** and needs a single page that names the candidate stack and the principles that drove the choice.
- Stakeholders keep asking "**which system owns that?**" and the answer changes depending on who is in the room — the major-systems catalogue settles it.
- An architecture review is **about to happen** and there is no outline-level artifact to anchor the conversation.

## What is an architecture outline?

An **architecture outline** is the *one-page* answer to "what is this system?". It is built around a small set of diagrams — platform, layered architecture, system context, deployment topology — supplemented by a consolidated list of guiding principles, the technology stack, and a one-line description of every major system or subsystem. It is **deliberately shallow**: it shows the system's silhouette and neighbours but explicitly defers internal mechanisms, component contracts, data models, and patterns to the **blueprint** and **reference** skills that come after it.

This skill ships **paired outputs**: a markdown file that humans read, and four `.drawio` sources that the team edits. The markdown embeds rendered PNGs (or links the `.drawio` files directly); the `.drawio` files are the source of truth that anyone can open in [draw.io Desktop](https://www.drawio.com/) or [app.diagrams.net](https://app.diagrams.net/) without checking out the repository. The CLI helper at `scripts/arch-drawio.ps1` initialises the four templates, exports PNGs, and verifies that every diagram in the markdown has a matching `.drawio` source.

The outline carries **decision records** for the choices visible at this level (chosen platform, chosen architectural style, chosen deployment model). Decisions below this level — how error handling works, which caching pattern, which test tier owns what — live with the blueprint or reference document that introduces them.

---

## Core concepts

### The four diagrams

Every architecture outline contains four diagrams. Each one answers a different question and a reviewer should be able to point at the answer without reading prose.

| Diagram | Question it answers | Notation |
|---|---|---|
| **Platform diagram** | What kind of system is this? (web app, mobile + API, desktop client, embedded device, distributed pipeline, etc.) | Block diagram or simple grouping; logo-level technology badges acceptable |
| **Layered architecture diagram** | What are the logical layers and what is the dependency direction between them? | Stacked-boxes diagram; arrows always point one way |
| **System context diagram** | Who and what does the system talk to? | C4 System Context, or a simple actor + neighbouring-system box diagram |
| **Deployment topology diagram** | Where does each part run, and what runtime container hosts it? | C4 Deployment, or boxes-inside-boxes (environment → host → process) |

### Guiding principles

A **guiding principle** is a one-sentence stance the system takes that constrains future decisions. Good principles are **decidable**, **directional**, and **traceable to a real trade-off** the team has accepted. They are pulled together in the outline so that everyone working on the system can see them in one place — even if the principles originate in deeper documents (the reference, the blueprint, or an ADR).

### Major systems catalogue

The outline names every **major system or subsystem** the architecture distinguishes and gives each one a single line of description. Internal organisation, components, interfaces, and patterns are *not* in scope here — they belong in the blueprint and reference. The catalogue exists so a reader can map any feature request, bug, or operations alert to a named owner-system within minutes.

### Decision records

A **decision record (ADR)** captures *why* a choice was made — context, options considered, consequences. The outline carries ADRs for choices visible at the outline level: platform, architectural style, deployment model, major external integrations. Decisions about internals (which caching pattern, which test tier) live with the document that introduces them.

---

## Example

A typical outline for a web-plus-API SaaS — markdown plus paired `.drawio` sources:

```
docs/architecture/
├── architecture-outline.md              ← human-readable, embeds the four PNGs
├── diagrams/
│   ├── platform-architecture.drawio     ← source (edited in draw.io Desktop)
│   ├── platform-architecture.png        ← rendered, embedded in the markdown
│   ├── layered-architecture.drawio
│   ├── layered-architecture.png
│   ├── system-context.drawio
│   ├── system-context.png
│   ├── deployment-architecture.drawio
│   └── deployment-architecture.png
└── decisions/
    ├── ADR-001-spa-plus-rest-api-platform.md
    ├── ADR-002-layered-clean-architecture.md
    └── ADR-003-aws-fargate-deployment.md

architecture-outline.md sections:
├── 1. Platform diagram                  ← React SPA + Node API + Postgres + Redis
├── 2. Layered architecture diagram      ← Presentation / Application / Domain / Infra
├── 3. System context diagram            ← actors + 3 external systems
├── 4. Deployment topology diagram       ← AWS: CloudFront → ALB → ECS → RDS
├── 5. Guiding principles (8 bullets)    ← "Domain never imports infrastructure", etc.
├── 6. Technology stack (table)          ← runtime + framework + library + tool per layer
├── 7. Major systems catalogue (table)   ← 5 named subsystems, 1 line each
└── 8. Decision records                  ← 3 ADRs (platform, style, deployment)
```

## The shape of a good outline

```
{Title} — Architecture Outline

1. Platform Diagram
   {diagram}
   {≤2 sentence caption}

2. Layered Architecture
   {diagram}
   {≤3 sentence caption naming dependency direction}

3. System Context
   {diagram}
   {≤2 sentence caption naming actors and external systems}

4. Deployment Topology
   {diagram}
   {≤3 sentence caption naming environments and hosts}

5. Guiding Principles
   - {Principle 1, one sentence, decidable}
   - {Principle 2, one sentence, decidable}
   - ... (5–10 total)

6. Technology Stack
   | Layer | Technology | Version | Purpose |
   |---|---|---|---|
   | ... |

7. Major Systems
   | System | One-line description | Primary owner / module |
   |---|---|---|
   | ... |

8. Decision Records
   - ADR-001: {chosen platform} — {one-line consequence}
   - ADR-002: {chosen architectural style}
   - ADR-003: {chosen deployment model}
   (each ADR is a separate file under docs/architecture/decisions/)
```

**What the outline does NOT contain** (lives in `abd-architecture-blueprint` and `abd-architecture-reference`):
- Component-by-component descriptions
- Cross-cutting concern implementations (auth, error handling, logging — those are *architecture mechanisms*)
- Data models or entity relationships
- Code-level patterns
- Detailed testing strategy beyond a one-liner stating where tests live

---

## Build

**Goal:** Produce `docs/architecture/architecture-outline.md`, four paired `.drawio` sources (+ rendered PNGs) under `docs/architecture/diagrams/`, and one ADR file per outline-level decision under `docs/architecture/decisions/`.

1. **Pick the output location and seed the diagrams folder.** Default is `docs/architecture/architecture-outline.md` with diagrams in `docs/architecture/diagrams/`. From this skill's folder, run:

   ```powershell
   .\scripts\arch-drawio.ps1 init -ProjectRoot <target-project-root>
   ```

   This copies the four `.drawio` templates (`platform-architecture.drawio`, `layered-architecture.drawio`, `system-context.drawio`, `deployment-architecture.drawio`) into the project's `docs/architecture/diagrams/` folder, skipping any that already exist (use `-Force` to overwrite).

2. **Open each `.drawio` in draw.io Desktop or app.diagrams.net and fill in the `{Placeholders}`.** The templates already match the canonical style (stacked layered platform, vertical layered dependency stack, central system + external actors context diagram, UML deployment with environment/host/process nesting). Replace placeholder text with real component names; add or remove boxes as the system demands. Do not break the canonical filenames — the verify command depends on them.

3. **Export the diagrams to PNG.** Run:

   ```powershell
   .\scripts\arch-drawio.ps1 export -ProjectRoot <target-project-root>
   ```

   This renders every `<name>.drawio` to a sibling `<name>.png` using the local draw.io Desktop binary. The skill assumes draw.io Desktop is installed at the default location; pass `-DrawIoExe <path>` if it lives elsewhere. (If draw.io is not installed, the markdown can link to the `.drawio` files directly — many editors render them inline.)

4. **Write the four diagram sections of `architecture-outline.md` in order: platform, layered, context, deployment.** Each section embeds the rendered PNG (or links the `.drawio` source) and adds a caption of three sentences or fewer naming what the reader should see. Use `templates/architecture-outline.md` as the starting point.

5. **Consolidate guiding principles.** Walk the existing documents (reference docs, ADRs, READMEs, code-review comments) and pull every one-sentence stance the team actually applies. Keep 5–10. Each principle must be one sentence, must be decidable against a piece of code or a design, and must name what it constrains.

6. **List the technology stack as a table.** Columns: Layer, Technology, Version, Purpose. One row per material technology; do not list every transitive dependency.

7. **List the major systems as a table.** Columns: System, One-line description, Primary owner/module. One row per subsystem the architecture distinguishes; no internals.

8. **Write the outline-level decision records.** One ADR per decision visible at the outline level (platform, style, deployment, major external integration). Each ADR is its own file under `docs/architecture/decisions/ADR-NNN-{slug}.md` using `templates/decision-record.md`. The outline lists them with a one-line consequence; the file carries the full record.

9. **Verify the paired outputs.** Run:

   ```powershell
   .\scripts\arch-drawio.ps1 verify -ProjectRoot <target-project-root>
   ```

   The verify step walks every diagram reference in `architecture-outline.md` and confirms a matching `.drawio` source exists, then confirms the four canonical diagrams are all referenced. Treat any FAIL line as blocking — either ship the missing source or fix the reference.

10. **Validate against the rules** bundled at the end of this `SKILL.md`. Walk each rule against the produced outline; fix violations before declaring done.

11. **Bundle this skill's rules into `SKILL.md`** when you have edited any `rules/*.md`:

    ```bash
    python skills/skill-builder/abd-author-practice-skill/scripts/bundle_rules_into_skill_md.py --skill-root skills/architecture-centric-delivery/abd-architecture-outline
    ```

---

## Validate

**Goal:** Inspect the produced outline the way a reviewer would inspect any architecture document — gaps and drift first, prose polish second.

- **Who is checking:** Software Architect (do the diagrams match the running system?), Tech Lead (can a new engineer onboard from this page alone?), Product Owner (are the major systems and principles ones product can defend?).
- **Cross-artifact parity:** Every ADR referenced from the outline exists as its own file under `docs/architecture/decisions/`. Every diagram caption names content visible in the diagram.

Checklist for the **produced outline**:

- **Four diagrams present** — platform, layered, system context, deployment topology — each with a caption of three sentences or fewer.
- **Each diagram has a paired `.drawio` source** — `.\scripts\arch-drawio.ps1 verify -ProjectRoot <project>` prints PASS. No diagram is a PNG-only orphan.
- **Canonical filenames used** — `platform-architecture.drawio`, `layered-architecture.drawio`, `system-context.drawio`, `deployment-architecture.drawio` all exist under `docs/architecture/diagrams/`.
- **Layered diagram shows dependency direction** — arrows are one-way, no cycles drawn.
- **Principles are decidable** — every principle is one sentence and could be applied to a real code change or design choice.
- **Technology stack is a table** — Layer / Technology / Version / Purpose; no narrative paragraphs.
- **Major systems are one line each** — no internal component descriptions, no patterns, no mechanisms.
- **ADRs exist on disk** — every ADR named in the outline has a matching file under `docs/architecture/decisions/`.
- **No mechanism detail** — auth, error handling, logging, caching are *named* if at all, never explained — those live in the blueprint and reference.
- **No data model** — entity relationships and persistence schemas are absent; they live in the blueprint and reference.

---

## Deploy

This skill ships IDE-deployable files under `ide-files/`. Deploy them to any project:

```powershell
.\skills\skill-builder\abd-author-practice-skill\scripts\Deploy-SkillOutputs.ps1 -SkillPath skills/architecture-centric-delivery/abd-architecture-outline -ProjectRoot <target-project> -Force
```

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Decision records are named and live on disk

Every architectural decision visible at the outline level (platform, architectural style, deployment model, major external integration) is captured as its own ADR file under `docs/architecture/decisions/ADR-NNN-{slug}.md`. The outline itself lists each ADR with a one-line consequence and a link to the file. Failing means an outline references decisions without files behind them, embeds a multi-paragraph rationale in the outline itself, or names decisions in prose without an ADR number.

#### DO

- List ADRs in the outline as a table or numbered list with ID, decision, and a one-line consequence; each ID links to the actual ADR file.

  **Example (pass):**

  | ID | Decision | One-line consequence |
  |---|---|---|
  | [ADR-001](../decisions/ADR-001-spa-plus-rest-api-platform.md) | SPA + REST API platform | No server rendering, no GraphQL surface. |
  | [ADR-003](../decisions/ADR-003-aws-fargate-deployment.md) | AWS ECS Fargate, single region, multi-AZ | No Kubernetes operations cost; region failure is a DR scenario. |

- Use the `decision-record.md` template in this skill's `templates/` folder for every ADR file.

  **Example (pass):** `ADR-001-spa-plus-rest-api-platform.md` has Status / Date / Deciders / Context / Decision / Options considered / Consequences / Compliance — same shape as the template.

- Keep the ADR list in the outline to outline-level decisions only (platform, style, deployment, major external integrations).

  **Example (pass):** "How error handling is structured" is an architectural decision but a *blueprint-level* one — its ADR is listed in the blueprint, not the outline.

#### DO NOT

- Embed a multi-paragraph rationale for a decision directly in the outline.

  **Example (fail):** A section 8 heading reads `## Decision Records — Why we chose AWS over Azure` followed by three paragraphs comparing services. The detail belongs in `ADR-003`, not the outline.

- Reference an ADR by name without an actual file existing under `docs/architecture/decisions/`.

  **Example (fail):** Outline lists "ADR-004: Auth0 identity" but `docs/architecture/decisions/` has no file with that ID.

- Number ADRs inconsistently or restart numbering per document.

  **Example (fail):** Outline cites `ADR-001` for the platform decision and `ADR-001` again for an unrelated networking decision in the blueprint. ADR numbers are project-wide and monotonic.

**Source:** Practice-skill authoring convention (abd-architecture-outline); ADRs are decisions-on-disk, the outline only summarises.

### Rule: Every diagram ships paired markdown reference and drawio source

Every diagram referenced from `architecture-outline.md` must have a matching `.drawio` source file on disk under `docs/architecture/diagrams/`. The markdown is what readers see; the `.drawio` is what the team edits. Without the source file, the next person who needs to update the diagram has to redraw it from scratch, and the architecture document drifts from the running system within a release. The canonical filenames for the four outline diagrams are `platform-architecture.drawio`, `layered-architecture.drawio`, `system-context.drawio`, and `deployment-architecture.drawio`. The CLI helper at `scripts/arch-drawio.ps1` initialises the templates, exports the PNGs, and verifies the pairs. Failing means a diagram appears in the markdown as a PNG with no `.drawio` source, a `.drawio` source exists for a diagram that the markdown never references, or the four canonical diagrams are not all present.

#### DO

- Place every diagram source as `docs/architecture/diagrams/<name>.drawio` and reference either the rendered `<name>.png` or the `<name>.drawio` file directly from the markdown.

  **Example (pass):** `architecture-outline.md` contains `![Platform diagram](./diagrams/platform-architecture.png)`. The file `docs/architecture/diagrams/platform-architecture.drawio` exists. Running `.\scripts\arch-drawio.ps1 verify` prints `[verify] OK   diagrams/platform-architecture.png -> platform-architecture.drawio exists`.

- Use the canonical filenames for the four outline diagrams so the verify command can confirm all four are present.

  **Example (pass):** `platform-architecture.drawio`, `layered-architecture.drawio`, `system-context.drawio`, `deployment-architecture.drawio` all exist; verify prints PASS.

- Initialise a fresh project's diagrams folder by running `.\scripts\arch-drawio.ps1 init -ProjectRoot <path>` from this skill, which copies the four templates without overwriting existing diagrams (unless `-Force`).

  **Example (pass):** A new project runs `init`, opens each `.drawio` in draw.io Desktop, fills in the `{Placeholder}` text, runs `export`, then `verify` returns PASS.

#### DO NOT

- Embed a screenshot or PNG in the markdown with no matching `.drawio` source on disk.

  **Example (fail):** `architecture-outline.md` references `./diagrams/platform-architecture.png` but `docs/architecture/diagrams/` contains only the PNG — no `.drawio`. The diagram becomes write-only; the next update redraws from scratch.

- Inline a mermaid diagram for the four canonical diagrams in place of a `.drawio` source.

  **Example (fail):** Section 1 of the outline has a fenced ` ```mermaid ` block for the platform diagram. Mermaid is fine for small ad-hoc figures inside mechanism walkthroughs, but the four outline-level diagrams need editable drawio sources so non-developer reviewers (architects, ops) can open and edit them in draw.io Desktop.

- Rename the canonical diagrams so the verify step cannot find them.

  **Example (fail):** A team renames `system-context.drawio` to `context-c4.drawio`. The verify step reports `MISS expected 'system-context' diagram not referenced in outline`. Either keep the canonical name, or update the skill convention and the CLI.

- Ship a `.drawio` source that the markdown never references.

  **Example (fail):** `diagrams/` contains five `.drawio` files; the outline only links to three. The two orphans are documentation rot — either reference them from the outline or delete them.

**Source:** Practice-skill authoring convention (abd-architecture-outline); paired markdown + drawio is what makes the outline maintainable past its first release.

### Rule: Major systems stay at one line

The Major Systems section of the outline lists each subsystem the architecture distinguishes and gives each one **one line of description**. Internal components, mechanisms, data models, and patterns are out of scope — they belong in the blueprint and reference documents. The catalogue exists so a reader can map any feature request or operations alert to a named owner-system in seconds. Failing means a system has a multi-paragraph description, a component list, code references, or an interface contract embedded in the outline.

#### DO

- Render the major systems as a table with three columns: System, One-line description, Primary owner/module.

  **Example (pass):**

  | System | One-line description | Primary owner / module |
  |---|---|---|
  | **Identity** | Authenticates users and issues tokens; thin wrapper over Auth0. | `packages/identity` |
  | **Orders** | Order lifecycle from cart to fulfilment; canonical source of revenue events. | `packages/orders` |

- Make the one-line description a *role-in-the-system* statement, not a feature list.

  **Example (pass):** "Read-mostly product catalogue with strong cache reliance." — names the role and a defining trait.

- Defer all "how" questions about a system to the blueprint or reference document linked from the outline.

  **Example (pass):** The Orders row above says nothing about *how* orders flow through the system; that lives in `architecture-blueprint.md`.

#### DO NOT

- Expand a major system's description into a paragraph about its internal components.

  **Example (fail):**

  | System | Description |
  |---|---|
  | Orders | The Orders system contains an `OrderService`, an `OrderRepository`, an `OrderEventPublisher`, and integrates with the Catalogue system to validate line items. It uses the Saga pattern for distributed transactions and stores events in an outbox table for at-least-once delivery. |

  This is blueprint-level content invading the outline.

- List endpoints, classes, database tables, or message topics in the outline.

  **Example (fail):** A "Notifications" row that lists six event-bus topics and four database tables. The outline should name the system; the blueprint owns the contract.

**Source:** Practice-skill authoring convention (abd-architecture-outline); the outline is deliberately shallow, the blueprint owns components.

### Rule: Outline leads with the four diagrams

The outline answers "what is this system?" through diagrams first and prose second. The first four numbered sections of the outline document must be the **platform diagram**, the **layered architecture diagram**, the **system context diagram**, and the **deployment topology diagram**, in that order, each followed by a caption of three sentences or fewer. Failing means the document opens with paragraphs of prose, has fewer than four diagrams, reorders the four into something else, or ships a diagram with a caption that runs to half a page.

#### DO

- Put the platform diagram, layered diagram, system context diagram, and deployment topology diagram as the first four numbered sections of the outline, each with its own heading.

  **Example (pass):** `architecture-outline.md` headings 1–4 are `## 1. Platform Diagram`, `## 2. Layered Architecture`, `## 3. System Context`, `## 4. Deployment Topology`. Sections 5+ are principles, tech stack, systems, ADRs.

- Limit every caption under a diagram to three sentences or fewer, naming what the reader should see.

  **Example (pass):** Layered diagram caption: "Dependencies point one way only: Presentation depends on Application, Application on Domain, Domain on Infrastructure interfaces (never their implementations). The Domain layer never imports from Infrastructure assemblies."

- Pick one diagram notation and stay consistent inside one outline (all mermaid, or all drawio links, or all PNGs).

  **Example (pass):** All four diagrams are mermaid fenced blocks. Switching is fine across outlines, not within one.

#### DO NOT

- Open the outline with a prose-only "Introduction" or "Background" section before the diagrams appear.

  **Example (fail):** Section 1 of the outline is `## Introduction` with five paragraphs of history. The platform diagram does not appear until section 6.

- Ship the outline with three diagrams (e.g. missing the deployment topology) on the grounds that "we will add it later".

  **Example (fail):** Outline has Platform, Layered, and Context diagrams but no Deployment Topology — readers cannot answer "where does this run?" from the page.

- Caption a diagram with a multi-paragraph essay about the history of the choice.

  **Example (fail):** Layered diagram caption is six paragraphs explaining how we tried hexagonal first; the rationale belongs in an ADR, not the caption.

**Source:** Practice-skill authoring convention (abd-architecture-outline); the outline is "the one-page picture of the system" and four diagrams are its load-bearing content.

### Rule: Principles are decidable one-sentence stances

A guiding principle in the outline is **one sentence** and **decidable against a real code change or design proposal**. It names what the system constrains itself to do, not what every engineer should aspire to. A reviewer should be able to look at a pull request and say "this violates principle 3" or "this is fine under principle 3". Failing means a principle is a paragraph, a slogan, a value statement, or so abstract that no piece of code could ever be measured against it.

#### DO

- State each principle as one declarative sentence naming the constraint and the thing constrained.

  **Example (pass):** "Domain never imports infrastructure — domain classes depend on interfaces; concrete database, HTTP, and message-bus types are referenced only from the Infrastructure layer."

- Give every principle a verifiable surface: a layer, a folder, a code path, or a build-time check.

  **Example (pass):** "Tests run without infrastructure — the full domain and application test suite runs in under 60 seconds with no databases, brokers, or third-party services started." (verifiable by running the suite.)

- Keep the principles list to 5–10 entries. If a candidate cannot fit alongside the others as a peer, it is probably not outline-level.

  **Example (pass):** Eight principles, each fitting on one bullet line plus an optional short clarification clause.

#### DO NOT

- Write a principle as a value statement or slogan that cannot be applied to a code change.

  **Example (fail):** "We value craftsmanship and clean code." — true but undecidable; a reviewer cannot pass/fail a PR with this.

- Use multi-paragraph principles that read like a mini essay.

  **Example (fail):** A principle that is three paragraphs explaining context, options, and consequences — that is an ADR, not a principle.

- Mix principles with implementation rules.

  **Example (fail):** "Use `Result<T, E>` from the `neverthrow` library and avoid `try/catch` except at the HTTP boundary, configuring the library at `src/shared/result.ts`." — this is implementation detail for a rule, not a principle.

**Source:** Practice-skill authoring convention (abd-architecture-outline); principles list is the outline's third load-bearing element.
<!-- execute_rules:bundle_rules:end -->
