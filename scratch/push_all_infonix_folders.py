import os
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
USER = "mdyasar49"
BASE_DIR = Path(r"d:\infonix")

print("=" * 65)
print("🚀 INFONIX WORKSPACE: PUSH ALL RESTRUCTURED FOLDERS TO GITHUB")
print(f"👤 GitHub Target Account: {USER}")
print("=" * 65)

def push_directory_to_repo(folder_path, repo_name, commit_msg):
    folder_path = Path(folder_path)
    if not folder_path.exists():
        print(f"[-] Directory {folder_path} not found. Skipping.")
        return False

    print(f"\n[+] Processing: {folder_path.name} ──► https://github.com/{USER}/{repo_name}")
    
    # 1. Ensure git init
    if not (folder_path / ".git").exists():
        subprocess.run(["git", "init"], cwd=folder_path, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.name", USER], cwd=folder_path, check=True)
        subprocess.run(["git", "config", "user.email", "mohamedyasar081786@gmail.com"], cwd=folder_path, check=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=folder_path, check=True)
        print("  -> Initialized new Git repository on 'main'")

    # 2. Add all files without ignoring
    subprocess.run(["git", "add", "-A"], cwd=folder_path, check=True)
    
    # 3. Check if changes exist
    status = subprocess.run(["git", "status", "--porcelain"], cwd=folder_path, capture_output=True, text=True).stdout.strip()
    if status:
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=folder_path, check=True)
        print("  -> Committed new changes")
    else:
        print("  -> Working tree already clean / committed")

    # 4. Set authenticated remote & push
    auth_remote = f"https://{USER}:{TOKEN}@github.com/{USER}/{repo_name}.git"
    clean_remote = f"https://github.com/{USER}/{repo_name}.git"
    
    # Check current remotes
    remotes = subprocess.run(["git", "remote"], cwd=folder_path, capture_output=True, text=True).stdout
    if "origin" in remotes.split():
        subprocess.run(["git", "remote", "set-url", "origin", auth_remote], cwd=folder_path, check=True)
    else:
        subprocess.run(["git", "remote", "add", "origin", auth_remote], cwd=folder_path, check=True)

    print(f"  -> Pushing to origin main...")
    push_res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=folder_path, capture_output=True, text=True)
    if push_res.returncode == 0:
        print(f"  ✅ [SUCCESS] Pushed to https://github.com/{USER}/{repo_name}")
    else:
        print(f"  ❌ Push failed: {push_res.stderr.strip()}")

    # Reset remote to clean URL
    subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=folder_path, check=True)
    return push_res.returncode == 0

# Execute for all folders
# 1. Cloudpanel Scripts
push_directory_to_repo(
    BASE_DIR / "cloudpanel-scripts",
    "cloudpanel-scripts",
    "feat: CloudPanel server automation, SSL installation, and vhost configuration tools"
)

# 2. Google Drive / Apps Script
push_directory_to_repo(
    BASE_DIR / "gdrive-scripts",
    "google-apps-script",
    "feat: Google Apps Script automation, Drive synchronization, and form ingestion pipelines"
)

# 3. Scripts / Data Scraping
push_directory_to_repo(
    BASE_DIR / "scripts",
    "Data-Scraping",
    "feat: Lead acquisition engines, LinkedIn scrapers, and Odoo/Zoho lead enrichment suite"
)

# 4. Documents
push_directory_to_repo(
    BASE_DIR / "documents",
    "infonix-documents",
    "docs: Infogenx enterprise SOPs, process flows, and lead management documentation"
)

# 5. Facebook
push_directory_to_repo(
    BASE_DIR / "Facebook",
    "Facebook",
    "feat: Facebook scraper and business leads verification"
)

# 6. Candidate Onboarding
push_directory_to_repo(
    BASE_DIR / "infogenx-candidates-onboarding",
    "infogenx-candidates-onboarding",
    "feat: Infogenx candidate onboarding & assessment ecosystem"
)

print("\n" + "=" * 65)
print("🎉 ALL FOLDERS IN INFINIX PROCESSED, COMMITTED & PUSHED!")
print("=" * 65)
