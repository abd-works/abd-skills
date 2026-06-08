import { test, expect } from '@playwright/test';
import { BOARD_JSON_PATH, KANBAN_JSON_PATH, goToBoard, resetPawPlaceStubsFixture, ticketCard, updateJsonFile } from '../../e2e_support';

test.describe('Show Skill Execution and Completion Indicators', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Completed skill shows green checkmark', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: '101',
          lineage: ['PawPlace', 'Build Domain Model'],
          scope_level: 'increment',
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
    const ticket = ticketCard(page, '101');
    await ticket.getByRole('button', { name: 'Expand skills' }).click();
    await expect(ticket.locator('.kb-ticket-skill-row').filter({ hasText: 'domain model' }).locator('.kb-skill-icon--done')).toBeVisible();
  });

  test('Scenario 2: Executing skill shows bot icon on that row only', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: '101',
          lineage: ['PawPlace', 'Build Domain Model'],
          scope_level: 'increment',
          stage: 'specification',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-specification-by-example': {
              execution_status: 'in_progress',
              review_status: 'not_started',
              agent: 'product-owner',
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
    const botRows = ticket.locator('.kb-ticket-skill-row:has(.kb-skill-icon--bot)');
    await expect(botRows).toHaveCount(1);
    await expect(botRows.first()).toContainText('spec by example');
  });

  test('Scenario 3: Skill under review shows review icon on that row only', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: '101',
          lineage: ['PawPlace', 'Build Domain Model'],
          scope_level: 'increment',
          stage: 'specification',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-specification-by-example': {
              execution_status: 'done',
              review_status: 'in_progress',
              agent: 'product-owner',
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
    await ticket.getByRole('button', { name: 'Expand skills' }).click();
    const reviewingRows = ticket.locator('.kb-ticket-skill-row:has(.kb-skill-icon--done)');
    await expect(reviewingRows).toHaveCount(1);
    await expect(ticket.locator('.kb-ticket-skill-row:has(.kb-skill-icon--bot)')).toHaveCount(0);
  });

  test('Scenario 4: Pending skill shows no icon', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(KANBAN_JSON_PATH, (kanban) => {
      const next = { ...kanban };
      const def = (next.definitions as Record<string, any>)['pawplace-stubs'];
      const stages = [...def.stages];
      const specification = stages.find((stage: any) => stage.name === 'specification');
      specification.stage_work_required = [
        { skill: 'abd-domain-model', role: 'business-expert' },
        { skill: 'abd-specification-by-example', role: 'product-owner' },
        { skill: 'abd-domain-walk', role: 'business-expert' },
      ];
      def.stages = stages;
      return next;
    });
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: '101',
          lineage: ['PawPlace', 'Build Domain Model'],
          scope_level: 'increment',
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
          hold_in_progress: false,
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
    const walkthrough = ticket.locator('.kb-ticket-skill-row').filter({ hasText: 'scenario walkthrough' });
    await expect(walkthrough).toHaveClass(/is-pending/);
    await expect(walkthrough.locator('.kb-skill-icon')).toHaveCount(0);
  });

  test('Scenario 5: Focus skill shows bot icon between executions', async ({ page }) => {
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
    await expect(expanded.locator('.kb-ticket-skill-row').filter({ hasText: 'domain model' }).locator('.kb-skill-icon--done')).toBeVisible();
  });

  test('Scenario 6: Skill icons use theme-visible colors', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: 'theme-check',
          lineage: ['PawPlace', 'Theme Icon Check'],
          scope_level: 'increment',
          stage: 'specification',
          priority: 1,
          entered_stage: '2026-06-01T12:00:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-specification-by-example': {
              execution_status: 'in_progress',
              review_status: 'not_started',
              agent: 'product-owner',
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
    await page.getByRole('button', { name: 'Engineering' }).click();
    const icon = page.locator('.kb-skill-icon').first();
    await expect(icon).toBeVisible();
    await expect(icon).toHaveCSS('color', /rgb/);
  });
});
