# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: manage_agent_pool\display_agent_pool\show_agent_liveness_in_stage_pool_e2e.spec.ts >> Indicate Agent Liveness from Heartbeat >> Scenario 4: Agent working — board engagement without heartbeat
- Location: tests\e2e\manage_agent_pool\display_agent_pool\show_agent_liveness_in_stage_pool_e2e.spec.ts:50:7

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
  11 | test.describe('Indicate Agent Liveness from Heartbeat', () => {
  12 |   test.beforeEach(() => {
  13 |     resetPawPlaceStubsFixture();
  14 |   });
  15 | 
  16 |   test('Scenario 1: Agent alive — heartbeat recent', async ({ page, request }) => {
  17 |     await goToBoard(page);
  18 |     const startResponse = await request.post('http://127.0.0.1:3001/api/board/agent/start', {
  19 |       data: { role: 'business-expert' },
  20 |     });
  21 |     expect(startResponse.ok()).toBe(true);
  22 |     await waitForUiRefresh(page);
  23 |     const status = await request.get('http://127.0.0.1:3001/api/board/agent/business-expert/status');
  24 |     expect(status.ok()).toBe(true);
  25 |     const payload = (await status.json()) as { state: string };
  26 |     expect(['running', 'completed', 'failed']).toContain(payload.state);
  27 |   });
  28 | 
  29 |   test('Scenario 2: Agent inactive — heartbeat stale with no board engagement', async ({ page }) => {
  30 |     await goToBoard(page);
  31 |     const avatar = page.locator('.kb-pool-group[data-role="business-expert"] [title]').first();
  32 |     await expect(avatar).toBeVisible();
  33 |     await avatar.hover();
  34 |     await expect(avatar).toHaveAttribute('title', /Business Expert/i);
  35 |   });
  36 | 
  37 |   test('Scenario 3: Agent idle — no heartbeat file', async ({ page }) => {
  38 |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  39 |       const next = { ...board };
  40 |       next.team = {
  41 |         ...(next.team as Record<string, number>),
  42 |         'ux-designer': 1,
  43 |       };
  44 |       return next;
  45 |     });
  46 |     await goToBoard(page);
  47 |     await expect(page.locator('.kb-pool-group[data-role="ux-designer"] .kb-agent-avatar--idle, .kb-pool-group[data-role="ux-designer"] .kb-agent-avatar--inactive').first()).toBeVisible();
  48 |   });
  49 | 
  50 |   test('Scenario 4: Agent working — board engagement without heartbeat', async ({ page }) => {
  51 |     await goToBoard(page);
  52 |     const roleGroup = page.locator('.kb-pool-group[data-role="engineer"]');
  53 |     const plus = roleGroup.locator('button[title="Add Engineer"]');
  54 |     const minus = roleGroup.locator('button[title="Remove Engineer"], button[title="Remove Engineer #1"], button[title="Remove Engineer #2"]');
  55 |     const beforeBoard = await readJsonFile<{ team: Record<string, number> }>(BOARD_JSON_PATH);
  56 |     const beforeCount = beforeBoard.team.engineer ?? 0;
  57 | 
> 58 |     await plus.click();
     |                ^ Error: locator.click: Test timeout of 60000ms exceeded.
  59 |     await waitForUiRefresh(page);
  60 |     const afterAddBoard = await readJsonFile<{ team: Record<string, number> }>(BOARD_JSON_PATH);
  61 |     expect(afterAddBoard.team.engineer).toBe(beforeCount + 1);
  62 | 
  63 |     const canRemove = await minus.first().isVisible().catch(() => false);
  64 |     if (canRemove) {
  65 |       await minus.first().click();
  66 |       await waitForUiRefresh(page);
  67 |       const afterRemoveBoard = await readJsonFile<{ team: Record<string, number> }>(BOARD_JSON_PATH);
  68 |       expect(afterRemoveBoard.team.engineer).toBe(beforeCount);
  69 |     }
  70 |   });
  71 | 
  72 |   test.skip('Scenario 5: Agent working — stale heartbeat but board engagement', async () => {
  73 |     // TODO: implement — Scenario 5: Agent working — stale heartbeat but board engagement
  74 |   });
  75 | });
  76 | 
```