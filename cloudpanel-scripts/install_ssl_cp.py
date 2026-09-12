import asyncio
import sys
from playwright.async_api import async_playwright

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

async def install_ssl():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(ignore_https_errors=True)

        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        print("Navigating to SSL/TLS certificates...")
        await page.goto("https://cp.infogenx.com/site/onboarding.infogenx.com/certificates", wait_until="networkidle")
        await asyncio.sleep(1)

        # Look for New Let's Encrypt Certificate
        le_action = page.locator('text="New Let\'s Encrypt Certificate", text="New Certificate", button:has-text("New Certificate"), button:has-text("New Let\'s Encrypt")')
        if await le_action.count() > 0:
            print("Clicking New Certificate action...")
            await le_action.first.click()
            await asyncio.sleep(1)

            # Click Create and Install
            install_btn = page.locator('button:has-text("Create and Install"), button:has-text("Install"), button[type="submit"]:has-text("Create")')
            if await install_btn.count() > 0:
                print("Installing Let's Encrypt certificate...")
                await install_btn.first.click()
                await asyncio.sleep(10)
                print("Installation requested!")

        await page.screenshot(path="ssl_installed.png")
        print("Saved screenshot to ssl_installed.png")

        await browser.close()

asyncio.run(install_ssl())
