import urllib.request
import json
import subprocess
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
USER_NAME = "mdyasar49"
BASE_DIR = r"d:\infonix"

ALL_REPOS = [
    "dev",
    "infogenx.com",
    "infogenx.com.au",
    "Infogenx-Voice-Agent",
    "blog-api",
    "blog-react",
    "Data-Scraping",
    "google-apps-script",
    "infogenx-twilio-dialer",
    "LinkedIn-Data-Scraping",
    "odoo-sheets-auto-sync",
    "odoo_uploader",
    "Social-Media-Data-Scraping"
]

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Infogenx-Automation"
}

def create_repo(repo_name):
    url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": repo_name,
        "description": f"InfogenX - {repo_name} repository",
        "private": False
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"  [✓] Created repository on GitHub: {repo_name}")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"  [i] Repository '{repo_name}' already exists on GitHub.")
            return True
        else:
            print(f"  [!] HTTP Error creating '{repo_name}': {e.code}")
            return False
    except Exception as e:
        print(f"  [!] Error creating '{repo_name}': {e}")
        return False

def push_repo(repo_name):
    repo_path = os.path.join(BASE_DIR, repo_name)
    if not os.path.exists(repo_path):
        print(f"  [!] Directory '{repo_path}' not found.")
        return False
    
    auth_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{repo_name}.git"
    clean_remote = f"https://github.com/{USER_NAME}/{repo_name}.git"
    
    try:
        # Check git init
        if not os.path.exists(os.path.join(repo_path, ".git")):
            subprocess.run(["git", "init"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "mdyasar49"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.email", "mohamedyasar081786@gmail.com"], cwd=repo_path, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path, check=True)
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)
        
        subprocess.run(["git", "remote", "set-url", "origin", auth_remote], cwd=repo_path, check=True)
        res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=repo_path, capture_output=True, text=True)
        subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=repo_path, check=True)
        
        if res.returncode == 0:
            print(f"  [🎉] {repo_name}: Pushed successfully!")
            return True
        else:
            err = res.stderr or res.stdout
            if "PUSH PROTECTION" in err or "violations found" in err:
                print(f"  [⚠️] {repo_name}: Created on GitHub (Push Protection Blocked due to API keys/credentials file in history)")
            else:
                print(f"  [!] {repo_name}: Push status -> {err.strip()[:150]}")
            return False
    except Exception as e:
        print(f"  [!] {repo_name}: Exception -> {e}")
        return False

def main():
    print("=" * 80)
    print(" 🚀 COPYING & PUSHING ALL 13 REPOSITORIES TO @mdyasar49 GITHUB ACCOUNT")
    print("=" * 80)
    
    status_summary = []
    for r in ALL_REPOS:
        print(f"\n[+] Repository: {r}")
        created = create_repo(r)
        if created:
            pushed = push_repo(r)
            status_summary.append((r, pushed))
        else:
            status_summary.append((r, False))
            
    print("\n" + "=" * 80)
    print(" 📊 COMPLETE 13 REPOSITORIES STATUS REPORT")
    print("=" * 80)
    for repo_name, success in status_summary:
        icon = "✅ Pushed & Active on @mdyasar49" if success else "⚠️ Created on @mdyasar49 GitHub"
        print(f"  • {repo_name:<30} -> {icon}")
    print("=" * 80)

if __name__ == "__main__":
    main()
