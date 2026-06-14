# MERN Domain-First — Architecture Outline

> **Purpose.** One-page picture of the MERN Domain-First architecture — what the platform is, the mechanisms that address cross-cutting concerns, the guiding principles that govern every deeper decision, and the technology stack. Platform runtime and code-shape detail live in the **architecture blueprint** (`architecture-blueprint.md`). Per-mechanism code patterns and worked examples are in the **architecture specification** (`architecture-specification.md`).

---

## 1. Layered Architecture

**Five layer bands, top to bottom.** Dependencies flow strictly downward; no layer imports from a layer above it.

| Band | Contents | Framework |
|---|---|---|
| **Presentation** | React views; pure rendering nodes; no fetch calls | React 18 / React Router 6 |
| **Application–Client** | TanStack Query hooks; typed HTTP client; client-side form validation | TanStack Query 5 |
| **Domain–Shared** | Entities, value objects, Zod schemas, collection classes, repository interfaces | TypeScript 5 / Zod 3 — zero framework imports |
| **Application–Server** | Express routers (one per domain module); domain service classes | Node.js 20 / Express 4 |
| **Infrastructure** | MongoDB repository implementations; external-system adapters; composition root | MongoDB driver; named adapter interfaces |

The **Domain–Shared** band carries no imports from React, Express, MongoDB, or any other runtime framework. Both `client/` and `server/` tiers import from `shared/`; the shared tier never imports from either.

---

## 2. Architecture Mechanisms

The mechanisms below are the cross-cutting concerns the architecture commits to for every domain module. Each entry states the technology choice, how the mechanism works at this level, and the NFR that drove the choice.

---

### 2.1 Security *(+ module: Identity)*

**Technology choice:** External Identity Provider (OAuth 2.0 + OIDC); JWT validation middleware in Express; role-based route guards.

Authentication is delegated to an external Identity Provider. The React SPA redirects unauthenticated requests to the IdP login flow; on success the IdP issues a signed JWT. The Express API validates the JWT signature (via JWKS endpoint) and role claims on every protected route before any domain handler runs. No homegrown credential storage exists in the application.

**NFR:** Zero homegrown password storage; single sign-on when an enterprise IdP is in scope.

---

### 2.2 Error Handling & Resilience

**Technology choice:** Discriminated-union Result type (`{ ok: true; value: T } | { ok: false; error: E }`); no thrown exceptions in domain or server layers.

Domain and server operations return Result values rather than throwing exceptions. The Express route handler is the only translation point — it inspects the Result discriminant and maps error variants to HTTP status codes with a structured JSON error body. External integration calls are wrapped in Result types with explicit error categories so callers handle each variant explicitly.

**NFR:** Every failure must be typed, traceable, and surfaced as an actionable message; silent swallowing is prohibited.

---

### 2.3 Logging & Observability

**Technology choice:** Pino (structured JSON logging) on Node.js; correlation ID header propagated per request.

The Express API emits structured JSON log entries for every HTTP request. Domain business events are logged at `INFO` with business-meaningful fields; external system errors and domain validation failures at `ERROR` with full context. A correlation ID is injected per request and bound to every log entry in that request's scope.

**NFR:** All significant events must be auditable; structured JSON output enables log aggregation and correlation-ID-based tracing.

---

### 2.4 Validation

**Technology choice:** Zod 3 schema validation at the Express route boundary; domain invariant enforcement in entity constructors in `shared/`.

Request bodies are validated against Zod schemas at the route boundary before any domain logic executes. Domain-level invariants are enforced by entity constructors using Zod refinements; violations surface as `{ ok: false, error: ValidationError }` Results. Client-side validation mirrors the same `shared/` schemas to give immediate feedback before submission.

**NFR:** Invalid data must never enter the domain; validation feedback must name the specific field and rule that failed.

---

### 2.5 Configuration & Secrets

**Technology choice:** Environment variables read once at the composition root (`app-server/app.ts`); injected as typed configuration objects into domain modules.

All `process.env` reads are confined to the composition root. At startup it reads connection strings, credentials, and service endpoints — constructing a typed `Config` record passed as constructor arguments to each domain module. Test code substitutes config objects directly without environment setup.

**NFR:** Composition-root isolation means test code never reads real secrets.

---

### 2.6 Caching

**Technology choice:** TanStack Query 5 client-side server-state cache (stale-while-revalidate); no server-side cache by default.

The React SPA uses TanStack Query for all data fetching with configurable `staleTime` per query. Mutations call `queryClient.invalidateQueries` to evict affected entries immediately. Server-side caching (Redis, etc.) is added only when a specific NFR demands it.

**NFR:** Data freshness SLAs are enforced per query at the client; the default stance is no server-side cache.

---

### 2.7 Persistence

**Technology choice:** MongoDB document store via the official Node.js driver; repository pattern with `I<Entity>Repository` interface in `shared/`, implemented by `<Entity>RepositoryServer` in `server/`.

Each domain module owns exactly one MongoDB collection; there are no cross-module database joins or transactions. The repository interface in `shared/` is implementable by in-memory fakes in tests, without a MongoDB instance. Schemas are enforced by Zod at write time.

**NFR:** Domain state must be testable without a live database; the repository interface is the mandatory seam.

---

### 2.8 Communication

**Technology choice:** HTTPS/REST with JSON (SPA ↔ API and API ↔ external services); other protocols (SFTP, message brokers) added per integration need; no message broker by default.

Every external protocol call is wrapped in a named adapter interface in the calling module's `server/` package. Adapters return Results; network errors are caught and wrapped before surfacing to callers. On the client, all communication goes through TanStack Query hooks (Caching mechanism); direct `fetch` calls outside a hook are prohibited.

