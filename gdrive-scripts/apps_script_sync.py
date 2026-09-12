import asyncio
import sys
import json
import os
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SOURCE_ID = "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"
DEST1_ID = "1gBRtVeDLmPOU6M0NIqwNeUuPAvXcsp3nM8CkCYBcnt7reaIio2WPyBig"
DEST2_ID = "1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww"

SOURCE_URL = f"https://script.google.com/home/projects/{SOURCE_ID}/edit"
DEST1_URL = f"https://script.google.com/d/{DEST1_ID}/edit"
DEST2_URL = f"https://script.google.com/d/{DEST2_ID}/edit"

async def inspect():
    async with async_playwright() as p:
        # Launch browser with temp profile or standard chromium
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print(f"[1] Navigating to source project: {SOURCE_URL}")
        await page.goto(SOURCE_URL, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(5)

        title = await page.title()
        url = page.url
        print(f"Page Title: {title}")
        print(f"Current URL: {url}")

        text = await page.evaluate("() => document.body.innerText")
        print(f"Body snippet (500 chars):\n{text[:500]}")

        await page.screenshot(path="d:/infonix/source_script_screenshot.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect())
