import json, requests, os, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def get_auth_token():
    clasprc = json.load(open(os.path.expanduser('~/.clasprc.json'), encoding='utf-8'))
    tokens = clasprc.get('tokens', {}).get('default', {}) or clasprc.get('token', {}) or clasprc
    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')
    client_id = tokens.get('client_id')
    client_secret = tokens.get('client_secret')

    if refresh_token and client_id and client_secret:
        r = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': client_id, 'client_secret': client_secret,
            'refresh_token': refresh_token, 'grant_type': 'refresh_token'
        })
        if r.status_code == 200:
            access_token = r.json().get('access_token', access_token)
    return access_token

token = get_auth_token()
headers = {"Authorization": f"Bearer {token}"}
folder_id = "1VYR5eScDWe6HaOsLKNQEViN2ainrUMPt"

print(f"Checking folder: {folder_id}...")
# 1. Check folder metadata
rf = requests.get(f"https://www.googleapis.com/drive/v3/files/{folder_id}?fields=id,name,mimeType,webViewLink", headers=headers)
print("Folder response:", rf.status_code, rf.text)

# 2. List files in folder
q = f"'{folder_id}' in parents and trashed = false"
r = requests.get(f"https://www.googleapis.com/drive/v3/files?q={q}&fields=files(id,name,mimeType,webViewLink,createdTime,modifiedTime)", headers=headers)
print("\nFiles in folder response:", r.status_code)
files = r.json().get('files', [])
print(f"Total files found: {len(files)}")
for f in files:
    print(f"- Name: {f.get('name')}")
    print(f"  ID: {f.get('id')}")
    print(f"  Type: {f.get('mimeType')}")
    print(f"  Link: {f.get('webViewLink')}")
