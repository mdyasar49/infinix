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
        ctx = await browser.new_context(ignore_https_errors=True)
        page = await ctx.new_page()

        print("[1] Logging in...", flush=True)
        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        for site in ["blogadmin.infogenx.com", "dev.infogenx.com"]:
            await page.goto(f"https://cp.infogenx.com/site/{site}/vhost", wait_until="networkidle")
            await asyncio.sleep(2)
            vhost = await page.evaluate('''() => {
                const ta = document.querySelector('textarea#site_vhost_vhost') || document.querySelector('textarea');
                return ta ? ta.value : 'N/A';
            }''')
            print(f"=== {site} VHOST ===", flush=True)
            print(vhost, flush=True)
            print("=" * 50, flush=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
