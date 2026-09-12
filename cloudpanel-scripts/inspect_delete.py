import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"
OLD_DOMAIN = "onboarding.infogenx.com"

async def inspect_delete():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        print("1. Logging in...")
        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        print("2. Navigating to settings...")
        await page.goto(f"https://cp.infogenx.com/site/{OLD_DOMAIN}/settings", wait_until="networkidle")
        await asyncio.sleep(2)

        # Print all inputs and buttons on page
        inputs = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('input, button')).map(el => ({
                tag: el.tagName,
                type: el.type,
                name: el.name,
                id: el.id,
                text: el.innerText || el.value,
                disabled: el.disabled
            }));
        }''')
        print("Elements on settings page:")
        for inp in inputs:
            print(" ", inp)

        await page.screenshot(path="delete_modal_debug.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_delete())
