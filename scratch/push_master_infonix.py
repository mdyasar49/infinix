import os
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
USER = "mdyasar49"
REPO_NAME = "infonix"
BASE_DIR = Path(r"d:\infonix")

print("=" * 65)
print("🚀 PUSHING MASTER REPOSITORY: d:\\infonix ──► mdyasar49/infonix")
print("=" * 65)

# Create a clean root README.md for infonix master repo
readme_content = """# 🏢 Infonix / Infogenx Master Engineering Workspace

This repository houses the consolidated engineering, automation, and operational systems for **Infogenx**, maintained under the **`mdyasar49`** organization.

---

## 📂 Workspace Architecture & Components

```
infonix/
├── infogenx-candidates-onboarding/  # Candidate onboarding portal (React 19, Express, MySQL, Twilio, Offer Letters)
│                                    # Dedicated Repo: https://github.com/mdyasar49/infogenx-candidates-onboarding
│
├── cloudpanel-scripts/              # CloudPanel server orchestration, SSL certs, and vhost automation
│                                    # Dedicated Repo: https://github.com/mdyasar49/cloudpanel-scripts
│
├── gdrive-scripts/                  # Google Drive & Google Apps Script enterprise sync pipelines
│                                    # Dedicated Repo: https://github.com/mdyasar49/google-apps-script
│
├── scripts/                         # Lead acquisition engines, LinkedIn automation, Odoo/Zoho CRM scrapers
│                                    # Dedicated Repo: https://github.com/mdyasar49/Data-Scraping
│
├── documents/                       # Enterprise SOPs, recruitment process flows, and lead management docs
│                                    # Dedicated Repo: https://github.com/mdyasar49/infonix-documents
│
├── Facebook/                        # Facebook business lead scrapers and verification tools
│                                    # Dedicated Repo: https://github.com/mdyasar49/Facebook
│
├── resumes/                         # Professional resume documents (PDF & HTML formats)
│                                    # Dedicated Repo: https://github.com/mdyasar49/resumes
│
├── deploy.ps1                       # Unified multi-environment deployment script
└── logo_white.png                   # Infogenx brand logo asset
```

---

## 🔗 Dedicated Sub-Repositories

Each major component is also independently maintained and synced to its dedicated repository:
1. **Candidate Onboarding:** [https://github.com/mdyasar49/infogenx-candidates-onboarding](https://github.com/mdyasar49/infogenx-candidates-onboarding)
2. **CloudPanel DevOps:** [https://github.com/mdyasar49/cloudpanel-scripts](https://github.com/mdyasar49/cloudpanel-scripts)
3. **Google Apps Script:** [https://github.com/mdyasar49/google-apps-script](https://github.com/mdyasar49/google-apps-script)
4. **Data Scraping & Leads:** [https://github.com/mdyasar49/Data-Scraping](https://github.com/mdyasar49/Data-Scraping)
5. **Documentation & SOPs:** [https://github.com/mdyasar49/infonix-documents](https://github.com/mdyasar49/infonix-documents)
6. **Facebook Scraper:** [https://github.com/mdyasar49/Facebook](https://github.com/mdyasar49/Facebook)
7. **Resumes & Portfolio:** [https://github.com/mdyasar49/resumes](https://github.com/mdyasar49/resumes)

---

## 📄 License & Copyright
Copyright © 2026 **Infogenx Private Limited**. All rights reserved.
"""

(BASE_DIR / "README.md").write_text(readme_content, encoding="utf-8")
print("[+] Created master README.md")

# Create root .gitignore for master repo (ignores heavy builds and caches)
gitignore_content = """# Heavy build artifacts
node_modules/
**/node_modules/
.venv/
**/.venv/
__pycache__/
**/__pycache__/
*.py[cod]

# Dist / build folders
dist/
**/dist/
build/
**/build/

# OS files
.DS_Store
Thumbs.db
"""

(BASE_DIR / ".gitignore").write_text(gitignore_content, encoding="utf-8")
print("[+] Created master .gitignore")

# Initialize master git repo if needed
if not (BASE_DIR / ".git").exists():
    subprocess.run(["git", "init"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "config", "user.name", USER], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "config", "user.email", "mohamedyasar081786@gmail.com"], cwd=BASE_DIR, check=True)
    subprocess.run(["git", "branch", "-M", "main"], cwd=BASE_DIR, check=True)
    print("[+] Initialized master Git repository on 'main'")

# Add all files in root
subprocess.run(["git", "add", "README.md", ".gitignore", "deploy.ps1", "logo_white.png"], cwd=BASE_DIR, check=True)
status = subprocess.run(["git", "status", "--porcelain"], cwd=BASE_DIR, capture_output=True, text=True).stdout.strip()
if status:
    subprocess.run(["git", "commit", "-m", "feat: Infonix master engineering workspace, architecture docs, and unified tools"], cwd=BASE_DIR, check=True)
    print("[+] Committed master repository updates")

auth_url = f"https://{USER}:{TOKEN}@github.com/{USER}/{REPO_NAME}.git"
clean_url = f"https://github.com/{USER}/{REPO_NAME}.git"

remotes = subprocess.run(["git", "remote"], cwd=BASE_DIR, capture_output=True, text=True).stdout
if "origin" in remotes.split():
    subprocess.run(["git", "remote", "set-url", "origin", auth_url], cwd=BASE_DIR, check=True)
else:
    subprocess.run(["git", "remote", "add", "origin", auth_url], cwd=BASE_DIR, check=True)

print("[+] Pushing to https://github.com/mdyasar49/infonix...")
push_res = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], cwd=BASE_DIR, capture_output=True, text=True)
print("STDOUT:", push_res.stdout)
print("STDERR:", push_res.stderr)

subprocess.run(["git", "remote", "set-url", "origin", clean_url], cwd=BASE_DIR, check=True)
print("\n🎉 MASTER REPOSITORY PUSHED SUCCESSFULLY!")
