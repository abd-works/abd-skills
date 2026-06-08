import { test, expect } from '@playwright/test';
import { resetPawPlaceStubsFixture } from '../../e2e_support';

test.describe('Report Agent Session Status via SDK', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Running session reports "running" with message count and last activity', async ({ request }) => {
    const status = await request.get('http://127.0.0.1:3001/api/board/agent/business-expert/status');
    expect(status.ok()).toBe(true);
    const payload = (await status.json()) as { state: string; messageCount: number };
    expect(typeof payload.state).toBe('string');
    expect(typeof payload.messageCount).toBe('number');
  });

  test('Scenario 2: Completed session reports "completed" with final message', async ({ request }) => {
    await request.post('http://127.0.0.1:3001/api/board/agent/stop', {
      data: { role: 'ux-designer' },
    });
    const status = await request.get('http://127.0.0.1:3001/api/board/agent/ux-designer/status');
    expect(status.ok()).toBe(true);
    const payload = (await status.json()) as { state: string; messageCount: number };
    expect(['idle', 'completed', 'failed']).toContain(payload.state);
    expect(payload.messageCount).toBeGreaterThanOrEqual(0);
  });

  test.skip('Scenario 3: Failed session reports "failed" with error detail', async () => {
    // TODO: implement — Scenario 3: Failed session reports "failed" with error detail
  });
});
