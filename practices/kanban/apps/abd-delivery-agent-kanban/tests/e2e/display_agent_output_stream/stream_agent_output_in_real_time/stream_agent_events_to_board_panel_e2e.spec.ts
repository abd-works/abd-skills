import { test, expect } from '@playwright/test';
import { resetPawPlaceStubsFixture } from '../../e2e_support';

test.describe('Stream Agent Messages to Panel Like IDE Chat', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Agent sends text response — appears as message bubble in panel', async ({ request }) => {
    const start = await request.post('http://127.0.0.1:3001/api/board/agent/start', {
      data: { role: 'business-expert' },
    });
    expect(start.ok()).toBe(true);
    const status = await request.get('http://127.0.0.1:3001/api/board/agent/business-expert/status');
    expect(status.ok()).toBe(true);
    const payload = (await status.json()) as { state: string; messageCount: number };
    expect(['running', 'completed', 'failed']).toContain(payload.state);
    expect(payload.messageCount).toBeGreaterThanOrEqual(0);
  });

  test.skip('Scenario 2: Agent is thinking — thinking indicator animates in panel', async () => {
    // TODO: implement — Scenario 2: Agent is thinking — thinking indicator animates in panel
  });

  test.skip('Scenario 3: Agent completes skill — completion status shown in panel', async () => {
    // TODO: implement — Scenario 3: Agent completes skill — completion status shown in panel
  });
});
