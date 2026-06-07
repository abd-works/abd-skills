# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: manage_agent_pool\adjust_wip_policy\scale_agent_pool_up_or_down_e2e.spec.ts >> Scale Agent Pool Up or Down >> Scenario 1: Delivery Lead adds an executor
- Location: tests\e2e\manage_agent_pool\adjust_wip_policy\scale_agent_pool_up_or_down_e2e.spec.ts:16:7

# Error details

```
Test timeout of 60000ms exceeded.
```

```
Error: locator.click: Test timeout of 60000ms exceeded.
Call log:
  - waiting for locator('.kb-pool-group[data-role="engineer"]').locator('button[title="Add Engineer"]')

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - generic [ref=e5]:
      - generic [ref=e6]: Agentic Agile Delivery
      - heading "Kanban Board — …" [level=1] [ref=e7]
    - generic [ref=e8]:
      - group "Display mode" [ref=e9]:
        - button "Executive" [ref=e10] [cursor=pointer]
        - button "Engineering" [ref=e11] [cursor=pointer]
      - link "home" [ref=e13] [cursor=pointer]:
        - /url: /
  - generic [ref=e14]:
    - generic [ref=e15]:
      - text: Planning folder
      - textbox "Planning folder" [ref=e16]:
        - /placeholder: C:/dev/.../docs/planning
        - text: C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning
    - button "Connect" [ref=e17] [cursor=pointer]
    - button "Use stubs" [ref=e18] [cursor=pointer]
    - button "Refresh" [ref=e19] [cursor=pointer]
    - generic [ref=e20]: Polled
  - generic [ref=e21]: "Unexpected token ' ', \" { \"sch\"... is not valid JSON"
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import {
  3  |   BOARD_JSON_PATH,
  4  |   goToBoard,
  5  |   readJsonFile,
  6  |   resetPawPlaceStubsFixture,
  7  |   updateJsonFile,
  8  |   waitForUiRefresh,
  9  | } from '../../e2e_support';
  10 | 
  11 | test.describe('Scale Agent Pool Up or Down', () => {
  12 |   test.beforeEach(() => {
  13 |     resetPawPlaceStubsFixture();
  14 |   });
  15 | 
  16 |   test('Scenario 1: Delivery Lead adds an executor', async ({ page }) => {
  17 |     await goToBoard(page);
  18 |     const roleGroup = page.locator('.kb-pool-group[data-role="engineer"]');
  19 |     const plus = roleGroup.locator('button[title="Add Engineer"]');
  20 |     const before = await readJsonFile<{ team: Record<string, number> }>(BOARD_JSON_PATH);
  21 |     const beforeCount = before.team.engineer ?? 0;
  22 | 
> 23 |     await plus.click();
     |                ^ Error: locator.click: Test timeout of 60000ms exceeded.
  24 |     await waitForUiRefresh(page);
  25 | 
  26 |     const after = await readJsonFile<{ team: Record<string, number> }>(BOARD_JSON_PATH);
  27 |     expect(after.team.engineer).toBe(beforeCount + 1);
  28 |     const avatars = roleGroup.locator('.kb-agent-avatar');
  29 |     await expect(avatars).toHaveCount(beforeCount + 1);
  30 |   });
  31 | 
  32 |   test('Scenario 2: Delivery Lead removes an executor', async ({ page }) => {
  33 |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  34 |       const next = { ...board };
  35 |       next.team = { ...(next.team as Record<string, number>), 'business-expert': 2 };
  36 |       return next;
  37 |     });
  38 |     await goToBoard(page);
  39 |     const roleGroup = page.locator('.kb-pool-group[data-role="business-expert"]');
  40 |     const minus = roleGroup.locator('button[title^="Remove Business Expert"]').first();
  41 | 
  42 |     await minus.click();
  43 |     await waitForUiRefresh(page);
  44 | 
  45 |     const after = await readJsonFile<{ team: Record<string, number> }>(BOARD_JSON_PATH);
  46 |     expect(after.team['business-expert']).toBe(1);
  47 |   });
  48 | 
  49 |   test.skip('Scenario 3: Cannot reduce below zero', async () => {
  50 |     // TODO: implement — Scenario 3: Cannot reduce below zero
  51 |   });
  52 | });
  53 | 
```