---
name: bounded-context-map
catalog_garden_order: 8
description: >-
  Map bounded contexts and their relationships so integration strategy, team
  collaboration, and domain translation are explicit before they are discovered
  in production.
---
# bounded-context-map

## Purpose

Teams working across multiple models, services, or subsystems need a single shared picture of how those pieces relate — which concepts cross boundaries, how the systems talk to each other, and how the teams will collaborate. Without that picture, integration strategy is discovered in production, translation is ad hoc, and team dependencies are invisible until they block someone. This skill produces a **Bounded Context Map**: a named inventory of every bounded context with every dependency declared across three explicit dimensions — domain mapping, integration mechanism, and team engagement model — so the architecture is honest and the team structure matches.

---

## When to use this skill

Load this skill when **any** of the following apply:

- Module or service boundaries exist and the team needs to declare **how they relate and integrate** rather than leaving relationships implicit.
- **Multiple teams** own different parts of the domain and need a shared record of dependencies, integration mechanisms, and collaboration patterns.
- The system has or will have **inter-service boundaries** (microservices, bounded subsystems, legacy integrations) and the integration patterns must be explicit before development begins.
- An **architecture review** requires a global view of model contexts, their points of contact, and the translation strategy at each boundary.

---

## Core concepts

### Bounded context

A **bounded context** is an explicitly set boundary in which a model applies and is managed to be uniform. It has two facets:

- **Organizational** — the team, department, or community responsible for the model.
- **Implementation** — the code base, database schema, or deployable unit that embodies the model.

Within a bounded context, every term in the model has one meaning. Across boundaries, the same word may mean something different — and that difference is either managed or it becomes a defect. Two failure modes signal missing or misdrawn boundaries:

- **Duplicate concepts** — two model elements represent the same real-world thing, forcing double updates and conversion logic.
- **False cognates** — two teams use the same term but mean different things, leading to contradictory code, confused databases, and miscommunication.

### Bounded context map

A **bounded context map** is a global view of all the model contexts in a project and the relationships between them. It marks the boundaries, determines integration strategies, identifies where contexts may be shared across teams, and may span an entire system, a portion of a system, or across several systems within the enterprise.

Creating a context map follows three steps:

1. **Identify** each model in play on the project and define its bounded context.
2. **Name** each bounded context and include the names in the ubiquitous language of the business domain model.
3. **Describe** the points of contact between the models, outlining explicit translation for any communication.

### Three dimensions per dependency

Every dependency between two bounded contexts must be declared across three dimensions. Leaving any dimension implicit is a gap the team will pay for later.

1. **Domain mapping** — which domain constructs or objects are relevant across more than one bounded context; how the specific elements in each context relate to each other and what translation is required at the boundary.

2. **Integration mechanism** — how the systems actually communicate: Events, Messaging, REST/API, Batch, Shared DB, File Transfer, or a Shared Kernel codebase. The mechanism constrains consistency, latency, and coupling.

3. **Team engagement model** — how the teams that own the two contexts will collaborate when changes are needed:
   - **Travelling Team Members** — members from multiple teams work as a single team (for significant changes).
   - **Service Provider** — one team makes changes according to the needs of the other team (for small changes).
   - **Enabler** — one team provides tools or APIs the other team uses self-service (for no-change integration).

### Relationship patterns

The relationship between two bounded contexts takes one of several named patterns. Each pattern encodes a different trade-off between autonomy and coupling. Choosing the right one depends on team structure, power dynamics, and how much model divergence the business can tolerate.

- **Shared Kernel** — a subset of the domain model that two teams agree to share, including associated code and data. No changes to the shared subset without consultation. Use when tight integration is needed and the teams can sustain the communication overhead.

- **Customer/Supplier** — one subsystem feeds another; all dependencies go one way. The downstream team plays the customer role, negotiating requirements. Both teams jointly develop automated acceptance tests to validate the interface.

- **Conformist** — the downstream team gives up on an independent model and slavishly adheres to the upstream team's model. Simplifies integration enormously but cramps downstream design. Often appropriate when consuming enterprise packages (ERP, CRM) that require only moderate customization.

- **Anticorruption Layer** — an isolation layer that provides clients with functionality in terms of their own domain model, translating in both directions between the two models. Use when a new system must interface with a large or messy legacy system without letting the legacy model pollute the new design.

- **Open Host Service / Published Language** — a common protocol published as a set of services, open to all who need to integrate. Often paired: the open host defines the access; the published language defines the shared vocabulary. Aligns with service-oriented architecture principles.

- **Separate Ways** — no integration. The bounded context has no connection to the others, allowing developers to find simple, specialized solutions within a small scope.

### Choosing and transforming boundaries

