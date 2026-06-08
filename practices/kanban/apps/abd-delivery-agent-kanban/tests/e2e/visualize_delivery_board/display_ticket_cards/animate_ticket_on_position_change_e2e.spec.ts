import { test, expect } from '@playwright/test';
import {
  BOARD_JSON_PATH,
  goToBoard,
  resetPawPlaceStubsFixture,
  stageDoneColumn,
  ticketCard,
  updateJsonFile,
  expectTicketInStageInProgress,
  waitForUiRefresh,
} from '../../e2e_support';

test.describe('Animate Ticket on Position Change', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Ticket moves stage and animates', async ({ page }) => {
    await goToBoard(page);
    const source = ticketCard(page, 'project-all');
    const doneZone = stageDoneColumn(page, 'shaping');
    await source.dragTo(doneZone);
    await waitForUiRefresh(page);
    await page.getByRole('button', { name: 'Refresh' }).click();
    await expect(source).toBeVisible();
  });

  test('Scenario 2: New ticket does not animate', async ({ page }) => {
    await goToBoard(page);
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        ...(next.active as any[]),
        {
          ticket_id: '301',
          lineage: ['PawPlace', 'Brand New Ticket'],
          scope_level: 'increment',
          stage: 'discovery',
          priority: 2,
          entered_stage: '2026-06-01T12:10:00Z',
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
    const newTicket = ticketCard(page, '301');
    await expectTicketInStageInProgress(page, '301', 'discovery');
    await expect(newTicket).not.toHaveClass(/kb-ticket--flip/);
  });
});
