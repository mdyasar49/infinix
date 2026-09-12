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

# Fetch Odoo Partners in India
url = "https://www.odoo.com/partners/country/india-101"
print(f"Fetching Live India Odoo Partners Page: {url}")
r = requests.get(url, headers=headers, timeout=15)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    # Find all individual partner profile URLs
    partner_urls = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/partners/" in href and not any(x in href for x in ["country/", "grade/", "industry=", "page="]):
            full_url = "https://www.odoo.com" + href if href.startswith("/") else href
            partner_urls.add(full_url)
            
    print(f"Total Unique Live India Partner Profile URLs Found: {len(partner_urls)}")
    
    # Inspect first 3 partner profile pages live
    for purl in list(partner_urls)[:3]:
        print(f"\n--------------------------------------------------")
        print(f"Scraping Live Partner Page: {purl}")
        pr = requests.get(purl, headers=headers, timeout=15)
        if pr.status_code == 200:
            psoup = BeautifulSoup(pr.text, "html.parser")
            
            # Extract Name
            h1 = psoup.find("h1")
            name = h1.text.strip() if h1 else "Unknown"
            
            # Extract Address / Contact info
            contact_div = psoup.find("div", id="partner_contact") or psoup.find("div", class_=re.compile(r"contact|address", re.I))
            address_text = contact_div.text.strip() if contact_div else psoup.text[:500]
            
            # Extract Phone
            phones = re.findall(r"(?:\+91[\s.-]?|0)?[6-9]\d{9}|\+91[\s.-]?\d{2,4}[\s.-]?\d{6,8}", psoup.text)
            
            # Extract Website
            web_link = None
            for wa in psoup.find_all("a", href=True):
                w_href = wa["href"]
                if w_href.startswith("http") and "odoo.com" not in w_href and "google.com" not in w_href:
                    web_link = w_href
                    break
                    
            print(f"Partner Name: {name}")
            print(f"Website     : {web_link}")
            print(f"Phones Found: {set(phones)}")
            print(f"Snippet     : {address_text[:200]}...")
