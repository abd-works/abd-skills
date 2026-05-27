---
name: mern-technical-architecture
catalog_garden_tier: practice
catalog_garden_family: architecture-centric-engineering
catalog_garden_order: 70
catalogue_one_liner: >-
  Domain-first MERN web applications: domain modules, shared logic, Clean Architecture layers, story-driven tests, scanner-verified compliance.
description: >-
  Generate production MERN (MongoDB, Express, React, Node.js) web applications
  using a domain-first architecture. Code is organized by business capability
  (domain module) with shared domain logic, Clean Architecture layer separation,
  and story-driven testing across three tiers. This skill covers the full
  structure: domain entities and Zod schemas in shared/, Express backend in
  server/, React frontend in client/, and Gherkin-aligned tests. Use it when
  scaffolding a new MERN project, adding a domain module, reviewing architecture
  compliance, or transforming a technically-organized codebase into domain-first
  structure. Produces TypeScript module output from templates and validates
  against embedded scanner-backed rules.
---
# mern-technical-architecture

## Purpose

Generate production MERN web applications using a **domain-first architecture** — organizing by business capability, sharing domain logic across tiers, enforcing Clean Architecture layer purity, and testing with story-driven scenarios.

This skill produces real, runnable TypeScript domain modules — each with a `shared/` domain core, `server/` Express backend, and `client/` React frontend. The output follows the architecture defined in [`inputs/mern-architecture.md`](inputs/mern-architecture.md): domain entities with business logic, Zod validation schemas shared across tiers, collection classes with domain-oriented query methods, and story-driven tests mirroring Gherkin scenarios.

## When to use this skill

Load this skill when **any** of the following apply:

- You are **scaffolding a new MERN project** and need the domain-first folder structure.
- You are **adding a new domain module** (e.g., recipients, payments, invoices) to an existing project.
- You are **reviewing architecture compliance** against Clean Architecture and domain-first principles.
- You are **transforming** a technically-organized codebase (`controllers/`, `models/`, `views/`) into domain-first structure.
- You are generating **shared domain logic** (entities, schemas, value objects) that must work identically on client and server.
- You are setting up **story-driven tests** across server, client, and E2E tiers.

---

## Agent Instructions

1. **Read the architecture reference first** — Load [`inputs/mern-architecture.md`](inputs/mern-architecture.md) to understand the authoritative architecture: 5 layers, domain-first file structure, shared logic strategies, testing pyramid, and example code.

2. **Templates**
   Generate content using **every** template file in this skill's `templates/` folder.
   **Do not** emit only partial output unless the user **explicitly** asks for a single tier.

   | Template | What to produce |
   | --- | --- |
   | `domain-module.ts` | Complete domain module with shared/, server/, and client/ packages |

   **Consistency:** All three tiers (shared, server, client) must reference the same domain entities, use the same Zod schemas, and maintain identical naming conventions.

   **If new files are added** under `templates/` later, produce a corresponding artifact for **each** new template the same way.

   When you **create or rewrite** a domain module, you **must** deliver all three tier packages (shared, server, client) as a complete unit.

3. **Rules**
   - Generate content following rules attached to this skill, listed below, assembled from rule files in `rules/`.
   - Validate — once content is generated, take on the role of a *Peer Reviewer* and validate that the content is correct by going through each of the skill's rules one at a time and looking deeply for violations. Be helpful but critical — compare content against each rule's constraints, DO/DON'T sections and examples.

   - **Who is checking:** Software Architect verifying layer purity and dependency direction, Domain Expert verifying ubiquitous language usage, Tech Lead verifying all interfaces are fully implemented, QA Lead verifying test structure follows story-driven pattern.

4. **Scanners**
   After generating code, run the architecture scanners in `scanners/typescript/` to verify:
   - Domain structure completeness (`domain_structure_scanner.py`)
   - Layer purity — no forbidden imports (`layer_purity_scanner.py`)
   - Naming conventions per tier (`naming_convention_scanner.py`)
   - Test structure — all 3 tiers present (`test_structure_scanner.py`)
   - Test data isolation — no blanket resets or `deleteMany({})` (`test_isolation_scanner.py`)

   Fix any violations before considering the implementation complete.

5. **Compilation Verification**
   After scanners pass, verify the generated code actually compiles:
   1. Run `npm install` from the workspace root — must exit with code 0.
   2. Run `npx tsc --noEmit` — must report zero errors. **This must include test files** (`tests/**/*.ts`, `tests/**/*.tsx`).
   3. If either fails, diagnose and fix (missing dependencies, type errors, import path issues) before proceeding.

   **E2E spec files compiling is not the same as E2E tests passing.** `npx tsc` confirms the spec files are syntactically valid. `npx vitest run` excludes `*_e2e.spec.ts` entirely — a full vitest pass says nothing about E2E. E2E tests only pass when a real browser navigates to real page routes served by a live `packages/app-client/` frontend. Until `app-client` exists and is wired into `playwright.config.ts` `webServer`, every Playwright test fails with `Cannot GET /<route>`.

   When reporting test status, be explicit:
   - "Server + client unit/component tests pass (`npm test`)."
   - "E2E tests require `packages/app-client/` — not yet runnable." (if app-client is absent)
   - "E2E tests pass (`npx playwright test`)." (only after app-client exists and Playwright runs green)
   
   **This step is mandatory.** Code that does not compile is not done. Common failures:
   - Missing external dependencies in `package.json` (zod, express, mongodb, react)
   - Missing test framework packages in root devDependencies (vitest, jsdom, @testing-library/react, @testing-library/jest-dom, @playwright/test)
   - Missing `@types/*` packages for type declarations
   - Import paths that don't resolve — verify test files use `@{appName}/{domain}-{tier}` not `@project/{domain}/{tier}`
   - TypeScript path aliases not configured for all tiers (shared, server, client) in `tsconfig.json`
   - Missing `"types"` in tsconfig for test globals (vitest/globals, @testing-library/jest-dom)
   - Controllers accessing `req.user` without Express type augmentation
   - Test runner collision: no `vitest.config.ts` or `playwright.config.ts` causes each runner to pick up the other's files

  **E2E tests (`npx playwright test`) require composition roots.** Ensure `packages/app-server/` (Express entry point mounting domain routers) and `packages/app-client/` (React/Vite shell rendering domain components) exist as part of the domain module generation. If either is missing, scaffold it. If either already exists, wire the generated module into the existing root rather than creating a duplicate shell. Without reachable composition roots, Playwright fails with `ERR_CONNECTION_REFUSED`. Both `npx vitest --run` (unit + component tests) and `npx playwright test` (E2E) should be runnable after generation.

6. **Assembling this Skill**
   This Skill file is assembled from all template files in `templates/` and all rules in `rules/`. Use **`bundle_rules_into_skill_md.py`** to reassemble this skill whenever rules or templates change.

---

## What is Domain-First MERN Architecture?

A domain-first MERN architecture prioritizes **business capability** over technical layers. Instead of grouping all controllers together, all models together, and all views together, you group everything for a single domain (e.g., "recipients") into one package with three tiers.

The architecture is guided by four principles:

- **Domain modules over technical modules** — organizing code by business capability, then by layer within each module.
- **High alignment to ubiquitous language** — scenarios, domain models, tests, and code use consistent domain terminology.
- **Minimizing logic duplication** — shared validation, types, and business rules across client and server tiers via the `shared/` package.
- **Clean Architecture principles** — dependencies point inward toward the domain core; infrastructure is at the edges.

---

## Core concepts

### Five Architecture Layers

| Layer | Tech | Location | Responsibility |
|-------|------|----------|----------------|
| **Presentation** | React, Hooks, TSX | `client/` | Render UI, capture input, manage local state |
| **Interface Adapters** | Express Router, Axios/Fetch | `server/routes.ts`, `client/api.ts` | Translate HTTP ↔ Application calls |
| **Application** | Plain TypeScript classes | `server/service.ts` | Orchestrate use cases, coordinate domain + infra |
| **Domain Core** | Plain TypeScript | `shared/` | Business rules, validation, domain logic (SHARED) |
| **Infrastructure** | MongoDB, external APIs | `server/repository.ts` | Persist data, call external services |

### Domain-First File Structure

Every domain module follows the pattern `packages/{domain}/{shared|client|server}`:

- `shared/` — Domain entities, value objects, Zod schemas, collection classes. **Zero framework imports.** Portable to both browser and Node.js.
- `server/` — Express routes, controllers, application services, MongoDB repositories. Imports from `shared/`.
- `client/` — React components, custom hooks, API client functions. Imports from `shared/`.

### Shared Domain Logic Strategy

