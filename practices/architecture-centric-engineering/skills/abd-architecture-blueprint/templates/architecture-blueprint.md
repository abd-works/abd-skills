# {SystemName} — Architecture Blueprint

> **Status:** Draft / Approved
> **Owner:** {team-or-person}
> **Last updated:** YYYY-MM-DD
>
> **Purpose.** Second-level architecture document for {SystemName}, building on `architecture-outline.md`. Shows the platform runtime, deployment topology, and per-OS environment picture. Names every architectural component. Deepens each mechanism from the outline — now in terms of which components interact, how the mechanism participates in deployment, and what the platform runtime provides. Sketches the data architecture and captures the common testing strategy. Decision records continue from the outline.

---

## 1. Scope

This blueprint extends [`architecture-outline.md`](./architecture-outline.md). Deep mechanism walkthroughs — code, sequence diagrams, test code, file structures — defer to [`architecture-reference.md`](./architecture-reference.md). Outline-level concerns (system-context diagram, functions and tech per system, mechanism technology choices, layered diagram, guiding principles, tech stack table, major systems catalogue, mechanism-choice ADRs) stay in the outline and are not repeated here.

---

## 2. Platform Architecture

![Platform Architecture]( ./diagrams/platform-architecture.png )

> Source: [`diagrams/platform-architecture.drawio`](./diagrams/platform-architecture.drawio). Edit in draw.io Desktop and re-export with `scripts\arch-drawio.ps1 export`.
> Element inventory: [`diagrams/platform-architecture-elements.md`](./diagrams/platform-architecture-elements.md)

**Caption.** {Describe the platform runtime in two to three sentences: client apps, backend services, data stores, CDN/edge, and the major third-party integrations. Name the runtime technologies and how the pieces connect.}

### Runtime components

| Component | Technology | Role |
|---|---|---|
| {Client app name} | {React / iOS / Android / etc.} | {User-facing purpose} |
| {Backend service name} | {Node.js/Fastify / Spring Boot / Django / etc.} | {Request handling role} |
| {Data store name} | {PostgreSQL / MongoDB / DynamoDB / etc.} | {What is persisted here} |
| {Cache / broker} | {Redis / Kafka / SQS / etc.} | {Role in the platform} |
| {CDN / edge} | {CloudFront / Cloudflare / etc.} | {What is cached or proxied} |

---

## 3. Deployment Topology

![Deployment Topology]( ./diagrams/deployment-architecture.png )

> Source: [`diagrams/deployment-architecture.drawio`](./diagrams/deployment-architecture.drawio).
> Element inventory: [`diagrams/deployment-architecture-elements.md`](./diagrams/deployment-architecture-elements.md)

**Caption.** {Describe the deployment topology in two to three sentences: where production runs, the redundancy model, and how staging and preview environments relate.}

### Environments

| Environment | Host / provider | Availability | Purpose |
|---|---|---|---|
| Production | {AWS / GCP / Azure / on-prem · region} | {99.9% / multi-AZ / etc.} | Live traffic |
| Staging | {Single-AZ mirror / same provider} | Best-effort | Pre-release testing |
| {Preview / Dev} *(if applicable)* | {Ephemeral / shared staging} | On-demand | PR previews / local dev |

### Operating systems *(if more than one)*

| Node / container | OS / runtime image | Notes |
|---|---|---|
| {API containers} | {Amazon Linux 2023 / Ubuntu 22.04 / Alpine} | {Why this OS — e.g. minimal attack surface, FIPS compliance} |
| {Worker containers} | {OS image} | {Notes} |
| {Database managed service} | {Managed by provider — no OS access} | n/a |

*(Omit this sub-section when all containers share a single OS image.)*

---

## 4. Components

Each subsection takes one major system from the outline and names its 2–4 components. Each component description covers **purpose**, **dependencies**, and **interactions** — no internal structure, no class lists, no method tables.

![Component Overview]( ./diagrams/component-overview.png )

> Source: [`diagrams/component-overview.drawio`](./diagrams/component-overview.drawio). Edit in draw.io Desktop and re-export with `scripts\arch-drawio.ps1 export`. The diagram captures the same information as the subsections below; keep them in sync.

### 4.1 {System A} components

#### {ComponentName}

**Purpose.** {What this component is responsible for within the system.}

**Dependencies.** {Interfaces and collaborators it receives through injection. Which platform services or data stores it uses.}

**Interactions.** {How it is called, what it calls, what events it publishes or subscribes to. Reference any mechanism it participates in — e.g. "all calls to external HTTP go through the Resilience mechanism's `Resilient<T>` wrapper" or "persisted writes go through the Persistence mechanism's outbox helper".}

#### {ComponentName}

**Purpose.** {What this component is responsible for.}

**Dependencies.** {Interfaces and collaborators.}

**Interactions.** {How it is called and what it calls.}

### 4.2 {System B} components

#### {ComponentName}

**Purpose.** {What this component is responsible for.}

