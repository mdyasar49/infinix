import urllib.request
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
repos = ["Data-Scraping", "Social-Media-Data-Scraping", "internship_outreach_automation_full"]

print("=" * 80)
print(" 🚀 CURRENT GITHUB ACTIONS STATUS FOR SCRAPING & AUTOMATION PIPELINES")
print("=" * 80)

for r in repos:
    url = f"https://api.github.com/repos/mdyasar49/{r}/actions/runs"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Infogenx"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data["workflow_runs"]:
                latest = data["workflow_runs"][0]
                print(f"[✓] {r:<35}: Run #{latest['run_number']} | Status: {latest['status']:<12} | URL: {latest['html_url']}")
            else:
                print(f"[✓] {r:<35}: Pipeline configured and ready for scheduled/manual trigger!")
    except Exception as e:
        print(f"[!] {r}: {e}")
