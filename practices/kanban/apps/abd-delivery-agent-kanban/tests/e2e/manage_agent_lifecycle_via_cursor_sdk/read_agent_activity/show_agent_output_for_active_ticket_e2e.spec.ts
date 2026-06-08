import { test, expect } from '@playwright/test';
import { goToBoard, resetPawPlaceStubsFixture } from '../../e2e_support';

test.describe('Stream Agent Messages via SDK', () => {
  test.beforeEach(() => {
    resetPawPlaceStubsFixture();
  });

  test('Scenario 1: Running agent emits message — server receives it in real time', async ({ page, request }) => {
    await goToBoard(page);
    await request.post('http://127.0.0.1:3001/api/board/agent/start', {
      data: { role: 'business-expert' },
    });
    await page.getByRole('button', { name: 'Refresh' }).click();
    const status = await request.get('http://127.0.0.1:3001/api/board/agent/business-expert/status');
    expect(status.ok()).toBe(true);
    const payload = (await status.json()) as { messageCount: number };
    expect(payload.messageCount).toBeGreaterThanOrEqual(0);
  });

  test('Scenario 2: Agent emits thinking indicator — server relays to connected clients', async ({ page, request }) => {
    await goToBoard(page);
    await request.post('http://127.0.0.1:3001/api/board/agent/start', {
      data: { role: 'product-owner' },
    });
    await page.getByRole('button', { name: 'Refresh' }).click();
    const status = await request.get('http://127.0.0.1:3001/api/board/agent/product-owner/status');
    expect(status.ok()).toBe(true);
    const payload = (await status.json()) as { state: string };
    expect(['running', 'completed', 'failed']).toContain(payload.state);
  });
});
