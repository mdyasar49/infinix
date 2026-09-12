import os
import sys
import re
import requests
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Fetch top Odoo partner pages
urls = [
    "https://www.odoo.com/partners/country/australia-14",
    "https://www.odoo.com/partners/country/india-101",
    "https://www.odoo.com/partners/country/united-states-225"
]

for target_url in urls:
    print(f"\n==================================================")
    print(f"Fetching Live Page: {target_url}")
    print(f"==================================================")
    try:
        r = requests.get(target_url, headers=headers, timeout=12)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            
            # Find all links pointing to individual partner profile pages
            links = soup.find_all("a", href=True)
            partner_links = set()
            for a in links:
                href = a["href"]
                if "/partners/" in href and not any(x in href for x in ["country/", "grade/", "industry=", "page="]):
                    full_link = "https://www.odoo.com" + href if href.startswith("/") else href
                    partner_links.add((a.text.strip(), full_link))
                    
            print(f"Discovered {len(partner_links)} Live Odoo Partner Profile Pages!")
            for name, purl in list(partner_links)[:5]:
                print(f"  - Partner: {name} | Link: {purl}")
                
    except Exception as e:
        print(f"Error: {e}")
