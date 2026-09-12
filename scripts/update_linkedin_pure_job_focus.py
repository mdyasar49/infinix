import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEV_EMAIL = "mdyasardeveloper786@gmail.com"
PORTFOLIO_URL = "https://github.com/mdyasar49"

# 100% Pure Job & Enterprise Engineering Focused Copy for LinkedIn
PURE_JOB_HEADLINE = "Senior Full-Stack AI & Enterprise Software Engineer | React, Vite, Node.js, Python & Cloud Telephony | Building Scalable Cloud Applications | mdyasardeveloper786@gmail.com"

PURE_JOB_ABOUT = f"""Senior Full-Stack AI & Enterprise Software Engineer with 5+ years of experience architecting high-performance web applications, cloud communication engines, and automated data processing pipelines.

🛠️ TECHNICAL CORE COMPETENCIES:
• Full-Stack Architecture: Modern React/Vite, Node.js/Express, Python (Django, FastAPI), REST & GraphQL APIs.
• AI & Machine Learning: Real-time Gemini AI integrations, multimodal voice agents, speech-to-text intelligence.
• Cloud Telephony & Infrastructure: Enterprise Twilio WebRTC dialer applications, PBX routing, GCP, Docker & MySQL/PostgreSQL.
• Data Engineering: High-concurrency automated data extraction, ETL pipelines, and API integrations.

💼 FEATURED ENGINEERING PROJECT:
• Infogenx Enterprise Telephony & AI Engine: Architected a full-stack WebRTC browser calling system and real-time AI voice assistant for high-volume enterprise operations.

💻 CODE PORTFOLIO & REPOSITORIES:
Explore my open-source projects, system architectures, and technical case studies:
{PORTFOLIO_URL}

📬 CONTACT:
📧 Email: {DEV_EMAIL}
🌐 GitHub: {PORTFOLIO_URL}"""

def main():
    print("=" * 80)
    print(" 🚀 100% PURE REMOTE JOB-FOCUSED LINKEDIN COPY GENERATED")
    print("=" * 80)
    print(f"📌 HEADLINE:\n{PURE_JOB_HEADLINE}\n")
    print(f"📝 ABOUT:\n{PURE_JOB_ABOUT}")
    print("=" * 80)

if __name__ == "__main__":
    main()
