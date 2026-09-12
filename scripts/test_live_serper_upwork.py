import requests
import json
import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

serper_key = "592605c9ec3bcff9bf492e4062ee21a1e8cd699a"
headers = {"X-API-KEY": serper_key, "Content-Type": "application/json"}

queries = [
    'site:upwork.com/jobs "python"',
    'site:upwork.com/jobs "react"',
    'site:upwork.com/jobs "developer"',
    'site:upwork.com/jobs "automation"',
    'site:upwork.com/jobs "scraping"',
    'site:upwork.com/jobs "australia"'
]

print("Fetching LIVE direct Upwork job URLs via Serper API...")
found_jobs = []

for q in queries:
    res = requests.post(
        "https://google.serper.dev/search",
        headers=headers,
        json={"q": q, "gl": "au", "num": 10},
        timeout=10
    )
    if res.status_code == 200:
        data = res.json()
        for item in data.get("organic", []):
            link = item.get("link", "")
            title = item.get("title", "").replace(" - Upwork", "").strip()
            snippet = item.get("snippet", "")
            date = item.get("date", "")
            
            if "upwork.com/jobs" in link:
                found_jobs.append((title, link, date, snippet))

print(f"Found {len(found_jobs)} direct live Upwork jobs!")
for idx, (t, l, d, s) in enumerate(found_jobs[:10], 1):
    print(f"\n[{idx}] {t}")
    print(f"    🔗 Direct Post URL : {l}")
    print(f"    📅 Posted Date    : {d}")
    print(f"    📝 Snippet        : {s[:120]}...")
