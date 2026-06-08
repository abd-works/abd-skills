import { test, expect } from '@playwright/test';
import { BOARD_JSON_PATH, readJsonFile, resetPawPlaceStubsFixture } from '../../e2e_support';

const planningRoot =
  'C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning';

test.describe('Advance Ticket to Next Stage (Same Scope)', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Ticket advances when stage complete and next stage has same scope', async ({ request }) => {
    const payload = {
      planningRoot,
      ticket_id: 'project-all',
      target_stage: 'discovery',
      placement: 'in_progress',
    };

    const response = await request.post('http://127.0.0.1:3001/api/board/ticket/move-to-stage', { data: payload });
    expect(response.ok()).toBe(true);
    const board = await readJsonFile<{ active: Array<{ ticket_id: string; stage: string; skill_progress: Record<string, unknown> }> }>(BOARD_JSON_PATH);
    const moved = board.active.find((ticket) => ticket.ticket_id === 'project-all');
    expect(moved?.stage).toBe('discovery');
    expect(Object.keys(moved?.skill_progress ?? {})).toHaveLength(0);
  });

  test('Scenario 2: Ticket does not advance automatically', async ({ request }) => {
    const moveForward = await request.post('http://127.0.0.1:3001/api/board/ticket/move-to-stage', {
      data: {
        planningRoot,
        ticket_id: 'project-all',
        target_stage: 'discovery',
        placement: 'in_progress',
      },
    });
    expect(moveForward.ok()).toBe(true);

    const moveBack = await request.post('http://127.0.0.1:3001/api/board/ticket/move-to-stage', {
      data: {
        planningRoot,
        ticket_id: 'project-all',
        target_stage: 'shaping',
        placement: 'in_progress',
      },
    });
    expect(moveBack.ok()).toBe(true);
    const board = await readJsonFile<{ active: Array<{ ticket_id: string; stage: string }> }>(BOARD_JSON_PATH);
    expect(board.active.find((ticket) => ticket.ticket_id === 'project-all')?.stage).toBe('shaping');
  });

  test.skip('Scenario 3: Ticket cannot skip a stage', async () => {
    // TODO: implement — Scenario 3: Ticket cannot skip a stage
  });
});
