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

PROFILE_DATA = {
    "name": "Mohamed Yasar",
    "company": "Infogenx Tech Solutions",
    "blog": "https://infogenx.com",
    "location": "Chennai, India / Remote Worldwide",
    "bio": "⚡ AI & Enterprise Automation Architect | Odoo ERP, Custom Web Crawlers, Twilio Telephony, Full-Stack Web & Mobile Solutions. Available for Hire & Technical Contracts.",
    "hireable": True
}

REPO_METADATA = {
    "blog-api": {
        "description": "🚀 High-Performance Node.js & Express REST API for Automated Content Publishing & SEO Optimization",
        "topics": ["nodejs", "express", "rest-api", "seo-automation", "backend", "javascript"]
    },
    "blog-react": {
        "description": "✨ Modern, Responsive React & Vite Frontend for Enterprise Content Management & Blog Applications",
        "topics": ["react", "vite", "frontend", "javascript", "ui-design", "web-development"]
    },
    "Data-Scraping": {
        "description": "⚡ Scalable Multi-Channel B2B Web Scraping Engine with Automated Google Sheets & CRM Integration",
        "topics": ["python", "web-scraping", "lead-generation", "google-sheets-api", "automation", "data-extraction"]
    },
    "dev": {
        "description": "⚙️ Enterprise Software Development Environment & Full-Stack Core Utilities",
        "topics": ["fullstack", "architecture", "enterprise", "web-apps", "automation"]
    },
    "google-apps-script": {
        "description": "🤖 Enterprise Google Apps Script Automation & AI Lead Enrichment Workflows for Google Workspace",
        "topics": ["google-apps-script", "google-sheets", "automation", "gemini-ai", "workflow-automation"]
    },
    "infogenx-twilio-dialer": {
        "description": "📞 Production-Ready Django & Twilio Cloud Dialer Engine with Live Call Intelligence & Zoho CRM Sync",
        "topics": ["twilio", "django", "telephony", "zoho-crm", "call-center", "python", "webrtc"]
    },
    "Infogenx-Voice-Agent": {
        "description": "🎙️ Next-Gen Conversational AI Voice Agent Engine powered by Gemini & Real-Time Audio Streaming",
        "topics": ["ai-voice-agent", "gemini-api", "conversational-ai", "python", "voice-bot", "webrtc"]
    },
    "infogenx.com": {
        "description": "🌐 Official Corporate Web Platform for Infogenx - Enterprise Digital Solutions & IT Services",
        "topics": ["corporate-website", "web-design", "react", "html5", "seo", "frontend"]
    },
    "infogenx.com.au": {
        "description": "🇦🇺 Australian Branch Enterprise Web Application & Local Business Automation Services Portal",
        "topics": ["australia-business", "corporate-website", "b2b-services", "web-development"]
    },
    "LinkedIn-Data-Scraping": {
        "description": "💼 Automated LinkedIn B2B Prospecting & Contact Intelligence Extractor with Anti-Detection Guard",
        "topics": ["linkedin-scraper", "b2b-leads", "python", "selenium", "lead-generation", "automation"]
    },
    "odoo-sheets-auto-sync": {
        "description": "🔄 Real-Time Two-Way Automated Sync Engine Between Odoo ERP & Google Sheets via REST API",
        "topics": ["odoo", "odoo-api", "google-sheets-api", "python", "erp-integration", "automation"]
    },
    "odoo_uploader": {
        "description": "⚡ High-Speed Bulk Odoo Lead & Sales Data Uploader Tool with Automated Validation Rules",
        "topics": ["odoo", "odoo-uploader", "python", "data-migration", "erp", "lead-management"]
    },
    "Social-Media-Data-Scraping": {
        "description": "🔍 All-in-One Multi-Platform Social Media Lead Scraper & AI Business Intelligence Analyzer",
        "topics": ["social-media-scraper", "facebook-scraper", "instagram-scraper", "python", "gemini-ai", "b2b-leads"]
    }
}

PROFILE_README = """# Hi there, I'm Mohamed Yasar 👋
### 🚀 AI & Enterprise Automation Architect | Full-Stack Software Engineer

I build high-scale **B2B lead generation engines**, **Odoo ERP integrations**, **Twilio Cloud Telephony systems**, and **AI-powered Web/Mobile Applications** that drive real business growth for clients worldwide.

---

### 🛠️ What I Specialize In & Build For Clients:
- 🤖 **AI & Voice Automation**: Custom Gemini AI Bots, WebRTC Voice Agents, Live Speech Intelligence.
- ⚙️ **ERP & CRM Integration**: Odoo ERP Customization, Bulk Data Uploaders, 2-Way Google Sheets & Zoho CRM Sync.
- 📞 **Cloud Telephony & Call Centers**: Custom Twilio Web Dialers, Auto-Call Dispatchers, PBX Systems.
- 🔍 **Web Scraping & Lead Engines**: Anti-detect multi-platform scrapers (LinkedIn, Facebook, Google Maps, Instagram).
- 💻 **Full-Stack Web Development**: High-converting React/Vite frontends, Node.js & Django REST APIs.

---

### 💻 Core Tech Stack:
- **Languages**: Python, JavaScript/TypeScript, HTML5, CSS3, SQL, Shell
- **Frameworks & Libraries**: Django, Node.js, Express, React, Vite, FastAPI
- **Databases & Cloud**: MySQL, PostgreSQL, SQLite, Google Cloud Platform (GCP), CloudPanel, Docker
- **APIs & Tools**: Odoo REST API, Twilio Voice API, Google Gemini AI API, Zoho CRM API, Google Sheets API

---

### 📬 Let's Build Your Project! (Contact / Hire Me)
- 🌐 **Company / Agency**: [Infogenx Tech Solutions](https://infogenx.com)
- 📧 **Email**: [mohamedyasar081786@gmail.com](mailto:mohamedyasar081786@gmail.com)
- 🤝 **Open for**: Freelance Contracts, Enterprise Consultations, Custom Software Development & Retainers.

---
*⚡ "Transforming complex business workflows into automated, high-margin software solutions."*
"""

