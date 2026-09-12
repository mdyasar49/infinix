import requests

urls_to_test = [
    "https://www.upwork.com/nx/search/jobs/?q=python",
    "https://www.upwork.com/freelance-jobs/python/",
    "https://www.freelancer.com/projects/web-development/Modern-Prop-Firm-Website-Build",
    "https://www.freelancer.com/jobs/",
    "https://www.linkedin.com/company/qantas",
    "https://www.linkedin.com/company/deloitte",
    "https://www.linkedin.com/company/telstra",
    "https://www.facebook.com/vbctampa",
    "https://www.facebook.com/faytthestore",
    "https://www.facebook.com/paintprotectionfilmperth"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Testing Real Web URLs HTTP status codes...")
for url in urls_to_test:
    try:
        res = requests.get(url, headers=headers, timeout=5)
        print(f"[{res.status_code}] {url}")
    except Exception as e:
        print(f"[ERR] {url} -> {e}")
