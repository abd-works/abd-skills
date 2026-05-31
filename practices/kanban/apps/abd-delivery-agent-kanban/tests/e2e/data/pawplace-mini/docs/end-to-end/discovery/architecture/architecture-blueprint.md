# PawPlace mini — Architecture Blueprint

> **Status:** Draft
> **Owner:** Engineer (discovery)
> **Last updated:** 2026-05-31
>
> **Purpose.** Second-level architecture for PawPlace mini — guest click-and-collect storefront across Store, Catalog, Cart, and Order modules. Names every architectural component, catalogues cross-cutting concerns as typed **architecture mechanisms**, sketches the data architecture, captures the common testing strategy, and records blueprint-level decisions. Deep mechanism walkthroughs defer to `architecture-reference.md` (specification stage).

---

## 1. Scope

This blueprint extends [`architecture-outline.md`](../../shaping/architecture-outline.md) by adding component-level descriptions and a mechanism catalogue. Outline-level material — platform diagram, deployment topology, technology stack, guiding principles, and major-systems one-liners — stays in the outline and is not repeated here.

Domain vocabulary for aggregates and terms lives in [`domain-terms.md`](../domain/domain-terms.md). Mechanism internals, sequence diagrams, file trees, and test code defer to `architecture-reference.md` when produced in specification.

---

## 2. Components

Each subsection names one major system from the outline and its 2–4 components. Descriptions cover **purpose**, **dependencies**, and **interactions** only — no internal class lists or file trees.

![Component Overview](./diagrams/component-overview.drawio)

> Source: [`diagrams/component-overview.drawio`](./diagrams/component-overview.drawio). Edit in draw.io Desktop and re-export PNG when `arch-drawio.ps1 export` is wired for this layout path. Keep diagram and subsections in sync.

### 2.1 App Shell components

#### AppServerHost

**Purpose.** Composes the Express application: mounts module routers for Store, Catalog, Cart, and Order; applies shared middleware (JSON parsing, error translation, request logging); exposes a single HTTP entry point for the React SPA.

**Dependencies.** MongoDB connection, factory functions from each module's server package, configuration loaded once at startup.

**Interactions.** Receives browser requests on `/api/v1/*`; delegates to module API adapters. Contains no domain logic — only wiring and cross-cutting middleware.

#### AppClientShell

**Purpose.** Top-level React application: route table, layout chrome, and store-scoped navigation that hosts views from Store, Catalog, Cart, and Order client packages.

**Dependencies.** React Router, API client modules from each capability package, build tooling (Vite).

**Interactions.** Renders customer flows (store map/list, catalog browse, cart, guest checkout) and store-employee stock update screens. Calls REST endpoints on AppServerHost; never infers stock or prices locally.

### 2.2 Store components

#### StoreService

**Purpose.** Application service for store discovery: map view, list view, distance ranking from customer location, and store detail for click-and-collect selection.

**Dependencies.** `IStoreRepository`, domain types from the Store module.

**Interactions.** Called by StoreApi controllers. Returns active stores sorted or filtered by distance. Catalog and Order reference stores by store code; Store does not call into those modules.

#### StoreRepository

**Purpose.** Persistence adapter for Store aggregates: name, geo-coordinates, address, hours, and active status.

**Dependencies.** MongoDB `store_*` collections.

**Interactions.** Called only by StoreService. Seed data supports dev and E2E environments.

#### StoreApi

**Purpose.** HTTP adapter for store locator endpoints (list, map, distance query, detail).

**Dependencies.** StoreService, Zod request/response schemas from the Store shared package.

**Interactions.** Mounted under `/api/v1` by AppServerHost. Consumed by map, list, and checkout store-selection views in AppClientShell.

### 2.3 Catalog components

#### CatalogService

**Purpose.** Application service for product browse/detail and per-store stock reads and staff stock updates. Enforces catalog invariants (non-negative stock, SKU identity, store-scoped availability).

**Dependencies.** `ICatalogRepository`, domain types from the Catalog module.

**Interactions.** Called by CatalogApi controllers. Cart validates line items against stock through this service's public read surface; Order snapshots product identity at checkout. Staff stock updates flow through the same service with an employee-scoped route.

#### CatalogRepository

**Purpose.** Persistence adapter for Product aggregates and per-store StockLevel records in MongoDB.

**Dependencies.** MongoDB `catalog_*` collections.

**Interactions.** Called exclusively by CatalogService. Stock records are keyed by product SKU and store code; no cross-module direct access.

#### CatalogApi

**Purpose.** HTTP adapter exposing catalog browse, product detail, stock-by-store, and staff stock-update endpoints.

**Dependencies.** CatalogService, Zod schemas from the Catalog shared package.

**Interactions.** Mounted under `/api/v1` by AppServerHost. Serves customer catalog views and the employee stock form.

### 2.4 Cart components

