import { expect, test } from "@playwright/test";

test("story detail shows activity preview headings", async ({ page }) => {
  await page.goto("/stories/story-1");

  await expect(page.getByRole("heading", { name: "最新解读" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "最新讨论" })).toBeVisible();
});
