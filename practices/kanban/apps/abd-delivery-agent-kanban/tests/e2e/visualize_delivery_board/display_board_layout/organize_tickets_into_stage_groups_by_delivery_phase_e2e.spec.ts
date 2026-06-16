import { test, expect } from '@playwright/test';
import {
  BOARD_JSON_PATH,
  goToBoard,
  resetPawPlaceStubsFixture,
  stageColumn,
  stageDoneColumn,
  updateJsonFile,
  expectTicketInStageInProgress,
  expectTicketNotInGlobalBacklog,
} from '../../e2e_support';

test.describe('Organize Tickets into Stage Groups by Delivery Phase', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Tickets grouped under their assigned stages', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: '101',
          lineage: ['PawPlace', 'Build Domain Model'],
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
        {
          ticket_id: '102',
          lineage: ['PawPlace', 'Write Acceptance Tests'],
          scope_level: 'increment',
          stage: 'exploration',
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
      ];
      next.backlog = [];
      next.done = [];
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    await expectTicketInStageInProgress(page, '101', 'discovery');
    await expectTicketInStageInProgress(page, '102', 'exploration');
    const discoveryX = await stageColumn(page, 'discovery').boundingBox();
    const explorationX = await stageColumn(page, 'exploration').boundingBox();
    expect(discoveryX?.x ?? 0).toBeLessThan(explorationX?.x ?? 0);
  });

  test('Scenario 2: Stage shows Queue, In Progress, and Done sub-columns', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: 'inc-sprint-b',
          lineage: ['PawPlace', 'Sprint B'],
          scope_level: 'sprint',
          stage: 'specification',
          priority: 2,
          entered_stage: '2026-06-01T12:01:00Z',
          completed_stage: null,
          stage_history: [],
          scatter_from: null,
          scatter_to: [],
          notes: '',
          skill_progress: {
            'abd-domain-model': {
              execution_status: 'in_progress',
              review_status: 'not_started',
              agent: 'business-expert',
            },
          },
          hold_in_progress: true,
        },
      ];
      next.done = [
        {
          ticket_id: 'inc-sprint-c',
          lineage: ['PawPlace', 'Sprint C'],
          scope_level: 'sprint',
          stage: 'specification',
          priority: 3,
          entered_stage: '2026-06-01T12:02:00Z',
          completed_stage: '2026-06-01T12:03:00Z',
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
        },
      ];
      next.backlog = [
        {
          ticket_id: 'inc-sprint-a',
          lineage: ['PawPlace', 'Sprint A'],
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
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    const specification = stageColumn(page, 'specification');
    await expect(specification.getByText('In Progress', { exact: true })).toBeVisible();
    await expect(specification.getByText('Done', { exact: true })).toBeVisible();
    await expect(stageDoneColumn(page, 'specification').getByText('Queued', { exact: true })).toHaveCount(0);
    await expect(specification.locator('[data-ticket="inc-sprint-a"]')).toHaveCount(0);
    await expect(specification.locator('[data-ticket="inc-sprint-b"]')).toBeVisible();
    await expect(specification.locator('[data-ticket="inc-sprint-c"]')).toBeVisible();
    await expectTicketNotInGlobalBacklog(page, 'inc-sprint-a');
  });

  test('Scenario 3: Stage queue tickets do not appear in global Backlog', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.backlog = [
        {
          ticket_id: 'inc-sprint-a',
          lineage: ['PawPlace', 'Sprint A'],
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
    await expect(stageColumn(page, 'specification').locator('[data-ticket="inc-sprint-a"]')).toHaveCount(0);
    await expectTicketNotInGlobalBacklog(page, 'inc-sprint-a');
  });

  test('Scenario 4: Empty stage still renders', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [
        {
          ticket_id: '200',
          lineage: ['PawPlace', 'Exploration Story'],
          scope_level: 'increment',
          stage: 'exploration',
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
    const shaping = stageColumn(page, 'shaping');
    await expect(shaping).toBeVisible();
    await expect(shaping.locator('[data-ticket]')).toHaveCount(0);
  });
});
