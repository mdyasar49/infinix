import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://www.odoo.com/partners/grade/gold-2'
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, 'html.parser')

print(f"Gold Page status: {resp.status_code}")

for a in soup.find_all('a', href=True):
    href = a['href']
    text = a.get_text(strip=True)
    if '/partners/' in href and not any(k in href for k in ['country', 'grade', 'category', 'industry', 'page', 'register']):
        print(f"Gold Partner: {href} -> {text}")
