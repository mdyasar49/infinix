import os
import sys
import json
import requests
import re
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SERPER_KEY = "592605c9ec3bcff9bf492e4062ee21a1e8cd699a"

print(f"[LIVE TEST] Using Serper.dev API Key: {SERPER_KEY[:8]}...")

# Query Serper for Live Odoo Sales Representatives / Account Executives / Solution Architects
serper_url = "https://google.serper.dev/search"
payload = json.dumps({
    "q": "site:linkedin.com/in \"Odoo\" (\"Sales Executive\" OR \"Account Executive\" OR \"Sales Manager\")",
    "num": 20
})
headers = {
    "X-API-KEY": SERPER_KEY,
    "Content-Type": "application/json"
}

res = requests.post(serper_url, headers=headers, data=payload, timeout=10)
print(f"HTTP Status Code: {res.status_code}")

if res.status_code == 200:
    data = res.json()
    organic = data.get("organic", [])
    print(f"Live Organic Profiles Discovered: {len(organic)}\n")
    for idx, item in enumerate(organic, 1):
        print(f"#{idx} Title  : {item.get('title')}")
        print(f"    Link   : {item.get('link')}")
        print(f"    Snippet: {item.get('snippet')}\n")
