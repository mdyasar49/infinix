import os
import sys
import gdown

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEST_DIR = r"d:\infonix\Matrimony-Scraping"
os.makedirs(DEST_DIR, exist_ok=True)

# Google Drive folder ID
FOLDER_URL = "https://drive.google.com/drive/folders/1s4CBPGNHYXKNcG6evUc7Q8Awv_SmLK0u"

print(f"[+] Starting download to {DEST_DIR}...")
try:
    # Use gdown to download folder
    gdown.download_folder(FOLDER_URL, output=DEST_DIR, quiet=False, use_cookies=False)
    print("[✓] Download completed successfully!")
except Exception as e:
    print(f"[!] Error during download: {e}")