Domain logic is defined **once** in `shared/` and imported by both tiers:
- **Zod schemas** — validate at repository boundary (server) AND form boundary (client)
- **Domain entities** — business methods like `isEligibleForPayment()` used everywhere
- **Collection classes** — `Recipients.filterByStatus('Active')` works identically on both tiers

### Story-Driven Testing

Tests mirror the story graph hierarchy:
- **Epic** → test folder
- **Sub-Epic** → nested test folder
- **Lowest Sub-Epic** → 3 test files (server, client, E2E)
- **Story** → test class
- **Scenario** → test method with Given/When/Then helpers

---

## Example

**Domain: Recipients** (from the architecture reference)

```typescript
// packages/recipients/shared/RecipientStatus.ts
export class RecipientStatus {
  constructor(
    public readonly status: RecipientStatusType,
    public readonly createdAt: Date,
    private readonly countryCode: 'US' | 'MX' = 'US'
  ) {}

  isEligibleForPayment(): boolean {
    return this.status === 'Active';
  }

  get remainingPendingMinutes(): number | null {
    if (this.countryCode !== 'MX' || this.status !== 'Pending') return null;
    const elapsed = Date.now() - this.createdAt.getTime();
    return Math.ceil(Math.max(0, 30 * 60 * 1000 - elapsed) / 60000);
  }
}

// packages/recipients/shared/Recipients.ts
export class Recipients {
  constructor(private readonly items: Recipient[]) {}

  filterByStatus(status: RecipientStatusType): Recipients {
    return new Recipients(this.items.filter(r => r.status.status === status));
  }

  search(query: string): Recipients {
    const lower = query.toLowerCase();
    return new Recipients(this.items.filter(r =>
      r.name.toLowerCase().includes(lower)
    ));
  }

  toArray(): Recipient[] { return [...this.items]; }
}

// packages/recipients/server/recipients.service.ts
export class RecipientsService {
  constructor(private repo: RecipientsRepository) {}

  async getRecipients(enterpriseId: string, filters?: { activeOnly?: boolean }) {
    const all = await this.repo.findByEnterprise(enterpriseId);
    let recipients = new Recipients(all);  // SHARED collection class
    if (filters?.activeOnly) {
      recipients = recipients.filterByStatus('Active');  // SHARED method
    }
    return recipients.toArray();
  }
}

// packages/recipients/client/useRecipients.ts
export function useRecipients() {
  const [items, setItems] = useState<Recipient[]>([]);
  useEffect(() => {
    fetchRecipients({ activeOnly: true }).then(setItems);
  }, []);

  const filterBySearch = useCallback((query: string) => {
    return new Recipients(items).search(query).toArray();  // SAME shared logic
  }, [items]);

  return { items, filterBySearch };
}
```

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
│   ├── <Entity>List.tsx             # Container component (list + search)
│   ├── <Entity>Card.tsx             # Presentational component (clickable → detail)
│   ├── Create<Entity>Form.tsx       # Creation form (validates with Zod from shared/)
│   ├── <Entity>DetailView.tsx       # Detail view with mutation controls
│   ├── use<Entity>s.ts              # Custom hook (state + effects)
│   ├── <domain>.api.ts              # API client (one function per server route)
│   ├── index.ts
│   └── package.json                 # depends on shared
│
└── server/                          # Application + Infrastructure (Express)
    ├── <domain>.routes.ts           # Express router
    ├── <domain>.controller.ts       # HTTP → Application translation
    ├── <domain>.service.ts          # Use case orchestration
    ├── <domain>.repository.ts       # MongoDB data access
    ├── <domain>.mapper.ts           # DTO ↔ Entity mapping (optional)
    ├── index.ts
    └── package.json                 # depends on shared
```

Key structural rules:
- `shared/` has **zero** imports from `express`, `react`, `mongodb`, `mongoose`
- `server/` imports from `shared/` — never from `client/`
- `client/` imports from `shared/` — never from `server/`
- Zod schemas in `shared/` are used by both repository (`.parse()`) and forms (`.safeParse()`)
- Domain entity methods (e.g., `isEligibleForPayment()`) are called from both tiers
- `client/` has **one API function per server route** — no unreachable endpoints
- `client/` exposes UI controls only for **user actions defined in the specs**; POST endpoints may be user-facing or system-only
- When the specs say users can create entities, include a **creation form**; when the specs define sub-item interactions, include a **detail view**
- When the specs say a user can do something, make sure the client tier exposes that capability through some type of UI control
- `app-client/App.tsx` manages **view navigation** (list ↔ create ↔ detail) — never a static single-view render

---

## Build

**Goal:** Author a complete domain module — turn domain requirements into all three tier packages as defined by the template.

- **Outputs:** One complete domain module with `shared/`, `client/`, `server/` packages. Each tier has its own `package.json` and `index.ts`.
- **Per format:** shared/ contains entities + schemas + collections. server/ contains routes + controller + service + repository. client/ contains components + hooks + API client.
- **While writing:** Use domain language for all names. Keep shared/ framework-free. Validate Zod schemas at boundaries. Business logic on entities, not services.
- **Persistence:** Monorepo `package.json` with workspaces pointing to all tier packages.

**Build steps:**
1. Identify the domain entity and its responsibilities from the story/requirements.
2. Create `shared/` — entity class, value objects, Zod schema, collection class.
3. Create `server/` — repository (MongoDB + schema validation), service (orchestration using shared collection), controller (HTTP parsing), routes (URL mapping).
4. Create `client/` — API client (one function per server route), hook (state + shared collection for filtering), components (list + card + **forms and detail views for every user action defined in the specs**). If the spec says users can create entities or interact with sub-items, the client must expose those capabilities through UI controls.
5. Ensure `packages/app-server/` exists — create it if missing; otherwise mount the new domain routes in the existing Express composition root. Required for E2E tests.
6. Ensure `packages/app-client/` exists — create it if missing; otherwise render or route to the new domain UI from the existing React/Vite composition root. **The App.tsx must manage view state** to navigate between list, create form, and detail views. A single static component render is insufficient. Required for E2E tests.
7. **Always create `packages/app-client/src/pages/HomePage.tsx`** with links to every major page route, and wire it to `<Route path="/" ... />` in `App.tsx`. This is the first page users see at `localhost:3000`.
8. **Always create `scripts/dev.ps1` and `scripts/dev.sh`** (if they don't already exist) to start both `app-server` and `app-client` with a single command. Also add `dev:api` and `dev:client` to root `package.json` scripts.
7. Create test structure — `tests/{epic}/{sub-epic}/` with helpers and 3 tier test files.
8. Create `scripts/` test runner scripts — `test.sh`, `test.ps1`, `test-e2e.sh`, `test-e2e.ps1` — at the workspace root. The `.sh` scripts navigate to the workspace root and call `npx vitest run` or `npx playwright test`; the `.ps1` scripts do the same for Windows. If the `scripts/` folder already exists, add only the missing scripts.
9. Run scanners to verify structural compliance.

---

## Validate

**Goal:** Inspect what was built — read the artifacts as reviewers, not a second authoring pass.

- **Who is checking:** Software Architect (layer purity, dependency direction), Domain Expert (ubiquitous language, entity behavior), Tech Lead (full interface implementation, no stubs), QA Lead (test structure, all 3 tiers, Given/When/Then).
- **Cross-artifact parity:** shared/ entities used identically by both client/ and server/. Same Zod schema validates on both sides. Collection class methods produce same results regardless of tier.

**Validation checklist:**

- Every domain entity in `shared/` has business methods — no anemic data bags.
- `shared/` contains zero framework imports (`express`, `react`, `mongodb`, `mongoose`).
- `server/` does not import from `client/`; `client/` does not import from `server/`.
- Zod schema is used at repository boundary (`.parse()`) AND API/form boundary (`.safeParse()`).
- Each domain module has `index.ts` and `package.json` in every tier.
- `server/` has `*.routes.ts`, `*.controller.ts`, `*.service.ts`, `*.repository.ts`.
- `client/` has `*.api.ts`, `use*.ts`, `*.tsx` components.
- **`client/` API file exports one function per server route** — no endpoints left unreachable.
- **`client/` has UI controls (forms, buttons, detail views) for every user action defined in the specs** — not just read-only list/search.
- **`app-client/App.tsx` implements view navigation** when specs define multiple user flows (create, view detail, interact) — not a single static render.
- Test folders follow `tests/{epic}/{sub-epic}/` with 3 tier files + helpers/.
- `scripts/` folder exists with `test.sh`, `test.ps1`, `test-e2e.sh`, `test-e2e.ps1`.
- All interfaces use TypeScript `implements` keyword for compile-time verification.
- Test methods mirror Gherkin scenario titles using Given/When/Then helpers.

Run scanners as final verification: `domain_structure_scanner.py`, `layer_purity_scanner.py`, `naming_convention_scanner.py`, `test_structure_scanner.py`, `test_isolation_scanner.py`.

---

<!-- execute_rules:bundle_rules:begin -->
### Rule: Ensure Type-Safe Controllers

Controllers in the `server/` tier must compile without implicit `any` types or missing property errors. When controllers access extended Express `Request` properties (e.g., `req.user`, `req.session`), they must include the necessary type declarations.

#### Express Type Augmentation

When a controller accesses properties not in the base Express `Request` type, include a **global type augmentation** at the top of the controller file:

```typescript
// packages/todo-lists/server/todoLists.controller.ts

