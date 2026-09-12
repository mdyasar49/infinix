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
form_id = "1ugPH89EBC1RSVJrrHKs3qnYnyR3y5rXAVwK43wamthE"

print("--- FORM DETAILS ---")
rf = requests.get(f"https://forms.googleapis.com/v1/forms/{form_id}", headers=headers)
print("Form response status:", rf.status_code)
if rf.status_code == 200:
    fdata = rf.json()
    print("Title:", fdata.get('info', {}).get('title'))
    print("ResponderUri:", fdata.get('responderUri'))
    items = fdata.get('items', [])
    print(f"Total form items: {len(items)}")
    for i, it in enumerate(items):
        print(f"  Item {i+1}: {it.get('title')} (ID: {it.get('itemId')})")

print("\n--- SPREADSHEETS INSPECTION ---")
sheets_to_check = [
    ("Non-IT Interns (Responses)", "17HwSLgqtsQBNFAo5Ua-ocA0KzY3gZxHmbIuC6PdrmTw"),
    ("Interns List (Responses)", "1qVv11xhfeIyYIrtHA7ChcTqaLPSYYp1Kza_fWdmafas")
]

for name, sid in sheets_to_check:
    print(f"\nSpreadsheet: {name} ({sid})")
    rs = requests.get(f"https://sheets.googleapis.com/v4/spreadsheets/{sid}", headers=headers)
    print("Status:", rs.status_code)
    if rs.status_code == 200:
        sdata = rs.json()
        sheets = sdata.get('sheets', [])
        for sh in sheets:
            props = sh.get('properties', {})
            print(f"  Sheet: '{props.get('title')}' (ID: {props.get('sheetId')}, Grid: {props.get('gridProperties', {}).get('rowCount')}x{props.get('gridProperties', {}).get('columnCount')})")
