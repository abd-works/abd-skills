---
name: mern-technical-architecture
catalog_garden_tier: practice
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
7. Create test structure — `tests/{epic}/{sub-epic}/` with helpers and 3 tier test files.
8. Run scanners to verify structural compliance.

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
- All interfaces use TypeScript `implements` keyword for compile-time verification.
- Test methods mirror Gherkin scenario titles using Given/When/Then helpers.

Run scanners as final verification: `domain_structure_scanner.py`, `layer_purity_scanner.py`, `naming_convention_scanner.py`, `test_structure_scanner.py`, `test_isolation_scanner.py`.

---

<!-- execute_rules:bundle_rules:begin -->
<!-- Rule prose is generated from rules/*.md — edit rules, then run:
     python skills/execute_using_rules/scripts/bundle_rules_into_skill_md.py --skill-root skills/mern-technical-architecture
-->
---
scanner: domain_structure_scanner.py
---

### Rule: Organize by Domain Module

Organize code by **business capability** (domain module) first, then by technical layer within each module. This ensures that all code for a single domain lives together — changes rarely ripple to other domains, teams can own entire domains, and each module can become its own microservice later without restructuring.

#### DO

- Structure each domain as `packages/{domain}/{shared|client|server}`.
- Include `index.ts` and `package.json` in each tier folder for clean imports.
- Keep the app shell (`app-server/`, `app-client/`) at the packages level as composition roots.
- Ensure `app-server/` and `app-client/` exist. If missing, scaffold them; if already present, update them to compose the new domain module.
- Ensure the client tier provides UI for every user action defined in the specs. If the requirements say a user can create a board, add tasks, or move items — the client must have corresponding forms, buttons, or controls. Derive required UI from the spec, not from a mechanical endpoint mirror.
- Wire navigation in `app-client/App.tsx` to support all spec-driven user flows (e.g., create → view → interact). The composition root must manage view state when multiple views are needed.
- Place test files under `tests/{epic}/{sub-epic}/` mirroring the domain structure.

```
project-root/
├── packages/
│   ├── recipients/              # Domain module
│   │   ├── shared/
│   │   ├── client/
│   │   └── server/
│   ├── app-server/
│   └── app-client/
├── tests/
└── package.json
```

#### DON'T

- Organize by technical layer at the top level (`controllers/`, `models/`, `views/`, `routes/`).
- Scatter a single domain's code across multiple unrelated folders.
- Mix multiple domain concerns in a single folder.
- Generate missing composition roots in a brand-new project later as follow-up work, or create duplicate composition roots in an existing project instead of reusing the current shells.
- Ship a client tier that omits user actions defined in the specs. If the requirements say users can create, edit, or move things, the UI must expose those capabilities — not just read-only search/list.
- Render a single static component in App.tsx when the specs define multiple user flows. If users need to create entities and interact with detail views, the composition root must manage view state to support those flows.

---
scanner: layer_purity_scanner.py
---

### Rule: Maintain Layer Purity

Dependencies point inward toward the domain core. The `shared/` package contains **plain TypeScript only** — no framework imports. The `server/` package never imports from `client/`, and vice versa.

#### DO

- Keep `shared/` free of Express, React, MongoDB, Mongoose, and any infrastructure framework.
- Import domain logic from `shared/` into both `client/` and `server/`.

```typescript
// packages/recipients/shared/RecipientStatus.ts — plain TypeScript only
export class RecipientStatus {
  isEligibleForPayment(): boolean {
    return this.status === 'Active';
  }
}
```

#### DON'T

- Import Express, React, MongoDB, or any framework/infrastructure library in `shared/`.
- Import `client/` code from `server/` or `server/` code from `client/`.

---
scanner: domain_structure_scanner.py
---

### Rule: Share Domain Logic

Define domain entities, value objects, Zod validation schemas, and business rule methods **once** in the `shared/` package. Both `client/` and `server/` import from `shared/` — never duplicate validation, type definitions, or business logic across tiers.

#### DO

- Place all Zod schemas in `shared/` so both tiers validate identically.
- Define domain entity classes with business methods in `shared/`.
- Export collection/aggregate classes from `shared/` for reuse in both tiers.

#### DON'T

- Duplicate Zod schemas or validation logic between `client/` and `server/`.
- Redefine TypeScript interfaces that already exist in `shared/`.
- Create separate "client types" and "server types" for the same domain concept.

---
scanner: naming_convention_scanner.py
---

### Rule: Use Ubiquitous Language

Class names, file names, method names, and test names come from the **domain model** and **Gherkin scenarios**. Technical suffixes like `Manager`, `Handler`, `Processor`, `Helper`, or `Utility` hide domain intent and must be avoided on domain classes.

#### DO

- Name domain classes after domain nouns: `Recipient`, `BeneficiaryBank`, `RecipientSelection`.
- Name domain methods after domain verbs: `isEligibleForPayment()`, `filterByStatus()`.
- Name test methods to mirror Gherkin scenarios verbatim.
- Use server-tier naming: `{domain}.routes.ts`, `{domain}.controller.ts`, `{domain}.repository.ts`.

#### DON'T

- Use `Manager`, `Handler`, `Processor`, `Helper`, `Utility`, `Utils` on domain classes.
- Name test methods with technical jargon instead of scenario language.

---
scanner: domain_structure_scanner.py
---

### Rule: Implement Domain Entities Correctly

Business rules belong **on domain classes**, not in services. Domain entities own their state and behavior. Zod schemas validate at the **repository boundary** and at the **API boundary**. Collection classes provide domain-oriented query methods.

#### DO

- Place business logic as methods on the entity or value object that owns the data.
- Create collection classes that wrap arrays with domain-oriented filter/search methods.
- Validate with `Schema.parse()` at the repository boundary.
- Keep domain classes portable: no framework imports, no side effects, no async.

#### DON'T

- Place business rules in services while leaving entities as plain data objects (Anemic Domain Model).
- Put async operations or framework calls inside domain entities.

---
scanner: test_structure_scanner.py
---

### Rule: Test Story-Driven

Tests mirror story scenarios across three tiers: Server-Side, Client-Side, and E2E. The test folder hierarchy maps to the story graph: Epic → Folder, Sub-Epic → Folder, Lowest Sub-Epic → 3 test files.

#### DO

- Create exactly 3 test files per lowest sub-epic: `*_server.test.ts`, `*_client.test.tsx`, `*_e2e.spec.ts`.
- Create a `helpers/` folder per sub-epic with base, server, client, and e2e helpers.
- Name test methods to mirror Gherkin scenario titles verbatim.
- Use Given/When/Then helper methods that read like scenario steps.

#### DON'T

- Skip any of the three test tiers for a sub-epic.
- Write tests without Given/When/Then helper methods.
- Place test files outside the epic/sub-epic folder structure.

---
scanner: test_structure_scanner.py
---

### Rule: Run E2E Tests

End-to-end tests are **mandatory** for every sub-epic. E2E tests must reuse the base helper class, verify **logic** (not just element presence), and be executed as a final verification step.

#### DO

- Create `*_e2e.spec.ts` for every lowest sub-epic.
- Assert on domain logic outcomes: filtered lists, eligibility, domain rules.
- Ensure the required composition roots exist and expose the new module before running Playwright. Scaffold missing roots; otherwise update the existing roots.
- Run E2E tests after implementation as final verification.

#### DON'T

- Skip E2E tests for any sub-epic.
- Write E2E tests that only check element presence without verifying logic.
- Write E2E tests from scratch without reusing the helper class.
- Tell the user `npx playwright test` is runnable before the required composition roots exist and expose the new module — E2E tests require a live server and will fail with `ERR_CONNECTION_REFUSED`.
- Generate duplicate composition roots for an existing project when compatible `app-server/` and `app-client/` shells already exist.

---
scanner: test_isolation_scanner.py
---

### Rule: Test Data Isolation — NEVER Reset All Data

Tests must **ONLY** delete the specific data they created. Never delete all data, never reset the database, never use blanket `deleteMany({})`. The `test_isolation_scanner.py` enforces this automatically.

#### Forbidden patterns (scanner flags these as violations):
- `deleteMany({})` — empty filter deletes ALL documents in the collection
- `.drop()` / `dropCollection()` / `dropDatabase()` — destroys entire collections or databases
- `POST /api/test/reset` or any `/reset` endpoint — blanket wipe of all data
- Any `beforeEach`/`afterAll` hook that calls the above

#### DO

- Track every resource ID created during a test (from API responses or GET queries).
- Delete **only those specific IDs** in `afterEach` via `DELETE /api/test/{resource}` with `{ ids: [...] }` body.
- Require the server cleanup endpoint to accept an `ids` array and reject requests without one.
- Make cleanup a no-op if no IDs were created (empty array = skip delete call).
- Use unique names per test run (e.g., append `Date.now()`) to avoid collisions with other data.

```typescript
// CORRECT — helper tracks created IDs, afterEach deletes only those
class BoardE2EHelper {
  private createdBoardIds: string[] = [];

  async whenUserCreatesBoard(name: string) {
    // ... create via UI or API ...
    const res = await this.request.get('/api/boards');
    const boards = await res.json();
    const created = boards.items.find((b: any) => b.name === name);
    if (created) this.createdBoardIds.push(created.id);
  }

  async cleanup() {
    if (this.createdBoardIds.length === 0) return;
    await this.request.delete('/api/test/boards', {
      data: { ids: this.createdBoardIds },
    });
    this.createdBoardIds = [];
  }
}
```

#### DON'T

- Use `deleteMany({})` with an empty filter — this deletes ALL documents in the collection, not just test data.
- Create a `/test/reset` endpoint that wipes entire collections.
- Assume the database is empty or that only test data exists — other developers, QA sessions, or parallel test runs share the same datastore.
- Use `.drop()` or `dropCollection()` to "clean up" — this destroys indexes and the collection itself.
- Rely on `beforeAll` to reset state — tests must be independent and clean up after themselves.

---
scanner: layer_purity_scanner.py
---

### Rule: Implement Full Interfaces

Every layer that claims to implement a domain interface must implement **all members**. Test adapters must correctly implement domain interfaces. Verify completeness at compile time using TypeScript `implements`.

#### DO

- Implement every method and property defined in the domain interface.
- Use TypeScript `implements` keyword so the compiler catches missing members.
- Ensure test adapters (mocks, fakes) implement the full interface.

#### DON'T

- Leave interface methods unimplemented or stubbed with `throw new Error('not implemented')`.
- Skip `implements` keyword.
- Create test adapters that only implement methods used in one test.

---
scanner: domain_structure_scanner.py
---

### Rule: Use Valid Package Names

Package names in `package.json` must be valid npm package names that pass `npm install` without errors. Derive the scope name from the **application's purpose** — not from generic placeholders.

**Naming pattern:** `@{appName}/{domainName}-{tier}`

Where:
- `{appName}` is derived from the application's purpose (e.g., `taskflow`, `payhub`, `channelone`)
- `{domainName}` is the domain module name (e.g., `recipients`, `todo-lists`, `payments`)
- `{tier}` is `shared`, `server`, or `client`

#### DO

- Derive the app scope name from the application's business purpose: `@taskflow`, `@payhub`, `@shopfront`.
- Use the pattern `@{appName}/{domainName}-{tier}` for tier packages.
- Ensure every `package.json` name passes `npm install` without `EINVALIDPACKAGENAME`.
- Keep names lowercase, URL-friendly (alphanumeric, hyphens only after scope).
- Use the same package name as the `import ... from` specifier in all TypeScript source files — **including test files and test helpers**.

```json
{
  "name": "@taskflow/todo-lists-shared",
  "dependencies": {}
}
```

```typescript
// Import path MUST match the package.json "name" field — in production AND test code
import { TodoList } from '@taskflow/todo-lists-shared';
import { TodoListsService } from '@taskflow/todo-lists-server';
import { TodoListList } from '@taskflow/todo-lists-client';
```

#### DON'T

- Use `@project`, `@acme`, or other generic placeholder scope names.
- Put multiple slashes in a package name: `@project/todo-lists/shared` is invalid npm.
- Leave template placeholder names in generated output.
- Use filesystem-style paths (e.g., `@scope/domain/tier`) as TypeScript import specifiers — use the package name (`@scope/domain-tier`).

---
scanner: layer_purity_scanner.py
---

### Rule: Ensure Type-Safe Controllers

Controllers in the `server/` tier must compile without implicit `any` types or missing property errors. When controllers access extended Express `Request` properties (e.g., `req.user`), include a type augmentation.

#### DO

- Include `declare global { namespace Express { interface Request { user?: { id: string }; } } }` when accessing `req.user`.
- Type all lambda/callback parameters explicitly when `noImplicitAny` or `strict` is enabled.
- Use domain types from `shared/` for callback parameters rather than `any`.

```typescript
import { Request, Response } from 'express';

declare global {
  namespace Express {
    interface Request {
      user?: { id: string };
    }
  }
}
```

#### DON'T

- Access `req.user` or extended properties without a type declaration (causes TS2339).
- Leave callback parameters untyped under `strict` mode (causes TS7006).
- Use `(req as any).user` to bypass type checking — augment the type instead.
- Suppress errors with `// @ts-ignore` instead of providing proper types.

---
scanner: domain_structure_scanner.py
---

### Rule: Include All External Dependencies

Every `package.json` must declare all external packages that its source files import. After `npm install`, the project must compile with zero unresolved module errors.

**Required dependencies by tier:**

| Tier | dependencies | devDependencies |
|------|-------------|-----------------|
| shared/ | `zod` | — |
| server/ | `express`, `mongodb`, workspace shared | `@types/express` |
| client/ | `react`, `react-dom`, workspace shared | `@types/react`, `@types/react-dom` |
| root | — | `typescript`, `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `@playwright/test` |

**Test dependencies:** When generating test files, the root `package.json` must include `vitest`, `jsdom`, `@testing-library/react`, `@testing-library/jest-dom`, and `@playwright/test`. The `tsconfig.json` must include `"types": ["vitest/globals", "@testing-library/jest-dom"]` and include `tests/**/*.ts` + `tests/**/*.tsx` in `include`.

**Use `vitest` imports in all unit/component tests — never `node:test`.** All `*_server.test.ts` and `*_client.test.tsx` files must import `describe`, `it`, `expect`, `beforeEach`, and `vi` from `'vitest'`. Mixing `node:test` with Vitest causes "No test suite found" failures.

**Test runner config files are required.** Create `vitest.config.ts` (include `*_server.test.ts` + `*_client.test.tsx`, environment `jsdom`) and `playwright.config.ts` (testMatch `*_e2e.spec.ts`) to prevent runners from picking up each other's files. Without these, Playwright errors with ESM/CJS import failures on `vitest` module.

**Test path aliases:** The `tsconfig.json` must have path aliases for **all** tier packages (shared, server, client) plus wildcard paths for sub-module imports:
```json
{
  "paths": {
    "@appName/domain-shared": ["./packages/domain/shared/index.ts"],
    "@appName/domain-server": ["./packages/domain/server/index.ts"],
    "@appName/domain-client": ["./packages/domain/client/index.ts"],
    "@appName/domain-client/*": ["./packages/domain/client/*"]
  }
}
```

#### DO

- List every imported external module in `dependencies` or `devDependencies`.
- Include `@types/*` packages for libraries without bundled declarations.
- Use caret ranges (`^`) for external packages: `"zod": "^3.22.0"`.
- Include `typescript` in root `devDependencies`.
- Run `npm install` + `npx tsc --noEmit` after generation to verify compilation.

#### DON'T

- Omit external packages and rely on hoisting or implicit resolution.
- Generate source files that import modules not listed in any `package.json`.
- Skip `@types/*` packages — TypeScript will fail with `Could not find a declaration file`.
- Use `*` or `latest` for external packages (only for workspace internal references).
- Consider the implementation complete if `npm install` or `tsc` fails.

<!-- execute_rules:bundle_rules:end -->
