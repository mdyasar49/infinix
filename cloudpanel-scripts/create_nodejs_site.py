import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

TARGET_DOMAIN = "candidates.infogenx.com"
SITE_USER = "infogenx-candidates"
SITE_PASS = "infogenx@1234"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await ctx.new_page()

        print("[1] Logging in...")
        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        print("[2] Navigating to /site/new/nodejs...")
        await page.goto("https://cp.infogenx.com/site/new/nodejs", wait_until="networkidle")
        await asyncio.sleep(1)

        print("[3] Filling Form...")
        await page.locator('input[name="site_new_nodejs[domainName]"]').fill(TARGET_DOMAIN)
        
        # Select Node.js Version 20
        select = page.locator('select[name="site_new_nodejs[nodejsVersion]"]')
        if await select.count() > 0:
            await select.select_option("20")

        await page.locator('input[name="site_new_nodejs[port]"]').fill("3000")
        await page.locator('input[name="site_new_nodejs[siteUser]"]').fill(SITE_USER)
        await page.locator('input[name="site_new_nodejs[siteUserPassword]"]').fill(SITE_PASS)

        await page.screenshot(path="nodejs_form_before_submit.png")

        print("[4] Submitting form...")
        btn = page.locator('button:has-text("Create")')
        await btn.click()

        # Wait up to 25s or until redirected
        print("[5] Waiting for creation completion...")
        for i in range(25):
            await asyncio.sleep(1)
            url = page.url
            if url != "https://cp.infogenx.com/site/new/nodejs":
                print(f"[+] Redirected to: {url}")
                break

        await page.screenshot(path="nodejs_form_after_submit.png")
        
        # Check sites list
        await page.goto("https://cp.infogenx.com/", wait_until="networkidle")
        await asyncio.sleep(2)
        sites = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('tr')).map(r => r.innerText.replace(/\\s+/g, ' ').trim());
        }''')
        print("Sites list match:")
        for s in sites:
            if "candidates" in s:
                print("  ->", s)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
