import os
import sys
import re
import json
import requests
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEST_DIR = r"d:\infonix\Matrimony-Scraping"
os.makedirs(DEST_DIR, exist_ok=True)

# Google Drive folder ID
FOLDER_ID = "1s4CBPGNHYXKNcG6evUc7Q8Awv_SmLK0u"
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

def download_file(file_id, dest_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    res = session.get(url, stream=True)
    if "confirm=" in res.text:
        # Large file confirmation
        token = re.search(r"confirm=([^&]+)", res.text)
        if token:
            url = f"{url}&confirm={token.group(1)}"
            res = session.get(url, stream=True)
    with open(dest_path, "wb") as f:
        for chunk in res.iter_content(32768):
            if chunk:
                f.write(chunk)
    print(f"  [✓] Downloaded: {os.path.relpath(dest_path, DEST_DIR)} ({os.path.getsize(dest_path)} bytes)")

print(f"[+] Initialized scraper for Google Drive folder {FOLDER_ID}")
