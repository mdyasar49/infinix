import urllib.request
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
url = "https://api.github.com/repos/mdyasar49/odoo-lead-generator/actions/runs"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Infogenx"
}

req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode("utf-8"))

for r in data["workflow_runs"][:3]:
    print(f"Run #{r['run_number']} | Status: {r['status']} | Conclusion: {r['conclusion']} | URL: {r['html_url']}")
