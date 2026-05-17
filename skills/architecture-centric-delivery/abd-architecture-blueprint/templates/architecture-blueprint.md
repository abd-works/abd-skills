# {SystemName} — Architecture Blueprint

> **Status:** Draft / Approved
> **Owner:** {team-or-person}
> **Last updated:** YYYY-MM-DD
>
> **Purpose.** Second-level architecture document for {SystemName}, building on `architecture-outline.md`. Names every architectural component, catalogues every cross-cutting concern as a typed **architecture mechanism**, sketches the data architecture, captures the common testing strategy, and records decisions. Deep mechanism walkthroughs live in `architecture-reference.md`.

---

## 1. Scope

This blueprint extends [`architecture-outline.md`](./architecture-outline.md) by adding component-level descriptions and a mechanism catalogue. Deep mechanism walkthroughs — code, sequence diagrams, test code, file structures — defer to [`architecture-reference.md`](./architecture-reference.md). Outline-level concerns (platform diagram, deployment topology, technology stack, guiding principles, one-line major-systems catalogue) stay in the outline and are not repeated here.

---

## 2. Components

Each subsection takes one major system from the outline and names its 2–4 components. Each component description is 1–2 paragraphs covering **purpose**, **dependencies**, and **interactions** — no internal structure, no class lists, no method tables.

![Component Overview]( ./diagrams/component-overview.png )

> Source: [`diagrams/component-overview.drawio`](./diagrams/component-overview.drawio). Edit in draw.io Desktop and re-export with `scripts\arch-drawio.ps1 export`. The diagram captures the same information as the subsections below; keep them in sync.

### 2.1 Identity components

#### IdentityService

**Purpose.** Owns user authentication and token issuance for {SystemName}; the only component allowed to call the Auth0 SDK directly.

**Dependencies.** Receives the Auth0 SDK client through constructor injection; depends on `IClock` for token expiry calculations; depends on `IUserRepository` for the application-side user profile (Auth0 stores identity only, not preferences).

**Interactions.** Called by the API authentication middleware on every request to validate tokens. Publishes a `UserAuthenticated` domain event after a successful login so downstream components (Notifications, Analytics) can react without coupling to identity internals.

#### IdentityRepository

**Purpose.** Application-side store of user profile data (display name, preferences, last-seen timestamp) keyed by the Auth0-issued subject ID.

**Dependencies.** Postgres connection pool, `IClock`.

**Interactions.** Called by `IdentityService` and the user-settings API. Not called from any other system directly — cross-system access goes through `IdentityService`.

### 2.2 Catalogue components

#### CatalogueService

**Purpose.** Read-mostly access to product data; the only component the rest of the system uses to look up products by SKU, search, or list catalogue entries.

**Dependencies.** `IProductRepository`, `IProductCache`, search index client.

**Interactions.** Heavily called by the Orders system at line-item validation time. Reads only — write paths (catalogue ingestion, price changes) go through `CatalogueAdminService` which is not part of the public surface.

### 2.3 Orders components

#### OrderService

**Purpose.** Owns the order lifecycle from cart to fulfilment. Canonical source of revenue events.

**Dependencies.** `IOrderRepository`, `ICatalogueClient` (for line-item validation against the Catalogue system), `IEventPublisher`, `IClock`.

**Interactions.** Called from the orders API; calls into the Catalogue system on validation, into the Notifications system through events, into the payment gateway through `IPaymentProvider`.

#### OrderRepository

**Purpose.** Aggregate-root persistence for the `Order` entity. Implements the outbox pattern: order changes and outgoing events commit in a single transaction.

**Dependencies.** Postgres connection pool, `IClock`.

**Interactions.** Called only by `OrderService` (the rest of the codebase has no direct access to the orders schema).

### 2.4 Notifications components

#### NotificationDispatcher

**Purpose.** Subscribes to domain events from across the system and routes them to the right outbound channel (email, push, webhook).

**Dependencies.** `IEmailProvider`, `IPushProvider`, `IWebhookDispatcher`, `INotificationTemplateRepository`.

**Interactions.** Listens to events published by `OrderService`, `IdentityService`. Does not call any other component synchronously; communication is purely event-driven.

---

## 3. Architecture Mechanisms

Each mechanism below names a cross-cutting concern the architecture commits to. Description is 1–2 paragraphs: **what concern it addresses**, **which components depend on it**, **how they interact with it**. Deep walkthroughs live in `architecture-reference.md`.

### 3.1 Security

The system delegates user identity to Auth0 and treats every API request as untrusted until `IdentityService` validates the bearer token. Authorization is role-based with role claims placed on the token at login time; per-request authorization decisions happen at the API edge (middleware) rather than inside domain services so the domain layer never reads request headers. Secrets (Auth0 client secret, DB password, payment provider keys) come from AWS Secrets Manager via the configuration mechanism, never from environment variables in code.

Every component that performs an action on behalf of a user receives the authenticated `Principal` through method arguments — there is no ambient identity context. The Reference document covers the full Principal contract, the role-claim list, the middleware sequence, and the audit-log shape.

### 3.2 Error Handling & Resilience

The Domain and Application layers return `Result<T, DomainError>` for all failure modes; exceptions are reserved for unexpected programmer errors (null where not allowed, contract violations). The API edge translates `DomainError` values into HTTP status codes via a single `ErrorTranslator` so no domain code knows about HTTP. External calls (Auth0, payment provider, Catalogue cross-system) are wrapped in a `Resilient<T>` decorator that adds retry with exponential backoff plus a circuit breaker per dependency.

