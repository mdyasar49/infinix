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

        print("[1] Logging in...")
        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        print("[2] Inspecting /site/new/nodejs...")
        await page.goto("https://cp.infogenx.com/site/new/nodejs", wait_until="networkidle")
        await asyncio.sleep(2)

        fields = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('input, select')).map(el => ({
                tag: el.tagName,
                name: el.name,
                id: el.id,
                type: el.type,
                options: el.tagName === 'SELECT' ? Array.from(el.options).map(o => o.value || o.text) : []
            }));
        }''')
        print("Fields on /site/new/nodejs:")
        for f in fields:
            print(" ", f)

        # Check existing ports on other nodejs sites
        for site in ["dev.infogenx.com", "api.infogenx.com", "blogadmin.infogenx.com", "voice.infogenx.com"]:
            await page.goto(f"https://cp.infogenx.com/site/{site}/nodejs", wait_until="networkidle")
            await asyncio.sleep(1)
            port_val = await page.evaluate('''() => {
                const portInput = document.querySelector('input[name*="port"], #site_nodejs_port');
                const nodeVer = document.querySelector('select[name*="nodejsVersion"], #site_nodejs_nodejsVersion');
                return {
                    port: portInput ? portInput.value : 'N/A',
                    nodeVer: nodeVer ? nodeVer.value : 'N/A'
                };
            }''')
            print(f"Site {site}: {port_val}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