Drawing a context map is not a one-time event. Boundaries shift as teams grow, systems evolve, and business needs change. Several heuristics help:

- **Larger vs smaller** — larger bounded contexts make the model more coherent and the flow between user tasks smoother, but increase communication overhead. Smaller contexts reduce communication, keep models less abstract, and can be tailored to special needs. A practical upper bound is roughly ten people per bounded context.
- **External systems** — three patterns typically apply: Separate Ways (no integration needed), Conformist (adopt their model), or Anticorruption Layer (insulate from their model).
- **Internal boundaries** — watch for informal sharing that signals two teams are not in the same context but think they are. Formalize the relationship with a Shared Kernel or Customer/Supplier pattern.
- **Transformation** — when initial boundary decisions change, ensure the current situation is fully understood, the end result is clearly defined, and processes are in place to execute the transformation without disrupting neighbouring contexts.

---

## Agent Instructions

1. **Templates**

Generate content using **every** template file in this skill's `templates/` folder.

| Template | What to produce |
| -------- | --------------- |
| `templates/bounded-context-map-template.md` | A single `bounded-context-map.md` file under `<active_skill_workspace>/` — inventory of bounded contexts, dependency arcs with three dimensions each, decisions and tensions. |

2. **Rules**

Follow the normative `rules/` prose bundled at the end of this `SKILL.md`. After generating content, act as a peer reviewer: walk each rule, read its DO and DO NOT, and check for concrete violations.

3. **Who is checking**

A **solution architect or delivery lead** — someone who needs the map to be honest about dependencies, integration costs, and team collaboration before committing to a delivery plan. They read the map and ask: *can I trust that every cross-boundary dependency has an explicit integration strategy and team engagement model, or are there hidden couplings?*

---

## Build

1. **Identify every bounded context in scope.** Walk the domain models, module boundaries, team structures, and system landscape. For each bounded context, record its name, the owning team, a one-sentence scope description, and an implementation note (monolith module, microservice, shared library, legacy system, external vendor).

2. **Map every dependency between contexts.** For each pair of contexts that interact, declare all three dimensions: what domain concepts cross the boundary (domain mapping), how the systems communicate (integration mechanism), and how the teams will collaborate (team engagement model with named pattern and direction).

3. **Choose relationship patterns deliberately.** For each dependency, select the named pattern that fits — Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host/Published Language, or Separate Ways — and record the rationale. If no pattern fits cleanly, record the tension.

4. **Record decisions and tensions.** Open questions, contested boundaries, deferred integrations, and transformation plans go in a dedicated section so they are visible, not buried in footnotes.

5. **Apply the rules, then review like a peer.** Walk the bundled `rules/` at the end of this file against the completed map. Fix violations before declaring done.

6. **Keep the bundled rules block honest.** After changing any `rules/*.md`, run the bundle script:

```bash
python skills/execute-skill-using-skills-rules/scripts/bundle_rules_into_skill_md.py \
  --skill-root skills/domain-driven-design/abd-bounded-context-map
```

---

## Validate

**Goal:** Inspect the completed bounded context map as a reviewer, not a second authoring pass.

- **Who is checking:** A solution architect who will use the map to plan integration work and allocate team capacity. A delivery lead who needs to know which teams must coordinate and when.
- **Completeness** — every bounded context in the system appears in the inventory with owning team and scope.
- **Three dimensions** — every dependency arc has all three dimensions filled: domain mapping, integration mechanism, and team engagement model. No blanks, no "TBD" without a follow-up action.
- **Named patterns** — every team engagement model uses a recognized pattern from the DDD/ABD catalogue (Shared Kernel, Customer/Supplier, Conformist, ACL, Open Host/Published Language, Separate Ways) or a named team collaboration model (Travelling Team Members, Service Provider, Enabler).
- **Direction** — every dependency states the direction explicitly: upstream/downstream, mutual, or standalone.
- **No orphans** — every bounded context participates in at least one dependency or is explicitly declared standalone with a rationale.
- **Decisions and tensions** — open questions, contested boundaries, and deferred integrations are recorded, not hidden.
- **Consistency with domain language** — bounded context names appear in the project's ubiquitous language; the map does not introduce unnamed or ad hoc context labels.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Direction stated per dependency — upstream, downstream, or mutual

Every dependency arc must explicitly state the direction of the relationship: which context is upstream (the supplier of data or capability), which is downstream (the consumer), or whether the relationship is mutual. Without direction, the reader cannot tell who depends on whom, who has the power to change the interface, and who bears the translation burden. Failure is a dependency arc with no direction field, or a direction that uses vague language instead of explicitly naming upstream and downstream.

#### DO

