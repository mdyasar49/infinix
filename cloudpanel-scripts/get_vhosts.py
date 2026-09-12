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

        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        for site in ["blogadmin.infogenx.com", "dev.infogenx.com"]:
            await page.goto(f"https://cp.infogenx.com/site/{site}/vhost", wait_until="networkidle")
            await asyncio.sleep(2)
            vhost_text = await page.evaluate('''() => {
                if (window.monaco && monaco.editor && monaco.editor.getModels().length > 0) {
                    return monaco.editor.getModels()[0].getValue();
                }
                const cm = document.querySelector('.CodeMirror');
                if (cm && cm.CodeMirror) {
                    return cm.CodeMirror.getValue();
                }
                const ta = document.querySelector('textarea');
                if (ta) return ta.value;
                const viewLines = document.querySelector('.view-lines');
                if (viewLines) return viewLines.innerText;
                return document.body.innerText;
            }''')
            print(f"=== {site} VHOST ===", flush=True)
            print(vhost_text, flush=True)
            print("=" * 60, flush=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
