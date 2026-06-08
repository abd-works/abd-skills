import { test, expect } from '@playwright/test';
import {
  BOARD_JSON_PATH,
  goToBoard,
  resetPawPlaceStubsFixture,
  stageInProgressColumn,
  ticketCard,
  updateJsonFile,
} from '../../e2e_support';

test.describe('Display Backlog Tickets', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Backlog tickets ordered by priority', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.done = [];
      next.archived = [];
      next.active = [
        {
          ticket_id: 'STORY-007',
          lineage: ['PetStore', 'Sprint 1', 'List Pets'],
          scope_level: 'sprint',
          stage: 'discovery',
          priority: 2,
          entered_stage: '2026-06-01T12:01:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {},
          hold_in_progress: true,
        },
        {
          ticket_id: 'STORY-003',
          lineage: ['PetStore', 'Sprint 1', 'Add Pet'],
          scope_level: 'sprint',
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
    const stageTickets = stageInProgressColumn(page, 'discovery');
    const story3 = stageTickets.locator('[data-ticket="STORY-003"]');
    const story7 = stageTickets.locator('[data-ticket="STORY-007"]');
    await expect(story3.getByText('Add Pet', { exact: true })).toBeVisible();
    await expect(story7.getByText('List Pets', { exact: true })).toBeVisible();
    await expect(stageTickets.locator('[data-ticket="STORY-003"], [data-ticket="STORY-007"]')).toHaveCount(2);
  });

  test('Scenario 2: Hovering backlog ticket shows full lineage', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: 'STORY-003',
          lineage: ['PetStore', 'Sprint 1', 'Add Pet'],
          scope_level: 'sprint',
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
      next.done = [];
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    await expect(ticketCard(page, 'STORY-003')).toHaveAttribute('title', /PetStore > Sprint 1 > Add Pet/);
  });

  test('Scenario 3: Empty backlog renders without cards', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [];
      next.backlog = [];
      next.done = [];
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    const backlog = page.locator('[data-end-col="backlog"]');
    await expect(backlog).toBeVisible();
    await expect(backlog.locator('[data-ticket]')).toHaveCount(0);
  });
});
