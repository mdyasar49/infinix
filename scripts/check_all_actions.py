import urllib.request
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
repos = [
    "Data-Scraping",
    "Social-Media-Data-Scraping",
    "LinkedIn-Data-Scraping",
    "internship_outreach_automation_full",
    "google-apps-script"
]

print("=" * 95)
print(" 🚀 REAL-TIME GITHUB ACTIONS DEPLOYMENT & CI/CD PIPELINE STATUS")
print("=" * 95)

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
            runs = data.get("workflow_runs", [])
            if runs:
                latest = runs[0]
                print(f"[✓] {r:<38}: Run #{latest['run_number']:<3} | Event: {latest['event']:<8} | Status: {latest['status']:<11} | Conclusion: {str(latest['conclusion']):<9} | URL: {latest['html_url']}")
            else:
                print(f"[✓] {r:<38}: Workflow active and waiting for hourly trigger!")
    except Exception as e:
        print(f"[!] {r}: {e}")

print("=" * 95)
