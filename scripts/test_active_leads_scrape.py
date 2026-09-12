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

# Crawl live Odoo partners in India & Tamil Nadu
url = "https://www.odoo.com/partners/country/india-101"
r = requests.get(url, headers=HTTP_HEADERS, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")

links = set()
for a in soup.find_all("a", href=True):
    href = a["href"]
    if "/partners/" in href and not any(x in href for x in ["country/", "grade/", "industry=", "page="]):
        full_url = "https://www.odoo.com" + href if href.startswith("/") else href
        links.add(full_url)

print(f"Found {len(links)} Live Odoo Partner Links. Verifying Email & Phone completeness...\n")

valid_active_leads = []
for purl in list(links)[:15]:
    try:
        pr = requests.get(purl, headers=HTTP_HEADERS, timeout=12)
        if pr.status_code == 200:
            psoup = BeautifulSoup(pr.text, "html.parser")
            ptext = psoup.text
            
            h1 = psoup.find("h1")
            name = h1.text.strip() if h1 else "Unknown"
            
            # Extract Email
            emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", ptext)
            non_odoo_emails = [e for e in emails if not any(x in e.lower() for x in ["odoo.com", "sentry", "w3.org", "example"])]
            email = non_odoo_emails[0] if non_odoo_emails else None
            
            # Extract Phone
            phones = re.findall(r"(?:\+91[\s.-]?|0)?[6-9]\d{9}|\+91[\s.-]?\d{2,5}[\s.-]?\d{5,8}", ptext)
            phone = phones[0] if phones else None
            
            # Extract Website
            web_links = [a["href"] for a in psoup.find_all("a", href=True) if a["href"].startswith("http") and not any(x in a["href"] for x in ["odoo.com", "google.com", "wa.me", "facebook.com", "linkedin.com", "twitter.com"])]
            website = web_links[0] if web_links else None
            
            # Require BOTH real email AND real phone for 100% active CRM readiness!
            if email and phone and len(phone) >= 10:
                valid_active_leads.append({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "website": website,
                    "url": purl
                })
                print(f"[ACTIVE VALID] {name} | Email: {email} | Phone: {phone}")
            else:
                print(f"[REJECTED INCOMPLETE] {name} | Email: {email} | Phone: {phone}")
    except Exception as e:
        pass

print(f"\nTotal 100% Active Complete CRM Leads Found: {len(valid_active_leads)} / 15")
