import asyncio
import sys
from playwright.async_api import async_playwright

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

async def check_ssl_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(ignore_https_errors=True)

        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        await page.goto("https://cp.infogenx.com/site/onboarding.infogenx.com/ssl", wait_until="networkidle")
        
        buttons = await page.locator("button, a").all()
        for b in buttons:
            txt = (await b.inner_text()).strip()
            href = await b.get_attribute("href")
            if txt:
                print(f"Button/Link: text='{txt}', href='{href}'")

        await browser.close()

asyncio.run(check_ssl_page())
