import asyncio
import sys
from playwright.async_api import async_playwright

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"
LE_URL = "https://cp.infogenx.com/site/candidates.infogenx.com/lets-encrypt-certificate/new"

async def direct_install():
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

        print(f"[2] Navigating directly to {LE_URL}...")
        await page.goto(LE_URL, wait_until="networkidle", timeout=20000)
        await asyncio.sleep(2)
        await page.screenshot(path="d:/infonix/le_form.png")

        print("[3] Clicking Create and Install button...")
        submit_btn = page.locator('button:has-text("Create and Install"), button[type="submit"]')
        if await submit_btn.count() > 0:
            await submit_btn.first.click()
            print("Submitting Let's Encrypt request...")
            await asyncio.sleep(15)

        await page.screenshot(path="d:/infonix/le_done.png")
        print("Completed Let's Encrypt installation!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(direct_install())
