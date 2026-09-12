import json
import sys
import os
import requests
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SPREADSHEET_ID = "1Y8Xdj3jNvh34zTK0OPfhH-7SzxE2frWQ0KJfnErrqXE"
CLASPRC_PATH = Path(os.path.expanduser("~/.clasprc.json"))
LOCAL_DIR = Path(__file__).parent / "extracted_project" / "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"

def get_auth_token():
    with open(CLASPRC_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    token_dict = data.get("tokens", {}).get("default", {}) or data.get("token", {}) or data
    access_token = token_dict.get("access_token")
    refresh_token = token_dict.get("refresh_token")
    client_id = token_dict.get("client_id")
    client_secret = token_dict.get("client_secret")

    if refresh_token and client_id and client_secret:
        refresh_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        try:
            r = requests.post("https://oauth2.googleapis.com/token", data=refresh_data, timeout=15)
            if r.status_code == 200:
                access_token = r.json().get("access_token", access_token)
        except Exception as e:
            print(f"Refresh error: {e}")
            
    return access_token

def create_and_bind_script():
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print(f"[*] Creating Container-Bound Apps Script directly inside Spreadsheet ({SPREADSHEET_ID})...")
    create_url = "https://script.googleapis.com/v1/projects"
    body = {
        "title": "Infogenx Student Onboarding Engine",
        "parentId": SPREADSHEET_ID
    }
    
    resp = requests.post(create_url, headers=headers, json=body)
    print(f"Status: {resp.status_code}")
    if resp.status_code != 200:
        print("Error:", resp.text)
        return None
    
    project_data = resp.json()
    new_script_id = project_data.get("scriptId")
    print(f"[+] CONTAINER-BOUND SCRIPT CREATED! Script ID: {new_script_id}")

    # Push all 9 files into this bound script
    files = []
    manifest_path = LOCAL_DIR / "appsscript.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as mf:
            files.append({"name": "appsscript", "type": "JSON", "source": mf.read()})

    for gs_file in LOCAL_DIR.glob("*.gs"):
        name = gs_file.stem
        with open(gs_file, "r", encoding="utf-8") as gf:
            files.append({"name": name, "type": "SERVER_JS", "source": gf.read()})

    print(f"[*] Uploading {len(files)} files to the new bound script...")
    put_url = f"https://script.googleapis.com/v1/projects/{new_script_id}/content"
    put_resp = requests.put(put_url, headers=headers, json={"files": files})
    if put_resp.status_code == 200:
        print(f"✅ [SUCCESS] All code bound directly to Google Spreadsheet {SPREADSHEET_ID}!")
        return new_script_id
    else:
        print(f"Push error: {put_resp.status_code} - {put_resp.text}")
        return None

if __name__ == "__main__":
    create_and_bind_script()
