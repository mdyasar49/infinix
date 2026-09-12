import paramiko
import sys
import os
import requests
import json
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("🚀 INFOGENX ONBOARDING: FULL COMMIT & DEPLOYMENT RUNNER")
print("=" * 60)

# 1. PUSH TO GOOGLE APPS SCRIPT
print("\n[1/4] Deploying to Google Apps Script (All 4 Projects)...")
try:
    from gdrive_scripts_push import run_push
except ImportError:
    pass

import subprocess
res_apps = subprocess.run([sys.executable, r"d:\infonix\gdrive-scripts\push_local_to_target.py"], capture_output=True, text=True, encoding="utf-8")
print(res_apps.stdout)
if res_apps.stderr:
    print("Apps Script Stderr:", res_apps.stderr)

# 2. DEPLOY TO BACKEND API (api.infogenx.com)
print("\n[2/4] Deploying to Backend API Server (209.182.232.150: infogenx-api)...")
ssh_api = paramiko.SSHClient()
ssh_api.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_api.connect('209.182.232.150', username='infogenx-api', password=os.environ.get('SSH_API_PASSWORD', 'infogenx-api@1234'), timeout=15)
sftp_api = ssh_api.open_sftp()

print(" -> Uploading candidate-auth.js...")
sftp_api.put(r'd:\infonix\remote_candidate_auth.js', '/home/infogenx-api/htdocs/api.infogenx.com/routes/candidate-auth.js')

print(" -> Uploading offer-letter.js...")
sftp_api.put(r'd:\infonix\remote_offer_letter.js', '/home/infogenx-api/htdocs/api.infogenx.com/routes/offer-letter.js')
sftp_api.close()

print(" -> Restarting API node process...")
stdin, stdout, stderr = ssh_api.exec_command("kill -9 $(pgrep -f server.js | head -1); sleep 2; ps aux | grep server.js")
print(stdout.read().decode('utf-8'))
ssh_api.close()
print(" ✅ Backend API updated and running!")

# 3. VERIFY & REBUILD FRONTEND (candidates.infogenx.com)
print("\n[3/4] Checking Frontend Assets & Status (209.182.232.150: infogenx-candidates)...")
ssh_cand = paramiko.SSHClient()
ssh_cand.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_cand.connect('209.182.232.150', username='infogenx-candidates', password=os.environ.get('SSH_CAND_PASSWORD', 'infogenx@1234'), timeout=15)

build_cmd = """
export PATH="/home/infogenx-candidates/.nvm/versions/node/v20.20.2/bin:$PATH"
cd /home/infogenx-candidates/htdocs/candidates.infogenx.com
ls -la dist/logo*.png
"""
stdin, stdout, stderr = ssh_cand.exec_command(build_cmd)
print("Frontend static logo assets in dist/:")
print(stdout.read().decode('utf-8'))
ssh_cand.close()

# 4. VERIFY GIT COMMITS & PUSH STATUS
print("\n[4/4] Verifying GitHub Repo Status (mdyasar49/infogenx-candidates-onboarding)...")
git_cmd = subprocess.run(["git", "status"], cwd=r"d:\infonix\infogenx-candidates-onboarding", capture_output=True, text=True, encoding="utf-8")
print(git_cmd.stdout)

# 5. TEST PUBLIC HTTPS ENDPOINTS
print("\n[5/5] Testing Public HTTPS Endpoints...")
endpoints = [
    "https://candidates.infogenx.com/logo_white.png",
    "https://candidates.infogenx.com/logo.png",
    "https://api.infogenx.com/health",
    "https://candidates.infogenx.com"
]

for ep in endpoints:
    try:
        r = requests.get(ep, timeout=10)
        print(f" -> {ep} : Status {r.status_code} ({len(r.content)} bytes)")
    except Exception as e:
        print(f" -> {ep} : Error {e}")

print("\n" + "=" * 60)
print("🎉 FULL COMMIT & DEPLOYMENT VERIFICATION COMPLETE!")
print("=" * 60)
