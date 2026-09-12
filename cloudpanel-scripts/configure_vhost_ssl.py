import asyncio
import sys
import os
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"
DOMAIN = "onboarding.infogenx.com"

async def configure_vhost_and_ssl():
    print("=" * 70)
    print(f"  CONFIGURING PROFESSIONAL NGINX VHOST & SSL FOR {DOMAIN}")
    print("=" * 70)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        # Login
        print("\n[1/3] Logging into CloudPanel (headless)...")
        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)
        print("[+] Logged in successfully!")

        # 2. Check and configure Vhost for React SPA (try_files $uri $uri/ /index.html;)
        print(f"\n[2/3] Checking Nginx Vhost for React SPA routing...")
        await page.goto(f"https://cp.infogenx.com/site/{DOMAIN}/vhost", wait_until="networkidle")
        await asyncio.sleep(2)

        # Get current vhost text
        vhost_editor = page.locator('.ace_text-input, textarea, [class*="ace_editor"]')
        editor_text = await page.locator('.ace_content').inner_text()
        print("[+] Current Vhost snippet:")
        print(editor_text[:400] + "...")

        # 3. Check and install SSL
        print(f"\n[3/3] Setting up SSL Certificate on https://cp.infogenx.com/site/{DOMAIN}/certificates...")
        await page.goto(f"https://cp.infogenx.com/site/{DOMAIN}/certificates", wait_until="networkidle")
        await asyncio.sleep(2)

        # Click Actions -> New Let's Encrypt Certificate if available
        new_cert_btn = page.locator('button:has-text("New Let\'s Encrypt Certificate"), a:has-text("New Let\'s Encrypt"), button:has-text("New Certificate"), button:has-text("Actions")')
        if await new_cert_btn.count() > 0:
            print("[+] Clicking New Certificate button...")
            await new_cert_btn.first.click()
            await asyncio.sleep(2)

            create_install_btn = page.locator('button:has-text("Create and Install"), button:has-text("Install"), button[type="submit"]:has-text("Create")')
            if await create_install_btn.count() > 0:
                print("[+] Requesting Let's Encrypt SSL installation...")
                await create_install_btn.first.click()
                await asyncio.sleep(10)

        await page.screenshot(path="cloudpanel_site_final_verified.png")
        print("[+] Final screenshot saved to cloudpanel_site_final_verified.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(configure_vhost_and_ssl())
