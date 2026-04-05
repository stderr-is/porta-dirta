import { expect, test } from '@playwright/test';

for (const path of ['/', '/en', '/fr', '/de']) {
  test(`loads ${path}`, async ({ page }) => {
    const response = await page.goto(path);
    expect(response?.ok()).toBeTruthy();
    await expect(page.locator('body')).toBeVisible();
  });
}
