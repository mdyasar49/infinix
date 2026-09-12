import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEV_EMAIL = "mdyasardeveloper786@gmail.com"
PORTFOLIO_URL = "https://github.com/mdyasar49"

STRATEGY_SUMMARY = {
    "linkedin_strategy": {
        "focus": "100% High-Paying Remote Software Engineering Jobs (Full-Time / Senior Engineer)",
        "headline": "Senior Full-Stack AI & Enterprise Software Engineer | React, Vite, Node.js, Python & Cloud Telephony | Building Scalable Cloud Applications | mdyasardeveloper786@gmail.com",
        "freelance_mention": "None on LinkedIn (Directs all code/technical inquiries to GitHub)"
    },
    "github_strategy": {
        "focus": "B2B Freelance Client Contracts, Code Portfolio, Case Studies & Direct Contact",
        "url": PORTFOLIO_URL,
        "avatar_theme": "d:\\infonix\\profile_avatar_gold.jpg",
        "freelance_services": [
            "B2B Web Scraping & Data Extraction Engines",
            "Twilio Cloud Telephony & WebRTC Dialers",
            "Conversational AI & Gemini Voice Bots",
            "Full-Stack Web Development & Student Portals"
        ],
        "contact_email": DEV_EMAIL
    }
}

def main():
    print("=" * 80)
    print(" 🚀 STRATEGIC ALIGNMENT: LINKEDIN (JOBS) + GITHUB (FREELANCE)")
    print("=" * 80)
    print("  [✓] LinkedIn Profile: 100% Focused on Remote Full-Time Engineering Jobs")
    print(f"  [✓] GitHub Portfolio: {PORTFOLIO_URL} (Dedicated to Freelance Contracts & Code)")
    print("=" * 80)

    out_file = os.path.join(r"d:\infonix", "scratch", "strategy_alignment.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(STRATEGY_SUMMARY, f, indent=2, ensure_ascii=False)
        
    print(f" Saved strategy config to: {out_file}")

if __name__ == "__main__":
    main()
