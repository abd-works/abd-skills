# Corrections log

Project: mern-technical-architecture skill
Source: mern-technical-architecture skill — E2E test scaffolding and test runner scripts

---

## Entry: E2E spec files existing ≠ E2E tests passing

- **Status:** confirmed
- **Context:** mern-technical-architecture skill — Build steps, use-thorough-e2e-tests rule, scaffold-test-scripts rule
- **DO / DO NOT:** DO verify that `packages/app-client/` exists and is wired into `playwright.config.ts` `webServer` before claiming E2E tests are runnable or passing. DO distinguish between "spec files compile and list" and "E2E tests pass against a real browser."
- **Example (wrong):**
  Skill generated `*_e2e.spec.ts` files, reported `npx playwright test --list` succeeding and `npx vitest run` passing 62 tests, and implied all tests including E2E were complete. `vitest run` excludes `*_e2e.spec.ts` by design. `--list` only compiles — it does not run. Without `packages/app-client/` serving page routes, every Playwright test fails with `Cannot GET /<route>`.
- **Example (correct):**
  After generating `*_e2e.spec.ts` files, state explicitly: "E2E tests require `packages/app-client/` to serve page routes. Until that exists, spec files compile and list but will fail when run. Server + client unit/component tests (62) pass via `npm test`."
- **Likely source:** unclear expectation

---

## Entry: In-memory repositories used instead of MongoDB

- **Status:** confirmed
- **Context:** mern-technical-architecture skill — repository layer, infrastructure tier
- **DO / DO NOT:** DO implement repositories using MongoDB. DO NOT use in-memory Maps as the repository implementation. The MERN architecture is explicit: infrastructure layer = MongoDB. In-memory Maps lose all data on every server restart, making the running app permanently broken for any user who doesn't run test seeding commands manually.
- **Example (wrong):**
  Generated `InMemoryStoreRepository` and `ProductCatalogRepository` using `Map<string, T>`. App appeared to work during E2E tests (which seed and clean up their own data) but every time the dev server restarted all data was lost. Browsing `/store-locator` showed a blank screen. User had to manually POST seed data via curl after every restart.
- **Example (correct):**
  Implement `MongoStoreRepository extends InMemoryStoreRepository` and `MongoProductCatalogRepository extends ProductCatalogRepository` using write-through cache pattern: constructor connects to MongoDB collection, `loadFromMongo()` loads persisted data into memory on startup, all write methods call `super` then persist to MongoDB via `replaceOne`/`deleteOne`/`deleteMany`. `dev.ts` calls `connectDb()`, `loadFromMongo()`, and `seedDevData()` (idempotent upserts) on startup. Data survives restarts.
- **Likely source:** instruction not read — architecture reference says infrastructure = MongoDB, skill generated in-memory instead

- **Status:** confirmed
- **Context:** scaffold-test-scripts rule — generated `scripts/test.sh` and `scripts/test-e2e.sh`
- **DO / DO NOT:** DO add a `# Does NOT run E2E tests` comment to `test.sh`/`test.ps1` and a `# REQUIRES: packages/app-client` comment to `test-e2e.sh`/`test-e2e.ps1`.
- **Example (wrong):**
  `scripts/test.sh` ran `npx vitest run` with no comment. Developer running it would see "62 tests passing" and believe the full test suite including E2E was green.
- **Example (correct):**
  `scripts/test.sh` includes `# Runs server and client unit/component tests ONLY (Vitest). Does NOT run E2E tests.`
  `scripts/test-e2e.sh` includes `# REQUIRES: packages/app-client must exist and serve the React frontend.`
- **Likely source:** automation gap
