# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: manage_agent_pool\display_agent_pool\show_agent_liveness_in_stage_pool_e2e.spec.ts >> Indicate Agent Liveness from Heartbeat >> Scenario 3: Agent idle — no heartbeat file
- Location: tests\e2e\manage_agent_pool\display_agent_pool\show_agent_liveness_in_stage_pool_e2e.spec.ts:37:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('.kb-pool-group[data-role="ux-designer"] .kb-agent-avatar--idle, .kb-pool-group[data-role="ux-designer"] .kb-agent-avatar--inactive').first()
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('.kb-pool-group[data-role="ux-designer"] .kb-agent-avatar--idle, .kb-pool-group[data-role="ux-designer"] .kb-agent-avatar--inactive').first()

```

```yaml
- banner:
  - text: Agentic Agile Delivery
  - heading "Kanban Board — …" [level=1]
  - group "Display mode":
    - button "Executive"
    - button "Engineering"
  - link "home":
    - /url: /
- text: Planning folder
- textbox "Planning folder":
  - /placeholder: C:/dev/.../docs/planning
  - text: C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning
- button "Connect"
- button "Use stubs"
- button "Refresh"
- text: "Polled Unexpected token ' ', \" { \"sch\"... is not valid JSON"
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
> 47 |     await expect(page.locator('.kb-pool-group[data-role="ux-designer"] .kb-agent-avatar--idle, .kb-pool-group[data-role="ux-designer"] .kb-agent-avatar--inactive').first()).toBeVisible();
     |                                                                                                                                                                              ^ Error: expect(locator).toBeVisible() failed
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
  58 |     await plus.click();
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