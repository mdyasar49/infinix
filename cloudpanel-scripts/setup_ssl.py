import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

async def setup_ssl():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        print("1. Logging into CloudPanel...")
        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        print("2. Navigating to onboarding.infogenx.com SSL settings...")
        await page.goto("https://cp.infogenx.com/site/onboarding.infogenx.com/ssl", wait_until="networkidle")
        await asyncio.sleep(2)

        # Look for Let's Encrypt or New Let's Encrypt Certificate
        print("Checking SSL options...")
        le_btn = page.locator('text="New Let\'s Encrypt Certificate", button:has-text("New Let\'s Encrypt Certificate"), a:has-text("Let\'s Encrypt"), button:has-text("Create")')
        if await le_btn.count() > 0:
            print("Clicking Let's Encrypt Certificate button...")
            await le_btn.first.click()
            await asyncio.sleep(2)

            # Click create/confirm certificate
            confirm_btn = page.locator('button:has-text("Create and Install"), button:has-text("Create")')
            if await confirm_btn.count() > 0:
                print("Installing certificate...")
                await confirm_btn.first.click()
                await asyncio.sleep(8)

        await page.screenshot(path="ssl_status.png")
        print("SSL status screenshot saved to ssl_status.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(setup_ssl())
