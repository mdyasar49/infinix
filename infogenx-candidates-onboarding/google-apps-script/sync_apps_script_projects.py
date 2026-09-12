"""
Google Apps Script End-to-End Migration Script
=============================================
Source Project:
  ID:  1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p
  URL: https://script.google.com/home/projects/1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p/edit

Target Project:
  ID:  1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww
  URL: https://script.google.com/u/2/home/projects/1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww/edit
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SOURCE_ID = "1OEQHX65jAAkKmmhBvr73cZZUstCkgetZjjcTwI_weP8kay2u3XVuB40p"
TARGET_ID = "1KCvVM5_9iTYM484tL7Y2TeZq4QFR6EeA7xMpSwLnMolNTXQk3L_PBPww"

BASE_DIR = Path(__file__).parent
WORK_DIR = BASE_DIR / "apps_script_workspace"
SOURCE_DIR = WORK_DIR / "source"
TARGET_DIR = WORK_DIR / "target"

def run_cmd(cmd, cwd=None):
    print(f"[*] Executing: {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print(f"[stderr] {res.stderr}")
    return res.returncode == 0

def setup_directories():
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

def migrate_with_clasp():
    print("=" * 60)
    print("GOOGLE APPS SCRIPT END-TO-END MIGRATION")
    print("=" * 60)
    print(f"Source ID : {SOURCE_ID}")
    print(f"Target ID : {TARGET_ID}")
    print("=" * 60)

    setup_directories()

    # Step 1: Create .clasp.json for source
    source_clasp_config = {
        "scriptId": SOURCE_ID,
        "rootDir": str(SOURCE_DIR)
    }
    with open(SOURCE_DIR / ".clasp.json", "w", encoding="utf-8") as f:
        json.dump(source_clasp_config, f, indent=2)

    print("\n[Step 1] Pulling all code from Source Project...")
    success = run_cmd("npx @google/clasp pull", cwd=str(SOURCE_DIR))
    if not success:
        print("[!] Note: If not logged in, please run: npx @google/clasp login")
        return False

    # List pulled files
    pulled_files = list(SOURCE_DIR.glob("*.*"))
    print(f"[+] Successfully extracted {len(pulled_files)} files from source:")
    for pf in pulled_files:
        if pf.name != ".clasp.json":
            print(f"    - {pf.name} ({pf.stat().st_size} bytes)")

    # Step 2: Copy files to target directory
    print(f"\n[Step 2] Preparing Target Project ({TARGET_ID})...")
    for pf in pulled_files:
        if pf.name != ".clasp.json":
            shutil.copy2(pf, TARGET_DIR / pf.name)

    # Configure target .clasp.json
    target_clasp_config = {
        "scriptId": TARGET_ID,
        "rootDir": str(TARGET_DIR)
    }
    with open(TARGET_DIR / ".clasp.json", "w", encoding="utf-8") as f:
        json.dump(target_clasp_config, f, indent=2)

    # Step 3: Push to Target
    print("\n[Step 3] Pushing all code to Target Project...")
    push_success = run_cmd("npx @google/clasp push --force", cwd=str(TARGET_DIR))
    if push_success:
        print("\n" + "=" * 60)
        print("✅ SUCCESS: Google Apps Script migration completed successfully!")
        print(f"Target Project Live at: https://script.google.com/u/2/home/projects/{TARGET_ID}/edit")
        print("=" * 60)
        return True
    else:
        print("[!] Push to target project failed.")
        return False

if __name__ == "__main__":
    migrate_with_clasp()
