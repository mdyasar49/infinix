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

sheets = [
    ("Non-IT Interns", "17HwSLgqtsQBNFAo5Ua-ocA0KzY3gZxHmbIuC6PdrmTw"),
    ("Interns List", "1qVv11xhfeIyYIrtHA7ChcTqaLPSYYp1Kza_fWdmafas")
]

for name, sid in sheets:
    print(f"\n--- {name} ({sid}) ---")
    r = requests.get(f"https://www.googleapis.com/drive/v3/files/{sid}/export?mimeType=text/csv", headers=headers)
    print("Status:", r.status_code)
    if r.status_code == 200:
        lines = r.text.splitlines()
        print(f"Total rows: {len(lines)}")
        if len(lines) > 0:
            print("Header row:", lines[0][:200])
        if len(lines) > 1:
            print("Row 1 snippet:", lines[1][:200])
    else:
        print("Error:", r.text)
