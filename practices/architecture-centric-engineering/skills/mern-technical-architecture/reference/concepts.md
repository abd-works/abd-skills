# MERN Technical Architecture — Concepts

## What is Domain-First MERN Architecture?

A domain-first MERN architecture prioritizes **business capability** over technical layers. Instead of grouping all controllers together, all models together, and all views together, you group everything for a single domain (e.g., "recipients") into one package with three tiers.

The architecture is guided by four principles:

- **Domain modules over technical modules** — organizing code by business capability, then by layer within each module.
- **High alignment to ubiquitous language** — scenarios, domain models, tests, and code use consistent domain terminology.
- **Minimizing logic duplication** — shared validation, types, and business rules across client and server tiers via the `shared/` package.
- **Clean Architecture principles** — dependencies point inward toward the domain core; infrastructure is at the edges.

---

## Five Architecture Layers

| Layer | Tech | Location | Responsibility |
|-------|------|----------|----------------|
| **Presentation** | React, Hooks, TSX | `client/` | Render UI, capture input, manage local state |
| **Interface Adapters** | Express Router, Axios/Fetch | `server/routes.ts`, `client/api.ts` | Translate HTTP ↔ Application calls |
| **Application** | Plain TypeScript classes | `server/service.ts` | Orchestrate use cases, coordinate domain + infra |
| **Domain Core** | Plain TypeScript | `shared/` | Business rules, validation, domain logic (SHARED) |
| **Infrastructure** | MongoDB, external APIs | `server/repository.ts` | Persist data, call external services |

---

## Domain-First File Structure

Every domain module follows the pattern `packages/{domain}/{shared|client|server}`:

- `shared/` — Domain entities, value objects, Zod schemas, collection classes. **Zero framework imports.** Portable to both browser and Node.js.
- `server/` — Express routes, controllers, application services, MongoDB repositories. Imports from `shared/`.
- `client/` — React components, custom hooks, API client functions. Imports from `shared/`.

---

## Shared Domain Logic Strategy

Domain logic is defined **once** in `shared/` and imported by both tiers:
- **Zod schemas** — validate at repository boundary (server) AND form boundary (client)
- **Domain entities** — business methods like `isEligibleForPayment()` used everywhere
- **Collection classes** — `Recipients.filterByStatus('Active')` works identically on both tiers

---

## Story-Driven Testing

Tests mirror the story graph hierarchy:
- **Epic** → test folder
- **Sub-Epic** → nested test folder
- **Lowest Sub-Epic** → 3 test files (server, client, E2E)
- **Story** → test class
- **Scenario** → test method with Given/When/Then helpers

---

## The shape of a domain-first MERN module

```
packages/<domain>/
├── shared/                          # Domain Core (plain TypeScript + Zod)
│   ├── <Entity>.ts                  # Domain entity with business methods
│   ├── <ValueObject>.ts             # Value objects with constraints
│   ├── <entity>.schema.ts           # Zod validation schema
│   ├── <Entity>s.ts                 # Collection class with query methods
│   ├── index.ts                     # Barrel exports
│   └── package.json                 # "@appName/<domain>-shared"
│
├── client/                          # Presentation + Interface Adapter (React)
│   ├── <Entity>List.tsx             # Container component
│   ├── <Entity>Card.tsx             # Presentational component
│   ├── Create<Entity>Form.tsx       # Creation form (validates with Zod from shared/)
│   ├── <Entity>DetailView.tsx       # Detail view with mutation controls
│   ├── use<Entity>s.ts              # Custom hook (state + effects)
│   ├── <domain>.api.ts              # API client (one function per server route)
│   ├── index.ts
│   └── package.json                 # depends on shared
│
├── server/                          # Application + Interface Adapter + Infrastructure
│   ├── <domain>.routes.ts           # Express router (one route per use case)
│   ├── <domain>.controller.ts       # Request/response translation
│   ├── <domain>.service.ts          # Application-layer orchestration
│   ├── <domain>.repository.ts       # MongoDB persistence (uses Zod from shared/)
│   ├── index.ts
│   └── package.json                 # depends on shared
│
└── tests/                           # Story-driven across 3 tiers
    ├── server/                      # Server integration (vitest)
    ├── client/                      # React component (vitest + testing-library)
    └── e2e/                         # End-to-end (Playwright)
```

---

## Compilation and test verification

After generating code:
1. `npm install` — must exit 0.
2. `npx tsc --noEmit` — must report zero errors (including test files).
3. `npx vitest --run` — server + client unit/component tests pass.
4. `npx playwright test` — E2E tests pass (requires app-server and app-client composition roots).
