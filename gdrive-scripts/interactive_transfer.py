import asyncio
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SOURCE_ID = "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"
TARGET_ID = "1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww"

SOURCE_URL = f"https://script.google.com/home/projects/{SOURCE_ID}/edit"
TARGET_URL = f"https://script.google.com/u/2/home/projects/{TARGET_ID}/edit"

OUTPUT_DIR = Path(__file__).parent / "extracted_project" / SOURCE_ID
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    async with async_playwright() as p:
        print("[*] Launching Chromium browser (visible mode)...")
        # Launch non-headless browser so user can see or login if needed
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        print(f"[*] Navigating to Source Project:\n    {SOURCE_URL}")
        await page.goto(SOURCE_URL)

        print("[*] Waiting for Google Apps Script editor to load...")
        print("[*] (If login is required, please log in in the opened browser window)")

        # Wait up to 60 seconds for editor elements to appear
        for i in range(12):
            await asyncio.sleep(5)
            title = await page.title()
            url = page.url
            print(f"[{i*5}s] Title: {title} | URL: {url}")
            if "Apps Script" in title and "developers.google.com" not in url:
                print("[+] Apps Script Editor detected!")
                break

        await page.screenshot(path="d:/infonix/source_editor.png")
        print("[+] Screenshot saved to d:/infonix/source_editor.png")

        # Keep open briefly
        await asyncio.sleep(5)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
