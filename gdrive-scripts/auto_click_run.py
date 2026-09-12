import asyncio
import sys
import os
from pathlib import Path
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_URL = "https://script.google.com/u/2/home/projects/1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww/edit"

async def auto_run_trigger():
    print("[*] Launching Browser for Apps Script Trigger Activation...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--start-maximized"])
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()

        print(f"[*] Navigating to Apps Script Editor: {PROJECT_URL}")
        await page.goto(PROJECT_URL)

        print("[*] Waiting for editor interface to load...")
        await asyncio.sleep(8)

        # Look for run button or function selector
        print(f"[+] Page loaded: {await page.title()}")
        await page.screenshot(path="d:/infonix/apps_script_runner_view.png")

        # Let user see and click or automate click
        print("[*] Browser window is open. Waiting 30 seconds...")
        for i in range(6):
            await asyncio.sleep(5)
            print(f"    - [{ (i+1)*5 }s] Active URL: {page.url}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(auto_run_trigger())
