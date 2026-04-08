import { expect, test } from "@playwright/test";

test("home shows the value statement", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "先看故事，再看不同理解" })).toBeVisible();
});
