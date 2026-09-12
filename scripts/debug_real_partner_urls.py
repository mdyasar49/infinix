import os
import sys
import re
import requests
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

test_urls = [
    "https://www.odoo.com/partners/oodu-implementers-private-limited-2199251?country_id=101",
    "https://www.odoo.com/partners/closyss-technologies-llp-13254479?country_id=101",
    "https://www.odoo.com/partners/softhealer-technologies-private-limited-13363635?country_id=101",
    "https://www.odoo.com/partners/ksolves-india-ltd-6069511?country_id=101"
]

for purl in test_urls:
    print(f"\n==================================================")
    print(f"Inspecting Profile URL: {purl}")
    print(f"==================================================")
    r = requests.get(purl, headers=HTTP_HEADERS, timeout=12)
    soup = BeautifulSoup(r.text, "html.parser")
    
    h1 = soup.find("h1")
    name = h1.text.strip() if h1 else "Unknown"
    
    # Find all <a> tags with href
    all_links = soup.find_all("a", href=True)
    
    # Look for website link (often has icon or text, or contains company domain)
    website_link = None
    for a in all_links:
        href = a["href"]
        text = a.text.strip()
        # Look for links that lead to external company websites
        if href.startswith("http") and not any(x in href.lower() for x in ["odoo.com", "odoo.sh", "google.com", "wa.me", "facebook.com", "linkedin.com", "twitter.com", "instagram.com", "youtube.com"]):
            website_link = href
            break
            
    # Also check if website is displayed in text or contact box
    contact_box = soup.find("div", id="partner_contact")
    if contact_box:
        print("Contact Box Text:\n", contact_box.text.strip())
        
    print(f"\nPartner Name   : {name}")
    print(f"Extracted Website: {website_link}")
    
    # Print all external links found on the page
    ext_links = [a["href"] for a in all_links if a["href"].startswith("http")]
    print(f"All HTTP Links Found ({len(ext_links)}):")
    for el in ext_links:
        print("   ->", el)
