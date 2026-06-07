import { test, expect } from '@playwright/test';
import { BOARD_JSON_PATH, goToBoard, resetPawPlaceStubsFixture, ticketCard, updateJsonFile } from '../../e2e_support';

test.describe('Show Active Skill and Agent on Ticket', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Executing agent shown on ticket', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: '101',
          lineage: ['PawPlace', 'Build Domain Model'],
          scope_level: 'increment',
          stage: 'exploration',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-domain-language': {
              execution_status: 'in_progress',
              review_status: 'not_started',
              agent: 'business-expert',
            },
          },
          hold_in_progress: true,
        },
      ];
      next.backlog = [];
      next.done = [];
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    const ticket = ticketCard(page, '101');
    await ticket.getByRole('button', { name: 'Expand skills' }).click();
    await expect(
      ticket
        .locator('.kb-ticket-skill-row')
        .filter({ hasText: 'Domain Language' })
        .locator('.kb-skill-icon--bot, .kb-skill-icon--done'),
    ).toBeVisible();
    await expect(page.locator('.kb-pool-group[data-role="business-expert"] [title]').first()).toBeVisible();
  });

  test('Scenario 2: Focus skill shown between executions', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: 'inc-sprint-2',
          lineage: ['PawPlace', 'Increment Sprint 2'],
          scope_level: 'sprint',
          stage: 'specification',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-domain-model': {
              execution_status: 'done',
              review_status: 'done',
              agent: 'business-expert',
              reviewer: 'business-expert',
            },
          },
          hold_in_progress: true,
        },
      ];
      next.backlog = [];
      next.done = [];
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    const ticket = ticketCard(page, 'inc-sprint-2');
    await ticket.getByRole('button', { name: 'Expand skills' }).click();
    const expanded = ticket.locator('.kb-ticket-skills-expand');
    await expect(expanded.getByText('spec by example', { exact: true })).toBeVisible();
    await expect(expanded.locator('.kb-ticket-skill-row').filter({ hasText: 'domain model' }).locator('.kb-skill-icon--done')).toBeVisible();
  });

  test('Scenario 3: Bot icon visible without agent avatar', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: 'inc-sprint-2',
          lineage: ['PawPlace', 'Increment Sprint 2'],
          scope_level: 'sprint',
          stage: 'specification',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-domain-model': {
              execution_status: 'done',
              review_status: 'done',
            },
          },
          hold_in_progress: true,
        },
      ];
      next.backlog = [];
      next.done = [];
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    const ticket = ticketCard(page, 'inc-sprint-2');
    await expect(ticket.locator('.kb-skill-icon')).toHaveCount(0);
  });

  test('Scenario 4: Reviewing agent replaces executor', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: '101',
          lineage: ['PawPlace', 'Build Domain Model'],
          scope_level: 'increment',
          stage: 'exploration',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-domain-language': {
              execution_status: 'done',
              review_status: 'in_progress',
              agent: 'business-expert',
              reviewer: 'engineer',
            },
          },
          hold_in_progress: true,
        },
      ];
      next.backlog = [];
      next.done = [];
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    const ticket = ticketCard(page, '101');
    await expect(ticket.locator('.kb-skill-icon--done')).toBeVisible();
  });
});
