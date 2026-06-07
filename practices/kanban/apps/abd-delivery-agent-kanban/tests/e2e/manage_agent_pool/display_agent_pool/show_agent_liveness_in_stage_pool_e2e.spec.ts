import { test, expect } from '@playwright/test';
import {
  goToBoard,
  resetPawPlaceStubsFixture,
} from '../../e2e_support';

test.describe('Indicate Agent Liveness from Heartbeat', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Agent alive — heartbeat recent', async ({ page, request }) => {
    await goToBoard(page);
    const startResponse = await request.post('http://127.0.0.1:3001/api/board/agent/start', {
      data: { role: 'business-expert' },
    });
    expect(startResponse.ok()).toBe(true);
    await waitForUiRefresh(page);
    const status = await request.get('http://127.0.0.1:3001/api/board/agent/business-expert/status');
    expect(status.ok()).toBe(true);
    const payload = (await status.json()) as { state: string };
    expect(['running', 'completed', 'failed']).toContain(payload.state);
  });

  test.skip('Scenario 2: Agent inactive — heartbeat stale with no board engagement', async () => {
    // TODO: implement — Scenario 2: Agent inactive — heartbeat stale with no board engagement
  });

  test.skip('Scenario 3: Agent idle — no heartbeat file', async () => {
    // TODO: implement — Scenario 3: Agent idle — no heartbeat file
  });

  test.skip('Scenario 4: Agent working — board engagement without heartbeat', async () => {
    // TODO: implement — Scenario 4: Agent working — board engagement without heartbeat
  });

  test.skip('Scenario 5: Agent working — stale heartbeat but board engagement', async () => {
    // TODO: implement — Scenario 5: Agent working — stale heartbeat but board engagement
  });
});