import { Request, Response } from 'express';

declare global {
  namespace Express {
    interface Request {
      user?: { id: string };
    }
  }
}
```

This ensures `req.user` is typed correctly and `tsc --noEmit` passes without errors.

#### Lambda Parameter Types

When `strict` or `noImplicitAny` is enabled in `tsconfig.json`, all callback parameters must have explicit types. Use the domain types from `shared/`:

```typescript
// CORRECT — explicit type from shared domain
import { Task } from '@taskflow/todo-lists-shared';

const tasks = dto.tasks.map((t: TaskDTO) => Task.create({ ... }));
todoList.tasks.map((task: Task) => ({ ... }));

// WRONG — implicit any parameter
const tasks = dto.tasks.map(t => Task.create({ ... }));
```

#### DO

- Include `declare global { namespace Express { ... } }` when accessing `req.user`, `req.session`, or any custom middleware-injected property.
- Type all lambda/callback parameters explicitly when `noImplicitAny` or `strict` is enabled.
- Place the type augmentation in the controller file that uses it (or in a shared `types.d.ts`).
- Use domain types from `shared/` for parameters rather than `any`.

#### DON'T

- Access `req.user` or other extended properties without a type declaration — this causes TS2339.
- Leave callback parameters untyped under `strict` mode — this causes TS7006.
- Use `(req as any).user` to bypass type checking — augment the type instead.
- Suppress errors with `// @ts-ignore` instead of providing proper types.

### Rule: Implement Domain Entities Correctly

Business rules belong **on domain classes**, not in services. Domain entities own their state and behavior — they are not anemic data bags passed to services that do all the work. Zod schemas validate at the **repository boundary** (raw data → typed entity) and at the **API boundary** (request body → validated input). Value Objects encapsulate domain constraints (e.g., SWIFT format, status transitions). Collection classes provide domain-oriented query methods.

#### DO

- Place business logic as methods on the entity or value object that owns the data.
- Use Value Objects for constrained values: `RecipientStatus`, `BeneficiaryBank`, `RecipientEmail`.
- Create collection classes (e.g., `Recipients`) that wrap arrays with domain-oriented filter/search methods.
- Validate with `Schema.parse()` at the repository boundary (converting raw docs to entities).
- Validate with `Schema.safeParse()` at the API/form boundary (user input → request).
- Keep domain classes portable: no framework imports, no side effects, no async.

```typescript
// packages/recipients/shared/RecipientStatus.ts — CORRECT: logic on the value object
export class RecipientStatus {
  constructor(
    public readonly status: RecipientStatusType,
    public readonly createdAt: Date,
    private readonly countryCode: 'US' | 'MX' = 'US'
  ) {}

  isEligibleForPayment(): boolean {
    return this.status === 'Active';
  }

  get remainingPendingMinutes(): number | null {
    if (this.countryCode !== 'MX' || this.status !== 'Pending') return null;
    const elapsed = Date.now() - this.createdAt.getTime();
    return Math.ceil(Math.max(0, 30 * 60 * 1000 - elapsed) / 60000);
  }
}
```

```typescript
// packages/recipients/shared/Recipients.ts — CORRECT: collection with domain methods
export class Recipients {
  constructor(private readonly items: Recipient[]) {}

  filterByStatus(status: RecipientStatusType): Recipients {
    return new Recipients(this.items.filter(r => r.status.status === status));
  }

  search(query: string): Recipients {
    const lower = query.toLowerCase();
    return new Recipients(this.items.filter(r =>
      r.name.toLowerCase().includes(lower)
    ));
  }

  toArray(): Recipient[] { return [...this.items]; }
  get length(): number { return this.items.length; }
}
```

#### DON'T

- Place business rules in services while leaving entities as plain data objects (Anemic Domain Model).
- Scatter validation logic outside the schema/entity boundary.
- Use raw `Recipient[]` arrays everywhere instead of typed collection classes.
- Put async operations or framework calls inside domain entities.

```typescript
// WRONG — Anemic Domain Model: service does all the work, entity is a data bag
export interface Recipient {
  id: string;
  name: string;
  status: string;
}

export class RecipientService {
  isEligible(recipient: Recipient): boolean {   // WRONG: logic belongs on the entity
    return recipient.status === 'Active';
  }

  filterActive(recipients: Recipient[]): Recipient[] {  // WRONG: use a collection class
    return recipients.filter(r => r.status === 'Active');
  }
}
```

```typescript
// WRONG — domain entity with framework dependency
export class Recipient {
  async save() {                          // WRONG: persistence in domain entity
    await mongoose.model('Recipient').save(this);
  }
}
```

### Rule: Implement Full Interfaces

Every layer that claims to implement a domain interface must implement **all members**. Test adapters must correctly implement domain interfaces — no stub no-ops, no missing methods, no partial implementations. Both presentation (client) and persistence (server) layers implement the same domain interfaces independently, so domain logic is consistent across tiers. Verify completeness at compile time using TypeScript's type checker. Initialization order matters: all dependencies must be assigned before calling methods that use them.

#### DO

- Implement every method and property defined in the domain interface.
- Use TypeScript `implements` keyword so the compiler catches missing members.
- Ensure test adapters (mocks, fakes) implement the full interface.
- Assign all dependencies in the constructor before any method calls.
- Verify at compile time: `tsc --noEmit` should report zero errors for interface compliance.

```typescript
// packages/recipients/shared/types.ts — domain interface
export interface RecipientRepository {
  findAll(): Promise<Recipient[]>;
  findByIds(ids: string[]): Promise<Recipient[]>;
  findByEnterprise(enterpriseId: string): Promise<Recipient[]>;
}

// packages/recipients/server/recipients.repository.ts — CORRECT: all methods implemented
export class MongoRecipientsRepository implements RecipientRepository {
  constructor(private db: Db) {}

  async findAll(): Promise<Recipient[]> { ... }
  async findByIds(ids: string[]): Promise<Recipient[]> { ... }
  async findByEnterprise(enterpriseId: string): Promise<Recipient[]> { ... }
}

// tests/.../helpers/fake-recipients.repository.ts — CORRECT: test adapter implements full interface
export class FakeRecipientsRepository implements RecipientRepository {
  private items: Recipient[] = [];

  async findAll() { return this.items; }
  async findByIds(ids: string[]) { return this.items.filter(r => ids.includes(r.id)); }
  async findByEnterprise(eid: string) { return this.items.filter(r => r.enterpriseId === eid); }

  seed(recipients: Recipient[]) { this.items = recipients; }
}
```

#### DON'T

- Leave interface methods unimplemented or stubbed with `throw new Error('not implemented')`.
- Skip `implements` keyword — without it, TypeScript won't catch missing members.
- Create test adapters that only implement the methods used in one test (partial mocks).
- Call methods that depend on constructor-injected dependencies before those dependencies are assigned.
- Group unrelated methods into a single interface (Interface Segregation violation).

```typescript
// WRONG — partial implementation, missing findByEnterprise
export class RecipientsRepo implements RecipientRepository {
  async findAll() { ... }
  async findByIds(ids: string[]) { ... }
  // findByEnterprise is MISSING — compile error if `implements` is used
}

// WRONG — test adapter stubs with no-ops
export class MockRecipientsRepository implements RecipientRepository {
  async findAll() { return []; }
  async findByIds() { throw new Error('not implemented'); }  // WRONG: stub no-op
  async findByEnterprise() { return []; }
}

// WRONG — initialization order bug
export class RecipientsService {
  constructor(private repo: RecipientsRepository) {
    this.loadCache();  // WRONG: calls method before subclass fields are initialized
  }
}
```

### Rule: Include All External Dependencies

Every `package.json` must declare **all** external packages that its source files import. After `npm install`, the project must compile with zero unresolved module errors. This is non-negotiable — generated code that cannot compile is useless.

#### Required Dependencies by Tier

