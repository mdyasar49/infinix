"""
Update GitHub repository descriptions and topics via GitHub REST API.
"""

import urllib.request
import urllib.parse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
ORG = "mdyasar49"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Infogenx-Automation-Script"
}

REPOS_DATA = {
    "odoo-lead-generator": {
        "description": "Automated Odoo ERP technographic lead discovery, executive contact enrichment, and verification engine with multi-tab Excel/CSV exports for India, Australia & Global markets.",
        "topics": ["odoo", "lead-generation", "technographic-scraping", "google-dorks", "b2b-leads", "python", "openpyxl", "data-enrichment"]
    },
    "internship_outreach_automation_full": {
        "description": "End-to-end automated candidate discovery, AI extraction, multi-tier deduplication, SQLite persistence, and scheduled Gmail outreach pipeline with Google Sheets sync.",
        "topics": ["candidate-discovery", "gemini-api", "outreach-automation", "gmail-api", "google-sheets", "python", "sqlite", "recruitment-automation"]
    },
    "odoo_uploader": {
        "description": "Automated Python ETL tool to batch upload and map multi-tab Excel lead enquiries directly into Odoo CRM via XML-RPC with JSON audit reporting.",
        "topics": ["odoo-crm", "xmlrpc", "excel-uploader", "lead-ingestion", "crm-automation", "python", "openpyxl"]
    },
    "google-apps-script": {
        "description": "Infogenx Google Apps Script suite for automated Brisbane CRM pipelines, Gemini AI lead scoring, social intelligence scraping, and Google Sheets sync.",
        "topics": ["google-apps-script", "gemini-ai", "zoho-crm", "social-scraping", "google-sheets", "crm-pipeline"]
    },
    "infogenx-twilio-dialer": {
        "description": "Enterprise multi-channel Django web dialer integrating Twilio Voice/SMS, Zadarma, call recording playback, and real-time bidirectional Zoho CRM synchronization.",
        "topics": ["twilio", "django", "zoho-crm", "web-dialer", "call-recording", "telephony", "zadarma", "python"]
    },
    "blog-api": {
        "description": "High-performance Django REST Framework API and real-time WebSocket backend powering multi-tenant Infogenx blogs, view-count metrics, and admin management.",
        "topics": ["django-rest-framework", "websockets", "redis", "postgresql", "multi-site-blog", "jwt-auth", "python"]
    },
    "blog-react": {
        "description": "Modern React & Vite administrative dashboard with Material UI for managing InfogenX blog articles, categories, SEO tags, media assets, and view analytics.",
        "topics": ["react", "vite", "material-ui", "blog-admin", "dashboard", "frontend", "rich-text-editor"]
    },
    "dev": {
        "description": "Development and staging repository for InfogenX corporate web applications (dev.infogenx.com), testing microservices, UI components, and API integrations.",
        "topics": ["staging", "infogenx", "react", "frontend-development", "web-application"]
    },
    "infogenx.com": {
        "description": "Production source code for the global InfogenX corporate website (infogenx.com) featuring enterprise IT solutions, digital transformation, and SEO optimization.",
        "topics": ["corporate-website", "production", "infogenx", "react", "seo-optimization", "web-design"]
    },
    "infogenx.co.au": {
        "description": "Production source code for InfogenX Australia (infogenx.com.au) delivering specialized APAC regional IT consulting, cloud services, and localized enterprise solutions.",
        "topics": ["australia", "regional-website", "infogenx-australia", "react", "cloud-services", "it-consulting"]
    },
    "student-portal": {
        "description": "Integrated student onboarding and corporate portal for Infogenx, featuring student registration, interactive learning modules, assessments, digital offer letters, and day-one training.",
        "topics": ["student-portal", "onboarding", "infogenx", "react", "corporate-training"]
    },
    "Social-Media-Data-Scraping": {
        "description": "Unified social media scraping suite for LinkedIn, Facebook, Instagram, Twitter, YouTube, and Pinterest, featuring a FastAPI backend and search-based contact lead extraction.",
        "topics": ["social-media-scraping", "fastapi", "linkedin-scraper", "lead-generation", "python"]
    },
    "Data-Scraping": {
        "description": "Master web scraping suite containing independent scrapers for LinkedIn, Upwork, Freelancer, Clutch, DesignRush, PeoplePerHour, and Facebook with local MySQL integration.",
        "topics": ["web-scraping", "b2b-leads", "mysql", "clutch-scraper", "upwork-scraper", "python"]
    },
    "infogenx-voice": {
        "description": "AI Voice Agent web application with dashboard, call management, analytics, and administration features integrating Twilio and conversational AI.",
        "topics": ["voice-ai", "twilio", "call-management", "analytics", "conversational-ai"]
    }
}

def update_repo(repo_name, data):
    url = f"https://api.github.com/repos/{ORG}/{repo_name}"
    payload = json.dumps({"description": data["description"]}).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[✓ Description Updated] {repo_name}")
    except Exception as e:
        print(f"[✗ Description Error] {repo_name}: {e}")

    # Update Topics
    topics_url = f"https://api.github.com/repos/{ORG}/{repo_name}/topics"
    topics_payload = json.dumps({"names": data["topics"]}).encode("utf-8")
    topics_req = urllib.request.Request(topics_url, data=topics_payload, headers=HEADERS, method="PUT")
    try:
        with urllib.request.urlopen(topics_req) as resp:
            print(f"[✓ Topics Updated] {repo_name} -> {data['topics']}")
    except Exception as e:
        print(f"[✗ Topics Error] {repo_name}: {e}")

def main():
    print("=" * 80)
    print(" 🚀 DIRECTLY UPDATING ALL GITHUB REPO DESCRIPTIONS & TOPICS VIA API")
    print("=" * 80)
    
    for repo_name, data in REPOS_DATA.items():
        print(f"\n[-] Processing: {repo_name}...")
        update_repo(repo_name, data)

    print("\n" + "=" * 80)
    print("🎉 ALL GITHUB REPOSITORIES SUCCESSFULLY UPDATED!")
    print("=" * 80)

if __name__ == "__main__":
    main()
