import os
import sys
import json
import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"d:\infonix"
SCRATCH_DIR = os.path.join(BASE_DIR, "scratch", "job_applications")
os.makedirs(SCRATCH_DIR, exist_ok=True)

DEV_EMAIL = "mdyasardeveloper786@gmail.com"
PORTFOLIO_URL = "https://github.com/mdyasar49"

JOB_TARGET_ROLES = [
    {
        "role_title": "Senior Full-Stack AI Engineer (Remote)",
        "tech_focus": "React, Vite, Node.js, Python, Gemini AI, Microservices",
        "pitch_highlights": "5+ years architecting full-stack web applications, LLM/Gemini API integrations, and scalable REST backends.",
        "target_platforms": ["LinkedIn Jobs", "RemoteOK", "WeWorkRemotely", "Wellfound"],
        "cover_letter_snippet": f"""Dear Hiring Manager,

I am writing to express my strong interest in the Senior Full-Stack AI Engineer position. 

With extensive experience building enterprise-grade React/Node.js web apps, Google Gemini AI integrations, and high-concurrency Python backends, I deliver robust, scalable software solutions. 

Key Highlights of my technical background:
• Full-Stack Architecture: React/Vite frontends with Node.js/Express & Django REST backends.
• AI & Multimodal Integration: Real-time Gemini AI voice agents and multimodal media processing engines.
• Production Reliability: Containerized deployments (Docker), GCP cloud infrastructure, and database optimizations.

I would love to discuss how my technical skills can drive immediate value for your engineering team.

Best regards,
Mohamed Yasar
📧 Email: {DEV_EMAIL}
💻 Portfolio: {PORTFOLIO_URL}"""
    },
    {
        "role_title": "Lead Python Automation & Web Scraping Architect (Remote)",
        "tech_focus": "Python, Selenium, Anti-detect Scrapers, Multi-platform Crawling, Data Pipelines",
        "pitch_highlights": "Architected anti-detect web scrapers extracting thousands of leads daily with proxy rotation and anti-captcha mechanisms.",
        "target_platforms": ["LinkedIn Jobs", "Toptal", "FlexJobs", "Upwork"],
        "cover_letter_snippet": f"""Dear Hiring Team,

As a Senior Python Automation Engineer specializing in high-concurrency web scraping and data extraction pipelines, I am eager to contribute to your data engineering initiatives.

What I bring to your team:
• Anti-Detect Scraping: Multi-channel crawlers (LinkedIn, Google Maps, Social Media) with proxy rotation & captcha bypass.
• Automated Pipelines: Automated data transformation, schema validation, and direct sync to PostgreSQL/MySQL/Google Sheets.
• Performance Optimization: High-speed asynchronous requests and bulletproof error recovery.

Portfolio: {PORTFOLIO_URL}
Contact: {DEV_EMAIL}"""
    },
    {
        "role_title": "Cloud Telephony & WebRTC Engineer (Remote)",
        "tech_focus": "Twilio Voice API, WebRTC, Node.js, Django, Call Center Dialer Software",
        "pitch_highlights": "Engineered enterprise Twilio WebRTC browser dialers, auto-call dispatchers, and live speech intelligence systems for enterprise clients.",
        "target_platforms": ["LinkedIn Jobs", "Y Combinator Jobs", "RemoteOK"],
        "cover_letter_snippet": f"""Dear Engineering Director,

I am applying for the Cloud Telephony / WebRTC Engineer role. I specialize in building custom browser dialers, call center automation, and real-time voice streaming applications using Twilio Voice API and WebRTC.

Notable achievements:
• Infogenx Enterprise Dialer: Built a custom WebRTC browser calling application with auto-call dispatching and Twilio integration.
• AI Voice Assistant: Integrated real-time speech-to-text and AI voice bot workflows into telephony pipelines.

Portfolio: {PORTFOLIO_URL}
Contact: {DEV_EMAIL}"""
    }
]

def generate_job_acquisition_blueprint():
    print("=" * 80)
    print(" 🚀 DUAL-TRACK JOB & FREELANCE ACQUISITION ENGINE (MOHAMED YASAR)")
    print("=" * 80)

    output_path = os.path.join(SCRATCH_DIR, "remote_job_applications.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(JOB_TARGET_ROLES, f, indent=2, ensure_ascii=False)

    print(f"[✓] Saved Job Application pitches to: {output_path}")
    print("=" * 80)

if __name__ == "__main__":
    generate_job_acquisition_blueprint()