| Tier | Required dependencies | Required devDependencies |
|------|----------------------|--------------------------|
| **shared/** | `zod` | — |
| **server/** | `express`, `mongodb`, workspace shared package | `@types/express` |
| **client/** | `react`, `react-dom`, workspace shared package | `@types/react`, `@types/react-dom` |
| **root** | — | `typescript`, test framework packages (see below) |

##### Test Dependencies (root devDependencies)

When generating test files, the root `package.json` must include:

| Test framework | Required packages |
|---|---|
| **Server tests** | `vitest`, `jsdom` |
| **Client tests** (React component tests) | `vitest`, `jsdom`, `@testing-library/react`, `@testing-library/jest-dom` |
| **E2E tests** (Playwright) | `@playwright/test` |

**Never use `node:test` in Vitest-managed test files.** All `*_server.test.ts` and `*_client.test.tsx` files must import `describe`, `it`, `expect`, `beforeEach`, and `vi` from `'vitest'` — not `'node:test'`. Mixing test runners causes "No test suite found" failures and ESM/CJS conflicts.

##### Test Runner Config Files

The project **must** include both a `vitest.config.ts` and a `playwright.config.ts` at the root to prevent each runner from picking up the other's test files:

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    include: ['tests/**/*_server.test.ts', 'tests/**/*_client.test.tsx'],
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
  },
});

