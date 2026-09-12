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

REPOS = [
    "blog-api",
    "blog-react",
    "Data-Scraping",
    "dev",
    "google-apps-script",
    "infogenx-twilio-dialer",
    "Infogenx-Voice-Agent",
    "infogenx.com",
    "infogenx.com.au",
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

def create_github_repo(repo_name):
    url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": repo_name,
        "description": f"InfogenX - {repo_name} repository",
        "private": False
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"  [✓] GitHub Repo '{repo_name}' created successfully.")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"  [i] Repository '{repo_name}' already exists on GitHub.")
            return True
        else:
            print(f"  [!] Failed to create '{repo_name}': HTTP {e.code} - {e.read().decode('utf-8')}")
            return False
    except Exception as e:
        print(f"  [!] Error creating '{repo_name}': {e}")
        return False

def push_repo(repo_name):
    repo_path = os.path.join(BASE_DIR, repo_name)
    if not os.path.exists(repo_path):
        print(f"  [!] Directory '{repo_path}' does not exist.")
        return False
    
    authenticated_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{repo_name}.git"
    clean_remote = f"https://github.com/{USER_NAME}/{repo_name}.git"
    
    try:
        # Check if git is initialized
        git_dir = os.path.join(repo_path, ".git")
        if not os.path.exists(git_dir):
            subprocess.check_call(["git", "init"], cwd=repo_path)
            subprocess.check_call(["git", "config", "user.name", "mdyasar49"], cwd=repo_path)
            subprocess.check_call(["git", "config", "user.email", "mohamedyasar081786@gmail.com"], cwd=repo_path)
            subprocess.check_call(["git", "branch", "-M", "main"], cwd=repo_path)
            subprocess.check_call(["git", "add", "."], cwd=repo_path)
            subprocess.check_call(["git", "commit", "-m", "Initial commit"], cwd=repo_path)
        
        # Set authenticated remote for pushing
        subprocess.check_call(["git", "remote", "set-url", "origin", authenticated_remote], cwd=repo_path)
        
        # Push to GitHub
        print(f"  [➔] Pushing code to https://github.com/{USER_NAME}/{repo_name}.git...")
        subprocess.check_call(["git", "push", "-u", "origin", "main", "--force"], cwd=repo_path)
        
        # Reset remote URL to clean URL (without token embedded)
        subprocess.check_call(["git", "remote", "set-url", "origin", clean_remote], cwd=repo_path)
        print(f"  [🎉] {repo_name} successfully pushed and configured!")
        return True
    except Exception as e:
        print(f"  [!] Error pushing '{repo_name}': {e}")
        # Ensure clean remote is set even on failure
        try:
            subprocess.check_call(["git", "remote", "set-url", "origin", clean_remote], cwd=repo_path)
        except Exception:
            pass
        return False

def main():
    print("=" * 80)
    print(" 🚀 AUTOMATED CREATION & PUSH FOR ALL 13 REPOSITORIES TO @mdyasar49")
    print("=" * 80)
    
    success_count = 0
    for repo_name in REPOS:
        print(f"\n[+] Processing Repository: {repo_name}")
        created = create_github_repo(repo_name)
        if created:
            pushed = push_repo(repo_name)
            if pushed:
                success_count += 1
    
    print("\n" + "=" * 80)
    print(f" 🎉 MIGRATION COMPLETE: {success_count}/{len(REPOS)} Repositories successfully created and pushed!")
    print("=" * 80)

if __name__ == "__main__":
    main()
