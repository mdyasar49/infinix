import asyncio
import sys
from playwright.async_api import async_playwright

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

async def check_site_settings():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(ignore_https_errors=True)

        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        await page.goto("https://cp.infogenx.com/site/onboarding.infogenx.com", wait_until="networkidle")
        
        # Print subnavigation tabs
        tabs = await page.locator("a, button").all()
        for t in tabs:
            txt = (await t.inner_text()).strip()
            href = await t.get_attribute("href")
            if href and "/site/onboarding.infogenx.com" in href:
                print(f"Tab: text='{txt}', href='{href}'")

        await browser.close()

asyncio.run(check_site_settings())
