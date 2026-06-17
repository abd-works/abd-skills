import { test, expect } from '@playwright/test';
import {
  BOARD_JSON_PATH,
  KANBAN_JSON_PATH,
  goToBoard,
  resetPawPlaceStubsFixture,
  stageColumn,
  updateJsonFile,
} from '../../e2e_support';

test.describe('Show Assigned Skills per Stage', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Stage skill rail appears with skill chips', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(KANBAN_JSON_PATH, (kanban) => {
      const next = { ...kanban };
      const def = (next.definitions as Record<string, any>)['pawplace-stubs'];
      const stages = [...def.stages];
      const discovery = stages.find((stage: any) => stage.name === 'discovery');
      discovery.stage_work_required = [
        { skill: 'abd-domain-language', role: 'business-expert' },
        { skill: 'abd-domain-sketch', role: 'business-expert' },
      ];
      def.stages = stages;
      return next;
    });

    await goToBoard(page);
    const discovery = stageColumn(page, 'discovery');
    await expect(discovery.locator('.kb-stage-skills')).toBeVisible();
    await expect(discovery.getByText('Domain Language', { exact: true })).toBeVisible();
    await expect(discovery.getByText('domain sketch', { exact: true })).toBeVisible();
  });

  test('Scenario 2: Stage with no skills shows no rail', async ({ page }) => {
    await updateJsonFile<Record<string, unknown>>(KANBAN_JSON_PATH, (kanban) => {
      const next = { ...kanban };
      const def = (next.definitions as Record<string, any>)['pawplace-stubs'];
      const stages = [...def.stages];
      const shaping = stages.find((stage: any) => stage.name === 'shaping');
      shaping.stage_work_required = [];
      def.stages = stages;
      return next;
    });
    await updateJsonFile<Record<string, unknown>>(BOARD_JSON_PATH, (board) => {
      const next = { ...board };
      next.active = [];
      next.backlog = [];
      next.done = [];
      next.archived = [];
      return next;
    });

    await goToBoard(page);
    await expect(stageColumn(page, 'shaping')).toHaveCount(0);
    await expect(stageColumn(page, 'discovery')).toBeVisible();
  });
});
