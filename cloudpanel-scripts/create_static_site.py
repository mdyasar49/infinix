import asyncio
import sys
import os
import subprocess
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

TARGET_DOMAIN = "onboarding.infogenx.com"
SITE_USER = "infogenx-onboarding"
SITE_PASS = "infogenx@1234"

async def create_site():
    print("=" * 70)
    print("  CLOUDPANEL AUTOMATED SITE CREATION & DEPLOYMENT")
    print("=" * 70)
    print(f"Target Domain  : {TARGET_DOMAIN}")
    print(f"Site Username  : {SITE_USER}")
    print(f"Site Password  : {SITE_PASS}")
    print("=" * 70)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        # Step 1: Login
        print("\n[1/4] Logging into CloudPanel (https://cp.infogenx.com)...")
        await page.goto(CP_URL, wait_until="networkidle", timeout=20000)
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)
        print("[+] Login Successful!")

        # Step 2: Navigate to Create Static HTML Site
        print(f"\n[2/4] Navigating to Create Static HTML Site...")
        await page.goto("https://cp.infogenx.com/site/new/static", wait_until="networkidle")
        await asyncio.sleep(1)

        # Step 3: Fill Form
        print(f"[3/4] Submitting Site Creation Form for '{TARGET_DOMAIN}'...")
        domain_input = page.locator('input[name="site_new_static[domainName]"]')
        await domain_input.fill(TARGET_DOMAIN)

        # Fill Site User and Password
        user_input = page.locator('input[name="site_new_static[siteUser]"]')
        await user_input.fill(SITE_USER)

        pass_input = page.locator('input[name="site_new_static[siteUserPassword]"]')
        await pass_input.fill(SITE_PASS)

        await page.screenshot(path="site_form_filled.png")
        print("[+] Form filled. Clicking 'Create' button...")

        # Click Create
        create_btn = page.locator('button:has-text("Create")')
        await create_btn.click()

        # Wait for site creation processing
        print("Waiting for CloudPanel to provision Nginx vhost, directories, and user...")
        await asyncio.sleep(8)

        # Check for success
        await page.screenshot(path="site_created_result.png")
        print(f"[+] Current URL after creation: {page.url}")

        # Check if site created or if already exists
        if TARGET_DOMAIN in page.url or "site" in page.url:
            print(f"[+] Site '{TARGET_DOMAIN}' created successfully on CloudPanel!")
        else:
            err = page.locator('.alert-danger, .error, [class*="error"]')
            if await err.count() > 0:
                print(f"[-] Status: {await err.first.inner_text()}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(create_site())