def update_user_profile():
    print("\n[+] Updating GitHub User Profile (Bio, Name, Company, Location)...")
    url = "https://api.github.com/user"
    payload = json.dumps(PROFILE_DATA).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            print("  [🎉] User Profile Updated Successfully!")
            return True
    except Exception as e:
        print(f"  [!] Error updating user profile: {e}")
        return False

def update_repo_metadata(repo_name, meta):
    print(f"\n[+] Updating Metadata & Topics for repository: '{repo_name}'...")
    
    # 1. Update Description
    url_repo = f"https://api.github.com/repos/{USER_NAME}/{repo_name}"
    payload_repo = json.dumps({
        "description": meta["description"]
    }).encode("utf-8")
    req_repo = urllib.request.Request(url_repo, data=payload_repo, headers=HEADERS, method="PATCH")
    try:
        with urllib.request.urlopen(req_repo) as resp:
            print(f"  [✓] Updated description for {repo_name}")
    except Exception as e:
        print(f"  [!] Error updating description for {repo_name}: {e}")

    # 2. Update Topics (Tags)
    url_topics = f"https://api.github.com/repos/{USER_NAME}/{repo_name}/topics"
    payload_topics = json.dumps({
        "names": meta["topics"]
    }).encode("utf-8")
    req_topics = urllib.request.Request(url_topics, data=payload_topics, headers=HEADERS, method="PUT")
    try:
        with urllib.request.urlopen(req_topics) as resp:
            print(f"  [✓] Updated topics for {repo_name}: {meta['topics']}")
    except Exception as e:
        print(f"  [!] Error updating topics for {repo_name}: {e}")

def setup_profile_readme():
    print("\n[+] Setting up GitHub Profile README (Repository: mdyasar49/mdyasar49)...")
    readme_repo = USER_NAME
    url_create = "https://api.github.com/user/repos"
    payload_create = json.dumps({
        "name": readme_repo,
        "description": "Mohamed Yasar - Client-Converting Developer Profile README",
        "private": False, # Profile README must be public to display on GitHub profile header!
        "auto_init": True
    }).encode("utf-8")
    
    req_create = urllib.request.Request(url_create, data=payload_create, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req_create) as resp:
            print(f"  [✓] Created Profile README repo '{readme_repo}'")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            print(f"  [i] Profile README repo '{readme_repo}' already exists.")
        else:
            print(f"  [!] HTTP Error creating Profile README repo: {e.code}")

    # Write local Profile README and push to mdyasar49/mdyasar49
    readme_dir = os.path.join(r"d:\infonix", "scratch", "profile_readme")
    os.makedirs(readme_dir, exist_ok=True)
    with open(os.path.join(readme_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(PROFILE_README)

    auth_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{readme_repo}.git"
    clean_remote = f"https://github.com/{USER_NAME}/{readme_repo}.git"

    git_dir = os.path.join(readme_dir, ".git")
    if os.path.exists(git_dir):
        import shutil
        shutil.rmtree(git_dir, ignore_errors=True)

    subprocess.run(["git", "init"], cwd=readme_dir, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["git", "config", "user.name", "mdyasar49"], cwd=readme_dir, check=True)
    subprocess.run(["git", "config", "user.email", "mohamedyasar081786@gmail.com"], cwd=readme_dir, check=True)
    subprocess.run(["git", "branch", "-M", "main"], cwd=readme_dir, check=True)
    subprocess.run(["git", "add", "."], cwd=readme_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Create client-converting GitHub Profile README"], cwd=readme_dir, check=True, stdout=subprocess.DEVNULL)
    res = subprocess.run(["git", "push", "-u", auth_remote, "main", "--force"], cwd=readme_dir, capture_output=True, text=True)

    if res.returncode == 0:
        print(f"  [🎉] SUCCESS: GitHub Profile README Pushed & Active!")
    else:
        print(f"  [!] Profile README Push Error: {res.stderr}")

def main():
    print("=" * 80)
    print(" 🚀 OPTIMIZING GITHUB PROFILE & ALL REPOSITORIES FOR CLIENT ACQUISITION")
    print("=" * 80)

    # 1. Update Bio / Profile Details
    update_user_profile()

    # 2. Setup Profile README
    setup_profile_readme()

    # 3. Update all 13 Repo Descriptions & Topics
    for repo, meta in REPO_METADATA.items():
        update_repo_metadata(repo, meta)

    print("\n" + "=" * 80)
    print(" 🎉 ALL GITHUB PROFILE & REPOSITORY ENHANCEMENTS COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    main()
