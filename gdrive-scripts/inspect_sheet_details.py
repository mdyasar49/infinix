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

def inspect():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Drive File info
    f_res = requests.get(f"https://www.googleapis.com/drive/v3/files/{SPREADSHEET_ID}?fields=id,name,owners,mimeType", headers=headers)
    print("Drive File:", f_res.json())
    
    # Sheets API metadata
    s_res = requests.get(f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}", headers=headers)
    print("Sheets API Status:", s_res.status_code)
    if s_res.status_code == 200:
        s_data = s_res.json()
        print("Spreadsheet Title:", s_data.get("properties", {}).get("title"))
        for sheet in s_data.get("sheets", []):
            props = sheet.get("properties", {})
            print(f"Sheet: {props.get('title')} (ID: {props.get('sheetId')}, rowCount: {props.get('gridProperties', {}).get('rowCount')})")
            
            # Read first 10 rows
            val_res = requests.get(f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{props.get('title')}!A1:Z10", headers=headers)
            if val_res.status_code == 200:
                vals = val_res.json().get("values", [])
                print(f"  Rows count: {len(vals)}")
                for row in vals[:5]:
                    print("  Row:", row[:6])
    else:
        print("Sheets API error:", s_res.text)

if __name__ == "__main__":
    inspect()