#### CartService

**Purpose.** Application service for guest shopping cart lifecycle: add, update quantity, remove line items, and resolve cart by session token.

**Dependencies.** `ICartRepository`, `ICatalogClient` (read-only stock and product lookup), `IClock`.

**Interactions.** Called by CartApi controllers. Validates additions against Catalog stock availability before persisting. Order checkout reads the cart through this service — not the repository directly.

#### CartRepository

**Purpose.** Persistence adapter for Cart aggregate roots and line items keyed by guest session identifier.

**Dependencies.** MongoDB `cart_*` collections.

**Interactions.** Called only by CartService. Carts expire after a configured TTL; no account linkage in mini scope.

#### CartApi

**Purpose.** HTTP adapter for cart mutation and retrieval endpoints.

**Dependencies.** CartService, Zod schemas, session/cart token handling at the edge.

**Interactions.** Mounted under `/api/v1` by AppServerHost. Consumed by catalog and cart views in AppClientShell.

### 2.5 Order components

#### OrderService

**Purpose.** Owns guest checkout and click-and-collect order lifecycle: cart conversion, billing capture, payment, confirmation, and fulfillment status transitions.

**Dependencies.** `IOrderRepository`, `ICartClient`, `ICatalogClient`, `IStoreClient`, `IPaymentProvider`, `IEmailProvider`, `IClock`.

**Interactions.** Called by OrderApi controllers. Validates line items and selected store at placement; invokes PaymentGatewayAdapter for card capture; triggers order confirmation email. Store employees update fulfillment status through the same service.

#### OrderRepository

**Purpose.** Persistence adapter for Order aggregate roots, line items with price snapshots, and idempotency records for submit-payment retries.

**Dependencies.** MongoDB `order_*` collections.

**Interactions.** Called only by OrderService. Order placement and idempotency key storage commit in one logical unit per module conventions.

#### OrderApi

**Purpose.** HTTP adapter for checkout, payment submission, order confirmation read-back, and employee fulfillment endpoints.

**Dependencies.** OrderService, Zod schemas, idempotency-key header handling at the edge.

**Interactions.** Mounted under `/api/v1` by AppServerHost. Guest checkout and fulfillment flows in AppClientShell call these endpoints.

#### PaymentGatewayAdapter

**Purpose.** Wraps StripeWave behind `IPaymentProvider`; the only component that imports StripeWave SDK types.

**Dependencies.** StripeWave client configuration, `IClock`.

**Interactions.** Invoked by OrderService during payment submission. Returns authorization result to OrderService; domain code never sees vendor types.

#### NotificationAdapter

**Purpose.** Sends transactional order confirmation email through the configured email provider.

**Dependencies.** Email provider credentials from configuration, order confirmation template inputs from OrderService.

**Interactions.** Called synchronously by OrderService after successful payment; failures surface as order-level errors with retry guidance at the API edge.

---

## 3. Architecture Mechanisms

Each mechanism names a cross-cutting concern the architecture commits to. Description is 1–2 paragraphs; deep walkthroughs defer to `architecture-reference.md`.

### 3.1 Security

PawPlace mini is **guest-only** — no customer accounts or login in increments 1–2. Security focuses on transport (HTTPS in deployed environments), input validation at the API edge, and least-privilege MongoDB credentials. Store-employee stock and fulfillment routes use a simple shared staff token or basic auth configured per environment until a fuller identity mechanism is scoped. Domain services receive explicit context (store code, cart token) through method arguments rather than ambient request globals.

*See `architecture-reference.md` § Security when produced for staff-route hardening and secret rotation.*

### 3.2 Error Handling & Resilience

Domain layer returns typed domain errors for expected failures (insufficient stock, invalid cart state, payment declined). API adapters map known failures to HTTP 4xx responses; unexpected errors become 500 with a generic body. External calls to StripeWave and the email provider use retry with bounded backoff for transient failures; payment submission remains idempotent via client idempotency keys stored with the order.

*See `architecture-reference.md` § Error Handling & Resilience for the error taxonomy and retry tuning.*

### 3.3 Logging & Observability

Structured JSON logging at API entry, checkout milestones, and domain failure points. OpenTelemetry traces cover the checkout spine (cart read → stock validation → payment → confirmation). Correlation IDs propagate from the API edge through OrderService calls to external providers.

*See `architecture-reference.md` § Logging & Observability for log shape and span naming.*

### 3.4 Validation

Request and response contracts are validated with **Zod schemas** colocated in each module's shared package. Invalid requests fail at the API edge before application services run. Business-rule validation (stock quantity, cart line limits, store active status) runs inside domain services and returns typed errors.

*See `architecture-reference.md` § Validation for schema-sharing between API and client.*

### 3.5 Configuration

