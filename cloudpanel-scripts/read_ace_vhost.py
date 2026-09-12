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
        ctx = await browser.new_context(viewport={"width": 1440, "height": 1000}, ignore_https_errors=True)
        page = await ctx.new_page()

        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        await page.goto("https://cp.infogenx.com/site/blogadmin.infogenx.com/vhost", wait_until="networkidle")
        await asyncio.sleep(2)

        # In CloudPanel v2.5.4 (Ace Editor or Monaco)
        vhost_text = await page.evaluate('''() => {
            // Check Ace Editor
            if (window.ace) {
                const editor = ace.edit(document.querySelector('.ace_editor'));
                if (editor) return editor.getValue();
            }
            // Check Monaco
            const lines = Array.from(document.querySelectorAll('.view-line')).map(l => l.innerText);
            if (lines.length > 0) return lines.join('\\n');
            
            // Check if hidden input / textarea exists
            const hidden = document.querySelector('input[name*="vhost"], textarea[name*="vhost"]');
            if (hidden) return hidden.value;
            return "Not found";
        }''')

        print("=== blogadmin.infogenx.com FULL VHOST ===")
        print(vhost_text)

        await page.screenshot(path="D:\\infonix\\blogadmin_vhost_full.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
