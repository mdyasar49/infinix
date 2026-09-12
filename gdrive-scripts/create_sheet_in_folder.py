import json
import os
import requests
from pathlib import Path

CLASPRC_PATH = Path(os.path.expanduser("~/.clasprc.json"))
with open(CLASPRC_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
token_dict = data.get("tokens", {}).get("default", {}) or data.get("token", {}) or data
access_token = token_dict.get("access_token")
refresh_token = token_dict.get("refresh_token")
client_id = token_dict.get("client_id")
client_secret = token_dict.get("client_secret")

if refresh_token and client_id and client_secret:
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }, timeout=15)
    if r.status_code == 200:
        access_token = r.json().get("access_token", access_token)

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

FOLDER_ID = "1KySxmIbc5Kcw9hksmnzX0s6r5IDBJozv"

# Create new Google Spreadsheet in the folder
metadata = {
    "name": "Infogenx Candidates Master Database",
    "mimeType": "application/vnd.google-apps.spreadsheet",
    "parents": [FOLDER_ID]
}

res = requests.post("https://www.googleapis.com/drive/v3/files", headers=headers, json=metadata)
print("Create Sheet Status:", res.status_code)
sheet_info = res.json()
print("New Sheet Created:", sheet_info)
sheet_id = sheet_info.get("id")

print(f"\nNEW_SHEET_ID: {sheet_id}")
print(f"URL: https://docs.google.com/spreadsheets/d/{sheet_id}/edit")
