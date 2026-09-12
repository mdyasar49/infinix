import json, requests, os, sys

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

ids = [
    ("Form", "1ugPH89EBC1RSVJrrHKs3qnYnyR3y5rXAVwK43wamthE"),
    ("Sheet 1 (Non-IT)", "17HwSLgqtsQBNFAo5Ua-ocA0KzY3gZxHmbIuC6PdrmTw"),
    ("Sheet 2 (Interns List)", "1qVv11xhfeIyYIrtHA7ChcTqaLPSYYp1Kza_fWdmafas")
]

for label, fid in ids:
    r = requests.get(f"https://www.googleapis.com/drive/v3/files/{fid}?fields=*", headers=headers)
    print(f"\n[{label}] ID: {fid}")
    if r.status_code == 200:
        data = r.json()
        print("  Name:", data.get('name'))
        print("  Mime:", data.get('mimeType'))
        print("  Owners:", [o.get('emailAddress') for o in data.get('owners', [])])
        print("  webViewLink:", data.get('webViewLink'))
        print("  description:", data.get('description'))
        print("  properties:", data.get('properties'))
    else:
        print("  Error:", r.status_code, r.text)
