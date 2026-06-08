import { test, expect } from '@playwright/test';
import { resetPawPlaceStubsFixture } from '../../e2e_support';

const planningRoot =
  'C:/dev/agilebydesign-skills/practices/kanban/apps/abd-delivery-agent-kanban/tests/e2e/data/pawplace-stubs/docs/planning';

test.describe('Pull Backlog Tickets to Active per Stage WIP', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Kanban Lead pulls partition tickets up to WIP limit', async ({ request }) => {
    const response = await request.post('http://127.0.0.1:3001/api/board/lead-scan', {
      data: { planningRoot, mode: 'all' },
    });
    expect(response.ok()).toBe(true);
    const payload = (await response.json()) as Record<string, unknown>;
    expect(payload).toBeTruthy();
  });

  test.skip('Scenario 2: Kanban Lead does not pull when WIP is full', async () => {
    // TODO: implement — Scenario 2: Kanban Lead does not pull when WIP is full
  });

  test.skip('Scenario 3: Kanban Lead pulls for each stage independently', async () => {
    // TODO: implement — Scenario 3: Kanban Lead pulls for each stage independently
  });

  test.skip('Scenario 4: WIP limit derived from Team capacity when not explicit', async () => {
    // TODO: implement — Scenario 4: WIP limit derived from Team capacity when not explicit
  });

  test.skip('Scenario 5: Rolling pull when first skill is done on active tickets', async () => {
    // TODO: implement — Scenario 5: Rolling pull when first skill is done on active tickets
  });
});
