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

print("=== Searching for files with INFOGENX or logo in name or mimeType image ===")
queries = [
    "name contains 'INFOGENX'",
    "name contains 'Candidate'",
    "name contains 'logo' or name contains 'Logo'",
    "mimeType contains 'image/'"
]

for q in queries:
    print(f"\nQuery: {q}")
    r = requests.get(f"https://www.googleapis.com/drive/v3/files?q={q}&fields=files(id,name,mimeType,webViewLink)&pageSize=20", headers=headers)
    for f in r.json().get('files', []):
        print(f"  {f['name']} | ID: {f['id']} | {f['mimeType']}")