- State direction using explicit upstream/downstream language that names which context is which.

  **Example (pass):**

  ```
  - Direction: Trading is upstream; Front Page is downstream
  ```

- For mutual relationships where both contexts supply and consume from each other, state "mutual" and explain what flows in each direction.

  **Example (pass):**

  ```
  - Direction: mutual — Inventory pushes stock levels to Order Management; Order Management pushes reservation requests to Inventory
  ```

- For standalone contexts (Separate Ways pattern), the direction is "none" — but this belongs in the Standalone Contexts section, not in a dependency arc.

  **Example (pass):**

  ```
  ## Standalone Contexts

  ### Analytics Warehouse
  Standalone — Separate Ways. No runtime dependency; consumes read-only replicas outside the operational model.
  ```

#### DO NOT

- Omit the direction field from a dependency arc.

  **Example (fail):**

  ```
  ### Trading → Invoice
  - Domain mapping: deal identifiers
  - Integration mechanism: Batch
  - Team engagement model: Conformist
  ```

  No direction field — the reader must guess who depends on whom.

- Use vague direction language that does not name the upstream and downstream contexts.

  **Example (fail):**

  ```
  - Direction: one-way
  ```

  "One-way" does not say which context is upstream and which is downstream.

- Use arrow notation in the heading as a substitute for the direction field — the heading is a label, not the specification.

  **Example (fail):**

  ```
  ### Trading → Invoice
  ```

  The arrow in the heading suggests direction, but without an explicit Direction field, a reviewer cannot confirm it was a deliberate choice.

### Rule: Every dependency has three dimensions — domain mapping, integration mechanism, team engagement

Every dependency arc in `bounded-context-map.md` must record all three dimensions: what domain concepts cross the boundary, how the systems communicate, and how the teams collaborate. A complete dependency means no reviewer has to guess at any of the three. Failure is a dependency row with one or more dimensions missing, blank, or filled with only a placeholder.

#### DO

- Fill all three dimension fields for every dependency arc: **Domain mapping**, **Integration mechanism**, and **Team engagement model**.

  **Example (pass):**

  ```
  ### Trading → DCF — Front Page
  - Direction: Trading is upstream; Front Page is downstream
  - Domain mapping: Deal information and counterparty details flow into Front Page for case aggregation
  - Integration mechanism: REST/API (via Filing and Communications Service)
  - Team engagement model: Anticorruption Layer — Service Provider
  ```

- When a dimension is genuinely undecided, write a specific follow-up action with an owner and target date rather than leaving the field blank.

  **Example (pass):**

  ```
  - Integration mechanism: TBD — decision pending POC results from API team. Owner: Sarah. Target: Sprint 12.
  ```

#### DO NOT

- Leave any of the three dimension fields blank or missing from a dependency arc.

  **Example (fail):**

  ```
  ### Trading → Front Page
  - Direction: upstream/downstream
  - Domain mapping: deal data
  ```

  Integration mechanism and team engagement model are absent — the arc is incomplete.

- Use generic placeholders like "TBD" or "various" without a named owner and resolution date.

  **Example (fail):**

  ```
  - Integration mechanism: TBD
  - Team engagement model: TBD
  ```

  No owner, no target date — the placeholder will never be resolved.

**Source:** Kept chunk #7 in `inputs/abd-answers-retrieval.md` — ABD three-dimension dependency model (DDD Training slide 66, EWMA slide 6).

### Rule: Integration mechanism names a concrete approach

The integration mechanism on every dependency arc must name a concrete, implementable communication approach — not a vague category or a deferred placeholder. The mechanism constrains consistency, latency, coupling, and operational complexity; leaving it vague means the architecture is not actually decided. Failure is a dependency whose integration mechanism is missing, says only "TBD" without a follow-up action, or uses a label too broad to implement ("various", "as needed").

#### DO

- Name a specific mechanism from the recognized catalogue: Events, Messaging, REST/API, Batch, Shared DB, File Transfer, or Shared Kernel codebase.

  **Example (pass):**

  ```
  - Integration mechanism: Messaging (message queue for inbound/outbound business messages)
  ```

- Add a brief qualifier when it clarifies the implementation (protocol, transport, frequency).

  **Example (pass):**

  ```
  - Integration mechanism: Batch (nightly extract from Trading into Invoice ledger)
  ```

- When the mechanism is genuinely undecided, state what is blocking the decision, who owns it, and when it will be resolved.

  **Example (pass):**

  ```
  - Integration mechanism: TBD — choosing between Events and REST/API pending latency requirements from Product. Owner: Tech Lead. Target: Sprint 14.
  ```

#### DO NOT

