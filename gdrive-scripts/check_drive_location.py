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
    return token_dict.get("access_token")

def get_drive_details():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    file_ids = [
        ("Database Spreadsheet", "1tEjn1hJ0rd2pNV3kaLyv4SitFyoRLwCKb5loAdEvjoM"),
        ("Registration Form", "1531Djx394duVArz8FnexfpgTqyr1gO6X6aJstRs7DNQ")
    ]
    
    print("=== GOOGLE DRIVE FILE DETAILS ===")
    for label, fid in file_ids:
        r = requests.get(f"https://www.googleapis.com/drive/v3/files/{fid}?fields=id,name,mimeType,parents,webViewLink,createdTime,modifiedTime", headers=headers)
        if r.status_code == 200:
            d = r.json()
            print(f"\n[{label}]")
            print(f"  File Name: {d.get('name')}")
            print(f"  File ID:   {d.get('id')}")
            print(f"  Type:      {d.get('mimeType')}")
            print(f"  Web Link:  {d.get('webViewLink')}")
            print(f"  Parents:   {d.get('parents', ['My Drive (Root)'])}")
        else:
            print(f"[!] Error fetching {label}: {r.status_code}")

if __name__ == "__main__":
    get_drive_details()
