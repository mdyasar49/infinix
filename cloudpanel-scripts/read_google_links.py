import asyncio
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

DRIVE_URL = "https://drive.google.com/drive/folders/1KySxmIbc5Kcw9hksmnzX0s6r5IDBJozv"
SCRIPT_URL = "https://script.google.com/u/0/home/projects/1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p/edit?aaac=true&pli=1&pageId=none"

async def main():
    async with async_playwright() as p:
        # Launch Chromium
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await ctx.new_page()

        print("[1] Opening Google Drive Folder...")
        await page.goto(DRIVE_URL, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)
        drive_title = await page.title()
        print(f"Drive Page Title: {drive_title}")
        print(f"Drive URL: {page.url}")
        
        # Check text content on drive
        drive_text = await page.evaluate('''() => {
            return document.body.innerText;
        }''')
        print(f"Drive Text Preview:\n{drive_text[:1000]}")
        await page.screenshot(path="drive_folder_view.png")

        print("\n[2] Opening Google Apps Script...")
        await page.goto(SCRIPT_URL, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)
        script_title = await page.title()
        print(f"Script Page Title: {script_title}")
        print(f"Script URL: {page.url}")
        
        script_text = await page.evaluate('''() => {
            return document.body.innerText;
        }''')
        print(f"Script Text Preview:\n{script_text[:1000]}")
        await page.screenshot(path="script_view.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
