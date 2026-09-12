import json
import sys
import os
import requests
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

CLASPRC_PATH = Path(os.path.expanduser("~/.clasprc.json"))

def get_auth_token():
    with open(CLASPRC_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    token_dict = data.get("tokens", {}).get("default", {})
    if not token_dict and "token" in data:
        token_dict = data.get("token", {})
    if not token_dict:
        token_dict = data
    return token_dict.get("access_token")

def create_spreadsheet_via_drive():
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("[1] Creating Spreadsheet via Drive API v3...")
    body = {
        "name": "Infogenx Student Database",
        "mimeType": "application/vnd.google-apps.spreadsheet"
    }
    
    resp = requests.post("https://www.googleapis.com/drive/v3/files", headers=headers, json=body)
    print("Status:", resp.status_code)
    print("Response:", resp.text)
    if resp.status_code == 200:
        file_info = resp.json()
        print(f"[+] SPREADSHEET CREATED! ID: {file_info.get('id')}")
        return file_info.get('id')
    return None

if __name__ == "__main__":
    create_spreadsheet_via_drive()
