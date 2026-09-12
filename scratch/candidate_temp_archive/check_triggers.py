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

headers = {'Authorization': f'Bearer {access_token}'}
TARGET_IDS = [
    "1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww",
    "1gBRtVeDLmPOU6M0NIqwNeUuPAvXcsp3nM8CkCYBcnt7reaIio2WPyBig",
    "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p",
    "1u1_v1sF907CLG4Yk33NHYMQEtNnpgENiNq4CHqAbUMLHmioZAjvJVzC4"
]

for tid in TARGET_IDS:
    # Run processes or inspect project
    url = f'https://script.googleapis.com/v1/processes?userProcessFilter.scriptId={tid}'
    r = requests.get(url, headers=headers)
    print(f'=== Processes for {tid} === (Status: {r.status_code})')
    if r.status_code == 200:
        procs = r.json().get('processes', [])
        print(f'Found {len(procs)} executions.')
        for p in procs[:5]:
            print(f" - {p.get('functionName')}: {p.get('processStatus')} at {p.get('startTime')}")
    else:
        print(r.text[:150])
