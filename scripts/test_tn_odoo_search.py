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

tn_search_urls = [
    "https://www.odoo.com/partners?search=Chennai",
    "https://www.odoo.com/partners?search=Coimbatore",
    "https://www.odoo.com/partners?search=Tamil+Nadu",
    "https://www.odoo.com/partners/country/india-101"
]

tn_partner_links = set()

for url in tn_search_urls:
    print(f"\nFetching TN Search URL: {url}", flush=True)
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/partners/" in href and not any(x in href for x in ["country/", "grade/", "industry=", "page=", "search="]):
                    full_link = "https://www.odoo.com" + href if href.startswith("/") else href
                    tn_partner_links.add(full_link)
    except Exception as e:
        print(f"Error: {e}")

print(f"\nTotal Unique Tamil Nadu & India Partner Profile URLs Found: {len(tn_partner_links)}", flush=True)
for l in list(tn_partner_links)[:10]:
    print("  -", l)
