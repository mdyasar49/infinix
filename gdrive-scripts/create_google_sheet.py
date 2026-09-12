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

def create_database_sheet():
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("[1] Creating 'Infogenx Student Database' Google Spreadsheet...")
    body = {
        "properties": {
            "title": "Infogenx Student Database"
        },
        "sheets": [
            {
                "properties": {
                    "title": "Students",
                    "gridProperties": {
                        "frozenRowCount": 1
                    }
                }
            },
            {
                "properties": {
                    "title": "Config"
                }
            }
        ]
    }
    
    resp = requests.post("https://sheets.googleapis.com/v4/spreadsheets", headers=headers, json=body)
    if resp.status_code != 200:
        print(f"[!] Sheets API creation failed: HTTP {resp.status_code}")
        print(resp.text)
        return None
    
    sheet_data = resp.json()
    spreadsheet_id = sheet_data.get("spreadsheetId")
    spreadsheet_url = sheet_data.get("spreadsheetUrl")
    print(f"[+] Spreadsheet created successfully!")
    print(f"    ID : {spreadsheet_id}")
    print(f"    URL: {spreadsheet_url}")

    # 2. Populate Headers on Students Sheet
    headers_list = [
        "Registration Date", "Full Name", "Date of Birth", "Email", "Generated Password",
        "Password Hash", "Mobile Number", "City", "Highest Qualification", "College Name",
        "Department", "Year of Passing", "Skill Category", "Skills", "Experience Type",
        "Company Name", "Experience (Years)", "Current Salary", "Expected Salary",
        "Resume Link", "Preferred Time", "Status", "Created At", "Last Login",
        "Certification", "LinkedIn Profile URL", "Work Duration & Timings", "Start Date",
        "Current Monthly Take Home Salary / Hourly Rate", "Your Current Work Status",
        "If Working then", "Preferred Availability",
        "Assessment Score", "Assessment Status", "Assessment Date", "Candidate Role", "Task Status"
    ]

    print("\n[2] Setting Headers and Styles on 'Students' Sheet...")
    val_body = {
        "range": "Students!A1:AK1",
        "majorDimension": "ROWS",
        "values": [headers_list]
    }
    val_resp = requests.put(
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Students!A1:AK1?valueInputOption=RAW",
        headers=headers,
        json=val_body
    )
    print(f"[+] Headers write status: {val_resp.status_code}")

    # 3. Populate Config Sheet
    config_values = [
        ["Project Name", "Infogenx Student Onboarding"],
        ["Version", "1.0"],
        ["Database Name", "Infogenx Student Database"],
        ["Created By", "infogenx.jobs@gmail.com"],
        ["Default Status", "Active"],
        ["Password Rule", "First 4 letters of Name + Birth Year"],
        ["Developer", "Infogenx"]
    ]
    cfg_body = {
        "range": "Config!A1:B7",
        "majorDimension": "ROWS",
        "values": config_values
    }
    cfg_resp = requests.put(
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Config!A1:B7?valueInputOption=RAW",
        headers=headers,
        json=cfg_body
    )
    print(f"[+] Config sheet write status: {cfg_resp.status_code}")

    return spreadsheet_id, spreadsheet_url

if __name__ == "__main__":
    create_database_sheet()
