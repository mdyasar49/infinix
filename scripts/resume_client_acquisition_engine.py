import os
import sys
import json
import csv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"d:\infonix"

RESUME_PITCHES = {
    "Web Scraping & Data Extraction": """Subject: Custom Web Scraping & Lead Extraction Pipeline for {company}

Hi {name},

I am a Full-Stack Software Engineer specializing in Python web crawlers, anti-detect scrapers, and data extraction pipelines (LinkedIn, Google Maps, Social Media).

I can set up a custom data scraper for {company} that extracts verified decision-maker contacts and syncs them automatically to your database/Google Sheets.

Would you be open to seeing a quick sample list of leads for {niche} in {location}?

Best regards,
Mohamed Yasar
Full-Stack AI & Automation Engineer | https://github.com/mdyasar49
Email: mdyasardeveloper786@gmail.com
""",

    "AI Voice Agents & Gemini AI": """Subject: Conversational AI Voice Agent Integration for {company}

Hi {name},

I build real-time Conversational AI Voice Agents and Gemini AI integrations that automate customer support, lead qualification, and voice calls.

I can build a custom AI voice assistant prototype for {company} in 48 hours.

Would you like to try a live 30-second AI voice demo?

Best regards,
Mohamed Yasar | https://github.com/mdyasar49
""",

    "Twilio Telephony & Web Dialer": """Subject: Custom Twilio Web Dialer & SMS Automation for {company}

Hi {name},

I build custom Twilio WebRTC click-to-call dialers, automated SMS notification engines, and call center integrations.

I can set up a custom web dialer or SMS dispatcher for {company} in 24 hours.

Let me know if you would like to see a quick video demo!

Best regards,
Mohamed Yasar | https://github.com/mdyasar49
""",

    "Full-Stack Web Development": """Subject: High-Performance React/Node Web Development for {company}

Hi {name},

I build ultra-fast, responsive web applications and REST APIs using React, Vite, Node.js, Express, and Django.

I can help {company} build or modernize your web platform with high performance and mobile-first design.

Feel free to view my portfolio & code on GitHub: https://github.com/mdyasar49

Best regards,
Mohamed Yasar | mdyasardeveloper786@gmail.com
"""
}

def main():
    print("=" * 80)
    print(" 🚀 RESUME-TAILORED CLIENT OUTREACH ENGINE (MOHAMED YASAR)")
    print("=" * 80)

    out_dir = os.path.join(BASE_DIR, "scratch", "resume_outreach")
    os.makedirs(out_dir, exist_ok=True)

    out_file = os.path.join(out_dir, "resume_pitch_proposals.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(RESUME_PITCHES, f, indent=2)

    print("\n[+] Generated 4 Resume-Based Service Proposals:")
    for service_name in RESUME_PITCHES.keys():
        print(f"  • {service_name}")

    print(f"\n[✓] Saved proposals to: {out_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
