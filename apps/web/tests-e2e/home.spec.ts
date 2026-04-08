import { expect, test } from "@playwright/test";

test("home reflects the story-first browsing experience", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "先看故事，再看不同理解" })).toBeVisible();
  await expect(page.getByText("先选故事，再看不同角色的解读与讨论")).toBeVisible();
  await expect(page.getByText("最多人关注")).toBeVisible();
  await expect(page.getByText("查看这个故事的更多讨论")).not.toBeVisible();
});
