import asyncio
import sys
import subprocess
from playwright.async_api import async_playwright

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CP_URL = "https://cp.infogenx.com/login"
USERNAME = "infogenxsrv"
PASSWORD = "X5OyrnBy7XOkRTZ83Ima"

TARGET_DOMAIN = "candidates.infogenx.com"
SITE_USER = "infogenx-candidates"
SITE_PASS = "infogenx@1234"
NODE_VERSION = "20"
PORT = "3000"
SERVER_IP = "209.182.232.150"
DIST_DIR = r"D:\infonix\student-onboarding\dist"

async def main():
    print("=" * 70, flush=True)
    print("  CLOUDPANEL: RE-PROVISIONING CANDIDATES PORTAL AS NODEJS APP", flush=True)
    print("=" * 70, flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await ctx.new_page()

        # Step 1: Login
        print("[1/4] Logging into CloudPanel...", flush=True)
        await page.goto(CP_URL, wait_until="networkidle", timeout=20000)
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)
        print("[+] Login Successful!", flush=True)

        # Step 2: Delete Existing Static Site
        print(f"[2/4] Deleting existing '{TARGET_DOMAIN}'...", flush=True)
        await page.goto(f"https://cp.infogenx.com/site/{TARGET_DOMAIN}/settings", wait_until="networkidle")
        await asyncio.sleep(2)

        deleted = await page.evaluate(f'''() => {{
            const input = document.querySelector('#site_delete_domainName');
            const submitBtn = document.querySelector('#site_delete_submit');
            const form = document.querySelector('form[name="site_delete"]') || (submitBtn ? submitBtn.closest('form') : null);
            
            if (form) {{
                if (input) {{
                    input.value = "{TARGET_DOMAIN}";
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
            print("[+] Delete submitted. Waiting 10s for removal...", flush=True)
            await asyncio.sleep(10)

        # Step 3: Create Site as NODEJS
        print(f"[3/4] Creating '{TARGET_DOMAIN}' as NODEJS App (v{NODE_VERSION}, port {PORT})...", flush=True)
        await page.goto("https://cp.infogenx.com/site/new/nodejs", wait_until="networkidle")
        await asyncio.sleep(1)

        await page.locator('input[name="site_new_nodejs[domainName]"]').fill(TARGET_DOMAIN)
        
        # Select Node.js version
        node_select = page.locator('select[name="site_new_nodejs[nodejsVersion]"]')
        if await node_select.count() > 0:
            await node_select.select_option(NODE_VERSION)

        await page.locator('input[name="site_new_nodejs[port]"]').fill(PORT)
        await page.locator('input[name="site_new_nodejs[siteUser]"]').fill(SITE_USER)
        await page.locator('input[name="site_new_nodejs[siteUserPassword]"]').fill(SITE_PASS)

        create_btn = page.locator('button:has-text("Create")')
        await create_btn.click()
        print("[+] Submitting Node.js site creation. Waiting 12 seconds...", flush=True)
        await asyncio.sleep(12)
        print(f"[+] Site '{TARGET_DOMAIN}' successfully created as NODEJS!", flush=True)

        # Step 4: Verify Sites Table
        await page.goto("https://cp.infogenx.com/", wait_until="networkidle")
        await asyncio.sleep(2)
        sites_table = await page.evaluate('''() => {
            const rows = Array.from(document.querySelectorAll('tr'));
            return rows.map(r => r.innerText.replace(/\\s+/g, ' ').trim()).filter(t => t.includes('candidates.infogenx.com'));
        }''')
        print(f"[+] Sites table verification: {sites_table}", flush=True)

        await page.screenshot(path="candidates_nodejs_ready.png")
        await browser.close()

    # Step 5: Upload Files via SCP
    print(f"\n[4/4] Uploading build files to /home/{SITE_USER}/htdocs/{TARGET_DOMAIN}/ via SCP...", flush=True)
    remote_path = f"/home/{SITE_USER}/htdocs/{TARGET_DOMAIN}/"
    pscp_cmd = f'echo y | pscp -batch -r -scp -pw "{SITE_PASS}" "{DIST_DIR}\\*" {SITE_USER}@{SERVER_IP}:{remote_path}'
    res = subprocess.run(pscp_cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print("[+] Files uploaded successfully via SCP!", flush=True)
    else:
        print(f"[!] SCP upload output: {res.stdout}\n{res.stderr}", flush=True)

    print("\n" + "=" * 70, flush=True)
    print(f"  SUCCESS! '{TARGET_DOMAIN}' is now configured as NODEJS on CloudPanel!", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
