"""
Unified Master 24/7 Scraping & Dual Sync Orchestrator (Google Sheets + Zoho CRM):
Runs all lead harvesters:
1. Australia & India B2B Live Harvester (Data-Scraping)
2. Social Media Lead Scraper (Social-Media-Data-Scraping)
3. LinkedIn Cloud Lead Scraper (LinkedIn-Data-Scraping)
4. Uploads all verified leads to Google Sheets & Zoho CRM
"""

import os
import sys
import subprocess
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_EXE = sys.executable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}", flush=True)

def run_scraper(repo_name, script_name):
    repo_path = os.path.join(BASE_DIR, repo_name)
    script_path = os.path.join(repo_path, script_name)
    
    if not os.path.exists(script_path):
        log(f"[-] Script not found: {script_path}")
        return False
        
    log(f"==================================================")
    log(f"[*] RUNNING: {repo_name} -> {script_name}")
    log(f"==================================================")
    
    try:
        proc = subprocess.run([PYTHON_EXE, script_path], cwd=repo_path, capture_output=False)
        if proc.returncode == 0:
            log(f"[✓] SUCCESS: {repo_name} completed and synced.")
            return True
        else:
            log(f"[-] FAILED with code {proc.returncode}: {repo_name}")
            return False
    except Exception as e:
        log(f"[!] Error executing {repo_name}: {e}")
        return False

def main():
    log("================================================================================")
    log("🚀 STARTING UNIFIED 24/7 B2B SCRAPING & DUAL SYNC SCHEDULE RUN")
    log("================================================================================")
    
    # 1. Run Data-Scraping (Australia Top-Priority + India B2B Harvester)
    run_scraper("Data-Scraping", "sync_to_google_sheet.py")
    
    # 2. Run Social-Media-Data-Scraping
    run_scraper("Social-Media-Data-Scraping", "sync_to_google_sheet.py")
    
    # 3. Run LinkedIn-Data-Scraping
    run_scraper("LinkedIn-Data-Scraping", "sync_to_google_sheet.py")
    
    log("================================================================================")
    log("🎉 ALL SCRAPERS COMPLETED & SYNCED TO GOOGLE SHEETS & ZOHO CRM!")
    log("================================================================================")

if __name__ == "__main__":
    main()
