import asyncio
import sys
import os
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

async def explore_cloudpanel():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        print(f"1. Navigating to {CP_URL}...")
        await page.goto(CP_URL, wait_until="networkidle", timeout=20000)

        print(f"2. Logging in as {USERNAME}...")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()

        await asyncio.sleep(4)
        print(f"Landed URL: {page.url}")

        # Check if login succeeded
        if "/login" in page.url:
            err = page.locator('.alert, .error, [class*="error"], [class*="alert"]')
            if await err.count() > 0:
                print("Login failed with message:", await err.first.inner_text())
            await page.screenshot(path="login_failed.png")
            await browser.close()
            return

        print("✓ Login SUCCESSFUL!")
        await page.screenshot(path="dashboard.png")

        # Let's inspect available links / buttons on dashboard
        links = await page.locator("a, button").all()
        print(f"Found {len(links)} interactive elements on dashboard.")
        for el in links:
            txt = (await el.inner_text()).strip().replace("\n", " ")
            href = await el.get_attribute("href")
            if any(k in txt.lower() for k in ["site", "add", "domain", "create"]):
                print(f"  - Element: text='{txt}', href='{href}'")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(explore_cloudpanel())
