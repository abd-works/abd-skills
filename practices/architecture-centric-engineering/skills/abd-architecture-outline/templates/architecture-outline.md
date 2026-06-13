# {SystemName} — Architecture Outline

> **Status:** Draft / Approved / Superseded by …
> **Owner:** {team-or-person}
> **Last updated:** YYYY-MM-DD
>
> **Purpose.** One-page picture of {SystemName} — what it is, what it sits next to, the platform technology each system commits to, the mechanisms that address cross-cutting concerns, and the principles that guide every deeper decision. Deployment and platform runtime detail live in the **architecture blueprint** linked from section 5.

---

## 1. System Context

![System Context]( ./diagrams/system-context.png )

> Source: [`diagrams/system-context.drawio`](./diagrams/system-context.drawio).
> Element inventory: [`diagrams/system-context-elements.md`](./diagrams/system-context-elements.md)

**Caption.** {Two or three sentences: who uses the system, which external systems integrate, and the dominant protocol pattern across boundaries.}

### Systems

Each entry below summarises the functions and platform technology for one owned system. Full element descriptions are in the inventory file above.

#### {System A Name}

{What it is and its primary job.}

**Functions:** {function 1} · {function 2} · {function 3} · {function 4}

**Tech:** {runtime · framework} | **Persistence:** {database} | **Libs / tools:** {key libraries, observability, build}

#### {System B Name}

{What it is and its primary job.}

**Functions:** {function 1} · {function 2} · {function 3}

**Tech:** {runtime · framework} | **Persistence:** {database} | **Libs / tools:** {key libraries, observability, build}

*(One subsection per owned system. Mirror the element inventory — do not introduce systems not in the diagram.)*

---

## 2. Architecture Mechanisms

The mechanisms below are the cross-cutting concerns the architecture commits to. Each entry states the **technology or platform choice**, a **paragraph or two** on how it works at this level, and the **key non-functional requirement or justification** that drove the choice. Mechanisms that are novel or context-specific to this system are included alongside the standard set.

### 2.1 Security

**Technology choice:** {Auth provider / JWT / mTLS / API gateway policy / etc.}

{Paragraph 1: what the mechanism protects, who controls identity, where in the request pipeline authentication and authorisation occur.}

{Paragraph 2 (if warranted): key NFR or constraint that shaped this choice — e.g. compliance requirement, zero-trust policy, multi-tenancy boundary.}

### 2.2 Error Handling & Resilience

**Technology choice:** {Result type / circuit-breaker library / retry policy / dead-letter queue / etc.}

{How failures are represented and propagated. Where the boundary between domain errors and infrastructure errors lies. How the system degrades under partial failure.}

{Key NFR: availability target, acceptable degradation, or recovery time objective that justifies the approach.}

### 2.3 Logging & Observability

**Technology choice:** {Logging library · trace provider · metrics sink — e.g. Pino + OpenTelemetry → Datadog}

{What is captured, at what level, and how correlation IDs cross system boundaries. Whether structured or unstructured log output.}

{Key NFR: MTTR target, audit requirement, or regulatory constraint that drove the choice.}

### 2.4 Validation

**Technology choice:** {Schema library · validation framework — e.g. Zod, Joi, Bean Validation, Pydantic}

{Where validation runs (edge vs domain), what it protects against, and how validation failures surface to callers.}

### 2.5 Configuration & Secrets

**Technology choice:** {Config source — e.g. AWS Secrets Manager · Vault · environment variables via dotenv}

{When config is read (startup vs runtime), how secrets are rotated, and what code is and is not allowed to read `process.env` / equivalent directly.}

### 2.6 Caching

**Technology choice:** {Cache technology and pattern — e.g. Redis write-through, in-process LRU, CDN edge cache}

{What is cached, for how long, and how cache invalidation is handled. Any consistency guarantees or explicitly accepted staleness.}

{Key NFR: latency budget or throughput target that makes caching necessary.}

### 2.7 Persistence

**Technology choice:** {Database technology and access pattern — e.g. PostgreSQL via repository pattern, DynamoDB single-table}

{How data ownership boundaries are enforced, how cross-aggregate consistency is handled, and whether the system uses an outbox or saga pattern.}

### 2.8 Communication

**Technology choice:** {Synchronous: REST / gRPC / GraphQL. Async: AMQP broker / Kafka / SNS+SQS / etc.}