- Leave the integration mechanism field blank or missing.

  **Example (fail):**

  ```
  ### Trading → Invoice
  - Direction: upstream/downstream
  - Domain mapping: deal identifiers and pricing terms
  - Team engagement model: Conformist — Service Provider
  ```

  Integration mechanism is absent — the arc does not say how the systems actually talk.

- Use a label that is too broad to implement without further decisions.

  **Example (fail):**

  ```
  - Integration mechanism: various
  ```

  "Various" is not a mechanism — it defers every question about consistency, latency, and coupling.

- Write "TBD" without a named owner and resolution target.

  **Example (fail):**

  ```
  - Integration mechanism: TBD
  ```

  No owner, no timeline — the placeholder will persist indefinitely.

**Source:** Kept chunk #7 in `inputs/abd-answers-retrieval.md` — ABD three-dimension dependency model lists Events, Batch, Messaging, REST/API as the integration mechanism catalogue.

### Rule: No orphan contexts — every bounded context participates or is declared standalone

Every bounded context listed in the inventory must either appear in at least one dependency arc (as source or target) or be explicitly declared as **standalone** with a rationale in the Standalone Contexts section. A floating context with no arcs and no standalone declaration is a gap — the reviewer cannot tell whether it was forgotten or intentionally isolated. Failure is a bounded context that appears in the inventory but nowhere in the Dependencies or Standalone Contexts sections.

#### DO

- Ensure every bounded context name from the inventory appears as either a source or target in at least one dependency arc.

  **Example (pass):**

  Inventory lists: Supply Operation, Trading, Invoice, Communication Gateway, DCF Folder, DCF Front Page. Each appears in at least one arc under Dependencies.

- When a bounded context genuinely has no integration with others, declare it in the Standalone Contexts section with a rationale.

  **Example (pass):**

  ```
  ## Standalone Contexts

  ### Reporting Data Warehouse
  Standalone. Consumes nightly batch extracts but has no runtime integration with other contexts.
  Rationale: read-only analytics; no domain model coupling. Separate Ways pattern applies.
  ```

#### DO NOT

- List a bounded context in the inventory without it appearing in any dependency arc or the Standalone Contexts section.

  **Example (fail):**

  Inventory lists five contexts. Dependencies section has arcs for only four of them. The fifth context does not appear anywhere else in the document — the reader cannot tell if it was forgotten or intentionally left out.

- Assume that "no arc means standalone" without explicitly stating it in the Standalone Contexts section.

  **Example (fail):**

  ```
  ## Standalone Contexts

  No standalone contexts.
  ```

  But the Notification Service context from the inventory has no dependency arcs — the statement contradicts the evidence.

### Rule: Relationship pattern from the DDD/ABD catalogue

The team engagement model on every dependency arc must name a recognized pattern from the DDD strategic patterns catalogue or the ABD team collaboration models. Ad hoc labels ("we'll figure it out", "hybrid approach", "loose coupling") do not encode the specific trade-offs each named pattern carries. Failure is a dependency whose team engagement model uses an invented label instead of a named pattern.

#### DO

- Name one of the recognized **DDD relationship patterns** for each dependency: Shared Kernel, Customer/Supplier, Conformist, Anticorruption Layer, Open Host Service/Published Language, or Separate Ways.

  **Example (pass):**

  ```
  - Team engagement model: Anticorruption Layer — Front Page isolates itself from the legacy Supply Operation model
  ```

- When the arc also has a **team collaboration model**, name it from the ABD catalogue: Travelling Team Members, Service Provider, or Enabler.

  **Example (pass):**

  ```
  - Team engagement model: Customer/Supplier — Travelling Team Members (significant change requires cross-team pairing)
  ```

- When two patterns apply (a DDD relationship pattern plus an ABD team collaboration model), name both explicitly.

  **Example (pass):**

  ```
  - Team engagement model: Open Host Service / Published Language — Enabler (Gateway team provides transport; DCF team consumes self-service)
  ```

#### DO NOT

- Use ad hoc labels that do not appear in the DDD or ABD catalogues.

  **Example (fail):**

  ```
  - Team engagement model: loose coupling with occasional syncs
  ```

  "Loose coupling with occasional syncs" is not a named pattern — it hides the actual power dynamic and collaboration commitment.

- Name only a team collaboration model without the DDD relationship pattern (or vice versa) when both are relevant.

  **Example (fail):**

  ```
  - Team engagement model: Service Provider
  ```

  Service Provider describes team collaboration but does not say whether the relationship is Customer/Supplier, Conformist, or something else. Both dimensions are needed.

**Source:** Kept chunk #2 in `inputs/abd-answers-retrieval.md` — seven relationship patterns (Evans); Kept chunk #9 — ABD Model Sharing Patterns catalogue; Kept chunk #7 — ABD team engagement models.
<!-- execute_rules:bundle_rules:end -->
