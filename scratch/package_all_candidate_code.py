import os
import shutil
import sys
from pathlib import Path

repo_root = Path(r"d:\infonix\infogenx-candidates-onboarding")
infonix_root = Path(r"d:\infonix")

print("[*] Packaging all candidate onboarding code into repository...")

# 1. Google Apps Script
gas_dir = repo_root / "google-apps-script"
gas_dir.mkdir(parents=True, exist_ok=True)

source_gas_project = infonix_root / "gdrive-scripts" / "extracted_project" / "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"
if source_gas_project.exists():
    for f in source_gas_project.glob("*"):
        if f.is_file():
            shutil.copy2(f, gas_dir / f.name)
            print(f" -> Copied Apps Script: {f.name}")

gas_pipeline_scripts = [
    infonix_root / "gdrive-scripts" / "push_local_to_target.py",
    infonix_root / "gdrive-scripts" / "run_full_onboarding_pipeline.py",
    infonix_root / "gdrive-scripts" / "sync_apps_script_projects.py",
    infonix_root / "gdrive-scripts" / "check_drive_location.py",
    infonix_root / "gdrive-scripts" / "test_user_form_live.py",
    infonix_root / "update_appscript_and_deploy.py"
]

for s in gas_pipeline_scripts:
    if s.exists():
        shutil.copy2(s, gas_dir / s.name)
        print(f" -> Copied pipeline script: {s.name}")

# 2. Production Backend Routers
backend_routes_dir = repo_root / "backend" / "routes"
backend_routes_dir.mkdir(parents=True, exist_ok=True)

if (infonix_root / "remote_candidate_auth.js").exists():
    shutil.copy2(infonix_root / "remote_candidate_auth.js", backend_routes_dir / "candidate-auth.js")
    print(" -> Copied backend router: candidate-auth.js")

if (infonix_root / "remote_offer_letter.js").exists():
    shutil.copy2(infonix_root / "remote_offer_letter.js", backend_routes_dir / "offer-letter.js")
    print(" -> Copied backend router: offer-letter.js")

# 3. Deployment Scripts
deploy_dir = repo_root / "deployment"
deploy_dir.mkdir(parents=True, exist_ok=True)

deploy_scripts = [
    infonix_root / "scratch" / "full_deploy_and_verify.py",
    infonix_root / "scratch" / "deploy_updates.py",
    infonix_root / "scratch" / "deploy_consistent_emails.py",
    infonix_root / "scratch" / "check_remote_scores.py",
    infonix_root / "scripts" / "deploy_candidates.ps1"
]

for d in deploy_scripts:
    if d.exists():
        shutil.copy2(d, deploy_dir / d.name)
        print(f" -> Copied deploy script: {d.name}")

# 4. Brand assets
assets_dir = repo_root / "assets"
assets_dir.mkdir(parents=True, exist_ok=True)
if (infonix_root / "logo_white.png").exists():
    shutil.copy2(infonix_root / "logo_white.png", assets_dir / "logo_white.png")
    print(" -> Copied asset: logo_white.png")

# 5. Environment Template
backend_env_example = repo_root / "backend" / ".env.example"
backend_env_example.write_text("""# Infogenx Candidate Onboarding Backend Configuration
PORT=5000
NODE_ENV=production

# Database Configuration (cPanel MySQL)
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=infogenx_app
DB_PASSWORD=your_secure_password
DB_NAME=infogenx_candidates

# SMTP Configuration (Offer letter & Notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=infogenx.dm@gmail.com
SMTP_PASSWORD=your_app_password

# Owner & Notification Settings
OWNER_EMAIL=admin@infogenx.in
FORWARD_SMS_NUMBERS=+61403339424,+919787806366
DIALER_API_URL=https://twilliodialer.infogenx.com/api/send-sms

# Candidate Onboarding URLs
PORTAL_URL=https://candidates.infogenx.com
API_URL=https://api.infogenx.com
APPS_SCRIPT_URL=https://script.google.com/macros/s/AKfycbzBZ_OQKodlVo9M1bcUlBQXnZS93NxZQvJdqUIJiFf0ex6TVl-XrN0UW2sMJv8LBuyhhA/exec
""", encoding="utf-8")
print(" -> Created backend/.env.example")

print("[*] All candidate onboarding code packaged successfully!")
