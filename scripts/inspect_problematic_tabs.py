import os
import sys
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SERVICE_ACCOUNT_FILE = r"d:\infonix\sheet-sync-504707-85df40232946.json"
SPREADSHEET_ID = "1QY8hbycY-gdOWRch52SKoUS975U-t3EgZ0JrtdhPCoM"

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
service = build("sheets", "v4", credentials=creds)

target_tabs = ["Upwork Leads", "Instagram Leads", "Threads Leads"]

for tab in target_tabs:
    print("=" * 100)
    print(f" 🔍 INSPECTING ALL 31 COLUMNS IN TAB: '{tab}'")
    print("=" * 100)
    res = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=f"'{tab}'!A1:AE10").execute()
    rows = res.get("values", [])
    if not rows:
        print("  [!] Tab empty!")
        continue
    
    headers = rows[0]
    print(f"Total Columns: {len(headers)}")
    
    for row_idx, row in enumerate(rows[1:], 1):
        print(f"\n--- Row #{row_idx} ---")
        for col_idx, col_name in enumerate(headers):
            val = row[col_idx] if col_idx < len(row) else "<EMPTY>"
            print(f"  [{col_idx+1:02d}] {col_name:<45} : {val}")
