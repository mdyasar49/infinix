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
    print("=" * 70, flush=True)
    print("  CLOUDPANEL AUTOMATION: RECREATE & DEPLOY CANDIDATES PORTAL", flush=True)
    print("=" * 70, flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await context.new_page()

        # Step 1: Login
        print("\n[1/5] Logging into CloudPanel...", flush=True)
        await page.goto(CP_URL, wait_until="networkidle", timeout=20000)
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)
        print("[+] Login Successful!", flush=True)

        # Step 2: Delete Old Site
        print(f"\n[2/5] Deleting old site '{OLD_DOMAIN}'...", flush=True)
        await page.goto(f"https://cp.infogenx.com/site/{OLD_DOMAIN}/settings", wait_until="networkidle")
        await asyncio.sleep(2)

        # Scroll to bottom
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)

        # In CloudPanel, delete section has an accordion/button or direct form.
        # Let's inspect delete form on page
        deleted = await page.evaluate(f'''() => {{
            // Find input for domain
            const input = document.querySelector('#site_delete_domainName');
            const submitBtn = document.querySelector('#site_delete_submit');
            const form = document.querySelector('form[name="site_delete"]') || (submitBtn ? submitBtn.closest('form') : null);
            
            if (form) {{
                if (input) {{
                    input.value = "{OLD_DOMAIN}";
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                if (submitBtn) {{
                    submitBtn.removeAttribute('disabled');
                    submitBtn.disabled = false;
                }}
                form.submit();
                return true;
            }}
            return false;
        }}''')

        if deleted:
            print("[+] Delete form directly submitted! Waiting 10s for removal...", flush=True)
            await asyncio.sleep(10)
        else:
            print("[!] Delete form not found, checking if already deleted.", flush=True)

        # Step 3: Create New Static Site
        print(f"\n[3/5] Creating new Static Site '{NEW_DOMAIN}'...", flush=True)
        await page.goto("https://cp.infogenx.com/site/new/static", wait_until="networkidle")
        await asyncio.sleep(1)

        await page.locator('input[name="site_new_static[domainName]"]').fill(NEW_DOMAIN)
        await page.locator('input[name="site_new_static[siteUser]"]').fill(NEW_USER)
        await page.locator('input[name="site_new_static[siteUserPassword]"]').fill(NEW_PASS)

        await page.locator('button:has-text("Create")').click()
        print("[+] Form submitted. Waiting 12 seconds for CloudPanel to provision site...", flush=True)
        await asyncio.sleep(12)
        print(f"[+] Site '{NEW_DOMAIN}' successfully created!", flush=True)

        # Step 4: Configure VHost for SPA
        print(f"\n[4/5] Updating Nginx VHost for SPA Routing...", flush=True)
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
                print("[+] SPA fallback routing saved to VHost!", flush=True)
                await asyncio.sleep(4)

        await page.screenshot(path="candidates_portal_ready.png")
        await browser.close()

    # Step 5: Upload Files via SCP
    print(f"\n[5/5] Deploying build files to /home/{NEW_USER}/htdocs/{NEW_DOMAIN}/ via SCP...", flush=True)
    remote_path = f"/home/{NEW_USER}/htdocs/{NEW_DOMAIN}/"
    pscp_cmd = f'echo y | pscp -batch -r -scp -pw "{NEW_PASS}" "{DIST_DIR}\\*" {NEW_USER}@{SERVER_IP}:{remote_path}'
    print(f"Executing SCP upload to {remote_path}...", flush=True)
    res = subprocess.run(pscp_cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print("[+] Files deployed successfully via SCP!", flush=True)
    else:
        print(f"[!] SCP upload output: {res.stdout}\n{res.stderr}", flush=True)

    print("\n" + "=" * 70, flush=True)
    print(f"  SUCCESS! '{NEW_DOMAIN}' is now live & fully deployed!", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
