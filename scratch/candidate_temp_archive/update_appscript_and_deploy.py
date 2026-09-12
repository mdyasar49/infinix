import json, requests, os, sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

LOCAL_DIR = Path(__file__).parent / "gdrive-scripts" / "extracted_project" / "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"
TARGET_IDS = [
    "1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww",
    "1gBRtVeDLmPOU6M0NIqwNeUuPAvXcsp3nM8CkCYBcnt7reaIio2WPyBig",
    "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p",
    "1u1_v1sF907CLG4Yk33NHYMQEtNnpgENiNq4CHqAbUMLHmioZAjvJVzC4"
]

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

def main():
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Build files list
    files = []
    manifest_path = LOCAL_DIR / "appsscript.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as mf:
            files.append({
                "name": "appsscript",
                "type": "JSON",
                "source": mf.read()
            })

    for gs_file in LOCAL_DIR.glob("*.gs"):
        with open(gs_file, "r", encoding="utf-8") as gf:
            files.append({
                "name": gs_file.stem,
                "type": "SERVER_JS",
                "source": gf.read()
            })

    for html_file in LOCAL_DIR.glob("*.html"):
        with open(html_file, "r", encoding="utf-8") as hf:
            files.append({
                "name": html_file.stem,
                "type": "HTML",
                "source": hf.read()
            })

    payload = {"files": files}
    print(f"[*] Prepared {len(files)} files to push from {LOCAL_DIR}")

    # 2. Push content to all targets
    for tid in TARGET_IDS:
        print(f"\n[*] Pushing to {tid}...")
        put_url = f"https://script.googleapis.com/v1/projects/{tid}/content"
        r = requests.put(put_url, headers=headers, json=payload)
        if r.status_code == 200:
            print(f"    ✅ Successfully updated content of {tid}")
        else:
            print(f"    ❌ Failed: {r.status_code} {r.text}")

    # 3. Create a new version on 1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p
    main_script_id = "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"
    print(f"\n[*] Creating new version on {main_script_id}...")
    v_url = f"https://script.googleapis.com/v1/projects/{main_script_id}/versions"
    vr = requests.post(v_url, headers=headers, json={"description": "Fix login getStudentByEmail and resilient auth"})
    if vr.status_code == 200:
        new_version = vr.json().get("versionNumber")
        print(f"    ✅ Created Version {new_version}")

        # 4. Update deployment AKfycbzBZ_OQKodlVo9M1bcUlBQXnZS93NxZQvJdqUIJiFf0ex6TVl-XrN0UW2sMJv8LBuyhhA
        dep_id = "AKfycbzBZ_OQKodlVo9M1bcUlBQXnZS93NxZQvJdqUIJiFf0ex6TVl-XrN0UW2sMJv8LBuyhhA"
        dep_url = f"https://script.googleapis.com/v1/projects/{main_script_id}/deployments/{dep_id}"
        dep_config = {
            "deploymentConfig": {
                "scriptId": main_script_id,
                "versionNumber": new_version,
                "manifestFileName": "appsscript",
                "description": "Infogenx Student Portal API"
            }
        }
        print(f"[*] Updating deployment {dep_id} to Version {new_version}...")
        dr = requests.put(dep_url, headers=headers, json=dep_config)
        if dr.status_code == 200:
            print(f"    ✅ Deployment {dep_id} successfully updated to Version {new_version}!")
        else:
            print(f"    ❌ Deployment update failed: {dr.status_code} {dr.text}")
    else:
        print(f"    ❌ Version creation failed: {vr.status_code} {vr.text}")

if __name__ == "__main__":
    main()
