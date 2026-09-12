import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await ctx.new_page()

        print("[1] Logging in...", flush=True)
        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        print("[2] Reading sites table...", flush=True)
        rows = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('tr')).map(r => r.innerText.replace(/\\s+/g, ' ').trim());
        }''')
        
        for r in rows:
            print("  ", r, flush=True)

        await page.screenshot(path="D:\\infonix\\sites_current_view.png")
        print("[3] Screenshot saved to D:\\infonix\\sites_current_view.png", flush=True)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