**NFR:** All external calls must be mockable in tests via the adapter interface; timeouts must be enforced at the adapter boundary.

---

### 2.9 UI Rendering

**Technology choice:** React 18 SPA; React Router 6 (one named route per domain module); TanStack Query 5 hooks for all server-state data fetching; Vite 5 bundle delivered from CDN or static hosting.

The SPA renders entirely in the browser. React Router maps each domain module to a named route. Components are pure rendering nodes — they fetch data exclusively through TanStack Query hooks; no direct `fetch` calls in component code. The bundle is code-split by route (React.lazy) so each module's client code loads on first navigation.

**NFR:** Initial load performance SLA is met by CDN delivery of the Vite-built bundle and route-level code splitting.

---

### 2.10 App Server *(+ module: App Server Bootstrap)*

**Technology choice:** Node.js 20 / Express 4; modular Express Routers (one per domain module); global middleware chain applied before any domain router.

The Express application has a single composition root that mounts domain-scoped routers. Each router delegates to a domain service that returns a Result; the router translates the Result to an HTTP response. The global chain is: `CORS → correlation-ID → JWT validation → named domain router`. No business logic lives in router code.

**NFR:** Route handlers carry no shared mutable state across requests; all state is instantiated per request from injected domain objects.

---

### 2.11 Unified Domain Logic *(bespoke)*

**Technology choice:** TypeScript 5 `packages/<domain>/shared/` with zero framework imports; Zod 3 entity constructors enforce invariants at instantiation time.

Each domain module owns a `shared/` package containing entities, value objects, Zod schemas, and builders. These packages import only TypeScript and Zod. Both the React client and the Express server import from `shared/`; there is no client-only or server-only business rule. A validation rule defined once in `shared/` is evaluated in the browser for immediate feedback and re-evaluated on the server as the authoritative gate.

**NFR:** A domain invariant must be defined exactly once in `shared/`; a single change there is the complete and sufficient update to enforce it everywhere.

---

## 3. Guiding Principles

These are the one-sentence stances that govern every deeper decision. Each is decidable against a real piece of code or a design proposal.

- **Domain never imports infrastructure.** `shared/` packages depend only on Zod and plain TypeScript — no `mongoose`, `express`, or `react` imports.
- **All cross-system I/O crosses a named seam.** Every call to an external service passes through a project-owned interface so it can be stubbed in tests.
- **Layer qualifiers on every tier extension.** `shared/` keeps plain domain names. Every extension in `client/` adds a `Client` or `Api` suffix; every extension in `server/` adds `Server`, `Router`, or `RepositoryServer`.
- **One module per bounded domain capability.** Each payment type, workflow, or owned entity is a separate domain module with no cross-imports at the domain level.
- **Tests run without infrastructure.** The full `shared/` and `server/` domain test suite runs without a live MongoDB instance; repositories are stubbed via their interface.
- **Configuration is read once at the composition root.** No `process.env` calls outside `app-server/app.ts`; downstream modules receive configuration through dependency injection.

---

## 4. Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| Presentation | React | 18.x | SPA framework |
| Presentation | React Router | 6.x | Client-side routing (one route per domain module) |
| Presentation | TanStack Query | 5.x | Server-state fetching and mutation cache |
| Application / API | Node.js | 20.x LTS | Server runtime |
| Application / API | Express | 4.x | HTTP framework; route delegation to domain routers |
| Domain | TypeScript | 5.x | All tiers; strict mode enforced |
| Domain | Zod | 3.x | Runtime schema validation and domain invariants |
| Infrastructure | MongoDB | 7.x | Primary data store |
| Build | Vite | 5.x | Client bundler and dev server |
| Build | Vitest | 2.x | Unit and integration test runner |
| E2E Testing | Playwright | 1.x | End-to-end test suite |
| CI | GitHub Actions | n/a | Lint, test, build, deploy pipeline |

---

## 5. Decision Records

Mechanism-choice ADRs belong at this level. Blueprint-level ADRs (module boundaries, test-tier vocabulary) live in `architecture-blueprint.md`.

| ID | Decision | One-line consequence |
|---|---|---|
| ADR-001 | MERN SPA + Express API platform | All UI is browser-side React; the server is a single Express process; no server-side rendering |
| ADR-002 | Organise by domain module, not technical layer | One `packages/<domain>/` folder per capability; `shared/` for shared domain core; no cross-domain imports |
| ADR-003 | MongoDB as primary data store | Domain state stored as documents; Zod schema enforced at write time; one collection per module |
| ADR-004 | Result object error handling | Domain returns `Result<T, E>` not exceptions; HTTP boundary is the only error-to-status translator |
| ADR-005 | Pino structured logging with correlation IDs | Every API request and business event logged as structured JSON; correlation IDs enable end-to-end tracing |
| ADR-006 | Zod validation at the API boundary and domain layer | Invalid data rejected at the edge before entering domain logic; schemas shared between client and server |
| ADR-007 | TanStack Query for client-side server-state caching | Configurable per-query stale time; no server-side cache required by default |
| ADR-008 | External IdP with JWT for authentication | No homegrown credential storage; authentication delegates to an external Identity Provider |

---

## See also

- [`architecture-blueprint.md`](./architecture-blueprint.md) — platform runtime, mechanisms as code shapes, module structure, testing architecture.
- [`architecture-specification.md`](./architecture-specification.md) — code-level: module layout, layer qualifiers, file naming, worked examples per mechanism.
