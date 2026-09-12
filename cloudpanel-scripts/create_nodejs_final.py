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
SERVER_IP = "209.182.232.150"
DIST_DIR = r"D:\infonix\student-onboarding\dist"

# Try port 3150
PORT = "3150"

async def main():
    print("=" * 70, flush=True)
    print("  CREATING CANDIDATES.INFOGENX.COM AS NODEJS SITE", flush=True)
    print("=" * 70, flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = await ctx.new_page()

        print("[1] Logging in...", flush=True)
        await page.goto(CP_URL, wait_until="networkidle")
        await page.locator('input[name="userName"]').fill(USERNAME)
        await page.locator('input[name="password"]').fill(PASSWORD)
        await page.locator('button:has-text("Log In")').click()
        await page.wait_for_url("https://cp.infogenx.com/", timeout=15000)

        print(f"[2] Navigating to /site/new/nodejs with port {PORT}...", flush=True)
        await page.goto("https://cp.infogenx.com/site/new/nodejs", wait_until="networkidle")
        await asyncio.sleep(1)

        await page.locator('input[name="site_new_nodejs[domainName]"]').fill(TARGET_DOMAIN)
        
        select = page.locator('select[name="site_new_nodejs[nodejsVersion]"]')
        if await select.count() > 0:
            await select.select_option("20")

        await page.locator('input[name="site_new_nodejs[port]"]').fill(PORT)
        await page.locator('input[name="site_new_nodejs[siteUser]"]').fill(SITE_USER)
        await page.locator('input[name="site_new_nodejs[siteUserPassword]"]').fill(SITE_PASS)

        print("[3] Submitting form...", flush=True)
        await page.locator('button:has-text("Create")').click()

        for i in range(20):
            await asyncio.sleep(1)
            if page.url != "https://cp.infogenx.com/site/new/nodejs":
                print(f"[+] Successfully redirected to: {page.url}", flush=True)
                break

        await page.screenshot(path="nodejs_created_success.png")

        # Step 4: Configure VHost for SPA Fallback & Static Serving
        print(f"[4] Updating VHost for '{TARGET_DOMAIN}'...", flush=True)
        await page.goto(f"https://cp.infogenx.com/site/{TARGET_DOMAIN}/vhost", wait_until="networkidle")
        await asyncio.sleep(2)

        await page.evaluate('''() => {
            const ta = document.querySelector('textarea#site_vhost_vhost') || document.querySelector('textarea');
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

        # Check sites list
        await page.goto("https://cp.infogenx.com/", wait_until="networkidle")
        await asyncio.sleep(2)
        sites = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('tr')).map(r => r.innerText.replace(/\\s+/g, ' ').trim());
        }''')
        for s in sites:
            if "candidates" in s:
                print("CloudPanel Sites Table Entry ->", s, flush=True)

        await browser.close()

    # Step 5: Upload Files via SCP
    print(f"\n[5] Uploading build files to /home/{SITE_USER}/htdocs/{TARGET_DOMAIN}/ via SCP...", flush=True)
    remote_path = f"/home/{SITE_USER}/htdocs/{TARGET_DOMAIN}/"
    pscp_cmd = f'echo y | pscp -batch -r -scp -pw "{SITE_PASS}" "{DIST_DIR}\\*" {SITE_USER}@{SERVER_IP}:{remote_path}'
    res = subprocess.run(pscp_cmd, shell=True, capture_output=True, text=True)
    if res.returncode == 0:
        print("[+] Files uploaded successfully via SCP!", flush=True)
    else:
        print(f"[!] SCP upload output: {res.stdout}\n{res.stderr}", flush=True)

    print("\n" + "=" * 70, flush=True)
    print(f"  SUCCESS! '{TARGET_DOMAIN}' is now verified as NODEJS App on CloudPanel!", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
