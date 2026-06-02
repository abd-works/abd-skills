import { test, expect } from '@playwright/test';

test('home page links to live board', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('link', { name: /open live board/i })).toBeVisible();
  await expect(page.getByText(/default planning folder/i)).toBeVisible();
});

test('board loads ticket from planning folder', async ({ page }, testInfo) => {
  const fixture = testInfo.project.metadata?.fixture ?? 'pawplace-stubs';

  await page.goto('/board');
  await expect(page.getByRole('heading', { name: /kanban board/i })).toBeVisible();

  if (fixture === 'pawplace-stubs') {
    const ticket = page.locator('[data-ticket="project-all"]');
    await expect(ticket).toBeVisible();
    await expect(ticket.locator('.kb-ticket-label')).toHaveText('PawPlace');
    await expect(page.getByText('shaping', { exact: false })).toBeVisible();
  } else {
    const ticket = page.locator('[data-ticket="project-all-inc-1-find-products-and-check-store-stock"]');
    await expect(ticket).toBeVisible();
    await expect(ticket.locator('.kb-ticket-label')).toHaveText(/find products and check store stock/i);
    await expect(page.getByText('discovery', { exact: false })).toBeVisible();
  }
});