**Dependencies.** {Interfaces and collaborators.}

**Interactions.** {How it is called and what it calls.}

---

## 5. Architecture Mechanisms — Detail

The outline names each mechanism and states its technology choice and NFR justification. This section repeats every mechanism but goes deeper: it names the **components that participate**, references the **platform or deployment specifics** that shape the mechanism, and describes how the mechanism **behaves at runtime** in this system. Novel or bespoke mechanisms introduced in the outline are described here at the same depth as the standard set.

### 5.1 Security

**Outline reference:** {ADR-NNN — auth technology chosen}

**Participating components:** {IdentityService, API middleware, …}

**Platform / deployment detail.** {Where secrets are stored at rest (e.g. AWS Secrets Manager, Vault). How the identity provider integrates with the platform — e.g. Auth0 SDK loaded in the backend service container; JWT public keys cached in Redis. Load-balancer or API-gateway policy if any.}

**Runtime behaviour.** {Step-by-step token lifecycle: token issuance, request validation, role-claims extraction, per-component Principal propagation. Which component enforces what check. What happens on token expiry or revocation.}

**Component interactions.** {How IdentityService calls Auth0 over HTTPS at login. How the API middleware validates tokens on every request and passes a `Principal` downstream. How domain services receive the `Principal` through method arguments rather than thread-local or ambient context.}

---

### 5.2 Error Handling & Resilience

**Outline reference:** {ADR-NNN — Result type / circuit-breaker choice}

**Participating components:** {All application-layer services, API error translator, external HTTP adapters}

**Platform / deployment detail.** {How the circuit-breaker state is tracked — in-process per container replica, or centralised in Redis. How dead-letter behaviour maps to an SQS / database outbox queue. Health-check endpoints used by the load balancer to route around degraded replicas.}

**Runtime behaviour.** {`Result<T, DomainError>` returned through the domain and application layers. `ErrorTranslator` at the API edge maps domain error codes to HTTP status codes. `Resilient<T>` wrapper around every external call: retry with exponential backoff, circuit breaker per named dependency.}

**Component interactions.** {OrderService returns `Result<Order, OrderError>` to the API controller. API controller passes it to `ErrorTranslator`. `CatalogueAdapter` wraps all Catalogue HTTP calls in `Resilient<CatalogueResponse>`; breaker state stored in Redis so all replicas share the same open/closed state.}

---

### 5.3 Logging & Observability

**Outline reference:** {ADR-NNN — logging/tracing stack}

**Participating components:** {All components — logging is cross-cutting}

**Platform / deployment detail.** {Log aggregation target (CloudWatch, Datadog, ELK). Trace collector sidecar or OpenTelemetry Collector deployment. Dashboard and alerting tooling.}

**Runtime behaviour.** {Correlation ID injected at the API edge and propagated as a W3C `traceparent` header across all internal and external HTTP calls. Each component logs at INFO on public-method entry/exit and at WARN/ERROR on non-success `Result`. Metrics emitted through OpenTelemetry SDK; spans cover every cross-component call.}

**Component interactions.** {Logging middleware injects `correlationId` into the request context. Components receive the logger/tracer through constructor injection. External adapters emit a span for each outbound call, tagging HTTP status and latency.}

---

### 5.4 Validation

**Outline reference:** {ADR-NNN — schema/validation library}

**Participating components:** {API layer (edge schemas), domain services (business rules)}

**Platform / deployment detail.** {Whether schemas are shared as a published package between API and client. How schema versioning is handled in CI.}

**Runtime behaviour.** {Zod (or equivalent) schemas parse and validate every inbound request body and query at the API edge; invalid input returns a 422 with a structured error list before reaching the application layer. Business-rule validation inside domain services returns `Result` failures.}

**Component interactions.** {API route handler calls `RequestSchema.parse(body)`; on success it passes a typed DTO to the application service. Domain service calls domain validator helpers that return `Result<void, ValidationError>`.}

---

### 5.5 Configuration & Secrets

**Outline reference:** {ADR-NNN — config source}

**Participating components:** {Bootstrap / composition root, all components that receive config}

**Platform / deployment detail.** {Which secrets store is used per environment. How container task definitions reference secret ARNs. Secret-rotation approach — re-deploy vs in-process refresh.}

**Runtime behaviour.** {`Bootstrap.loadConfig()` called once at container startup. Secrets pulled from AWS Secrets Manager (or equivalent) at boot time. Frozen `Config` object injected into every component constructor. No `process.env` calls outside the composition root.}

**Component interactions.** {Bootstrap reads all config and secret values, constructs the `Config` record, and passes it into the dependency injection container. Components receive config through constructor injection; none read environment variables directly.}

---

### 5.6 Caching

**Outline reference:** {ADR-NNN — cache technology and pattern}

**Participating components:** {Components that read or write cached data — e.g. CatalogueService, IdentityService}

