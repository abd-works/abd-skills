# {SystemName} — Architecture Outline

> **Status:** Draft / Approved / Superseded by …
> **Owner:** {team-or-person}
> **Last updated:** YYYY-MM-DD
>
> **Purpose.** One-page picture of {SystemName} — what it is, what it sits next to, and the principles that guide every deeper decision. Internals (components, mechanisms, data models, patterns) live in the **architecture blueprint** and **architecture reference** documents linked from section 8.

---

## 1. Platform Diagram

![Platform Architecture]( ./diagrams/platform-architecture.png )

> Source: [`diagrams/platform-architecture.drawio`](./diagrams/platform-architecture.drawio). Edit in draw.io Desktop and re-export with `scripts\arch-drawio.ps1 export`.

**Caption.** {SystemName} is a {form factor — web-plus-API SaaS / desktop client + game / mobile + serverless / etc.}. The client talks to a single API gateway; the API holds all persisted state in {primary store} and uses {secondary stores} for {purpose}.

---

## 2. Layered Architecture

![Layered Architecture]( ./diagrams/layered-architecture.png )

> Source: [`diagrams/layered-architecture.drawio`](./diagrams/layered-architecture.drawio).

**Caption.** Dependencies point one way only: Presentation depends on Application, Application on Domain, Domain on Infrastructure interfaces (never their implementations). The Domain layer never imports from Infrastructure assemblies.

---

## 3. System Context

![System Context]( ./diagrams/system-context.png )

> Source: [`diagrams/system-context.drawio`](./diagrams/system-context.drawio).

**Caption.** Two human actor types interact with {SystemName}. Three external systems are integrated: identity is delegated to {Auth Provider}, transactional email is sent through {Email Provider}, product analytics flow to {Analytics}.

---

## 4. Deployment Topology

![Deployment Topology]( ./diagrams/deployment-architecture.png )

> Source: [`diagrams/deployment-architecture.drawio`](./diagrams/deployment-architecture.drawio).

**Caption.** Production runs in a single AWS region with multi-AZ failover at the data tier. Static assets are CDN-cached at the edge. Staging mirrors production at smaller instance sizes; preview environments are single-container deployments with shared staging data.

---

## 5. Guiding Principles

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

## 6. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Presentation | React | 18.x | SPA framework |
| Presentation | TanStack Query | 5.x | Server-state fetching/caching |
| Application / API | Node.js | 20.x LTS | Runtime |
| Application / API | Fastify | 4.x | HTTP framework |
| Domain | TypeScript | 5.x | Domain modelling language |
| Infrastructure | Postgres | 15.x | Primary data store |
| Infrastructure | Redis | 7.x | Cache + ephemeral state |
| Infrastructure | AWS ECS Fargate | n/a | Container runtime |
| Cross-cutting | OpenTelemetry | 1.x | Tracing + metrics |
| Build / CI | GitHub Actions | n/a | CI/CD |

*(One row per material technology. Omit transitive dependencies, lint configuration, and small utilities.)*

---

## 7. Major Systems

| System | One-line description | Primary owner / module |
|---|---|---|
| **Identity** | Authenticates users and issues tokens; thin wrapper over Auth0. | `packages/identity` |
| **Catalogue** | Read-mostly product catalogue with strong cache reliance. | `packages/catalogue` |
| **Orders** | Order lifecycle from cart to fulfilment; canonical source of revenue events. | `packages/orders` |
| **Notifications** | Outbound email, push, and webhook delivery; consumes order/identity events. | `packages/notifications` |
| **Admin Console** | Internal-only React app for support and ops queries. | `apps/admin` |

*(One row per major system the architecture distinguishes. No internal components, no mechanisms, no patterns — those go in the blueprint and reference.)*

---

## 8. Decision Records

The outline-level decisions are listed below. Each one has a full record at `docs/architecture/decisions/ADR-NNN-{slug}.md` using the [decision-record template](./decision-record.md).

| ID | Decision | One-line consequence |
|---|---|---|
| [ADR-001](../decisions/ADR-001-spa-plus-rest-api-platform.md) | SPA + REST API platform | All client code is browser-side; no server rendering, no GraphQL surface area. |
| [ADR-002](../decisions/ADR-002-layered-clean-architecture.md) | Layered/clean architecture with one-way dependencies | Domain stays portable; mocking infrastructure is free. |
| [ADR-003](../decisions/ADR-003-aws-fargate-deployment.md) | AWS ECS Fargate, single region, multi-AZ | No Kubernetes operations cost; region-failure is an explicit DR scenario. |
| [ADR-004](../decisions/ADR-004-auth0-identity.md) | Outsource identity to Auth0 | No homegrown password store; vendor lock at the identity layer is accepted. |

---

## See also

- [`architecture-blueprint.md`](./architecture-blueprint.md) — second-level: components, mechanisms, data models.
- [`architecture-reference.md`](./architecture-reference.md) — third-level: full mechanism walkthroughs and patterns.
- [`service-level-objectives.md`](./service-level-objectives.md) — non-functional requirements per major system.
