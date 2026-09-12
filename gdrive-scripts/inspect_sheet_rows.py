import json
import sys
import os
import requests
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SPREADSHEET_ID = "1tEjn1hJ0rd2pNV3kaLyv4SitFyoRLwCKb5loAdEvjoM"
CLASPRC_PATH = Path(os.path.expanduser("~/.clasprc.json"))

def get_auth_token():
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

def inspect_spreadsheet():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get metadata
    r = requests.get(f"https://www.googleapis.com/drive/v3/files/{SPREADSHEET_ID}?fields=*", headers=headers)
    print("Spreadsheet Drive Info:", r.status_code)
    
    # Let's see if we can export or check sheet details
    export_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv"
    exp_r = requests.get(export_url, headers=headers)
    print("CSV Export Status:", exp_r.status_code)
    print("CSV Preview:\n", exp_r.text[:1000])

if __name__ == "__main__":
    inspect_spreadsheet()
