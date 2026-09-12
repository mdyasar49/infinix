import os
import sys
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

gdown_bin = r"d:\infonix\internship_outreach_automation_full\.venv\Scripts\gdown.exe"

# 1. Download scrape_info.csv
subprocess.run([gdown_bin, "1wVBL-8Ve8kmMG_FSWqWp4LiMjGjjCNOq", "-O", r"d:\infonix\scrape_info.csv"])

# 2. Download Linkedin_scrape.py
subprocess.run([gdown_bin, "1YLe9tP73QfzKYVFhIWrwx9h-xd9iCxHC", "-O", r"d:\infonix\Linkedin_scrape.py"])

print("[✓] Individual files downloaded!")
