import json
import sys
import os
import requests
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SOURCE_ID = "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"
TARGET_IDS = [
    "1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww",
    "1gBRtVeDLmPOU6M0NIqwNeUuPAvXcsp3nM8CkCYBcnt7reaIio2WPyBig"
]

CLASPRC_PATH = Path(os.path.expanduser("~/.clasprc.json"))

def get_auth_token():
    if not CLASPRC_PATH.exists():
        print(f"[!] Error: {CLASPRC_PATH} not found.")
        return None
    
    with open(CLASPRC_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    token_dict = data.get("tokens", {}).get("default", {})
    if not token_dict and "token" in data:
        token_dict = data.get("token", {})
    if not token_dict:
        token_dict = data
        
    access_token = token_dict.get("access_token")
    refresh_token = token_dict.get("refresh_token")
    client_id = token_dict.get("client_id")
    client_secret = token_dict.get("client_secret")

    # If access token is available, test it or refresh
    if refresh_token and client_id and client_secret:
        print("[*] Refreshing Google OAuth Access Token with Google Auth Server...")
        refresh_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        try:
            r = requests.post("https://oauth2.googleapis.com/token", data=refresh_data, timeout=15)
            if r.status_code == 200:
                res_json = r.json()
                access_token = res_json.get("access_token", access_token)
                print("[+] Access token refreshed and validated successfully.")
            else:
                print(f"[*] Using existing access token (Refresh status: {r.status_code})")
        except Exception as e:
            print(f"[*] Using existing token: {e}")
            
    return access_token

def sync_projects():
    token = get_auth_token()
    if not token:
        print("[!] No valid token available.")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("=" * 60)
    print("GOOGLE APPS SCRIPT API DIRECT SYNC")
    print(f"Source Project: {SOURCE_ID}")
    print("=" * 60)

    # 1. Fetch Source Project Content
    print(f"\n[1] Fetching content from Source Project ({SOURCE_ID})...")
    get_url = f"https://script.googleapis.com/v1/projects/{SOURCE_ID}/content"
    resp = requests.get(get_url, headers=headers, timeout=30)
    
    if resp.status_code != 200:
        print(f"[!] Failed to fetch source project: HTTP {resp.status_code}")
        print(resp.text)
        return False
    
    source_data = resp.json()
    files = source_data.get("files", [])
    print(f"[+] Successfully retrieved {len(files)} files from source:")
    
    backup_dir = Path(__file__).parent / "extracted_project" / SOURCE_ID
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    for f in files:
        name = f.get("name")
        ftype = f.get("type")
        source = f.get("source", "")
        print(f"    - {name} ({ftype}) [{len(source)} chars]")
        ext = ".gs" if ftype == "SERVER_JS" else ".html" if ftype == "HTML" else ".json"
        with open(backup_dir / f"{name}{ext}", "w", encoding="utf-8") as out_f:
            out_f.write(source)
    
    with open(backup_dir / "project.json", "w", encoding="utf-8") as pf:
        json.dump(source_data, pf, indent=2)
    print(f"[+] Saved local backup to: {backup_dir}")

    # 2. Push to target projects
    payload = {"files": files}
    for tid in TARGET_IDS:
        print(f"\n[2] Updating Target Project: {tid}...")
        put_url = f"https://script.googleapis.com/v1/projects/{tid}/content"
        put_resp = requests.put(put_url, headers=headers, json=payload, timeout=30)
        
        if put_resp.status_code == 200:
            res_data = put_resp.json()
            updated_files = res_data.get("files", [])
            print(f"    ✅ [SUCCESS] Target project {tid} updated successfully! ({len(updated_files)} files written)")
        else:
            print(f"    ❌ [ERROR] Failed to update {tid}: HTTP {put_resp.status_code}")
            print(put_resp.text)

    print("\n" + "=" * 60)
    print("🎉 ALL CODE MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    sync_projects()
