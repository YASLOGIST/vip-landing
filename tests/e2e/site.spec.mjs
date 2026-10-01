import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("locale choice updates semantics and persists across a reload", async ({ page }) => {
  await page.goto("/");
  await page.locator('[data-language="ar"]').first().click();
  await expect.poll(() => page.evaluate(() => document.documentElement.lang)).toBe("ar");
  await expect.poll(() => page.evaluate(() => document.documentElement.dir)).toBe("rtl");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("فخامة");
  await page.reload();
  await expect.poll(() => page.evaluate(() => document.documentElement.lang)).toBe("ar");
});

test("the atmosphere selector changes the CSS-rendered hero profile", async ({ page }) => {
  await page.goto("/");
  await page.locator('[data-visual-mode="emerald"]').click();
  await expect(page.locator(".hero-visual")).toHaveClass(/visual-mode-emerald/);
  await expect(page.locator('[data-visual-mode="emerald"]')).toHaveAttribute("aria-pressed", "true");
  await page.reload();
  await expect(page.locator(".hero-visual")).toHaveClass(/visual-mode-emerald/);
});

test("mobile navigation opens, receives focus, and closes with Escape", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await page.locator("[data-menu-toggle]").click();
  await expect(page.locator("#mobile-menu")).toHaveClass(/is-open/);
  await expect(page.locator("#mobile-menu [data-close-menu]").first()).toBeFocused();
  await page.keyboard.press("Escape");
  await expect(page.locator("#mobile-menu")).not.toHaveClass(/is-open/);
  await expect(page.locator("[data-menu-toggle]")).toBeFocused();
});

test("private brief routes the selected vehicle into the concierge form", async ({ page }) => {
  await page.goto("/");
  await page.locator('[data-brief="hybrid-gt"]').click();
  const dialog = page.locator("[data-brief-dialog]");
  await expect(dialog).toBeVisible();
  await expect(dialog).toContainText("Emerald Voltage");
  await dialog.locator("[data-brief-request]").click();
  await expect(dialog).toHaveCount(0);
  await expect(page.locator('select[name="interest"]')).toHaveValue("hybrid-gt");
  await expect(page.locator('input[name="name"]')).toBeFocused();
});

test("consultation progress and successful delivery cover the main conversion flow", async ({ page }) => {
  await page.goto("/");
  await page.route("**/", async (route) => {
    if (route.request().method() === "POST") await route.fulfill({ status: 200, contentType: "text/html", body: "ok" });
    else await route.continue();
  });
  const form = page.locator(".contact-form");
  await form.locator('input[name="name"]').fill("Ari Client");
  await form.locator('input[name="email"]').fill("ari@example.test");
  await form.locator('select[name="interest"]').selectOption("grand-coupe");
  await form.locator('select[name="timeline"]').selectOption("30-days");
  await form.locator('select[name="channel"]').selectOption("private-viewing");
  await expect(form.locator("[data-form-progress]")).toHaveAttribute("aria-valuenow", "5");
  await form.getByRole("button", { name: "Request concierge call" }).click();
  await expect(form.locator(".form-status")).toHaveClass(/is-success/);
  await expect(form.locator(".form-status")).toContainText("Your brief is with the concierge desk");
  await expect(form.locator("[data-form-progress]")).toHaveAttribute("aria-valuenow", "0");
});

test("the no-JavaScript fallback retains a usable confidential brief form", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto("http://127.0.0.1:4173/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("darker kind of luxury");
  await expect(page.locator('form[name="vip-consultation"]')).toBeVisible();
  await expect(page.locator('input[name="channel"]')).toBeVisible();
  await context.close();
});

test("critical screen has no automated accessibility violations @a11y", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test("first-party experience remains inside the performance budget @performance", async ({ page }) => {
  await page.goto("/");
  const metrics = await page.evaluate(() => {
    const resources = performance.getEntriesByType("resource");
    const firstPartyBytes = resources
      .filter((entry) => new URL(entry.name).origin === location.origin)
      .reduce((total, entry) => total + entry.transferSize, 0);
    return { firstPartyBytes, nodes: document.getElementsByTagName("*").length };
  });
  expect(metrics.firstPartyBytes).toBeLessThan(150 * 1024);
  expect(metrics.nodes).toBeLessThan(500);
});
