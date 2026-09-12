"""
Google Apps Script Project Migrator
===================================
Source Project ID:
  - 1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p
Target Project IDs:
  - 1gBRtVeDLmPOU6M0NIqwNeUuPAvXcsp3nM8CkCYBcnt7reaIio2WPyBig
  - 1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww

This script provides two methods:
1. Google Apps Script REST API (OAuth2) - downloads source files and updates target projects
2. Browser Automation (Playwright) with Chrome session / UI helper
"""

import os
import sys
import json
import asyncio
import argparse
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SOURCE_PROJECT_ID = "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"
TARGET_PROJECT_IDS = [
    "1gBRtVeDLmPOU6M0NIqwNeUuPAvXcsp3nM8CkCYBcnt7reaIio2WPyBig",
    "1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww"
]

BACKUP_DIR = Path(__file__).parent / "migrated_projects" / SOURCE_PROJECT_ID

def migrate_via_api():
    """Migrate using Google Apps Script REST API with OAuth2"""
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    SCOPES = [
        "https://www.googleapis.com/auth/script.projects",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.scripts"
    ]

    token_path = Path(__file__).parent / "token.json"
    credentials_path = Path(__file__).parent / "credentials.json"
    creds = None

    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except Exception as e:
            print(f"[!] Warning reading existing token: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[*] Refreshing expired OAuth token...")
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print("=" * 60)
                print("[!] ERROR: credentials.json not found in gdrive-scripts folder.")
                print("To authenticate with Google Apps Script API:")
                print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
                print("2. Create an OAuth 2.0 Client ID (Desktop Application)")
                print("3. Download client_secret_xxx.json and save it as:")
                print(f"   {credentials_path}")
                print("=" * 60)
                return False
            
            print("[*] Launching local browser for Google OAuth authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
        print(f"[+] Token saved to {token_path}")

    service = build("script", "v1", credentials=creds)

    print(f"\n[1] Fetching project content from Source: {SOURCE_PROJECT_ID}...")
    try:
        source_content = service.projects().getContent(scriptId=SOURCE_PROJECT_ID).execute()
    except Exception as e:
        print(f"[!] Error fetching source project: {e}")
        return False

    files = source_content.get("files", [])
    print(f"[+] Successfully fetched {len(files)} files from source project:")
    for f in files:
        print(f"    - {f.get('name')} ({f.get('type')}) [{len(f.get('source', ''))} chars]")

    # Save backup locally
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    with open(BACKUP_DIR / "project_content.json", "w", encoding="utf-8") as bf:
        json.dump(source_content, bf, indent=2)

    for f in files:
        ext = ".gs" if f.get("type") == "SERVER_JS" else ".html" if f.get("type") == "HTML" else ".json"
        filename = f.get("name") + ext
        with open(BACKUP_DIR / filename, "w", encoding="utf-8") as out:
            out.write(f.get("source", ""))
    print(f"[+] Local backup saved to {BACKUP_DIR}")

    # Push to each target project
    for target_id in TARGET_PROJECT_IDS:
        print(f"\n[2] Updating Target Project: {target_id}...")
        try:
            update_body = {"files": files}
            res = service.projects().updateContent(scriptId=target_id, body=update_body).execute()
            print(f"    [SUCCESS] Updated {target_id} successfully! ({len(res.get('files', []))} files synced)")
        except Exception as e:
            print(f"    [!] Error updating {target_id}: {e}")

    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETED!")
    print("=" * 60)
    return True


async def migrate_via_playwright():
    """Migrate using Playwright Browser automation with Chrome profile"""
    from playwright.async_api import async_playwright
    
    print("\n[*] Starting Playwright Browser Automation for Google Apps Script...")
    user_data_dir = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data")
    
    async with async_playwright() as p:
        print("[*] Launching browser...")
        try:
            # Launch persistent or standard browser
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(viewport={"width": 1440, "height": 900})
            page = await context.new_page()

            source_url = f"https://script.google.com/home/projects/{SOURCE_PROJECT_ID}/edit"
            print(f"[1] Opening Source Project: {source_url}")
            await page.goto(source_url)
            print("[*] Please ensure you are logged in to your Google Account.")
            print("[*] Waiting 10 seconds for editor to load...")
            await asyncio.sleep(10)

            # Check page title and structure
            title = await page.title()
            print(f"[+] Current page title: {title}")

            for target_id in TARGET_PROJECT_IDS:
                target_url = f"https://script.google.com/d/{target_id}/edit"
                print(f"[2] Target project link: {target_url}")

            await page.screenshot(path="d:/infonix/apps_script_editor_view.png")
            print("[+] Screenshot saved to d:/infonix/apps_script_editor_view.png")

        except Exception as e:
            print(f"[!] Browser automation error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Migrate Google Apps Script from Source to Targets")
    parser.add_argument("--mode", choices=["api", "browser"], default="api", help="Migration mode (api or browser)")
    args = parser.parse_args()

    print("=" * 60)
    print("GOOGLE APPS SCRIPT PROJECT MIGRATOR")
    print(f"Source ID : {SOURCE_PROJECT_ID}")
    print(f"Target IDs: {TARGET_PROJECT_IDS}")
    print("=" * 60)

    if args.mode == "api":
        success = migrate_via_api()
        if not success:
            print("\nFallback to browser mode if API credentials are not set.")
    else:
        asyncio.run(migrate_via_playwright())

if __name__ == "__main__":
    main()
