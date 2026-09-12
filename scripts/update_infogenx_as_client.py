import urllib.request
import json
import subprocess
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
USER_NAME = "mdyasar49"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Python"
}

USER_PROFILE_UPDATE = {
    "name": "Mohamed Yasar",
    "company": "Independent Software Consultant",
    "blog": "https://github.com/mdyasar49",
    "location": "Chennai, India / Remote Worldwide",
    "bio": "⚡ Senior AI & Enterprise Software Architect | Specialist in Web Crawlers, Twilio Telephony & Full-Stack Apps. Open for Freelance & Technical Contracts.",
    "hireable": True
}

CORRECTED_PROFILE_README = """<p align="center">
  <img src="avatar_gold.jpg" width="220" style="border-radius: 16px; margin: 5px;" alt="Mohamed Yasar Avatar" />
</p>

<h1 align="center">Mohamed Yasar 👋</h1>
<h3 align="center">🚀 Senior AI & Enterprise Software Architect | Independent Full-Stack Engineer</h3>

<p align="center">
  <i>Building high-margin <b>B2B Lead Generation Engines</b>, <b>Twilio Cloud Telephony Apps</b>, <b>Conversational AI Voice Bots</b>, and <b>Enterprise Integrations</b> for clients worldwide.</i>
</p>

---

### 🎨 Profile Avatar Theme Options

| 1. Luxury Gold & Amber | 2. Emerald Green & Cyan | 3. Cyberpunk Violet & Magenta | 4. Crimson Red & Gold |
| :-: | :-: | :-: | :-: |
| <img src="avatar_gold.jpg" width="160" /> | <img src="avatar_emerald.jpg" width="160" /> | <img src="avatar_violet.jpg" width="160" /> | <img src="avatar_crimson.jpg" width="160" /> |

---

### 🛠️ Core Services & Engineering Expertise:
- 🤖 **AI & Voice Automation**: Custom Gemini AI Bots, WebRTC Voice Agents, Live Speech Intelligence.
- 📞 **Cloud Telephony & Call Centers**: Custom Twilio Web Dialers, Auto-Call Dispatchers, PBX Systems.
- 🔍 **Web Scraping & Lead Engines**: Anti-detect multi-platform scrapers (LinkedIn, Facebook, Google Maps, Instagram).
- 💻 **Full-Stack Web Development**: High-converting React/Vite frontends, Node.js & Django REST APIs.
- ⚙️ **Custom Enterprise Integrations**: REST API Connectors, Two-way Sync Engines, Data Migration Pipelines.

---

### 💼 Major Client Work & Case Studies:
- **Infogenx**: Built enterprise Twilio Cloud Dialer, Automated Social Lead Scrapers, and Multi-channel Lead Pipelines.
- **Enterprise Clients**: High-scale data scraping, Google Workspace Apps Script automations, and custom web portals.

---

### 💻 Core Tech Stack:
- **Languages**: Python, JavaScript/TypeScript, HTML5, CSS3, SQL, Shell
- **Frameworks & Libraries**: Django, Node.js, Express, React, Vite, FastAPI
- **Databases & Cloud**: MySQL, PostgreSQL, SQLite, Google Cloud Platform (GCP), CloudPanel, Docker
- **APIs & Tools**: Twilio Voice API, Google Gemini AI API, Zoho CRM API, Google Sheets API

---

### 📬 Let's Work Together! (Hire / Contract Me)
- 📧 **Direct Email**: [mohamedyasar081786@gmail.com](mailto:mohamedyasar081786@gmail.com)
- 🌐 **GitHub Portfolio**: [github.com/mdyasar49](https://github.com/mdyasar49)
- 🤝 **Available For**: Direct Client Contracts, Technical Consultations, Custom Software Development & Retainers.

---
*⚡ "Transforming complex business workflows into automated, high-margin software solutions."*
"""

def update_user_profile():
    print("[+] Updating User Profile (Setting Company = Independent Software Consultant)...")
    url = "https://api.github.com/user"
    payload = json.dumps(USER_PROFILE_UPDATE).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            print("  [✓] User Profile updated successfully!")
    except Exception as e:
        print(f"  [!] Error updating profile: {e}")

def update_profile_readme():
    print("[+] Updating Profile README on mdyasar49/mdyasar49...")
    readme_dir = os.path.join(r"d:\infonix", "scratch", "profile_readme")
    readme_path = os.path.join(readme_dir, "README.md")
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(CORRECTED_PROFILE_README)

    auth_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{USER_NAME}.git"
    clean_remote = f"https://github.com/{USER_NAME}/{USER_NAME}.git"

    subprocess.run(["git", "add", "."], cwd=readme_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Clarify Infogenx as key client & update profile to Independent Consultant"], cwd=readme_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    res = subprocess.run(["git", "push", "-u", auth_remote, "main", "--force"], cwd=readme_dir, capture_output=True, text=True)
    subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=readme_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if res.returncode == 0:
        print("  [🎉] SUCCESS: Profile README updated and pushed to GitHub!")
    else:
        print(f"  [!] Push Error: {res.stderr}")

def main():
    print("=" * 80)
    print(" 🚀 UPDATING PROFILE: SETTING INFOGENX AS CLIENT & INDEPENDENT CONSULTANT")
    print("=" * 80)

    update_user_profile()
    update_profile_readme()

    print("=" * 80)

if __name__ == "__main__":
    main()
