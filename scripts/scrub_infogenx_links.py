import urllib.request
import json
import subprocess
import os
import sys
import re

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

PROFILE_DATA_CLEAN = {
    "name": "Mohamed Yasar",
    "company": "Independent Full-Stack AI & Software Consultant",
    "blog": PORTFOLIO_URL,
    "location": "Chennai, India / Remote Worldwide",
    "bio": f"⚡ Senior AI & Enterprise Software Architect | Web Crawlers, Twilio Telephony & Full-Stack Web Apps. Contact: {DEV_EMAIL}",
    "hireable": True
}

CLEAN_PROFILE_README = f"""<p align="center">
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

### 💼 Past Technical Projects & Portfolio:
- **Cloud Dialer Engine**: Built enterprise Twilio Cloud Dialer, Auto-call dispatchers & WebRTC calling systems.
- **B2B Scraping Pipeline**: Anti-detect multi-channel web crawlers for LinkedIn, Google Maps & Social Media.
- **AI Speech Assistant**: Real-time Gemini AI voice agents & multimodal media analyzers.

---

### 💻 Core Tech Stack:
- **Languages**: Python, JavaScript/TypeScript, HTML5, CSS3, SQL, Shell
- **Frameworks & Libraries**: Django, Node.js, Express, React, Vite, FastAPI
- **Databases & Cloud**: MySQL, PostgreSQL, SQLite, Google Cloud Platform (GCP), CloudPanel, Docker
- **APIs & Tools**: Twilio Voice API, Google Gemini AI API, Zoho CRM API, Google Sheets API

---

### 📬 Let's Work Together! (Hire / Contract Me)
- 📧 **Direct Email**: [{DEV_EMAIL}](mailto:{DEV_EMAIL})
- 🌐 **GitHub Portfolio**: [{PORTFOLIO_URL}]({PORTFOLIO_URL})
- 🤝 **Available For**: Direct Client Contracts, Technical Consultations, Custom Software Development & Retainers.

---
*⚡ "Transforming complex business workflows into automated, high-margin software solutions."*
"""

def update_user_profile():
    print("[+] Updating User Profile (Removing infogenx website/links)...")
    url = "https://api.github.com/user"
    payload = json.dumps(PROFILE_DATA_CLEAN).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            print("  [✓] User Profile updated cleanly!")
    except Exception as e:
        print(f"  [!] Profile update output: {e}")

def update_profile_readme():
    print("[+] Updating Profile README on mdyasar49/mdyasar49 (Removing infogenx website/links)...")
    readme_dir = os.path.join(r"d:\infonix", "scratch", "profile_readme")
    readme_path = os.path.join(readme_dir, "README.md")
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(CLEAN_PROFILE_README)

    auth_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{USER_NAME}.git"
    clean_remote = f"https://github.com/{USER_NAME}/{USER_NAME}.git"

    subprocess.run(["git", "add", "."], cwd=readme_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Scrub infogenx links/emails & update clean portfolio links"], cwd=readme_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    res = subprocess.run(["git", "push", "-u", auth_remote, "main", "--force"], cwd=readme_dir, capture_output=True, text=True)
    subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=readme_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if res.returncode == 0:
        print("  [🎉] SUCCESS: Profile README updated cleanly!")
    else:
        print(f"  [!] Push Error: {res.stderr}")

def scrub_scripts():
    print("[+] Scrubbing infogenx website & emails from all outreach scripts...")
    script_files = [
        os.path.join(r"d:\infonix", "scripts", "resume_client_acquisition_engine.py"),
        os.path.join(r"d:\infonix", "scripts", "48hr_client_acquisition_engine.py")
    ]
    for sf in script_files:
        if os.path.exists(sf):
            with open(sf, "r", encoding="utf-8") as f:
                content = f.read()
            # Replace infogenx.com with github portfolio
            content = re.sub(r"https://infogenx\.com", PORTFOLIO_URL, content)
            content = re.sub(r"admin@infogenx\.com", DEV_EMAIL, content)
            content = re.sub(r"Infogenx Tech Solutions", "Independent Software Consultant", content)
            with open(sf, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [✓] Scrubbed: {os.path.basename(sf)}")

def main():
    print("=" * 80)
    print(" 🚀 SCRUBBING INFOGENX LINKS & EMAILS FOR CLIENT PRIVACY")
    print("=" * 80)

    update_user_profile()
    update_profile_readme()
    scrub_scripts()

    print("=" * 80)

if __name__ == "__main__":
    main()