// playwright.config.ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testMatch: '**/*_e2e.spec.ts',
  use: { baseURL: 'http://localhost:3000' },
});
```

Without these configs:
- Playwright picks up `*_client.test.tsx` Vitest files → ESM/CJS import error on `vitest` module
- Vitest picks up `*_e2e.spec.ts` Playwright files → "No test suite found" failure

The `tsconfig.json` must also include test type declarations:
```json
{
  "compilerOptions": {
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  },
  "include": [
    "packages/**/*.ts",
    "packages/**/*.tsx",
    "tests/**/*.ts",
    "tests/**/*.tsx"
  ]
}
```

##### Test Import Paths

Test files use the same package-name-based imports as production code. The `tsconfig.json` must include path aliases for **all** tier packages (shared, server, client) so tests can resolve them:

```json
{
  "compilerOptions": {
    "paths": {
      "@appName/domain-shared": ["./packages/domain/shared/index.ts"],
      "@appName/domain-server": ["./packages/domain/server/index.ts"],
      "@appName/domain-client": ["./packages/domain/client/index.ts"],
      "@appName/domain-client/*": ["./packages/domain/client/*"]
    }
  }
}
```

The wildcard path (`@appName/domain-client/*`) is needed when test files import sub-modules (e.g., `import * as api from '@appName/domain-client/todoLists.api'`).

Add additional packages when the generated code imports them (e.g., `crypto` for Node.js UUID, `@tanstack/react-query` for data fetching).

#### DO

- List every imported external module in `dependencies` or `devDependencies`.
- Include `@types/*` packages for libraries that don't ship their own type declarations.
- Use caret ranges (`^`) for version flexibility: `"zod": "^3.22.0"`.
- Include `typescript` in the root `package.json` devDependencies.
- Verify the project compiles after generation by running `npx tsc --noEmit`.
- Verify all modules resolve after `npm install` by checking for `Cannot find module` errors.

```json
// packages/{domain}/shared/package.json — CORRECT: includes zod
{
  "name": "@appName/domain-shared",
  "dependencies": {
    "zod": "^3.22.0"
  }
}

// packages/{domain}/server/package.json — CORRECT: includes express + mongodb + types
{
  "name": "@appName/domain-server",
  "dependencies": {
    "@appName/domain-shared": "*",
    "express": "^4.18.0",
    "mongodb": "^6.0.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.0"
  }
}

// packages/{domain}/client/package.json — CORRECT: includes react + types
{
  "name": "@appName/domain-client",
  "dependencies": {
    "@appName/domain-shared": "*",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0"
  }
}
```

#### DON'T

- Omit external packages from `dependencies` and rely on hoisting or implicit resolution.
- Generate source files that import modules not listed in any `package.json`.
- Skip `@types/*` packages — TypeScript will report `Could not find a declaration file`.
- Use `*` or `latest` for external packages (only for workspace internal references).
- Assume any dependency is "already installed" — declare everything explicitly.

```json
// WRONG — missing zod, express, react, mongodb
{
  "name": "@appName/domain-server",
  "dependencies": {
    "@appName/domain-shared": "*"
  }
}
```

#### Validation After Generation

After generating all files, the agent MUST:

1. Run `npm install` from the workspace root — must exit with code 0.
2. Run `npx tsc --noEmit` — must report zero errors.
3. If either step fails, diagnose and fix before considering implementation complete.

Compilation failures caused by missing dependencies are **blocking violations** — the generated module is not done until it compiles.

### Rule: Maintain Layer Purity

Dependencies point inward toward the domain core. The `shared/` package contains **plain TypeScript only** — no framework imports. The `server/` package never imports from `client/`, and vice versa. Both `client/` and `server/` depend on `shared/`, but `shared/` depends on neither.

#### DO

- Keep `shared/` free of Express, React, MongoDB, Mongoose, and any infrastructure framework.
- Use only plain TypeScript, Zod (validation), and standard library in `shared/`.
- Import domain logic from `shared/` into both `client/` and `server/`.
- Place HTTP/Express concerns exclusively in `server/`.
- Place React/UI concerns exclusively in `client/`.

```typescript
// packages/recipients/shared/RecipientStatus.ts — CORRECT: plain TypeScript only
export type RecipientStatusType = 'Active' | 'Pending' | 'Inactive';

export class RecipientStatus {
  constructor(
    public readonly status: RecipientStatusType,
    public readonly createdAt: Date
  ) {}

  isEligibleForPayment(): boolean {
    return this.status === 'Active';
  }
}
```

```typescript
// packages/recipients/server/recipients.service.ts — CORRECT: imports from shared
import { Recipients } from '@project/recipients/shared';
import { RecipientsRepository } from './recipients.repository';

export class RecipientsService {
  constructor(private repo: RecipientsRepository) {}

  async getRecipients(enterpriseId: string) {
    const all = await this.repo.findByEnterprise(enterpriseId);
    return new Recipients(all).filterByStatus('Active').toArray();
  }
}
```

```typescript
// packages/recipients/server/recipients.service.ts — CORRECT: depends on interface, not concrete class
import { RecipientsRepositoryInterface } from './recipients.repository';

export class RecipientsService {
  constructor(private repo: RecipientsRepositoryInterface) {}  // interface — not the concrete MongoRepo
}
```

#### DON'T

- Import Express, React, MongoDB, or any framework/infrastructure library in `shared/`.
- Import `client/` code from `server/` or `server/` code from `client/`.
- Place React components or hooks in `shared/`.
- Place Express middleware or route handlers in `shared/`.
- Depend on the concrete repository class in the service layer — services must accept the repository **interface** so they can work with any implementation (MongoDB, in-memory, test fake).

```typescript
// packages/recipients/shared/Recipient.ts — WRONG: framework import in shared
import { Schema, model } from 'mongoose';  // VIOLATION: infrastructure in domain core
import express from 'express';              // VIOLATION: server framework in shared

export const RecipientSchema = new Schema({ ... });
```

```typescript
// packages/recipients/server/recipients.service.ts — WRONG: importing from client
import { useRecipients } from '@project/recipients/client';  // VIOLATION: server imports client
```

```typescript
// packages/recipients/server/recipients.service.ts — WRONG: depends on concrete class
import { RecipientsRepository } from './recipients.repository';  // VIOLATION: concrete class, not interface

export class RecipientsService {
  constructor(private repo: RecipientsRepository) {}  // breaks when swapping implementations
}
```

### Rule: Organize by Domain Module

Organize code by **business capability** (domain module) first, then by technical layer within each module. This ensures that all code for a single domain lives together — changes rarely ripple to other domains, teams can own entire domains, and each module can become its own microservice later without restructuring.

#### DO

- Structure each domain as `packages/{domain}/{shared|client|server}`.
- Include `index.ts` and `package.json` in each tier folder for clean imports.
- Keep the app shell (`app-server/`, `app-client/`) at the packages level as composition roots.
- **Ensure `packages/app-server/` and `packages/app-client/` exist** as part of generating a domain module. If either root is missing, scaffold it. If either already exists, update it to mount or render the new domain module instead of generating a duplicate shell.
- **Ensure the client tier provides UI for every user action defined in the specs.** If the requirements say a user can create a board, add tasks, or move items — the client must have corresponding forms, buttons, or controls. Derive required UI from the spec, not from a mechanical endpoint mirror.
- **Wire navigation in `app-client/App.tsx`** to support all spec-driven user flows (e.g., create → view → interact). The composition root must manage view state when multiple views are needed.
- **Always create `scripts/dev.ps1`** (and `scripts/dev.sh`) if no startup script exists. The script must start both `packages/app-server/` and `packages/app-client/` so the developer can open `http://localhost:3000` immediately after running it. Also add `dev:api` and `dev:client` entries to the root `package.json` scripts.
- **Always include a home page at `/`** in `app-client/App.tsx`. The home page must render navigable links to every major page route in the app. This is the entry point a user hits at `localhost:3000` — without it, the app appears blank and every page route is unreachable from the browser.
- - **Ensure every user action has a user-facing form and server endpoint/route.** Some POST routes exist for system-to-system workflows, background processing, or integration callbacks and should remain server-only unless the specs explicitly define a user action behind them.
- Place test files under `tests/{epic}/{sub-epic}/` mirroring the domain structure.

```
project-root/
├── packages/
│   ├── recipients/              # Domain module
│   │   ├── shared/              # Domain core (entities, schemas, value objects)
│   │   │   ├── Recipient.ts
│   │   │   ├── recipient.schema.ts
│   │   │   ├── index.ts
│   │   │   └── package.json
│   │   ├── client/              # React frontend for this domain
│   │   │   ├── RecipientSelector.tsx
│   │   │   ├── CreateRecipientForm.tsx
│   │   │   ├── RecipientDetailView.tsx
│   │   │   ├── useRecipients.ts
│   │   │   ├── recipients.api.ts
│   │   │   ├── index.ts
│   │   │   └── package.json
│   │   └── server/              # Express backend for this domain
│   │       ├── recipients.routes.ts
│   │       ├── recipients.controller.ts
│   │       ├── recipients.service.ts
│   │       ├── recipients.repository.ts
│   │       ├── index.ts
│   │       └── package.json
│   ├── app-server/              # Composition root: create if missing, otherwise reuse
│   │   ├── app.ts              # Creates Express app, mounts domain routers
│   │   ├── index.ts
│   │   └── package.json
│   └── app-client/              # Composition root: create if missing, otherwise reuse
│       ├── App.tsx             # Renders domain components; MUST include <Route path="/" element={<HomePage />} />
│       ├── pages/
│       │   └── HomePage.tsx    # Home page: links to every major page route in the app
│       ├── main.tsx            # Entry point (createRoot)
│       ├── index.html
│       ├── vite.config.ts
│       ├── index.ts
│       └── package.json
├── tests/
└── package.json
```

#### DON'T

- Organize by technical layer at the top level (`controllers/`, `models/`, `views/`, `routes/`).
- Scatter a single domain's code across multiple unrelated folders.
- Mix multiple domain concerns in a single folder.
- **Generate domain module packages in a new project without also scaffolding missing composition roots.** Without these, the application cannot start and E2E tests fail with `ERR_CONNECTION_REFUSED`.
- **Create duplicate `app-server/` or `app-client/` shells, or overwrite an existing composition root, when adding a module to an existing project.** Extend the existing shells instead.
- **Ship a client tier that omits user actions defined in the specs.** If the requirements say users can create, edit, or move things, the UI must expose those capabilities — not just read-only search/list.
- **Mirror POST endpoints into UI controls by default.** A server route may support integrations or internal workflows without implying a corresponding form or button in the client tier.
- **Render a single static component in App.tsx when the specs define multiple user flows.** If users need to create entities and interact with detail views, the composition root must manage view state to support those flows.
- **Omit a home page at `/`.** Every app must have a `HomePage.tsx` with links to all page routes. Without it, hitting `localhost:3000` shows a blank page.
- **Omit a startup script.** Always create `scripts/dev.ps1` and `scripts/dev.sh` that start both the API server and the React frontend. Without them, the developer has no single command to bring the app up.
- **Do not assume every POST endpoint needs a user-facing form.** Some POST routes exist for system-to-system workflows, background processing, or integration callbacks and should remain server-only unless the specs explicitly define a user action behind them.

```
# WRONG — technical-first organization
project-root/
├── controllers/
│   ├── recipientController.ts    # Recipient logic scattered
│   └── paymentController.ts
├── models/
│   ├── Recipient.ts              # ... across multiple folders
│   └── Payment.ts
├── routes/
│   ├── recipientRoutes.ts        # ... making changes ripple everywhere
│   └── paymentRoutes.ts
└── views/
    ├── RecipientList.tsx
    └── PaymentForm.tsx
```

### Rule: Scaffold Test Runner Scripts

Every generated MERN project must include a `scripts/` folder at the workspace root with shell scripts that invoke each test tier. These scripts make test commands discoverable, CI-friendly, and runnable without knowing npm script names.

#### Required Scripts

| File | Tier | Requires |
|------|------|---------|
| `scripts/test.sh` | Server + client unit/component tests (Vitest) | Node.js only |
| `scripts/test.ps1` | Same — Windows equivalent | Node.js only |
| `scripts/test-e2e.sh` | End-to-end browser tests (Playwright) | `packages/app-client` serving the React frontend |
| `scripts/test-e2e.ps1` | Same — Windows equivalent | `packages/app-client` serving the React frontend |

**`test.sh` / `test.ps1` do NOT run E2E tests.** They run Vitest only — server and client unit/component tests. This is intentional: E2E tests require a live frontend and are a separate step.

**`test-e2e.sh` / `test-e2e.ps1` require `packages/app-client` to exist and be wired into `playwright.config.ts`.** Without a running React frontend, every Playwright test will fail with `Cannot GET /<route>` because the page routes (`/products/:sku`, `/store-locator`, etc.) only exist when a frontend app is serving them. The API routes (`/api/...`) are not the same as page routes.

#### Script Contents

##### `scripts/test.sh`

```bash
#!/usr/bin/env bash
# Runs server and client unit/component tests ONLY (Vitest).
# Does NOT run E2E tests. Use scripts/test-e2e.sh for end-to-end tests.
set -euo pipefail
cd "$(dirname "$0")/.."
npx vitest run
```

##### `scripts/test.ps1`

```powershell
# Runs server and client unit/component tests ONLY (Vitest).
# Does NOT run E2E tests. Use scripts/test-e2e.ps1 for end-to-end tests.
Set-Location (Split-Path -Parent $PSScriptRoot)
npx vitest run
```

##### `scripts/test-e2e.sh`

```bash
#!/usr/bin/env bash
# Runs Playwright end-to-end tests.
#
# REQUIRES: packages/app-client must exist and serve the React frontend.
# Without it, page routes like /products/:sku do not exist and every test
# will fail with "Cannot GET /<route>".
set -euo pipefail
cd "$(dirname "$0")/.."
npx playwright test
```

##### `scripts/test-e2e.ps1`

```powershell
# Runs Playwright end-to-end tests.
#
# REQUIRES: packages/app-client must exist and serve the React frontend.
# Without it, page routes like /products/:sku do not exist and every test
# will fail with "Cannot GET /<route>".
Set-Location (Split-Path -Parent $PSScriptRoot)
npx playwright test
```

The `playwright.config.ts` `webServer` block starts the Express API server automatically. The React frontend must also be wired into `webServer` (as a second entry) before E2E tests can pass.

#### DO

- Create all four scripts every time a new project is scaffolded.
- Make `.sh` scripts executable: `git update-index --chmod=+x scripts/test.sh scripts/test-e2e.sh`.
- Keep scripts thin — they `cd` to the workspace root and delegate to `npx`; no test logic lives in the script.
- Include `set -euo pipefail` in `.sh` scripts so failures surface immediately.
- Include the `# REQUIRES:` comment in both `test-e2e` scripts so developers know what must exist before running them.
- Add both the API server **and** the React frontend as `webServer` entries in `playwright.config.ts` before claiming E2E tests are runnable.

```typescript
// playwright.config.ts — CORRECT: both servers declared
webServer: [
  {
    command: 'node --import tsx/esm packages/app-server/dev.ts',
    url: 'http://localhost:3001/health',
    reuseExistingServer: true,
  },
  {
    command: 'npx vite packages/app-client',
    url: 'http://localhost:3000',
    reuseExistingServer: true,
  },
],
```

#### DON'T

- Omit the `# REQUIRES:` comment from the `test-e2e` scripts.
- Omit either platform's scripts — teams on Windows need `.ps1`; teams on Mac/Linux need `.sh`.
- Hard-code absolute paths in scripts — always navigate relative to the script's own location.
- Claim that E2E tests are complete or passing just because the `*_e2e.spec.ts` files compile and list with `--list`. **Spec files existing ≠ E2E tests passing.** They need a live frontend serving real page routes.
- Generate `test-e2e.sh` without first verifying `packages/app-client` exists and is wired into `playwright.config.ts`.

```bash
# WRONG — no warning, developer has no idea why every test fails
#!/usr/bin/env bash
npx playwright test
```

### Rule: Share Domain Logic

Define domain entities, value objects, Zod validation schemas, and business rule methods **once** in the `shared/` package. Both `client/` and `server/` import from `shared/` — never duplicate validation, type definitions, or business logic across tiers. This eliminates drift between frontend and backend validation, ensures consistent behavior, and creates a single source of truth for domain rules.

#### DO

- Place all Zod schemas in `shared/` so both tiers validate identically.
- Define domain entity classes with business methods in `shared/`.
- Export collection/aggregate classes (e.g., `Recipients`) from `shared/` for reuse in both tiers.
- Use the shared schema in the repository layer to validate raw DB documents into typed entities.
- Use the same shared schema in the client for form validation before HTTP calls.
- **Hydrate API responses** into domain class instances in the API client layer. `fetch()` returns plain JSON objects — calling domain methods like `completedCount()` on them throws `TypeError: not a function`. The API client (`*.api.ts`) must reconstruct domain entities using static factory methods (e.g., `TodoList.create()`, `Task.create()`).

```typescript
// packages/todo-lists/client/todoLists.api.ts — CORRECT: hydrates JSON → domain classes
import { TodoList, Task } from '@taskflow/todo-lists-shared';

function hydrateTodoList(raw: any): TodoList {
  const tasks = (raw.tasks || []).map((t: any) =>
    Task.create({ id: t.id, title: t.title, completed: t.completed, createdAt: new Date(t.createdAt) })
  );
  return TodoList.create({
    id: raw.id, userId: raw.userId, name: raw.name, tasks,
    createdAt: new Date(raw.createdAt), updatedAt: new Date(raw.updatedAt),
  });
}

export async function fetchTodoLists(): Promise<TodoList[]> {
  const response = await fetch(API_BASE);
  const data = await response.json();
  return (data.items || []).map(hydrateTodoList);  // hydrate each item
}
```

```typescript
// WRONG — returns raw JSON, domain methods will crash at runtime
export async function fetchTodoLists(): Promise<TodoList[]> {
  const response = await fetch(API_BASE);
  const data = await response.json();
  return data.items;  // BUG: these are plain objects, not class instances
}
```

```typescript
// packages/recipients/shared/recipient.schema.ts — CORRECT: single source of truth
import { z } from 'zod';

export const RecipientSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(140),
  status: z.enum(['Active', 'Pending', 'Inactive']),
  beneficiaryBank: BeneficiaryBankSchema,
});

export type RecipientDTO = z.infer<typeof RecipientSchema>;
```

```typescript
// packages/recipients/server/recipients.repository.ts — CORRECT: validates with shared schema
import { RecipientSchema } from '@project/recipients/shared';

async findAll(): Promise<Recipient[]> {
  const docs = await this.collection.find().toArray();
  return docs.map(doc => RecipientSchema.parse(doc));  // shared validation
}
```

```typescript
// packages/recipients/client/RecipientForm.tsx — CORRECT: same schema for client validation
import { RecipientSchema } from '@project/recipients/shared';

const result = RecipientSchema.safeParse(formData);
if (!result.success) { setErrors(result.error.issues); }
```

#### DON'T

- Duplicate Zod schemas or validation logic between `client/` and `server/`.
- Redefine TypeScript interfaces that already exist in `shared/`.
- Place business rule methods (e.g., eligibility checks) in only one tier.
- Create separate "client types" and "server types" for the same domain concept.

```typescript
// packages/recipients/server/validation.ts — WRONG: duplicated schema
import { z } from 'zod';
export const ServerRecipientSchema = z.object({  // DUPLICATE of shared schema
  id: z.string().uuid(),
  name: z.string().min(1).max(140),
  status: z.enum(['Active', 'Pending', 'Inactive']),
});
```

```typescript
// packages/recipients/client/types.ts — WRONG: separate type definition
export interface ClientRecipient {  // DUPLICATE: already defined in shared
  id: string;
  name: string;
  status: 'Active' | 'Pending' | 'Inactive';
}
```

### Rule: Test Story-Driven

Tests mirror story scenarios across three tiers: **Server-Side** (Node.js Test Runner + Supertest), **Client-Side** (Vitest + Testing Library), and **E2E** (Playwright). Each tier tests the **same scenarios** with different emphasis. The test folder hierarchy maps directly to the story graph: Epic → Folder, Sub-Epic → Folder, Lowest Sub-Epic → 3 test files (one per tier). Each test file contains one class per Story and one method per Scenario using Given/When/Then helper methods from a shared base helper.

#### DO

- Organize test folders by `tests/{epic}/{sub-epic}/`.
- Create exactly 3 test files per lowest sub-epic: `*_server.test.ts`, `*_client.test.tsx`, `*_e2e.spec.ts`.
- Create a `helpers/` folder per sub-epic with base, server, client, and e2e helpers.
- Name test methods to mirror Gherkin scenario titles verbatim.
- Use Given/When/Then helper methods that read like scenario steps.
- Share test data and abstract helpers in the `.base.ts` helper.

```
tests/
├── create-wire-payment/                    # Epic folder
│   └── select-recipient/                   # Sub-Epic folder (lowest level)
│       ├── helpers/
│       │   ├── select-recipient.base.ts    # Shared test data & abstract helpers
│       │   ├── select-recipient.server.ts  # Server-tier helper (Supertest)
│       │   ├── select-recipient.client.ts  # Client-tier helper (Testing Library)
│       │   └── select-recipient.e2e.ts     # E2E-tier helper (Playwright)
│       ├── select-recipient_server.test.ts
│       ├── select-recipient_client.test.tsx
│       └── select-recipient_e2e.spec.ts
```

```typescript
// select-recipient_server.test.ts — CORRECT: Class = Story, Method = Scenario
import { SelectRecipientServerHelper } from './helpers/select-recipient.server';

class TestViewActiveRecipients {
  helper = new SelectRecipientServerHelper();

  async test_user_views_list_of_active_recipients() {
    await this.helper.givenUserLoggedIntoChannelOne();
    await this.helper.givenEnterpriseHasRecipientsWithActiveStatus();
    await this.helper.whenUserInitiatesWirePayment();
    await this.helper.thenOnlyActiveRecipientsDisplayed();
  }
}
```

#### DON'T

- Skip any of the three test tiers for a sub-epic.
- Write tests without Given/When/Then helper methods.
- Name test methods with technical HTTP language instead of scenario language.
- Write E2E tests separately without reusing the base helper class.
- Place test files outside the epic/sub-epic folder structure.
- **Mock `fetch` without realistic response shape.** If the API client checks `response.ok`, the mock must include `ok: true`. Incomplete mocks cause silent failures that only surface as "element not found" errors.

```typescript
// WRONG — no helper, no Given/When/Then structure, technical naming
test('GET /api/recipients returns 200', async () => {
  const res = await request(app).get('/api/recipients');
  expect(res.status).toBe(200);
  expect(res.body.recipients.length).toBe(2);
});

// WRONG — tests placed in flat structure, not by epic/sub-epic
tests/
├── recipients.test.ts        # No hierarchy, no tier separation
├── payments.test.ts
└── e2e.spec.ts               # All E2E in one file
```

### Rule: Use Thorough E2E Tests

End-to-end tests are **mandatory** for every sub-epic. E2E tests must reuse the base helper class (not be manually written from scratch), verify **logic** (filtering, eligibility, domain rules) not just element presence, and be executed as a final verification step after implementation. E2E tests exercise the same Gherkin scenarios as server and client tests, but through the complete user workflow: browser → React → HTTP → Express → MongoDB → response → rendered UI.

#### E2E Spec Files Existing ≠ E2E Tests Passing

**Generating `*_e2e.spec.ts` files is not the same as having passing E2E tests.** This is a critical distinction.

- `npx playwright test --list` succeeds as long as the spec files compile. It does **not** run the tests.
- `npx vitest run` never runs `*_e2e.spec.ts` files — the Vitest `include` pattern explicitly excludes them. Reporting "all tests pass" after `vitest run` says nothing about E2E.
- E2E tests only pass when a real browser navigates to real page routes served by a live frontend.

**E2E tests require both composition roots to exist and be reachable:**

- `packages/app-server/` — Express entry point that mounts domain API routes
- `packages/app-client/` — React/Vite shell that serves page routes (`/products/:sku`, `/store-locator`, `/admin/...`)

Without `app-client`, navigating to any page route returns `Cannot GET /<route>` — because Express API routes (`/api/...`) are not the same as frontend page routes. The browser has nothing to render. **Every E2E test fails.**

Do **not** tell the user they can run `npx playwright test` until both composition roots exist, are wired to the new module, and are declared in `playwright.config.ts` `webServer`. Running Playwright against a missing frontend produces `Cannot GET` on every test — this is a broken state, not a partial one.

**The complete generation order before E2E tests can pass:**
1. Domain packages (`shared/`, `server/`, `client/`) ← domain module template
2. `packages/app-server/` — scaffold if missing, otherwise mount new domain routes
3. `packages/app-client/` — scaffold if missing, otherwise add page routes for the new domain's views
4. `playwright.config.ts` with `webServer` entries for **both** the API server and the React frontend
5. Run `npx playwright test` — only now can tests actually pass

#### DO

- Create `*_e2e.spec.ts` for every lowest sub-epic.
- Extend the base helper class for E2E-specific setup (Playwright page, browser context).
- Assert on **domain logic outcomes**: filtered lists exclude ineligible items, tooltips show remaining time, selected recipients persist across navigation.
- Run E2E tests after implementation as final verification.
- Test the same scenarios as server/client tiers, with complete workflow emphasis.
- Include edge cases and domain variants, not just the happy path.
- Ensure both `app-server/` and `app-client/` composition roots exist and expose the new module before attempting to run E2E tests. Scaffold missing roots; otherwise update the existing shells and then start the dev server.
- Navigate to `/` (or the correct root route) — only navigate to a sub-route if a router exists that handles it.
- Scope all locators to the specific card/section under test: `page.locator('.card', { hasText: 'Name' })` to prevent strict mode violations when multiple matching elements exist.
- Assert on locator text content after state changes, not on the original element reference — React re-renders replace DOM nodes.
- Seed all required test data within each test via API calls or UI interactions — never rely on pre-existing data in the database.
- Implement both the UI affordance and the test that exercises it together — neither should be left incomplete.
- Use unique names per test run (e.g. append `Date.now()`) to prevent collisions with leftover data from previous runs.
- **Match E2E interactions to the actual UI controls.** If the UI uses a button + dropdown to move items, the E2E helper must click that button and select from the dropdown — not use `dragTo()` or other interactions the UI doesn't support.
- **Wait for async results after mutations.** After clicking "Save" or "Submit", wait for the resulting view to render (e.g., `await heading.waitFor({ state: 'visible' })`) before proceeding to the next step.
- **Handle view state transitions in helpers.** If a "When" step needs the list view but the app is showing a detail view, navigate back first. Check current view state before acting.

```typescript
// select-recipient_e2e.spec.ts — CORRECT: reuses helper, verifies logic
import { test, expect } from '@playwright/test';
import { SelectRecipientE2EHelper } from './helpers/select-recipient.e2e';

test.describe('View Active Recipients', () => {
  const helper = new SelectRecipientE2EHelper();

  test.beforeEach(async ({ page }) => {
    await helper.setup(page);
  });

  test('user views list of active recipients when initiating wire payment', async () => {
    await helper.givenEnterpriseHasRecipientsWithActiveStatus();
    await helper.whenUserInitiatesWirePayment();
    await helper.thenOnlyActiveRecipientsDisplayed();
    await helper.thenPendingRecipientsAreExcluded();  // verifies logic, not just count
  });

  test('user cannot select pending recipient (MX country variance)', async () => {
    await helper.givenCountryIsMX();
    await helper.givenRecipientCreated15MinutesAgo();
    await helper.whenUserViewsRecipientList();
    await helper.thenRecipientIsNotSelectable();
    await helper.thenTooltipShowsRemainingTime('15 minutes');  // verifies domain logic
  });
});
```

#### DON'T

- Skip E2E tests for any sub-epic.
- Write E2E tests that only check element presence without verifying logic.
- Write E2E tests from scratch without reusing the helper class.
- Forget to run E2E tests after implementation.
- Test only the happy path — include edge cases and domain variants.
- Tell the user they can run `npx playwright test` before the required composition roots exist and expose the new module — E2E tests require a live server.
- Claim E2E tests are passing or complete because `*_e2e.spec.ts` files compile, or because `npx playwright test --list` succeeds, or because `npx vitest run` passes. **None of these run E2E tests against a real browser.** E2E tests pass only when Playwright navigates a real browser to real page routes served by a live `app-client` frontend.
- Generate duplicate composition roots for an existing project when compatible `app-server/` and `app-client/` shells already exist.
- Navigate to non-existent routes — if the app has no router, navigate to `/`, not `/todo-lists`.
- Use unscoped locators when multiple elements may match — always scope assertions to a specific card/section using `page.locator('.card', { hasText: 'Specific Name' })`.
- **Use `getByText()` without scoping when the text appears in both a parent container and a child element.** A parent `<div>` containing multiple column names will also match `getByText('Released')`. Scope to the specific element class: `page.locator('.column-tag', { hasText: 'Released' })`.
- Assert on stale element references after state changes — React re-renders replace DOM nodes; assert on the new state via locator text content instead.
- Assume pre-seeded data exists — E2E tests must create their own data via API calls or the UI.
- Leave placeholder or skeleton tests for UI that doesn't exist yet — every E2E scenario must be fully implemented end-to-end: the UI affordance and the test that exercises it must both be complete before moving on. Write them in any order (test-first or component-first), but never leave one without the other.
- Use hardcoded names that may collide with leftover data — use unique names (e.g. append `Date.now()`) so tests are isolated from stale data in the persistent datastore.
- **Use `dragTo()` or other Playwright interactions that don't match the actual UI.** If the component uses click-based interactions (buttons, dropdowns), test with clicks — not drag-and-drop.
- **Proceed to the next step immediately after a mutation without waiting for the result.** Always wait for the expected view/element to appear after a create/update action.
- **Use blanket `deleteMany({})` or "reset all" endpoints in test cleanup.** Only delete the specific resources created during that test run.

```typescript
// WRONG — only checks elements exist, doesn't verify filtering logic
test('recipients page loads', async ({ page }) => {
  await page.goto('/recipients');
  await expect(page.locator('.recipient-card')).toBeVisible();  // WRONG: no logic verified
  // Does NOT check that Pending recipients are excluded
  // Does NOT verify country-specific behavior
});

// WRONG — manually written without helper, duplicates setup logic
test('select recipient', async ({ page }) => {
  await page.goto('/recipients');
  await page.click('[data-testid="recipient-1"]');  // WRONG: hardcoded, no helper
  await expect(page.locator('.selected')).toHaveCount(1);
});
```

#### Test Isolation — NEVER Reset All Data

> **CRITICAL:** Tests must ONLY delete the specific data they created. Never delete all data, never reset the database, never use blanket `deleteMany({})`. This is enforced by `test_isolation_scanner.py`.

E2E tests **must** be independent — each test must pass regardless of run order or previous runs. When using a persistent datastore (MongoDB), accumulated data from prior test runs causes strict mode violations and false assertions.

##### Forbidden patterns (scanner will flag these):
- `deleteMany({})` — empty filter deletes ALL documents
- `.drop()` / `dropCollection()` / `dropDatabase()` — destroys entire collections/databases
- `POST /api/test/reset` or any `/reset` endpoint — blanket wipe
- `beforeEach`/`afterAll` hooks that call any of the above

##### Required pattern — tests clean up ONLY their own data:
1. Each test that creates data **must capture the created resource's ID** (from API response or by querying the GET endpoint after UI creation).
2. Track all created IDs in the test helper (e.g., `createdIds: string[]`).
3. In `afterEach`, delete **only those specific IDs** via `DELETE /api/test/{resource}` with `{ ids: [...] }` body.
4. The server endpoint **must require an `ids` array** and reject requests without one — never expose a "delete all" capability.
5. If no IDs were created during a test, cleanup is a no-op.

##### Why this matters:
- Blanket resets destroy data created by other developers, other test suites, or manual QA sessions sharing the same database.
- Parallel test runs (sharded Playwright workers) can delete each other's data mid-test.
- A "clean slate" approach masks bugs that only surface when real data exists alongside test data.

```typescript
// playwright.config.ts — CORRECT: starts both server and client, waits for each
export default defineConfig({
  webServer: [
    {
      command: 'npx tsx watch packages/app-server/index.ts',
      url: 'http://localhost:3001/health',
      reuseExistingServer: true,
    },
    {
      command: 'cd packages/app-client && npx vite',
      url: 'http://localhost:3000',
      reuseExistingServer: true,
    },
  ],
});
```

```typescript
// CORRECT — test creates data, asserts, then deletes only what it created
test('User marks a task as completed', async ({ page, request }) => {
  // Seed via API — capture the created ID
  const createRes = await request.post('/api/todo-lists', {
    data: { name: 'Errands', tasks: [{ title: 'Buy milk' }] },
  });
  const createdList = await createRes.json();

  await page.goto('/');

  // Scoped locator — targets specific card
  const card = page.locator('.todo-list-card', { hasText: 'Errands' });
  await expect(card).toBeVisible();

  // Assert on outcome, not stale reference
  const checkbox = card.locator('input[type="checkbox"]').first();
  await checkbox.click();
  await expect(card.locator('.task-count')).toContainText('1/1 completed');

  // Cleanup — delete only the item this test created
  await request.delete(`/api/todo-lists/${createdList.id}`);
});

// CORRECT — data created via UI, cleanup via query + delete
test('User creates a new todo list', async ({ page, request }) => {
  await page.goto('/');
  await page.fill('input[placeholder="New list name..."]', 'Shopping List');
  await page.click('button:text("Create List")');

  const card = page.locator('.todo-list-card', { hasText: 'Shopping List' });
  await expect(card).toBeVisible();

  // Cleanup — find the created item and delete it
  const listsRes = await request.get('/api/todo-lists');
  const { items } = await listsRes.json();
  const created = items.find((l: any) => l.name === 'Shopping List');
  if (created) await request.delete(`/api/todo-lists/${created.id}`);
});
```

```typescript
// WRONG — blanket reset destroys all data including non-test data
test.beforeEach(async ({ request }) => {
  await request.post('/api/test/reset');  // WRONG: deletes everything
});

// WRONG — no isolation, assumes empty DB, unscoped locators
test('User marks a task as completed', async ({ page }) => {
  await page.goto('/todo-lists');  // WRONG: route may not exist
  await expect(page.locator('.todo-list-card')).toBeVisible();  // WRONG: strict mode if multiple
  const checkbox = page.locator('input[type="checkbox"]:not(:checked)').first();
  await checkbox.click();
  await expect(checkbox).toBeChecked();  // WRONG: stale reference after re-render
});
```

#### Composition Root Requirements for E2E

The app-server composition root must include:
- A **valid UUID** for the stub development user (Zod schemas validate `userId` as UUID). Never use plain strings like `'dev-user'`.
- A `DELETE /api/test/{resource}` route for each domain resource that **requires an `ids` array in the request body** and deletes only those specific documents. Example: `DELETE /api/test/boards` with body `{ ids: ["id1", "id2"] }`. The handler must reject requests with missing or empty `ids`.
- **Never expose a blanket reset endpoint** (`POST /api/test/reset`, `DELETE /api/test/reset`, or any route that calls `deleteMany({})`, `.drop()`, or `dropCollection()`). The scanner will flag these.
- **Error handling** in the Express pipeline so unhandled exceptions return 500 instead of crashing the server.

### Rule: Use Ubiquitous Language

Class names, file names, method names, and test names come from the **domain model** and **Gherkin scenarios** — not from technical patterns. When the story says "Recipient", the class is `Recipient`, the file is `Recipient.ts`, the collection is `Recipients`, and tests say "user views list of active recipients". Technical suffixes like `Manager`, `Handler`, `Processor`, `Helper`, or `Utility` hide domain intent and must be avoided on domain classes. Application services (the orchestration layer) may use the `Service` suffix.

#### DO

- Name domain classes after domain nouns: `Recipient`, `BeneficiaryBank`, `RecipientSelection`.
- Name domain methods after domain verbs: `isEligibleForPayment()`, `filterByStatus()`, `placeOrder()`.
- Name files to match the domain concept: `Recipient.ts`, `RecipientStatus.ts`, `recipient.schema.ts`.
- Name test methods to mirror Gherkin scenarios verbatim: `test_user_views_list_of_active_recipients`.
- Use the `Service` suffix only for application-layer orchestrators: `RecipientsService`.
- Use server-tier naming conventions: `{domain}.routes.ts`, `{domain}.controller.ts`, `{domain}.repository.ts`.

```typescript
// CORRECT: domain class named after the domain concept
export class RecipientSelection {
  getEligibleForPayment(): Recipient[] { ... }
  filterByBankType(type: 'domestic' | 'international'): Recipient[] { ... }
}

// CORRECT: test name mirrors the Gherkin scenario
test('user views list of active recipients when initiating wire payment', async () => {
  await helper.givenEnterpriseHasRecipientsWithActiveStatus();
  await helper.whenUserInitiatesWirePayment();
  await helper.thenOnlyActiveRecipientsDisplayed();
});
```

#### DON'T

- Use `Manager`, `Handler`, `Processor`, `Helper`, `Utility`, `Utils` on domain classes.
- Use generic names that hide domain meaning: `DataProcessor`, `ItemHandler`, `EntityManager`.
- Name test methods with technical jargon instead of scenario language.
- Use abbreviations that obscure domain concepts: `RecSel`, `BenBank`, `pymtCtrl`.

```typescript
// WRONG: technical suffixes hiding domain intent
export class RecipientManager { ... }      // What does "manage" mean in the domain?
export class PaymentProcessor { ... }      // Use the domain verb: Order.placeOrder()
export class BankDataHelper { ... }        // "Helper" is never a domain concept

// WRONG: test name uses technical language, not scenario language
test('GET /api/recipients returns 200 with filtered array', async () => { ... });
// CORRECT equivalent:
test('user views list of active recipients when initiating wire payment', async () => { ... });
```

### Rule: Use Valid Package Names

Package names in `package.json` must be valid npm package names that pass `npm install` without errors. Derive the scope name from the **application's purpose** — not from generic placeholders.

#### Naming Pattern

npm scoped packages allow exactly **one** slash: `@scope/package-name`. For a domain-first monorepo with tier subfolders, flatten the path into the package name using hyphens:

```
@{app-name}/{domain}-{tier}
```

Where:
- `{app-name}` is derived from the application's purpose (e.g., `taskflow`, `payhub`, `channelone`)
- `{domain}` is the domain module name (e.g., `recipients`, `todo-lists`, `payments`)
- `{tier}` is `shared`, `server`, or `client`

#### DO

- Derive the app scope name from the application's business purpose: `@taskflow`, `@payhub`, `@shopfront`.
- Use the pattern `@{app-name}/{domain}-{tier}` for tier packages.
- Ensure every `package.json` name passes `npm install` without `EINVALIDPACKAGENAME`.
- Keep names lowercase, URL-friendly (alphanumeric, hyphens, dots only after scope).
- Use the same scope across all packages in the monorepo for consistent imports.

```json
// packages/todo-lists/shared/package.json — CORRECT
{
  "name": "@taskflow/todo-lists-shared",
  "version": "0.0.0",
  "private": true,
  "main": "index.ts",
  "types": "index.ts"
}

// packages/todo-lists/server/package.json — CORRECT
{
  "name": "@taskflow/todo-lists-server",
  "dependencies": {
    "@taskflow/todo-lists-shared": "*"
  }
}
```

```typescript
// Import using the valid package name
import { TodoList } from '@taskflow/todo-lists-shared';
```

#### Import Path Consistency

**All `import ... from` statements in TypeScript source files must use the package name** — the exact string from the target package's `package.json` `"name"` field. Never use filesystem-style paths or placeholder scope names in import paths.

**This applies equally to production code AND test files.** Test helpers and test specs import from the same package names as production code.

```typescript
// CORRECT — matches "name": "@taskflow/todo-lists-shared" in package.json
import { TodoList } from '@taskflow/todo-lists-shared';
import { CreateTodoListSchema } from '@taskflow/todo-lists-shared';

// CORRECT — test file importing from server/client packages
import { TodoListsService } from '@taskflow/todo-lists-server';
import { TodoListList } from '@taskflow/todo-lists-client';
import * as api from '@taskflow/todo-lists-client/todoLists.api';

// WRONG — filesystem-style path with multiple slashes
import { TodoList } from '@project/todo-lists/shared';
import { TodoListsService } from '@project/todo-lists/server';

// WRONG — placeholder scope name
import { TodoList } from '@acme/todo-lists-shared';
```

**When generating server/ or client/ source files**, look at the `shared/package.json` `"name"` field to determine the correct import path. Do not construct import paths from the folder structure — derive them from the declared package name.

#### DON'T

- Use `@project`, `@acme`, or other **generic placeholder** scope names. Always derive from app purpose.
- Put multiple slashes in a package name: `@project/todo-lists/shared` is **invalid npm**.
- Use `@` scopes with paths that contain more than one `/` — npm only allows `@scope/name`.
- Leave template placeholder names (`@project/domainName/shared`) in generated output.
- Use filesystem-style paths (e.g., `@scope/domain/tier`) as TypeScript import specifiers — use the package name (`@scope/domain-tier`).

```json
// WRONG — multiple slashes, invalid npm package name
{ "name": "@project/todo-lists/shared" }

// WRONG — generic placeholder scope
{ "name": "@acme/todo-lists-shared" }

// WRONG — not URL-friendly
{ "name": "@My App/Todo Lists" }
```

#### How to Derive App Name

1. Identify the application's core purpose (e.g., "task management", "payment processing", "e-commerce").
2. Create a short, memorable, lowercase name: `taskflow`, `payhub`, `shopfront`, `docvault`.
3. Use that as the `@scope` across all packages in the monorepo.

If the user has not specified an app name, **ask** or infer from the domain being built. Never default to `@project` or `@acme`.
<!-- execute_rules:bundle_rules:end -->
