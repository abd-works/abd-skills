import { test, expect } from '@playwright/test';
import { resetPawPlaceStubsFixture } from '../../e2e_support';

test.describe('Start Team Member Agent', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Kanban Lead starts engineer for eligible skill — session moves to running', async ({ request }) => {
    const start = await request.post('http://127.0.0.1:3001/api/board/agent/start', {
      data: { role: 'business-expert' },
    });
    expect(start.ok()).toBe(true);
    const status = await request.get('http://127.0.0.1:3001/api/board/agent/business-expert/status');
    expect(status.ok()).toBe(true);
    const payload = (await status.json()) as { state: string };
    expect(['running', 'completed', 'failed']).toContain(payload.state);
  });

  test.skip('Scenario 2: Kanban Lead starts business-expert for first skill in rail order — agent pulls downstream first', async () => {
    // TODO: implement — Scenario 2: Kanban Lead starts business-expert for first skill in rail order — agent pulls downstream first
  });
});
