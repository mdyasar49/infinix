import json, requests, os

clasprc = json.load(open(os.path.expanduser('~/.clasprc.json'), encoding='utf-8'))
tokens = clasprc.get('tokens', {}).get('default', {}) or clasprc.get('token', {}) or clasprc
access_token = tokens.get('access_token')
refresh_token = tokens.get('refresh_token')
client_id = tokens.get('client_id')
client_secret = tokens.get('client_secret')

if refresh_token and client_id:
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': client_id, 'client_secret': client_secret,
        'refresh_token': refresh_token, 'grant_type': 'refresh_token'
    })
    if r.status_code == 200:
        access_token = r.json().get('access_token')

headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
script_id = '1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p'

# List versions
r = requests.get(f'https://script.googleapis.com/v1/projects/{script_id}/versions', headers=headers)
print("VERSIONS STATUS:", r.status_code)
print("VERSIONS:", r.text)
