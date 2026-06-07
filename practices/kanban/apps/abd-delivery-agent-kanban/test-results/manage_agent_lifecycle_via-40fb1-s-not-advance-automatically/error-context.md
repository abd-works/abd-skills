# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: manage_agent_lifecycle_via_cursor_sdk\orchestrate_delivery_cycle\manual_drag_in_stage_flow_logic_e2e.spec.ts >> Advance Ticket to Next Stage (Same Scope) >> Scenario 2: Ticket does not advance automatically
- Location: tests\e2e\manage_agent_lifecycle_via_cursor_sdk\orchestrate_delivery_cycle\manual_drag_in_stage_flow_logic_e2e.spec.ts:28:7

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: true
Received: false
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import { BOARD_JSON_PATH, readJsonFile, resetPawPlaceStubsFixture } from '../../e2e_support';
  3  | 
  4  | const planningRoot =
  5  |   'C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning';
  6  | 
  7  | test.describe('Advance Ticket to Next Stage (Same Scope)', () => {
  8  |   test.beforeEach(() => {
  9  |     resetPawPlaceStubsFixture();
  10 |   });
  11 | 
  12 |   test('Scenario 1: Ticket advances when stage complete and next stage has same scope', async ({ request }) => {
  13 |     const payload = {
  14 |       planningRoot,
  15 |       ticket_id: 'project-all',
  16 |       target_stage: 'discovery',
  17 |       placement: 'in_progress',
  18 |     };
  19 | 
  20 |     const response = await request.post('http://127.0.0.1:3001/api/board/ticket/move-to-stage', { data: payload });
  21 |     expect(response.ok()).toBe(true);
  22 |     const board = await readJsonFile<{ active: Array<{ ticket_id: string; stage: string; skill_progress: Record<string, unknown> }> }>(BOARD_JSON_PATH);
  23 |     const moved = board.active.find((ticket) => ticket.ticket_id === 'project-all');
  24 |     expect(moved?.stage).toBe('discovery');
  25 |     expect(Object.keys(moved?.skill_progress ?? {})).toHaveLength(0);
  26 |   });
  27 | 
  28 |   test('Scenario 2: Ticket does not advance automatically', async ({ request }) => {
  29 |     const moveForward = await request.post('http://127.0.0.1:3001/api/board/ticket/move-to-stage', {
  30 |       data: {
  31 |         planningRoot,
  32 |         ticket_id: 'project-all',
  33 |         target_stage: 'discovery',
  34 |         placement: 'in_progress',
  35 |       },
  36 |     });
> 37 |     expect(moveForward.ok()).toBe(true);
     |                              ^ Error: expect(received).toBe(expected) // Object.is equality
  38 | 
  39 |     const moveBack = await request.post('http://127.0.0.1:3001/api/board/ticket/move-to-stage', {
  40 |       data: {
  41 |         planningRoot,
  42 |         ticket_id: 'project-all',
  43 |         target_stage: 'shaping',
  44 |         placement: 'in_progress',
  45 |       },
  46 |     });
  47 |     expect(moveBack.ok()).toBe(true);
  48 |     const board = await readJsonFile<{ active: Array<{ ticket_id: string; stage: string }> }>(BOARD_JSON_PATH);
  49 |     expect(board.active.find((ticket) => ticket.ticket_id === 'project-all')?.stage).toBe('shaping');
  50 |   });
  51 | 
  52 |   test.skip('Scenario 3: Ticket cannot skip a stage', async () => {
  53 |     // TODO: implement — Scenario 3: Ticket cannot skip a stage
  54 |   });
  55 | });
  56 | 
```