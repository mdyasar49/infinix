import urllib.request
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
url = "https://api.github.com/repos/mdyasar49/Data-Scraping/actions/runs/33237135802/jobs"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Infogenx"
}

req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode("utf-8"))

for j in data["jobs"]:
    print(f"Job: {j['name']} | Status: {j['status']} | Conclusion: {j['conclusion']}")
    for s in j["steps"]:
        print(f"  Step #{s['number']} '{s['name']}': status={s['status']}, conclusion={s['conclusion']}")
