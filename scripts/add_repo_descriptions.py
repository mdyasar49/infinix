"""
Update .git/description and README.md top description across all 11 Infogenx repositories.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_METADATA = {
    "odoo-lead-generator": {
        "description": "Automated Odoo ERP technographic lead discovery, executive contact enrichment, and verification engine with multi-tab Excel/CSV exports for India, Australia & Global markets.",
        "topics": ["odoo", "lead-generation", "technographic-scraping", "google-dorks", "b2b-leads", "python", "openpyxl", "data-enrichment"]
    },
    "internship_outreach_automation_full": {
        "description": "End-to-end automated candidate discovery, AI extraction, multi-tier deduplication, SQLite persistence, and scheduled Gmail outreach pipeline with Google Sheets sync.",
        "topics": ["candidate-discovery", "gemini-api", "outreach-automation", "gmail-api", "google-sheets", "python", "sqlite", "recruitment-automation"]
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
    "infogenx.com.au": {
        "description": "Production source code for InfogenX Australia (infogenx.com.au) delivering specialized APAC regional IT consulting, cloud services, and localized enterprise solutions.",
        "topics": ["australia", "regional-website", "infogenx-australia", "react", "cloud-services", "it-consulting"]
    },
    "Infogenx-Voice-Agent": {
        "description": "Multimodal outbound sales AI voice agent ('Sarah') integrating Google Gemini 2.5 Live and Twilio for real-time speech conversations and automated SMS follow-ups.",
        "topics": ["voice-ai", "gemini-live", "twilio-voice", "conversational-ai", "sales-automation", "python", "fastapi"]
    },
    "odoo_uploader": {
        "description": "Automated Python ETL tool to batch upload and map multi-tab Excel lead enquiries directly into Odoo CRM via XML-RPC with JSON audit reporting.",
        "topics": ["odoo-crm", "xmlrpc", "excel-uploader", "lead-ingestion", "crm-automation", "python", "openpyxl"]
    },
    "google-apps-script": {
        "description": "Infogenx Google Apps Script suite for automated Brisbane CRM pipelines, Gemini AI lead scoring, social intelligence scraping, and Google Sheets sync.",
        "topics": ["google-apps-script", "gemini-ai", "zoho-crm", "social-scraping", "google-sheets", "crm-pipeline"]
    }
}

def update_git_description(repo_name, desc):
    workspace = r"d:\infonix"
    repo_path = os.path.join(workspace, repo_name)
    desc_path = os.path.join(repo_path, ".git", "description")
    if os.path.exists(os.path.dirname(desc_path)):
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write(desc + "\n")
        print(f"[✓] Updated .git/description for: {repo_name}")

def update_readme_header(repo_name, meta):
    workspace = r"d:\infonix"
    readme_path = os.path.join(workspace, repo_name, "README.md")
    if not os.path.exists(readme_path):
        return
    
    with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    desc_block = f"> **Description**: {meta['description']}\n>\n> **Topics**: `{', '.join(meta['topics'])}`\n"
    
    if "> **Description**:" not in content:
        lines = content.splitlines()
        new_lines = []
        inserted = False
        for line in lines:
            new_lines.append(line)
            if not inserted and line.startswith("# "):
                new_lines.append("")
                new_lines.append(desc_block)
                inserted = True
        
        if not inserted:
            new_lines.insert(0, desc_block + "\n")

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
        print(f"[✓] Added structured Description header to README for: {repo_name}")
    else:
        print(f"[-] README already has description header for: {repo_name}")

def main():
    print("=" * 80)
    print(" 🚀 UPDATING REPOSITORY DESCRIPTIONS ACROSS ALL INFONIX REPOS")
    print("=" * 80)
    
    for repo_name, meta in REPO_METADATA.items():
        update_git_description(repo_name, meta["description"])
        update_readme_header(repo_name, meta)

if __name__ == "__main__":
    main()