**Platform / deployment detail.** {Redis cluster topology in each environment (standalone, sentinel, cluster mode). How Redis TLS and auth token are injected. Eviction policy and memory configuration.}

**Runtime behaviour.** {Write-through: cache is updated atomically with the primary store write. Cache-aside fallback for read-heavy paths where write-through is not practical. TTL and explicit invalidation for each key namespace.}

**Component interactions.** {`CatalogueService.getProduct(sku)` checks `IProductCache`; on miss reads `IProductRepository` and fills the cache. `CatalogueAdminService.updateProduct(sku, …)` writes to Postgres and calls `IProductCache.invalidate(sku)` in the same transaction to prevent stale reads.}

---

### 5.7 Persistence

**Outline reference:** {ADR-NNN — persistence pattern}

**Participating components:** {All repository components, outbox publisher if present}

**Platform / deployment detail.** {Database server configuration per environment (multi-AZ, connection pooler, replica for reads). Migration toolchain and how it runs in CI and on deploy. Backup and restore policy.}

**Runtime behaviour.** {Each aggregate root has exactly one repository; no component writes to another's aggregate. The outbox pattern (if used): state-change row and event row committed in a single Postgres transaction; a background poller publishes pending events and marks them delivered.}

**Component interactions.** {`OrderService` calls `IOrderRepository.save(order)`, which commits the `orders` row and inserts an `outbox_events` row in one transaction. The `OutboxPublisher` background worker polls the `outbox_events` table and calls `IEventPublisher.publish(event)` for each pending row.}

---

### 5.8 Communication

**Outline reference:** {ADR-NNN — synchronous protocol and async bus choice}

**Participating components:** {All components that call external systems or publish/consume events}

**Platform / deployment detail.** {Message broker deployment — managed service (SQS, EventBridge, Confluent) or self-hosted Kafka in the cluster. Topic and queue naming conventions. Dead-letter queue configuration.}

**Runtime behaviour.** {Synchronous REST (or gRPC) for request/response paths. Async event publication through the domain event mechanism for cross-system side effects. Contract versioning — schema registry or envelope version field.}

**Component interactions.** {`OrderService` publishes `OrderPlaced` and `OrderFulfilled` domain events via `IEventPublisher`. `NotificationDispatcher` subscribes to the same event bus and routes each event type to the appropriate outbound channel. `CatalogueAdapter` calls the Catalogue system over HTTPS/REST; request/response is wrapped in the Resilience mechanism.}

---

### 5.{N} {Bespoke Mechanism Name} *(if applicable)*

**Outline reference:** {ADR-NNN — bespoke mechanism choice}

**Participating components:** {Named components that implement or depend on this mechanism}

**Platform / deployment detail.** {Relevant platform services, infrastructure configuration, or OS-level tooling this mechanism relies on.}

**Runtime behaviour.** {How the mechanism works end-to-end: initialisation, steady-state operation, failure modes.}

**Component interactions.** {How the participating components call into or configure the mechanism. Which components produce data, which consume it, and what crosses the component boundaries.}

*(Repeat for each additional bespoke mechanism from the outline. Remove this placeholder when none is needed.)*

---

## 6. Testing Architecture

Test tiers common to the whole system:

| Tier | Scope | Test doubles | Where it runs |
|---|---|---|---|
| **Domain** | One aggregate, no infrastructure | Real domain objects, no doubles | In-process, no DB |
| **Application** | One use case through the service layer | Fake repositories, fake providers | In-process, no DB |
| **Integration** | One component against real infrastructure | Real DB (testcontainer), fake external HTTP | CI, slower |
| **E2E** | One key user path through the deployed system | Real everything, against staging | Pre-prod |

Common test doubles: `{FakeClock}`, `{FakeEventPublisher}`, `{FakeEmailProvider}`, `{FakeCatalogueClient}`. Per-mechanism testing detail defers to each mechanism's architecture reference section.

---

## 7. Extension & Evolution *(if applicable)*

{Only include when the system has real plug-in points: a documented adapter contract, a registry-driven extension, a SaaS multi-tenancy isolation seam. Remove this section if none exist.}

---

## 8. Decision Records

Blueprint-level decisions (continuing ADR numbering from the outline):

| ID | Decision | One-line consequence |
|---|---|---|
| [ADR-{NNN}](../decisions/ADR-{NNN}-{slug}.md) | {Decision} | {One-line consequence} |

*(Mechanism technology choices have their ADRs in the outline. Blueprint ADRs cover: component boundaries, test-tier vocabulary, data ownership patterns, extension seam contracts.)*

---

## See also

- [`architecture-outline.md`](./architecture-outline.md) — one-page outline (layered diagram, system context with functions + tech, mechanisms catalogue, principles, tech stack, major systems, mechanism ADRs).
- [`architecture-reference.md`](./architecture-reference.md) — deep-dive per mechanism (code walkthroughs, sequence diagrams, tests).
- [`service-level-objectives.md`](./service-level-objectives.md) — non-functional requirements per major system.
