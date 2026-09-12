import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_URL = "https://script.google.com/u/0/home/projects/1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p/edit?aaac=true&pli=1&pageId=none"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()

        print("[1] Opening Google Apps Script...")
        await page.goto(SCRIPT_URL, wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(5)
        
        print("Page URL:", page.url)
        print("Page Title:", await page.title())
        
        text = await page.evaluate('''() => {
            return document.body.innerText;
        }''')
        print(f"\n--- SCRIPT PAGE TEXT PREVIEW ---\n{text[:2000]}")
        await page.screenshot(path="D:\\infonix\\script_page_view.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
