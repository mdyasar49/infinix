import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

async def list_all_sites():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(ignore_https_errors=True)

        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        site_links = await page.locator('a[href^="/site/"]').all()
        print(f"Total existing sites: {len(site_links)}")
        for sl in site_links:
            txt = (await sl.inner_text()).strip()
            href = await sl.get_attribute("href")
            if href != "/site/new" and txt:
                print(f"  - Site: {txt} ({href})")

        # Let's inspect the /site/new/nodejs and /site/new/static forms
        await page.goto("https://cp.infogenx.com/site/new/nodejs", wait_until="networkidle")
        print("\n--- Form fields on /site/new/nodejs ---")
        inputs = await page.locator("input, select").all()
        for inp in inputs:
            name = await inp.get_attribute("name")
            typ = await inp.get_attribute("type")
            placeholder = await inp.get_attribute("placeholder")
            print(f"  - input name={name}, type={typ}, placeholder={placeholder}")

        await page.goto("https://cp.infogenx.com/site/new/static", wait_until="networkidle")
        print("\n--- Form fields on /site/new/static ---")
        inputs = await page.locator("input, select").all()
        for inp in inputs:
            name = await inp.get_attribute("name")
            typ = await inp.get_attribute("type")
            placeholder = await inp.get_attribute("placeholder")
            print(f"  - input name={name}, type={typ}, placeholder={placeholder}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(list_all_sites())
