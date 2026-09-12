import requests
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SERPER_KEY = "592605c9ec3bcff9bf492e4062ee21a1e8cd699a"

queries = [
    "site:upwork.com/jobs python",
    "site:freelancer.com/projects python",
    "site:linkedin.com/posts python developer australia",
    "site:facebook.com/permalink.php python"
]

headers = {
    "X-API-KEY": SERPER_KEY,
    "Content-Type": "application/json"
}

for q in queries:
    print("=" * 80)
    print(f" 🔎 SEARCH QUERY: {q}")
    print("=" * 80)
    try:
        res = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json={"q": q, "gl": "au", "num": 5},
            timeout=10
        )
        if res.status_code == 200:
            data = res.json()
            for item in data.get("organic", []):
                title = item.get("title", "")
                link = item.get("link", "")
                date_str = item.get("date", "")
                snippet = item.get("snippet", "")
                print(f"  Title   : {title}")
                print(f"  Link    : {link}")
                print(f"  Date    : {date_str}")
                print(f"  Snippet : {snippet[:100]}...\n")
        else:
            print(f"Serper error: {res.status_code}")
    except Exception as e:
        print(f"Error: {e}")
