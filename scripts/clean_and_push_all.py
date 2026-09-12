import os
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
USER_NAME = "mdyasar49"
BASE_DIR = r"d:\infonix"

TARGET_REPOS = [
    "blog-api",
    "Data-Scraping",
    "google-apps-script",
    "infogenx-twilio-dialer",
    "odoo-sheets-auto-sync",
    "Social-Media-Data-Scraping"
]

GITIGNORE_CONTENT = """# Secret files & environment
.env
*.env
*.json
!package.json
!package-lock.json
!manifest.json
!workflow_settings.yaml

# Dependencies & build
node_modules/
.venv/
__pycache__/
*.pyc
dist/
build/
.DS_Store
"""

def sanitize_and_push(repo_name):
    repo_path = os.path.join(BASE_DIR, repo_name)
    if not os.path.exists(repo_path):
        print(f"  [!] Path '{repo_path}' does not exist.")
        return False
    
    auth_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{repo_name}.git"
    clean_remote = f"https://github.com/{USER_NAME}/{repo_name}.git"
    
    print(f"\n[+] Sanitizing & Pushing '{repo_name}'...")
    
    # 1. Update/Write .gitignore
    gitignore_path = os.path.join(repo_path, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(GITIGNORE_CONTENT)
    
    # 2. Reset .git history to clear old secret commits
    git_dir = os.path.join(repo_path, ".git")
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir, ignore_errors=True)
    
    try:
        # 3. Clean Git Init
        subprocess.run(["git", "init"], cwd=repo_path, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.name", "mdyasar49"], cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.email", "mohamedyasar081786@gmail.com"], cwd=repo_path, check=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path, check=True)
        subprocess.run(["git", "remote", "add", "origin", clean_remote], cwd=repo_path, check=True)
        
        # 4. Add & Commit
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", f"Initial commit for {repo_name}"], cwd=repo_path, check=True, stdout=subprocess.DEVNULL)
        
        # 5. Push using authenticated URL
        print(f"  [➔] Pushing clean commit to https://github.com/{USER_NAME}/{repo_name}.git...")
        res = subprocess.run(["git", "push", "-u", auth_remote, "main", "--force"], cwd=repo_path, capture_output=True, text=True)
        
        # Ensure clean origin URL is set
        subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=repo_path, check=True)
        
        if res.returncode == 0:
            print(f"  [🎉] SUCCESS: {repo_name} pushed to GitHub!")
            return True
        else:
            err = res.stderr or res.stdout
            print(f"  [!] {repo_name} push error: {err.strip()[:200]}")
            return False
            
    except Exception as e:
        print(f"  [!] Error processing {repo_name}: {e}")
        try:
            subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=repo_path, check=True)
        except Exception:
            pass
        return False

def main():
    print("=" * 80)
    print(" 🚀 SANITIZING & PUSHING ALL REMAINING REPOSITORIES TO @mdyasar49")
    print("=" * 80)
    
    results = []
    for r in TARGET_REPOS:
        ok = sanitize_and_push(r)
        results.append((r, ok))
        
    print("\n" + "=" * 80)
    print(" 📊 REMAINING REPOSITORIES PUSH STATUS")
    print("=" * 80)
    for repo_name, ok in results:
        status = "✅ Pushed & Active" if ok else "❌ Failed"
        print(f"  • {repo_name:<30} -> {status}")
    print("=" * 80)

if __name__ == "__main__":
    main()
