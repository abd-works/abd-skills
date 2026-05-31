# PawPlace — Architecture Outline (mini)

> **Status:** Draft  
> **Owner:** Engineer (shaping)  
> **Last updated:** 2026-05-31  
>
> **Purpose.** One-page picture of PawPlace mini — web storefront, store-scoped stock, guest click-and-collect — before blueprint and reference work. Modules: Store, Catalog, Cart, Order (see `module-partition.md`).

---

## 1. Platform Diagram

![Platform Architecture](./diagrams/platform-architecture.drawio)

> Source: [`diagrams/platform-architecture.drawio`](./diagrams/platform-architecture.drawio). E2E fixture: edit in draw.io Desktop; export PNG when `arch-drawio.ps1 export` is wired for this layout path.

**Caption.** PawPlace mini is a browser SPA plus a single REST API. The SPA calls the API for catalog, per-store stock, cart, and guest checkout; the API persists orders and stock in MongoDB and calls StripeWave and email providers at the boundary.

---

## 2. Layered Architecture

![Layered Architecture](./diagrams/layered-architecture.drawio)

> Source: [`diagrams/layered-architecture.drawio`](./diagrams/layered-architecture.drawio).

**Caption.** Presentation (React) depends on Application (Express routes/use-cases), Application on Domain (TypeScript modules per bounded context), Domain on Infrastructure interfaces only. MongoDB and StripeWave adapters live in Infrastructure and are injected at startup.

---

## 3. System Context

![System Context](./diagrams/system-context.drawio)

> Source: [`diagrams/system-context.drawio`](./diagrams/system-context.drawio).

**Caption.** Customers and store employees use the PawPlace web app. External systems: StripeWave (card payments), transactional email (order confirmations), and optional maps/geocoding for store distance (provider TBD in discovery).

---

## 4. Deployment Topology

![Deployment Topology](./diagrams/deployment-architecture.drawio)

> Source: [`diagrams/deployment-architecture.drawio`](./diagrams/deployment-architecture.drawio).

**Caption.** Mini fixture targets a single-region deployment: static SPA on CDN, API on one container service, MongoDB as managed cluster. Staging mirrors production at smaller scale; no multi-region requirement for increments 1–2.

---

## 5. Guiding Principles

- **Domain modules match partition boundaries.** Store, Catalog, Cart, and Order code live in separate domain packages; cross-module calls go through application services, not direct persistence reach-through.
- **Store-scoped stock is authoritative at the API.** The SPA never infers stock; every availability read goes through Catalog+Store application APIs.
- **Guest checkout only for mini scope.** No account aggregate in increments 1–2; session/cart identity is explicit and short-lived.
- **Payments cross one seam.** StripeWave is wrapped behind a single payment port; domain never imports Stripe SDK types.
- **Idempotent order placement.** Submit-payment handlers are safe to retry at the HTTP boundary with a client idempotency key.
- **Configuration at composition root.** Environment and secrets are read once when the API process starts; handlers receive typed config objects.
- **Fast domain tests.** Domain and application tests run without MongoDB or StripeWave using in-memory fakes.

---

## 6. Technology Stack

| Layer | Technology | Version | Purpose |
| --- | --- | --- | --- |
| Presentation | React | 18.x | Customer and employee SPA |
| Presentation | React Router | 6.x | Store-scoped routes and flows |
| Application / API | Node.js | 20.x LTS | API runtime |
| Application / API | Express | 4.x | HTTP API |
| Domain | TypeScript | 5.x | Module models and use-cases |
| Infrastructure | MongoDB | 7.x | Catalog, stock, cart, orders |
| Infrastructure | StripeWave API | n/a | Card capture (fixture name) |
| Cross-cutting | OpenTelemetry | 1.x | Traces for checkout spine |
| Build / CI | GitHub Actions | n/a | Lint, test, deploy |

---

## 7. Major Systems

| System | One-line description | Primary owner / module |
| --- | --- | --- |
| **Store** | Store list, map, distance, click-and-collect selection. | `store` |
| **Catalog** | Product browse and per-store stock read/update. | `catalog` |
| **Cart** | Guest cart mutations. | `cart` |
| **Order** | Guest checkout, payment, confirmation, pickup fulfillment. | `order` |
| **Notifications** | Order confirmation email via provider adapter. | `order` (adapter) |

---

## 8. Decision Records

| ID | Decision | One-line consequence |
| --- | --- | --- |
| [ADR-001](./decisions/ADR-001-spa-plus-rest-api.md) | SPA + REST API | Browser client; no SSR for mini scope. |
| [ADR-002](./decisions/ADR-002-domain-modules-by-partition.md) | Domain modules by partition | Aligns code to Store/Catalog/Cart/Order boundaries. |
| [ADR-003](./decisions/ADR-003-mongodb-single-database.md) | MongoDB single database | One cluster for mini; collections per module. |

---

## See also

- [`module-partition.md`](./module-partition.md) — shaping module boundaries  
- [`story-map.md`](./story-map.md) — Patton outline  
- [`impact-map.md`](./impact-map.md) — outcomes and deliverables  
- Discovery roll-up (later): `docs/end-to-end/discovery/architecture/architecture-blueprint.md`
