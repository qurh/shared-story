import { expect, test } from "@playwright/test";

test("story detail renders the back navigation", async ({ page }) => {
  await page.goto("/stories/story-1");

  await expect(page.getByRole("link", { name: /返回故事列表/ })).toBeVisible();
});

// TODO: Task 4 完成后，再补“最新解读/最新讨论”这类业务断言。