Configuration is read once at process startup from environment variables and frozen into a typed `Config` object. Domain and shared packages do not read `process.env` directly — only AppServerHost and composition-root scripts do. StripeWave keys and email provider credentials follow the same bootstrap pattern.

*See `architecture-reference.md` § Configuration for per-environment layering.*

### 3.6 Persistence

Each module owns its MongoDB collections (`store_*`, `catalog_*`, `cart_*`, `order_*`) accessed through a dedicated repository interface. Cross-module consistency is **read-by-reference** (store code on stock and orders) with checkout orchestration in OrderService. Order placement persists the aggregate and idempotency record together within the Order module boundary.

*See `architecture-reference.md` § Persistence for collection ownership and migration conventions.*

### 3.7 Communication

**Synchronous REST** over HTTP/JSON is the only integration style for mini scope. AppClientShell calls AppServerHost; AppServerHost routes to module APIs. Cross-module calls inside the API process go through published application service interfaces or HTTP internal clients — never direct repository imports across modules.

*See `architecture-reference.md` § Communication for route grouping and versioning.*

---

## 4. Data Architecture

### 4.1 Entity overview

![Entity Relationships](./diagrams/entity-relationships.drawio)

> Source: [`diagrams/entity-relationships.drawio`](./diagrams/entity-relationships.drawio). Colour groups aggregates by owning module named in section 2. Schemas and indexes live with the Persistence mechanism reference.

### 4.2 Ownership boundaries

| Aggregate / entity | Owning component | Cross-module access |
|---|---|---|
| `Store` | StoreRepository | Read via StoreService / StoreApi only |
| `Product` | CatalogRepository | Read via CatalogService / CatalogApi only |
| `StockLevel` (product × store) | CatalogRepository | References `Store` by store code; Cart and Order read via `ICatalogClient` |
| `Cart`, `CartLineItem` | CartRepository | Read via CartService; Order reads cart at checkout via `ICartClient` |
| `Order`, `LineItem`, `BillingAddress` | OrderRepository | References product by SKU snapshot and store by code; no direct Cart writes after placement |

Cross-aggregate consistency within a module is **immediate** where the repository supports it. Across modules it is **orchestrated** at checkout (OrderService) with **reference-by-id** elsewhere.

---

## 5. Testing Architecture

Test tiers common to PawPlace mini:

| Tier | Scope | Test doubles | Where it runs |
|---|---|---|---|
| **Domain** | One aggregate or domain service, no I/O | Real domain objects; fake clocks | Vitest — module `shared` packages |
| **Application** | One use case through service + fake repository | In-memory repositories, fake catalog/cart clients | Vitest — module `server` packages |
| **Integration** | One module against real MongoDB | Real DB (test container or dev DB); supertest for HTTP | Vitest — app-server integration tests |
| **E2E** | Key user paths through browser + API | Real dev stack | Playwright — checkout and store-locator flows |

Common doubles: `FakeClock`, in-memory repository implementations, `FakePaymentProvider`, `FakeEmailProvider`, seeded MongoDB fixtures. Mechanism-specific testing (idempotency replay, StripeWave sandbox) lives in the architecture reference.

---

## 6. Extension & Evolution

The architecture has one documented extension seam: **payment providers**. New card processors implement `IPaymentProvider` and register at the composition root; StripeWave is the first adapter. OrderService depends only on the interface — not vendor SDK types. Contract, registration, and refund behaviour are documented in `architecture-reference.md` when the Payment mechanism is expanded.

No other parts of mini scope are pluggable; new behaviour lands as new components within module boundaries.

---

## 7. Decision Records

Blueprint-level decisions (continuing ADR numbering from the outline):

| ID | Decision | One-line consequence |
|---|---|---|
| [ADR-004](./ADR-004-zod-api-validation.md) | Zod schemas at the API boundary | Invalid requests fail before application services; schemas shared with client where useful. |
| [ADR-005](./ADR-005-vitest-playwright-test-tiers.md) | Vitest for unit/application/integration; Playwright for E2E | Fast in-process domain tests; browser coverage for checkout spine. |
| [ADR-006](./ADR-006-stripewave-payment-port.md) | StripeWave behind `IPaymentProvider` | Domain never imports vendor SDK types; new providers swap at composition root. |
| [ADR-007](./ADR-007-idempotent-order-placement.md) | Client idempotency key on submit-payment | Safe HTTP retries without duplicate charges or orders. |

---

## See also

- [`architecture-outline.md`](../../shaping/architecture-outline.md) — platform, layering, context, deployment, principles, tech stack
- [`domain-terms.md`](../domain/domain-terms.md) — Store, Catalog, Cart, Order vocabulary
- [`module-partition.md`](../../shaping/module-partition.md) — shaping module boundaries
- [`story-map.md`](../../shaping/story-map.md) — Patton outline
- [`thin-slicing.md`](../stories/thin-slicing.md) — increment scope and ordering
