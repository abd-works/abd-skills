import { test, expect } from '@playwright/test';
import {
  BOARD_JSON_PATH,
  goToBoard,
  resetPawPlaceStubsFixture,
  updateJsonFile,
  waitForUiRefresh,
  expectTicketInStageInProgress,
} from '../e2e_support';

test.describe('Board Reflects Agent Changes Automatically', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Agent moves a ticket — board refreshes', async ({ page }) => {
    await goToBoard(page);
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        ...(next.active as any[]),
        {
          ticket_id: 'refreshed-ticket',
          lineage: ['PawPlace', 'Refresh Story'],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 2,
          entered_stage: '2026-06-01T12:11:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {},
          hold_in_progress: true,
        },
      ];
      return next;
    });

    await page.getByRole('button', { name: 'Refresh' }).click();
    await waitForUiRefresh(page);
    await expectTicketInStageInProgress(page, 'refreshed-ticket', 'discovery');
  });

  test.skip('Scenario 2: Agent writes heartbeat — liveness updates', async () => {
    // TODO: implement — Scenario 2: Agent writes heartbeat — liveness updates
  });

  test.skip('Scenario 3: Non-board file changes do not trigger refresh', async () => {
    // TODO: implement — Scenario 3: Non-board file changes do not trigger refresh
  });

  test.skip('Scenario 4: Skill state transitions refresh UI with unchanged ticket/stage counts', async () => {
    // TODO: implement — Scenario 4: Skill state transitions refresh UI with unchanged ticket/stage counts
  });
});
