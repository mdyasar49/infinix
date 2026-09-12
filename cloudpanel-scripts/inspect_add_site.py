import asyncio
import sys
import os
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

async def inspect_add_site():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        print("Navigating to /site/new...")
        await page.goto("https://cp.infogenx.com/site/new", wait_until="networkidle")
        await asyncio.sleep(2)
        print("Landed at:", page.url)

        # Inspect site options
        options = await page.locator(".site-type-item, .card, [class*='site-type'], a, button").all()
        print(f"Found {len(options)} elements on /site/new")
        for opt in options:
            txt = (await opt.inner_text()).strip().replace("\n", " ")
            href = await opt.get_attribute("href")
            if len(txt) > 0 and len(txt) < 80:
                print(f"  Option: '{txt}', href='{href}'")

        await page.screenshot(path="add_site_page.png")
        print("Screenshot saved to add_site_page.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_add_site())