The mechanism reference covers the full `DomainError` taxonomy, the retry and circuit-breaker tuning, and the dead-letter handling for event publication failures.

### 3.3 Logging & Observability

Structured JSON logging through Pino with a per-request correlation ID propagated as a W3C `traceparent` header. Every component logs at INFO on entry/exit of public methods and at WARN/ERROR when returning a non-success `Result`. Metrics emit through OpenTelemetry to CloudWatch; trace spans cover every cross-component call.

The mechanism reference details the log-shape contract, the metric naming conventions, and how to instrument a new component to participate.

### 3.4 Validation

Input validation runs at the API edge using Zod schemas; valid requests reach the application layer as parsed DTOs. Business-rule validation (inventory available, customer credit limit) runs inside domain services and returns `Result` failures, not exceptions.

The reference covers the schema-sharing strategy between API and clients, the business-rule helper conventions, and the error-detail shape returned to clients.

### 3.5 Configuration

Configuration is read **once** at application start by `Bootstrap.loadConfig()` and frozen into a `Config` object. After bootstrap, no code calls `process.env` directly. Secrets are pulled from AWS Secrets Manager at the same point; rotation is supported by re-deploying the container.

The reference covers the per-environment config layering, the secret-rotation runbook, and how feature flags fit in.

### 3.6 Caching

Catalogue data is cached in Redis with a write-through pattern (catalogue admin writes invalidate the keys they touch). Identity data is cached at the API edge with a 60-second TTL keyed on the bearer token; rotation is opportunistic. No other component caches; ad-hoc caching is a code-review red flag.

The reference covers the cache-key convention, the invalidation strategy in detail, and the consistency guarantees this gives clients.

### 3.7 Persistence

Each aggregate root has one repository; cross-aggregate consistency happens through domain events, not direct cross-aggregate writes. The Orders aggregate uses the outbox pattern (state change + event row commit together). Migrations are forward-only; rolling back a deploy never requires rolling back the schema.

The reference covers the repository base-class, the outbox helper, and the migration runbook.

---

## 4. Data Architecture

### 4.1 Entity overview

![Entity Relationships]( ./diagrams/entity-relationships.png )

> Source: [`diagrams/entity-relationships.drawio`](./diagrams/entity-relationships.drawio). Each colour groups aggregates by owning component named in section 2. Schemas, indexes, and ORM mappings live with the persistence mechanism reference, not here.

### 4.2 Ownership boundaries

| Aggregate | Owning component | Cross-aggregate access |
|---|---|---|
| `User` | `IdentityRepository` | Read-only via `IdentityService.getById(userId)` |
| `Order` (root) + `LineItem` | `OrderRepository` | None — events propagate state |
| `Product` (read-only outside admin) | `CatalogueService` | `ICatalogueClient.lookup(sku)` |
| `NotificationTemplate` | `NotificationDispatcher` | Internal to Notifications |

Cross-aggregate consistency is **eventual**, propagated through domain events, never through direct cross-aggregate writes.

---

## 5. Testing Architecture

Test tiers common to the whole system:

| Tier | Scope | Test doubles | Where it runs |
|---|---|---|---|
| **Domain** | One aggregate, no infrastructure | Real domain objects, no doubles | In-process, no DB |
| **Application** | One use case end-to-end through the service layer | Fake repositories, fake providers | In-process, no DB |
| **Integration** | One component against real infrastructure | Real DB (testcontainer), fake external HTTP | CI, slower |
| **E2E** | One key user path through the deployed system | Real everything, against a staging env | Pre-prod |

Common test doubles: `FakeClock`, `FakeEventPublisher`, `FakeEmailProvider`, `FakeCatalogueClient`. Per-mechanism testing (how Security tests verify Principal flow, how Resilience tests trigger circuit-breaker opens) lives in the architecture reference.

---

## 6. Extension & Evolution

The architecture has one documented extension seam: **notification channels**. New channels (Slack, SMS, in-app) implement `INotificationChannel` and register through `ChannelRegistry.register()` at startup. The contract, registration mechanism, and template requirements are documented in `architecture-reference.md` section 5.

No other parts of the architecture are pluggable; new behaviour lands as new components, not as plug-ins.

---

## 7. Decision Records

Blueprint-level decisions (continuing ADR numbering from the outline):

| ID | Decision | One-line consequence |
|---|---|---|
| [ADR-005](../decisions/ADR-005-result-types-not-exceptions.md) | Domain returns `Result<T, DomainError>`, not exceptions | Failure handling is type-checked; the HTTP boundary is the only translator. |
| [ADR-006](../decisions/ADR-006-outbox-pattern-for-orders.md) | Orders use the outbox pattern for events | At-least-once delivery without a 2PC; consumer idempotency is required. |
| [ADR-007](../decisions/ADR-007-write-through-cache-strategy.md) | Catalogue cache is write-through, not cache-aside | Predictable freshness; admin writes do extra work. |
| [ADR-008](../decisions/ADR-008-four-test-tiers.md) | Domain / Application / Integration / E2E test tiers | Most tests run with no infrastructure; integration is bounded. |

---

## See also

- [`architecture-outline.md`](./architecture-outline.md) — one-page outline (platform, layered, context, deployment, principles, tech stack, major systems).
- [`architecture-reference.md`](./architecture-reference.md) — deep-dive per mechanism (code walkthroughs, sequence diagrams, tests).
- [`service-level-objectives.md`](./service-level-objectives.md) — non-functional requirements per major system.
