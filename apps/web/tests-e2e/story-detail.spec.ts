import { expect, test } from "@playwright/test";

test("story detail shows preview content and next steps", async ({ page }) => {
  await page.goto("/stories/story-1");

  await expect(page.getByRole("link", { name: /返回故事列表/ })).toBeVisible();
  await expect(page.getByRole("heading", { name: "最新解读" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "最新讨论" })).toBeVisible();
  await expect(page.locator(".detail-panel")).toHaveCount(2);
  await expect(page.locator(".detail-preview-card").first()).toBeVisible();
  await expect(page.locator(".detail-preview-card").last()).toBeVisible();
  await expect(page.getByRole("link", { name: "继续看其他故事" })).toBeVisible();
});
