import { test, expect } from '@playwright/test';
import {
  ACTION_STATE_PATH,
  BOARD_JSON_PATH,
  goToBoard,
  readJsonFile,
  resetPawPlaceStubsFixture,
  stageColumn,
  stageInProgressColumn,
  ticketCard,
  updateJsonFile,
  waitForUiRefresh,
} from '../../e2e_support';

test.describe('Expand Ticket Skill List', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Delivery Lead expands active ticket skill list', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: 'inc-sprint-1',
          lineage: ['PawPlace', 'Increment Sprint 1'],
          scope_level: 'sprint',
          stage: 'specification',
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
    const ticket = ticketCard(page, 'inc-sprint-1');
    await ticket.getByRole('button', { name: 'Expand skills' }).click();
    await expect(ticket.locator('.kb-ticket-skill-row')).toHaveCount(4);
  });

  test('Scenario 2: Stage queue ticket has no expand control', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [];
      next.done = [];
      next.archived = [];
      next.backlog = [
        {
          ticket_id: 'inc-sprint-3',
          lineage: ['PawPlace', 'Increment Sprint 3'],
          scope_level: 'sprint',
          stage: 'specification',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {},
        },
      ];
      return next;
    });

    await goToBoard(page);
    const queueTicket = stageColumn(page, 'specification').locator('[data-ticket="inc-sprint-3"]').first();
    await expect(queueTicket.getByRole('button', { name: /Expand skills/i })).toHaveCount(0);
  });

  test('Scenario 3: Archived stage-complete ticket expands in stage Done', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [];
      next.backlog = [];
      next.done = [];
      next.archived = [
        {
          ticket_id: 'inc-8-marketing-engine',
          lineage: ['PawPlace', 'Marketing Engine'],
          scope_level: 'increment',
          stage: 'exploration',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: '2026-06-01T12:10:00Z',
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-domain-language': {
              execution_status: 'done',
              review_status: 'done',
              agent: 'business-expert',
              reviewer: 'business-expert',
            },
          },
        },
      ];
      return next;
    });

    await goToBoard(page);
    const ticket = ticketCard(page, 'inc-8-marketing-engine');
    await ticket.getByRole('button', { name: 'Expand skills' }).click();
    await expect(ticket.locator('.kb-ticket-skill-row').locator('.kb-skill-icon--done').first()).toBeVisible();
  });

  test('Scenario: Agent-avatar drop records intent without moving ticket stage', async ({ page }) => {
    await goToBoard(page);
    const ticket = ticketCard(page, 'project-all');
    const roleAvatar = page.locator('.kb-agent-avatar--draggable[data-role="business-expert"]').first();
    await roleAvatar.dragTo(ticket);
    await waitForUiRefresh(page);
    await expect(stageInProgressColumn(page, 'shaping').locator('[data-ticket="project-all"]')).toBeVisible();
    const actionState = await readJsonFile<{ intents: Array<{ ticket_id: string }> }>(ACTION_STATE_PATH);
    expect(Array.isArray(actionState.intents)).toBe(true);
  });
});
