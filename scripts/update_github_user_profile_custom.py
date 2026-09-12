import urllib.request
import json
import subprocess
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
USER_NAME = "mdyasar49"
DEV_EMAIL = "mdyasardeveloper786@gmail.com"
PORTFOLIO_URL = "https://github.com/mdyasar49"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Python"
}

NEW_PROFILE_DATA = {
    "name": "Mohamed Yasar",
    "company": "Independent Full-Stack AI Consultant",
    "blog": PORTFOLIO_URL,
    "location": "Chennai, India / Remote Worldwide",
    "bio": f"⚡ Senior Full-Stack AI & Enterprise Software Architect | Web Scrapers, Twilio Telephony & SaaS Web Apps. Contact: {DEV_EMAIL}",
    "hireable": True
}

NEW_PROFILE_README = f"""<p align="center">
  <img src="avatar_gold.jpg" width="220" style="border-radius: 16px; margin: 5px;" alt="Mohamed Yasar Avatar" />
</p>

<h1 align="center">Mohamed Yasar 👋</h1>
<h3 align="center">🚀 Senior Full-Stack AI Architect & Enterprise Software Specialist</h3>

<p align="center">
  <i>Specializing in <b>B2B Web Scraping Systems</b>, <b>Twilio Cloud Telephony Apps</b>, <b>Conversational AI Voice Bots</b>, and <b>React/Node/Python SaaS Applications</b> for clients worldwide.</i>
</p>

---

### 🎨 Profile Avatar Theme Options

| 1. Luxury Gold & Amber | 2. Emerald Green & Cyan | 3. Cyberpunk Violet & Magenta | 4. Crimson Red & Gold |
| :-: | :-: | :-: | :-: |
| <img src="avatar_gold.jpg" width="160" /> | <img src="avatar_emerald.jpg" width="160" /> | <img src="avatar_violet.jpg" width="160" /> | <img src="avatar_crimson.jpg" width="160" /> |

---

### 🛠️ Core Engineering Capabilities:
- 🤖 **AI & Voice Automation**: Real-time Gemini AI Assistants, WebRTC Voice Bots, Speech Intelligence.
- 📞 **Cloud Telephony & Call Centers**: Custom Twilio WebRTC Dialers, Auto-Call Dispatchers, PBX Systems.
- 🔍 **Web Scraping & Lead Engines**: Multi-channel B2B crawlers (LinkedIn, Google Maps, Facebook, Directories).
- 💻 **Full-Stack Web Development**: Modern React/Vite Frontends, Node.js & Django REST APIs, Microservices.
- 🎓 **Academic & Portal Solutions**: Custom Student Portals, Analytics Dashboards & Data Processing Engines.

---

### 💻 Core Tech Stack:
- **Languages**: Python, JavaScript/TypeScript, HTML5, CSS3, SQL, Shell
- **Frameworks**: Django, Node.js, Express, React, Vite, FastAPI
- **Databases & Cloud**: MySQL, PostgreSQL, SQLite, Google Cloud Platform (GCP), CloudPanel, Docker
- **APIs & Tools**: Twilio Voice API, Google Gemini AI API, Zoho CRM API, Google Sheets API

---

### 📬 Direct Contact & Consultations:
- 📧 **Official Email**: [{DEV_EMAIL}](mailto:{DEV_EMAIL})
- 🌐 **GitHub Portfolio**: [{PORTFOLIO_URL}]({PORTFOLIO_URL})
- 🤝 **Available For**: Freelance Contracts, Direct Client Retainers, Technical Architecture & Software Projects.

---
*⚡ "Building robust, scalable, high-margin software systems for modern businesses."*
"""

def update_profile_api():
    print("[+] Updating GitHub User Profile API Settings...")
    url = "https://api.github.com/user"
    payload = json.dumps(NEW_PROFILE_DATA).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            print("  [✓] GitHub Profile API settings updated successfully!")
    except Exception as e:
        print(f"  [!] Error updating profile API: {e}")

def update_profile_readme():
    print("[+] Updating Profile README on mdyasar49/mdyasar49...")
    readme_dir = os.path.join(r"d:\infonix", "scratch", "profile_readme")
    readme_path = os.path.join(readme_dir, "README.md")
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(NEW_PROFILE_README)

    auth_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{USER_NAME}.git"
    clean_remote = f"https://github.com/{USER_NAME}/{USER_NAME}.git"

    subprocess.run(["git", "add", "."], cwd=readme_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Update profile details & skills overview"], cwd=readme_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    res = subprocess.run(["git", "push", "-u", auth_remote, "main", "--force"], cwd=readme_dir, capture_output=True, text=True)
    subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=readme_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if res.returncode == 0:
        print("  [🎉] SUCCESS: Profile README updated and pushed to GitHub!")
    else:
        print(f"  [!] Push Error: {res.stderr}")

def main():
    print("=" * 80)
    print(" 🚀 CUSTOMIZING GITHUB USER PROFILE Settings FOR @mdyasar49")
    print("=" * 80)

    update_profile_api()
    update_profile_readme()

    print("=" * 80)

if __name__ == "__main__":
    main()
