# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: configure_planning_folder\connect_to_planning_folder_and_load_board_data_e2e.spec.ts >> Connect Board to a Planning Folder >> Scenario 1: Successful connection loads the board
- Location: tests\e2e\configure_planning_folder\connect_to_planning_folder_and_load_board_data_e2e.spec.ts:9:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('[data-ticket="fixture-ticket"]')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('[data-ticket="fixture-ticket"]')

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
  2  | import { BOARD_JSON_PATH, goToBoard, readJsonFile, resetPawPlaceStubsFixture, updateJsonFile } from '../e2e_support';
  3  | 
  4  | test.describe('Connect Board to a Planning Folder', () => {
  5  |   test.beforeEach(() => {
  6  |     resetPawPlaceStubsFixture();
  7  |   });
  8  | 
  9  |   test('Scenario 1: Successful connection loads the board', async ({ page }) => {
  10 |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  11 |       const next = { ...board };
  12 |       next.active = [
  13 |         {
  14 |           ticket_id: 'fixture-ticket',
  15 |           lineage: ['Fixture', 'Read Board JSON'],
  16 |           scope_level: 'increment',
  17 |           stage: 'discovery',
  18 |           priority: 1,
  19 |           entered_stage: '2026-06-01T12:00:00Z',
  20 |           completed_stage: null,
  21 |           stage_history: [],
  22 |           scatter_from: null,
  23 |           scatter_to: [],
  24 |           notes: '',
  25 |           skill_progress: {},
  26 |           hold_in_progress: true,
  27 |         },
  28 |       ];
  29 |       next.backlog = [];
  30 |       return next;
  31 |     });
  32 |     await goToBoard(page);
> 33 |     await expect(page.locator('[data-ticket="fixture-ticket"]')).toBeVisible();
     |                                                                  ^ Error: expect(locator).toBeVisible() failed
  34 |     const board = await readJsonFile<{ active: Array<{ ticket_id: string }> }>(BOARD_JSON_PATH);
  35 |     expect(board.active.some((ticket) => ticket.ticket_id === 'fixture-ticket')).toBe(true);
  36 |   });
  37 | 
  38 |   test('Scenario 2: Invalid folder shows error', async ({ page, request }) => {
  39 |     await goToBoard(page);
  40 |     const response = await request.get('http://127.0.0.1:3001/api/board?planningRoot=C:/tmp/missing-root');
  41 |     const payload = (await response.json()) as { active?: unknown[]; backlog?: unknown[]; error?: string };
  42 |     if (response.ok()) {
  43 |       expect(Array.isArray(payload.active)).toBe(true);
  44 |       expect(Array.isArray(payload.backlog)).toBe(true);
  45 |     } else {
  46 |       expect(typeof payload.error).toBe('string');
  47 |     }
  48 |   });
  49 | 
  50 |   test.skip('Scenario 3: Missing board file shows initialization message', async () => {
  51 |     // TODO: implement — Scenario 3: Missing board file shows initialization message
  52 |   });
  53 | });
  54 | 
```