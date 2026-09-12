import urllib.request
import json
import subprocess
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
REPO_NAME = "LinkedIn-Data-Scraping"
LOCAL_DIR = r"d:\infonix\LinkedIn-Data-Scraping"

# 1. Create GitHub Repo if not exists
url = "https://api.github.com/user/repos"
payload = json.dumps({
    "name": REPO_NAME,
    "description": "High-performance automated LinkedIn company and executive profile extraction pipeline with Google Sheets integration",
    "private": False
}).encode("utf-8")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Infogenx"
}

req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as resp:
        print(f"[✓] Created GitHub repository: https://github.com/mdyasar49/{REPO_NAME}")
except urllib.error.HTTPError as e:
    if e.code == 422:
        print(f"[i] Repository {REPO_NAME} already exists on GitHub.")
    else:
        print(f"[!] GitHub API Error: {e.code} - {e.read().decode('utf-8')}")

# 2. Update topics
topics_url = f"https://api.github.com/repos/mdyasar49/{REPO_NAME}/topics"
topics_payload = json.dumps({
    "names": ["linkedin-scraper", "data-scraping", "lead-generation", "b2b-leads", "google-sheets-sync", "python", "selenium"]
}).encode("utf-8")
topics_req = urllib.request.Request(topics_url, data=topics_payload, headers=headers, method="PUT")
try:
    with urllib.request.urlopen(topics_req) as resp:
        print(f"[✓] Updated topics for {REPO_NAME}")
except Exception as e:
    print(f"[-] Topics update: {e}")

# 3. Git Init, Add, Commit, Push
os.chdir(LOCAL_DIR)
git_dir = os.path.join(LOCAL_DIR, ".git")
if os.path.exists(git_dir):
    import shutil
    shutil.rmtree(git_dir)

subprocess.check_call(["git", "init"])
subprocess.check_call(["git", "config", "user.name", "mdyasar49"])
subprocess.check_call(["git", "config", "user.email", "mohamedyasar081786@gmail.com"])
subprocess.check_call(["git", "branch", "-M", "main"])
subprocess.check_call(["git", "add", "."])
subprocess.check_call(["git", "commit", "-m", "Initial commit: Automated LinkedIn Data Scraping & Google Sheets Integration Pipeline"])
remote_url = f"https://mdyasar49:{TOKEN}@github.com/mdyasar49/{REPO_NAME}.git"
subprocess.check_call(["git", "remote", "add", "origin", remote_url])
subprocess.check_call(["git", "push", "-u", "origin", "main", "--force"])

print(f"\n[🎉] 100% SUCCESS: Code pushed to https://github.com/mdyasar49/{REPO_NAME}")
