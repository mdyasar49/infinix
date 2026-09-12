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

OLD_DOMAIN = "onboarding.infogenx.com"
NEW_DOMAIN = "candidates.infogenx.com"
NEW_USER = "infogenx-candidates"
NEW_PASS = "infogenx@1234"

async def recreate():
    print("=" * 70)
    print("  CLOUDPANEL AUTOMATION: DELETE OLD & CREATE NEW SITE")
    print("=" * 70)
    print(f"Old Site to Delete : {OLD_DOMAIN}")
    print(f"New Site to Create : {NEW_DOMAIN}")
    print(f"New Site User      : {NEW_USER}")
    print("=" * 70)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        # Step 1: Login
        print("\n[1/5] Logging into CloudPanel...")
        await page.goto(CP_URL, wait_until="networkidle", timeout=20000)
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)
        print("[+] Login Successful!")

        # Step 2: Delete Old Site
        print(f"\n[2/5] Navigating to '{OLD_DOMAIN}' settings to delete...")
        await page.goto(f"https://cp.infogenx.com/site/{OLD_DOMAIN}/settings", wait_until="networkidle")
        await asyncio.sleep(2)

        # Look for Delete Site button
        delete_btn = page.locator('button:has-text("Delete Site"), button:has-text("Delete"), a:has-text("Delete")')
        if await delete_btn.count() > 0:
            print("[+] Found Delete button, clicking...")
            await delete_btn.first.click()
            await asyncio.sleep(2)

            # Confirm modal if any
            confirm_input = page.locator('input[type="text"]')
            if await confirm_input.count() > 0:
                await confirm_input.last.fill(OLD_DOMAIN)
                await asyncio.sleep(1)

            confirm_btn = page.locator('button:has-text("Confirm"), button:has-text("Delete"), button.btn-danger, button[type="submit"]')
            if await confirm_btn.count() > 0:
                await confirm_btn.last.click()
                print("[+] Confirmed deletion. Waiting 6 seconds...")
                await asyncio.sleep(6)
        else:
            print("[-] Delete button not directly found on settings page, checking screenshot.")
            await page.screenshot(path="delete_site_page.png")

        # Step 3: Create New Static Site
        print(f"\n[3/5] Navigating to Create Static Site for '{NEW_DOMAIN}'...")
        await page.goto("https://cp.infogenx.com/site/new/static", wait_until="networkidle")
        await asyncio.sleep(1)

        domain_input = page.locator('input[name="site_new_static[domainName]"]')
        await domain_input.fill(NEW_DOMAIN)

        user_input = page.locator('input[name="site_new_static[siteUser]"]')
        await user_input.fill(NEW_USER)

        pass_input = page.locator('input[name="site_new_static[siteUserPassword]"]')
        await pass_input.fill(NEW_PASS)

        print("[+] Form filled. Submitting creation...")
        create_btn = page.locator('button:has-text("Create")')
        await create_btn.click()

        print("[+] Waiting for site creation to complete (10s)...")
        await asyncio.sleep(10)

        # Step 4: Configure Vhost
        print(f"\n[4/5] Updating Nginx Vhost for SPA Routing on '{NEW_DOMAIN}'...")
        await page.goto(f"https://cp.infogenx.com/site/{NEW_DOMAIN}/vhost", wait_until="networkidle")
        await asyncio.sleep(2)

        vhost_editor = page.locator('textarea, .monaco-editor, .cm-editor, #site_vhost_vhost, textarea[name*="vhost"]')
        if await vhost_editor.count() > 0:
            current_vhost = await page.evaluate('''() => {
                const ta = document.querySelector('textarea');
                if (ta) return ta.value;
                return "";
            }''')
            if "try_files" not in current_vhost:
                print("[+] Patching Vhost with SPA routing (try_files $uri $uri/ /index.html;)...")
                # Update textarea if present
                await page.evaluate('''() => {
                    const ta = document.querySelector('textarea');
                    if (ta && !ta.value.includes('try_files $uri $uri/ /index.html;')) {
                        ta.value = ta.value.replace(/location \\/ {([^}]+)}/s, 'location / {\\n    try_files $uri $uri/ /index.html;\\n}');
                        ta.dispatchEvent(new Event('input', { bubbles: true }));
                        ta.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }''')
                save_btn = page.locator('button:has-text("Save"), button:has-text("Update")')
                if await save_btn.count() > 0:
                    await save_btn.first.click()
                    await asyncio.sleep(3)

        await page.screenshot(path="new_site_status.png")
        print("[+] Headless CloudPanel operations completed!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(recreate())
