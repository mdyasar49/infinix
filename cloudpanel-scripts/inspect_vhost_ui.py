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

        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        await page.goto("https://cp.infogenx.com/site/blogadmin.infogenx.com/vhost", wait_until="networkidle")
        await asyncio.sleep(3)
        await page.screenshot(path="D:\\infonix\\blogadmin_vhost_screen.png")

        content = await page.evaluate('''() => {
            const lines = Array.from(document.querySelectorAll('.view-line, .view-lines, pre, code, textarea')).map(e => e.innerText || e.value);
            return lines.filter(t => t && t.trim().length > 0);
        }''')
        print("Lines found in editor:")
        for l in content:
            print(l)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
