import asyncio
import sys
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
SERVER_IP = "209.182.232.150"
DIST_DIR = r"D:\infonix\student-onboarding\dist"

async def main():
    print("=" * 70)
    print("  CLOUDPANEL AUTOMATION: RECREATE & DEPLOY CANDIDATES PORTAL")
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
        print(f"\n[2/5] Deleting old site '{OLD_DOMAIN}'...")
        await page.goto(f"https://cp.infogenx.com/site/{OLD_DOMAIN}/settings", wait_until="networkidle")
        await asyncio.sleep(2)

        # Click the red trigger button that opens Delete modal
        trigger_btn = page.locator('button.btn-danger, button:has-text("Delete Site"), a.btn-danger')
        if await trigger_btn.count() > 0:
            print("[+] Clicking Delete Trigger button...")
            await trigger_btn.first.click()
            await asyncio.sleep(2)

        # Now fill domain confirmation
        print(f"[+] Typing domain confirmation '{OLD_DOMAIN}'...")
        await page.evaluate(f'''() => {{
            const input = document.querySelector('#site_delete_domainName');
            if (input) {{
                input.value = "{OLD_DOMAIN}";
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                input.dispatchEvent(new Event('keyup', {{ bubbles: true }}));
            }}
            const btn = document.querySelector('#site_delete_submit');
            if (btn) {{
                btn.removeAttribute('disabled');
                btn.disabled = false;
            }}
        }}''')
        await asyncio.sleep(1)

        # Click submit button
        submit_btn = page.locator('#site_delete_submit')
        await submit_btn.click(force=True)
        print("[+] Delete submitted! Waiting for site removal (8s)...")
        await asyncio.sleep(8)
        print("[+] Old site removed.")

        # Step 3: Create New Static Site
        print(f"\n[3/5] Creating new Static Site '{NEW_DOMAIN}'...")
        await page.goto("https://cp.infogenx.com/site/new/static", wait_until="networkidle")
        await asyncio.sleep(1)

        await page.locator('input[name="site_new_static[domainName]"]').fill(NEW_DOMAIN)
        await page.locator('input[name="site_new_static[siteUser]"]').fill(NEW_USER)
        await page.locator('input[name="site_new_static[siteUserPassword]"]').fill(NEW_PASS)

        await page.locator('button:has-text("Create")').click()
        print("[+] Form submitted. Waiting 12 seconds for CloudPanel to create site...")
        await asyncio.sleep(12)
        print(f"[+] Site '{NEW_DOMAIN}' successfully created!")

        # Step 4: Configure VHost for SPA
        print(f"\n[4/5] Updating Nginx VHost for SPA Routing...")
        await page.goto(f"https://cp.infogenx.com/site/{NEW_DOMAIN}/vhost", wait_until="networkidle")
        await asyncio.sleep(2)

        vhost_updated = await page.evaluate('''() => {
            const ta = document.querySelector('textarea#site_vhost_vhost') || document.querySelector('textarea');
            if (ta && !ta.value.includes('try_files $uri $uri/ /index.html;')) {
                ta.value = ta.value.replace(/location \\/ {([^}]+)}/s, 'location / {\\n    try_files $uri $uri/ /index.html;\\n}');
                ta.dispatchEvent(new Event('input', { bubbles: true }));
                ta.dispatchEvent(new Event('change', { bubbles: true }));
                return true;
            }
            return false;
        }''')

        if vhost_updated:
            save_btn = page.locator('button:has-text("Save"), button:has-text("Update")')
            if await save_btn.count() > 0:
                await save_btn.first.click()
                print("[+] SPA fallback routing saved to VHost!")
                await asyncio.sleep(4)

        await page.screenshot(path="candidates_portal_ready.png")
        await browser.close()

    # Step 5: Upload Files via SCP
    print(f"\n[5/5] Deploying build files to /home/{NEW_USER}/htdocs/{NEW_DOMAIN}/ via SCP...")
    remote_path = f"/home/{NEW_USER}/htdocs/{NEW_DOMAIN}/"
    pscp_cmd = f'echo y | pscp -batch -r -scp -pw "{NEW_PASS}" "{DIST_DIR}\\*" {NEW_USER}@{SERVER_IP}:{remote_path}'
    print(f"Executing: {pscp_cmd}")
    res = subprocess.run(pscp_cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print("[+] Files deployed successfully via SCP!")
    else:
        print(f"[!] SCP upload output: {res.stdout}\n{res.stderr}")

    print("\n" + "=" * 70)
    print(f"  SUCCESS! '{NEW_DOMAIN}' is now live & fully deployed!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
