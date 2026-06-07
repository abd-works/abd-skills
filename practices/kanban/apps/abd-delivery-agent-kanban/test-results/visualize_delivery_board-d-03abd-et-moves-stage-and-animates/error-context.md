# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visualize_delivery_board\display_ticket_cards\animate_ticket_on_position_change_e2e.spec.ts >> Animate Ticket on Position Change >> Scenario 1: Ticket moves stage and animates
- Location: tests\e2e\visualize_delivery_board\display_ticket_cards\animate_ticket_on_position_change_e2e.spec.ts:18:7

# Error details

```
Test timeout of 60000ms exceeded.
```

```
Error: locator.dragTo: Test timeout of 60000ms exceeded.
Call log:
  - waiting for locator('[data-ticket="project-all"]').first()

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
  - generic [ref=e21]: Failed to fetch
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import {
  3  |   BOARD_JSON_PATH,
  4  |   goToBoard,
  5  |   resetPawPlaceStubsFixture,
  6  |   stageDoneColumn,
  7  |   ticketCard,
  8  |   updateJsonFile,
  9  |   expectTicketInStageInProgress,
  10 |   waitForUiRefresh,
  11 | } from '../../e2e_support';
  12 | 
  13 | test.describe('Animate Ticket on Position Change', () => {
  14 |   test.beforeEach(() => {
  15 |     resetPawPlaceStubsFixture();
  16 |   });
  17 | 
  18 |   test('Scenario 1: Ticket moves stage and animates', async ({ page }) => {
  19 |     await goToBoard(page);
  20 |     const source = ticketCard(page, 'project-all');
  21 |     const doneZone = stageDoneColumn(page, 'shaping');
> 22 |     await source.dragTo(doneZone);
     |                  ^ Error: locator.dragTo: Test timeout of 60000ms exceeded.
  23 |     await waitForUiRefresh(page);
  24 |     await page.getByRole('button', { name: 'Refresh' }).click();
  25 |     await expect(source).toBeVisible();
  26 |   });
  27 | 
  28 |   test('Scenario 2: New ticket does not animate', async ({ page }) => {
  29 |     await goToBoard(page);
  30 |     await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
  31 |       const next = { ...board };
  32 |       next.active = [
  33 |         ...(next.active as any[]),
  34 |         {
  35 |           ticket_id: '301',
  36 |           lineage: ['PawPlace', 'Brand New Ticket'],
  37 |           scope_level: 'increment',
  38 |           stage: 'discovery',
  39 |           priority: 2,
  40 |           entered_stage: '2026-06-01T12:10:00Z',
  41 |           completed_stage: null,
  42 |           stage_history: [],
  43 |           scatter_from: null,
  44 |           scatter_to: [],
  45 |           notes: '',
  46 |           skill_progress: {},
  47 |           hold_in_progress: true,
  48 |         },
  49 |       ];
  50 |       return next;
  51 |     });
  52 | 
  53 |     await page.getByRole('button', { name: 'Refresh' }).click();
  54 |     const newTicket = ticketCard(page, '301');
  55 |     await expectTicketInStageInProgress(page, '301', 'discovery');
  56 |     await expect(newTicket).not.toHaveClass(/kb-ticket--flip/);
  57 |   });
  58 | });
  59 | 
```