"""
================================================================================
CloudPanel / cPanel Automated Site Creation Script
================================================================================
Target URL   : https://cp.infogenx.com/login
Mode         : Headless Automation (No visible browser window)
================================================================================
"""

import sys
import os
import asyncio
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"

async def create_cloudpanel_site(username: str, password: str, domain_name: str = "onboarding.infogenx.com"):
    print("=" * 70)
    print("  CLOUDPANEL AUTOMATED SITE CREATION (HEADLESS)")
    print("=" * 70)
    print(f"Panel URL    : {CP_URL}")
    print(f"Username     : {username}")
    print(f"Target Domain: {domain_name}")
    print("=" * 70)

    async with async_playwright() as p:
        # Run completely in the background without opening a browser window
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        try:
            # 1. Login
            print("\n[1/4] Navigating to CloudPanel Login...")
            await page.goto(CP_URL, wait_until="networkidle", timeout=20000)

            print("[2/4] Entering credentials...")
            await page.locator('input[name="userName"]').fill(username)
            await page.locator('input[name="password"]').fill(password)
            await page.locator('button:has-text("Log In")').click()

            await asyncio.sleep(3)

            # Check if login succeeded
            if "/login" in page.url:
                err_el = page.locator('.alert, .error, [class*="error"], [class*="alert"]')
                err_msg = await err_el.first.inner_text() if await err_el.count() > 0 else "Invalid User Name or Password"
                print(f"[-] Login Failed: {err_msg.strip()}")
                await page.screenshot(path="cp_login_failed.png")
                await browser.close()
                return False

            print("[+] Login Successful! Landed on CloudPanel Dashboard.")

            # 2. Navigate to Add Site
            print("\n[3/4] Navigating to Sites -> Add Site...")
            add_site_btn = page.locator('a:has-text("Add Site"), button:has-text("Add Site"), a[href*="add-site"], a[href*="sites/add"]')
            if await add_site_btn.count() > 0:
                await add_site_btn.first.click()
            else:
                await page.goto("https://cp.infogenx.com/sites/add", wait_until="networkidle")

            await asyncio.sleep(2)

            # 3. Choose Static HTML Site / Node.js
            print(f"[4/4] Creating Site for domain: {domain_name}...")
            static_site_card = page.locator('text="Static HTML Site", text="HTML Site", a:has-text("Static HTML")')
            if await static_site_card.count() > 0:
                await static_site_card.first.click()
                await asyncio.sleep(1)

            # Fill domain name
            domain_input = page.locator('input[name="domainName"], input[name="domain"], input[placeholder*="domain" i]').first
            await domain_input.fill(domain_name)

            # Submit Site creation
            create_btn = page.locator('button:has-text("Create"), button[type="submit"]:has-text("Add Site")')
            await create_btn.click()

            # Wait for creation to complete
            await asyncio.sleep(5)

            proof_screenshot = os.path.abspath("cloudpanel_site_created.png")
            await page.screenshot(path=proof_screenshot, full_page=True)
            print(f"[+] Site Created Successfully! Verification screenshot saved: {proof_screenshot}")

            await browser.close()
            return True

        except Exception as e:
            print(f"[-] Error during site creation: {e}")
            await page.screenshot(path="cloudpanel_error.png")
            await browser.close()
            return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python create_site_cloudpanel.py <USERNAME> <PASSWORD> [DOMAIN_NAME]")
        print("Example:")
        print("  python create_site_cloudpanel.py admin MySecurePass123 onboarding.infogenx.com")
        sys.exit(1)

    user = sys.argv[1]
    pwd = sys.argv[2]
    domain = sys.argv[3] if len(sys.argv) > 3 else "onboarding.infogenx.com"

    asyncio.run(create_cloudpanel_site(user, pwd, domain))
