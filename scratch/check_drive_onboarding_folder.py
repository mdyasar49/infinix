import json, requests, os, sys
sys.stdout.reconfigure(encoding='utf-8')

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

headers = {'Authorization': f'Bearer {access_token}'}

# Folder: Infogenx onboarding files (1KySxmIbc5Kcw9hksmnzX0s6r5IDBJozv)
folder_id = '1KySxmIbc5Kcw9hksmnzX0s6r5IDBJozv'
q = f"'{folder_id}' in parents and trashed = false"
r = requests.get(f"https://www.googleapis.com/drive/v3/files?q={q}&fields=files(id,name,mimeType,webViewLink)", headers=headers)
print("Files in Infogenx onboarding files folder:")
for f in r.json().get('files', []):
    print(f"  {f['name']} | ID: {f['id']} | {f['mimeType']}")

# Also Folder: 1VYR5eScDWe6HaOsLKNQEViN2ainrUMPt
folder2 = '1VYR5eScDWe6HaOsLKNQEViN2ainrUMPt'
q2 = f"'{folder2}' in parents and trashed = false"
r2 = requests.get(f"https://www.googleapis.com/drive/v3/files?q={q2}&fields=files(id,name,mimeType,webViewLink)", headers=headers)
print("\nFiles in folder 1VYR5eScDWe6HaOsLKNQEViN2ainrUMPt:")
for f in r2.json().get('files', []):
    print(f"  {f['name']} | ID: {f['id']} | {f['mimeType']}")
