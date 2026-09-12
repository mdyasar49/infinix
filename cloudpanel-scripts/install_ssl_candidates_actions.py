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

        # Click Actions button
        print("[3] Clicking Actions dropdown...")
        actions_btn = page.locator('button:has-text("Actions")')
        await actions_btn.click()
        await asyncio.sleep(1)
        await page.screenshot(path="d:/infonix/cert_actions_clicked.png")

        # Click New Let's Encrypt Certificate
        print("[4] Clicking New Let's Encrypt Certificate...")
        le_item = page.locator('text="New Let\'s Encrypt Certificate", text="New Certificate", a:has-text("Let\'s Encrypt"), div:has-text("Let\'s Encrypt")')
        await le_item.first.click()
        await asyncio.sleep(2)
        await page.screenshot(path="d:/infonix/cert_modal.png")

        # Click Create and Install
        print("[5] Submitting installation...")
        install_btn = page.locator('button:has-text("Create and Install"), button:has-text("Create"), button[type="submit"]')
        await install_btn.first.click()
        print("Waiting 15s for certificate generation...")
        await asyncio.sleep(15)

        await page.screenshot(path="d:/infonix/cert_final.png")
        print("Finished!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(install_ssl())
