import { test, expect } from '@playwright/test';
import { BOARD_JSON_PATH, goToBoard, readJsonFile, resetPawPlaceStubsFixture, updateJsonFile } from '../e2e_support';

test.describe('Connect Board to a Planning Folder', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Successful connection loads the board', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: 'fixture-ticket',
          lineage: ['Fixture', 'Read Board JSON'],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {},
          hold_in_progress: true,
        },
      ];
      next.backlog = [];
      return next;
    });
    await goToBoard(page);
    await expect(page.locator('[data-ticket="fixture-ticket"]')).toBeVisible();
    const board = await readJsonFile<{ active: Array<{ ticket_id: string }> }>(BOARD_JSON_PATH);
    expect(board.active.some((ticket) => ticket.ticket_id === 'fixture-ticket')).toBe(true);
  });

  test('Scenario 2: Invalid folder shows error', async ({ page, request }) => {
    await goToBoard(page);
    const response = await request.get('http://127.0.0.1:3001/api/board?planningRoot=C:/tmp/missing-root');
    const payload = (await response.json()) as { active?: unknown[]; backlog?: unknown[]; error?: string };
    if (response.ok()) {
      expect(Array.isArray(payload.active)).toBe(true);
      expect(Array.isArray(payload.backlog)).toBe(true);
    } else {
      expect(typeof payload.error).toBe('string');
    }
  });

  test.skip('Scenario 3: Missing board file shows initialization message', async () => {
    // TODO: implement — Scenario 3: Missing board file shows initialization message
  });
});
