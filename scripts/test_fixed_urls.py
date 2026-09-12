import requests, re, sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

urls = [
    "https://www.odoo.com/partners/oodu-implementers-private-limited-2199251?country_id=101",
    "https://www.odoo.com/partners/closyss-technologies-llp-13254479?country_id=101",
    "https://www.odoo.com/partners/softhealer-technologies-private-limited-13363635?country_id=101",
    "https://www.odoo.com/partners/ksolves-india-ltd-6069511?country_id=101"
]

ignored_domains = [
    "odoo.com", "odoo.sh", "odoo.fm", "odoo.org", "google.com", "wa.me", 
    "facebook.com", "linkedin.com", "twitter.com", "instagram.com", 
    "youtube.com", "tiktok.com", "github.com", "runbot.odoo.com"
]

headers = {'User-Agent': 'Mozilla/5.0'}
for u in urls:
    r = requests.get(u, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    h1 = soup.find('h1').text.strip()
    
    website = "N/A"
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http") and not any(ign in href.lower() for ign in ignored_domains):
            website = href.split("?")[0]
            break
            
    print(f"Partner: {h1}")
    print(f"  ✓ Fixed Real Website: {website}\n")
