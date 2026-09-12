import os
import re
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
USER_NAME = "mdyasar49"

REPOS = ["google-apps-script", "infogenx-twilio-dialer"]

def sanitize_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        orig = text
        text = re.sub(r"[\'\"]592605c9ec3bcff9bf492e4062ee21a1e8cd699a[\'\"]", '"YOUR_SERPER_API_KEY"', text)
        text = re.sub(r"[\'\"]AQ\.Ab8RN6[a-zA-Z0-9_-]{30,}[\'\"]", '"YOUR_GEMINI_API_KEY"', text)
        text = re.sub(r"[\'\"]AC[a-f0-9]{32}[\'\"]", '"YOUR_TWILIO_ACCOUNT_SID"', text)
        text = re.sub(r"[\'\"]SK[a-f0-9]{32}[\'\"]", '"YOUR_TWILIO_API_KEY"', text)
        
        if text != orig:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"  [✓] Sanitized keys in: {os.path.basename(filepath)}")
    except Exception as e:
        pass

def main():
    print("=" * 80)
    print(" 🚀 SANITIZING & PUSHING FINAL REPOSITORIES TO GITHUB")
    print("=" * 80)

    for repo in REPOS:
        repo_path = os.path.join(r"d:\infonix", repo)
        print(f"\n[+] Processing '{repo}'...")
        
        for root, dirs, files in os.walk(repo_path):
            if ".git" in dirs:
                dirs.remove(".git")
            for file in files:
                if file.endswith((".js", ".gs", ".py", ".sh", ".txt", ".json", ".ps1", ".deluge", ".yml", ".env.example", ".md")):
                    sanitize_file(os.path.join(root, file))

        git_dir = os.path.join(repo_path, ".git")
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir, ignore_errors=True)

        auth_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{repo}.git"
        clean_remote = f"https://github.com/{USER_NAME}/{repo}.git"

        subprocess.run(["git", "init"], cwd=repo_path, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.name", "mdyasar49"], cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.email", "mohamedyasar081786@gmail.com"], cwd=repo_path, check=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path, check=True)
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", f"Initial commit for {repo}"], cwd=repo_path, check=True, stdout=subprocess.DEVNULL)

        print(f"  [➔] Pushing {repo} to GitHub...")
        res = subprocess.run(["git", "push", "-u", auth_remote, "main", "--force"], cwd=repo_path, capture_output=True, text=True)
        
        subprocess.run(["git", "remote", "add", "origin", clean_remote], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=repo_path, check=True)

        if res.returncode == 0:
            print(f"  [🎉] SUCCESS: {repo} pushed to GitHub!")
        else:
            print(f"  [!] ERROR pushing {repo}:\n{res.stderr[:400]}")

if __name__ == "__main__":
    main()
