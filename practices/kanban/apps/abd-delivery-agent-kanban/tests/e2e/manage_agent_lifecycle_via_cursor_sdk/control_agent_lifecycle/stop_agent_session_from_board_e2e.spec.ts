import { test, expect } from '@playwright/test';
import { resetPawPlaceStubsFixture } from '../../e2e_support';

test.describe('Stop Team Member Agent', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Kanban Lead stops idle team member — session terminates cleanly', async ({ request }) => {
    const start = await request.post('http://127.0.0.1:3001/api/board/agent/start', {
      data: { role: 'business-expert' },
    });
    expect(start.ok()).toBe(true);
    const stop = await request.post('http://127.0.0.1:3001/api/board/agent/stop', {
      data: { role: 'business-expert' },
    });
    expect(stop.ok()).toBe(true);
    const status = await request.get('http://127.0.0.1:3001/api/board/agent/business-expert/status');
    const payload = (await status.json()) as { state: string };
    expect(['idle', 'completed', 'failed']).toContain(payload.state);
  });

  test.skip('Scenario 2: Stop agent that has in-progress skill — skill progress preserved before termination', async () => {
    // TODO: implement — Scenario 2: Stop agent that has in-progress skill — skill progress preserved before termination
  });
});
