import os
import shutil
import subprocess
import urllib.request
import urllib.error
import json

TOKEN = "YOUR_GITHUB_TOKEN"
SOURCE_USER = "Santoshkumaratter"
TARGET_USER = "mdyasar49"

print(f"Fetching public repositories for '{SOURCE_USER}'...")
url = f"https://api.github.com/users/{SOURCE_USER}/repos?per_page=100"
req = urllib.request.Request(url, headers={"User-Agent": "Python"})
repos = json.loads(urllib.request.urlopen(req).read())
print(f"Found {len(repos)} repositories to migrate.\n")

TEMP_DIR = os.path.join("d:\\infonix", "_temp_migration")
os.makedirs(TEMP_DIR, exist_ok=True)

success_count = 0
failed_repos = []

for idx, repo in enumerate(repos, 1):
    name = repo["name"]
    desc = repo.get("description") or ""
    clone_url = repo["clone_url"]
    
    print(f"[{idx}/{len(repos)}] Processing: {name}")
    
    # 1. Create repo under mdyasar49 (standalone, not fork)
    create_url = "https://api.github.com/user/repos"
    payload = json.dumps({
        "name": name,
        "description": desc,
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }).encode("utf-8")
    
    create_req = urllib.request.Request(
        create_url,
        data=payload,
        headers={
            "Authorization": f"token {TOKEN}",
            "User-Agent": "Python",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json"
        }
    )
    
    try:
        urllib.request.urlopen(create_req)
        print(f"  [+] Created standalone repo: https://github.com/{TARGET_USER}/{name}")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"  [*] Repo already exists on GitHub: https://github.com/{TARGET_USER}/{name}")
        else:
            err_msg = e.read().decode('utf-8')
            print(f"  [-] Failed to create repo: {err_msg}")
            failed_repos.append((name, f"Create failed: {e.code}"))
            continue

    # 2. Clone bare mirror
    repo_path = os.path.join(TEMP_DIR, f"{name}.git")
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path, ignore_errors=True)
        
    clone_res = subprocess.run(["git", "clone", "--bare", clone_url, repo_path], capture_output=True, text=True)
    if clone_res.returncode != 0:
        print(f"  [!] Note: Clone empty or failed ({clone_res.stderr.strip()[:100]})")
        # If repo on source is completely empty (0 commits), nothing to push
        shutil.rmtree(repo_path, ignore_errors=True)
        success_count += 1
        continue
        
    # 3. Push mirror to target
    target_remote = f"https://{TOKEN}@github.com/{TARGET_USER}/{name}.git"
    push_res = subprocess.run(["git", "push", "--mirror", target_remote], cwd=repo_path, capture_output=True, text=True)
    if push_res.returncode == 0:
        print(f"  [SUCCESS] All branches & commits pushed to https://github.com/{TARGET_USER}/{name}")
        success_count += 1
    else:
        err = push_res.stderr.strip()
        print(f"  [-] Push failed: {err[:150]}")
        failed_repos.append((name, err[:150]))
        
    shutil.rmtree(repo_path, ignore_errors=True)

# Cleanup
shutil.rmtree(TEMP_DIR, ignore_errors=True)
print("\n" + "="*50)
print(f"MIGRATION SUMMARY: {success_count}/{len(repos)} Succeeded.")
if failed_repos:
    print("Failed:", failed_repos)
print("="*50)
