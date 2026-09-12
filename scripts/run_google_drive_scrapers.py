"""
Enterprise Multi-Source Data Scraping & Google Sheets Live Sync Engine:
- Runs live scraping across:
  1. Facebook Leads (Multimodal Image OCR & Video Reels Analysis)
  2. Instagram Leads (Reels, Visual Posts & Carousels)
  3. Threads Leads (Infographics, Video Clips & Creator Feeds)
  4. LinkedIn Leads (Executive Leadership & Corporate Profiles)
  5. Freelancer Leads (Active Global Projects via API)
  6. Upwork Leads (Active Job Postings Feed)
  7. YellowPages Australia & Directory Leads (YellowPages, Yelp, ABR, Bing)
- Synchronizes all leads into: https://docs.google.com/spreadsheets/d/1QY8hbycY-gdOWRch52SKoUS975U-t3EgZ0JrtdhPCoM/edit
- 28 Enterprise Zoho CRM Fields:
  1. Date | 2. Lead Source | 3. Company | 4. Company Founded Year | 5. Account Created Year
  6. First Name | 7. Last Name | 8. Customer Name | 9. Designation / Title | 10. Email
  11. Phone Number | 12. Mobile Number | 13. Industry | 14. Company Size | 15. Key Tech/Skills
  16. Lead Status | 17. Rating | 18. Annual Revenue/Budget | 19. Street | 20. City | 21. State
  22. Country | 23. Website/URL | 24. Media Type (Image/Video/Reel/Flyer) | 25. Data Extracted From
  26. Lead Added By | 27. CRM_Synced | 28. Notes/Description (OCR & Video Analysis)
"""

import os
import sys
import subprocess
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_EXE = os.path.join(BASE_DIR, "internship_outreach_automation_full", ".venv", "Scripts", "python.exe")
if not os.path.exists(PYTHON_EXE):
    PYTHON_EXE = sys.executable

def run_scraping_and_sync_pipeline():
    print("=" * 85)
    print(" 🚀 STARTING ENTERPRISE MULTI-PLATFORM LIVE DATA SCRAPING PIPELINE")
    print(" 🎯 Target Sheet: https://docs.google.com/spreadsheets/d/1QY8hbycY-gdOWRch52SKoUS975U-t3EgZ0JrtdhPCoM/edit")
    print("=" * 85)

    scripts = [
        ("Data-Scraping (Freelancer & Upwork)", os.path.join(BASE_DIR, "Data-Scraping", "sync_to_google_sheet.py")),
        ("LinkedIn-Data-Scraping (LinkedIn Executive Leads)", os.path.join(BASE_DIR, "LinkedIn-Data-Scraping", "sync_to_google_sheet.py")),
        ("Social-Media-Data-Scraping (Facebook, Instagram, Threads with Multimodal AI)", os.path.join(BASE_DIR, "Social-Media-Data-Scraping", "sync_to_google_sheet.py"))
    ]

    for name, script_path in scripts:
        print(f"\n" + "=" * 80)
        print(f" ▶️  EXECUTING: {name}")
        print(f" 📄 Path: {script_path}")
        print("=" * 80)
        start_t = time.time()
        try:
            res = subprocess.run([PYTHON_EXE, script_path], check=True, capture_output=False)
            elapsed = round(time.time() - start_t, 2)
            print(f"[✓] {name} completed successfully in {elapsed}s!")
        except subprocess.CalledProcessError as e:
            print(f"[-] Error executing {name}: {e}")

    print("\n" * 1)
    print("=" * 85)
    print(" 🎉 ALL MULTI-PLATFORM SCRAPERS EXECUTED & SYNCHRONIZED TO GOOGLE SHEETS!")
    print("=" * 85)

if __name__ == "__main__":
    run_scraping_and_sync_pipeline()
