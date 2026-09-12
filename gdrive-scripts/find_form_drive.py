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

headers = {"Authorization": f"Bearer {access_token}"}
url = "https://www.googleapis.com/drive/v3/files"
params = {
    "q": "name contains 'intern' or name contains 'Intern' or name contains 'Registration' or name contains 'registration'",
    "fields": "files(id,name,mimeType,owners,webViewLink)",
    "pageSize": 50
}
res = requests.get(url, headers=headers, params=params)
for f in res.json().get("files", []):
    print(f"{f.get('name')} -> {f.get('id')} ({f.get('mimeType')})")
