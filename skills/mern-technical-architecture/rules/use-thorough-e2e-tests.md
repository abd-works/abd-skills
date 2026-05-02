---
scanner: test_structure_scanner.py
---

# Rule: Use Thorough E2E Tests

End-to-end tests are **mandatory** for every sub-epic. E2E tests must reuse the base helper class (not be manually written from scratch), verify **logic** (filtering, eligibility, domain rules) not just element presence, and be executed as a final verification step after implementation. E2E tests exercise the same Gherkin scenarios as server and client tests, but through the complete user workflow: browser → React → HTTP → Express → MongoDB → response → rendered UI.

## E2E Tests Require a Running Application

**E2E tests cannot run without a live server.** Generating `*_e2e.spec.ts` files is not sufficient — the project also needs runnable composition roots:

- `packages/app-server/` — Express entry point that mounts domain routes
- `packages/app-client/` — React/Vite shell that renders domain components

Do **not** tell the user they can run `npx playwright test` until both composition roots exist and a dev server is running. Running Playwright against a missing server produces `ERR_CONNECTION_REFUSED` errors on every test — this is a broken state, not a partial one.

**The complete generation order is:**
1. Domain packages (`shared/`, `server/`, `client/`) ← what the domain module template produces
2. Composition roots (`app-server/`, `app-client/`) ← required before E2E tests work
3. `playwright.config.ts` with a `webServer` block so Playwright starts the app automatically

## DO

- Create `*_e2e.spec.ts` for every lowest sub-epic.
- Extend the base helper class for E2E-specific setup (Playwright page, browser context).
- Assert on **domain logic outcomes**: filtered lists exclude ineligible items, tooltips show remaining time, selected recipients persist across navigation.
- Run E2E tests after implementation as final verification.
- Test the same scenarios as server/client tiers, with complete workflow emphasis.
- Include edge cases and domain variants, not just the happy path.
- Scaffold both `app-server/` and `app-client/` composition roots and start the dev server before attempting to run E2E tests.
- Navigate to `/` (or the correct root route) — only navigate to a sub-route if a router exists that handles it.
- Scope all locators to the specific card/section under test: `page.locator('.card', { hasText: 'Name' })` to prevent strict mode violations when multiple matching elements exist.
- Assert on locator text content after state changes, not on the original element reference — React re-renders replace DOM nodes.
- Seed all required test data within each test via API calls or UI interactions — never rely on pre-existing data in the database.
- Implement both the UI affordance and the test that exercises it together — neither should be left incomplete.
- Use unique names per test run (e.g. append `Date.now()`) to prevent collisions with leftover data from previous runs.

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

## DON'T

- Skip E2E tests for any sub-epic.
- Write E2E tests that only check element presence without verifying logic.
- Write E2E tests from scratch without reusing the helper class.
- Forget to run E2E tests after implementation.
- Test only the happy path — include edge cases and domain variants.
- Tell the user they can run `npx playwright test` before `app-server/` and `app-client/` are scaffolded — E2E tests require a live server.
- Navigate to non-existent routes — if the app has no router, navigate to `/`, not `/todo-lists`.
- Use unscoped locators when multiple elements may match — always scope assertions to a specific card/section using `page.locator('.card', { hasText: 'Specific Name' })`.
- Assert on stale element references after state changes — React re-renders replace DOM nodes; assert on the new state via locator text content instead.
- Assume pre-seeded data exists — E2E tests must create their own data via API calls or the UI.
- Leave placeholder or skeleton tests for UI that doesn't exist yet — every E2E scenario must be fully implemented end-to-end: the UI affordance and the test that exercises it must both be complete before moving on. Write them in any order (test-first or component-first), but never leave one without the other.
- Use hardcoded names that may collide with leftover data — use unique names (e.g. append `Date.now()`) so tests are isolated from stale data in the persistent datastore.

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

## Test Isolation

E2E tests **must** be independent — each test must pass regardless of run order or previous runs. When using a persistent datastore (MongoDB), accumulated data from prior test runs causes strict mode violations and false assertions.

**Required pattern — tests clean up their own data:**
1. Expose a `DELETE /api/{resource}/:id` endpoint on the server for each resource.
2. Each test that creates data must capture the created resource's ID from the API response.
3. At the end of each test, delete the specific items that were created — never blanket-delete all data.
4. If data is created via the UI (not API), query the GET endpoint to find the created item's ID, then delete it.

**Do NOT** use blanket reset endpoints (`POST /api/test/reset`) that wipe all data — this destroys data created by other users, dev sessions, or parallel test runs.

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

## Composition Root Requirements for E2E

The app-server composition root must include:
- A **valid UUID** for the stub development user (Zod schemas validate `userId` as UUID). Never use plain strings like `'dev-user'`.
- A `DELETE /api/{resource}/:id` route for each domain resource so tests can clean up their own data.
- **Error handling** in the Express pipeline so unhandled exceptions return 500 instead of crashing the server.
