import asyncio
import sys
from playwright.async_api import async_playwright

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"
SITE_CERT_URL = "https://cp.infogenx.com/site/candidates.infogenx.com/certificates"

async def install_ssl():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(ignore_https_errors=True)

        print("[1] Logging into CloudPanel...")
        await page.goto(CP_URL, wait_until="networkidle", timeout=30000)
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/**", timeout=20000)
        print("Logged in successfully!")

        print(f"[2] Navigating to {SITE_CERT_URL}...")
        await page.goto(SITE_CERT_URL, wait_until="networkidle", timeout=20000)
        await asyncio.sleep(2)
        await page.screenshot(path="d:/infonix/cert_page_before.png")

        # Check if there is "New Let's Encrypt Certificate" or "New Certificate" button
        print("[3] Looking for New Certificate button...")
        btn = page.locator('button:has-text("New Let\'s Encrypt Certificate"), a:has-text("New Let\'s Encrypt Certificate"), button:has-text("New Certificate"), a:has-text("New Certificate")')
        count = await btn.count()
        print(f"Found {count} certificate buttons.")

        if count > 0:
            await btn.first.click()
            await asyncio.sleep(2)
            await page.screenshot(path="d:/infonix/cert_modal.png")

            # Click Create and Install
            install_btn = page.locator('button:has-text("Create and Install"), button:has-text("Install Certificate"), button[type="submit"]')
            if await install_btn.count() > 0:
                print("[4] Submitting Let's Encrypt installation...")
                await install_btn.first.click()
                print("Waiting 15 seconds for Let's Encrypt verification...")
                await asyncio.sleep(15)

        await page.screenshot(path="d:/infonix/cert_page_after.png")
        print("Done! Check cert_page_after.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(install_ssl())
