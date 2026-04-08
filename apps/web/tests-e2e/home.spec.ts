import { expect, test } from "@playwright/test";

test("home renders the core browse controls", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "shared-story" })).toBeVisible();
  await expect(page.getByRole("textbox", { name: "搜索故事" })).toBeVisible();
  await expect(page.getByRole("button", { name: "搜索" })).toBeVisible();
});

// TODO: Task 3 完成后，把这里升级为更强的首屏价值文案断言。