{How systems and components communicate — synchronous protocols for reads and writes, async messaging for events and long-running processes. Contract versioning approach if any.}

### 2.{N} {Bespoke Mechanism Name} *(if applicable)*

**Technology choice:** {Named tool, library, or platform capability}

{1–2 paragraphs: what problem this addresses that the standard mechanisms do not, and the NFR or constraint that makes it necessary in this specific context.}

*(Add one subsection per additional novel or bespoke mechanism. Remove this placeholder when none is needed.)*

---

## 3. Guiding Principles

The principles below are the one-sentence stances that govern every deeper architectural decision. Each one is decidable against a real piece of code or a design proposal.

- **Domain never imports infrastructure.** Domain classes depend on interfaces; concrete database / HTTP / message-bus types are referenced only from the Infrastructure layer.
- **All cross-system I/O crosses a named seam.** Every interaction with an external system happens through a project-owned interface so it can be stubbed in tests.
- **Errors are values until the boundary.** Failures are returned as `Result<T, E>` (or equivalent) through the application; exceptions only cross the HTTP boundary.
- **One write, one event.** Every state-changing operation emits a domain event before returning; downstream concerns (audit, analytics, cache invalidation) subscribe.
- **Tests run without infrastructure.** The full domain and application test suite runs in under 60 seconds with no databases, brokers, or third-party services started.
- **Configuration is read once at startup.** No `process.env` outside the composition root; everything else receives configuration through injection.
- **Migrations are forward-only and reversible.** A failed deploy must be recoverable by deploying the previous version without manual data fixes.

*(Keep 5–10 principles. Each one must be one sentence, must be decidable, and must name what it constrains.)*

---

## 4. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Presentation | React | 18.x | SPA framework |
| Presentation | TanStack Query | 5.x | Server-state fetching/caching |
| Application / API | Node.js | 20.x LTS | Runtime |
| Application / API | Fastify | 4.x | HTTP framework |
| Domain | TypeScript | 5.x | Domain modelling language |
| Infrastructure | Postgres | 15.x | Primary data store |
| Infrastructure | Redis | 7.x | Cache + ephemeral state |
| Cross-cutting | OpenTelemetry | 1.x | Tracing + metrics |
| Build / CI | GitHub Actions | n/a | CI/CD |

*(One row per material technology. Omit transitive dependencies, lint configuration, and small utilities.)*

---

## 5. Major Systems

| System | One-line description | Primary owner / module |
|---|---|---|
| **{System A}** | {What it does in one line.} | `{packages/system-a}` |
| **{System B}** | {What it does in one line.} | `{packages/system-b}` |

*(One row per major system the architecture distinguishes. No internal components, no mechanisms, no patterns — those go in the blueprint and reference.)*

---

## 6. Decision Records

The outline-level decisions — including mechanism choices — are listed below. Each one has a full record at `docs/architecture/decisions/ADR-NNN-{slug}.md` using the [decision-record template](./decision-record.md).

| ID | Decision | One-line consequence |
|---|---|---|
| [ADR-001](../decisions/ADR-001-spa-plus-rest-api-platform.md) | SPA + REST API platform | All client code is browser-side; no server rendering, no GraphQL surface area. |
| [ADR-002](../decisions/ADR-002-auth0-identity.md) | Auth0 for identity | No homegrown password store; vendor lock at the identity layer is accepted. |
| [ADR-003](../decisions/ADR-003-result-types-not-exceptions.md) | Domain returns `Result<T, E>`, not exceptions | Failure handling is type-checked; the HTTP boundary is the only translator. |
| [ADR-004](../decisions/ADR-004-redis-write-through-cache.md) | Redis write-through cache for catalogue | Predictable freshness at accepted write overhead. |

*(Mechanism choices produce ADRs here. Blueprint-level decisions — component boundaries, test-tier vocabulary — continue numbering in the blueprint.)*

---

## See also

- [`architecture-blueprint.md`](./architecture-blueprint.md) — second-level: platform runtime, deployment topology, components, deeper mechanism walkthrough, data models.
- [`architecture-reference.md`](./architecture-reference.md) — third-level: full mechanism walkthroughs and patterns.
- [`service-level-objectives.md`](./service-level-objectives.md) — non-functional requirements per major system.
