import { expect, test } from "@playwright/test";

test("story detail shows preview content and next steps", async ({ page }) => {
  await page.goto("/stories/story-1");

  await expect(page.getByRole("link", { name: /返回故事列表/ })).toBeVisible();
  await expect(page.getByRole("heading", { name: "最新解读" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "最新讨论" })).toBeVisible();
  await expect(page.getByText("先清空，再吸收")).toBeVisible();
  await expect(page.getByText("真正的学习往往始于承认自己还没准备好。")).toBeVisible();
  await expect(page.getByText("这个故事提醒我们，知识输入不仅取决于内容质量，也取决于接收者是否有空间。")).toBeVisible();
  await expect(page.getByRole("link", { name: "继续看其他故事" })).toBeVisible();
});
