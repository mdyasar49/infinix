import os
import sys
import json
import csv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"d:\infonix"

EMAIL_TEMPLATE = """Subject: Quick question regarding your {niche} lead flow & Odoo automation - {company}

Hi {name},

I noticed you are running {company} in {location}. 

I recently built an automated system that cuts down manual data entry for Odoo ERP & Lead Prospecting by 90%, helping companies capture 3x more verified decision-maker leads every week.

Here is a quick breakdown of what I can set up for {company} in 24 hours:
1. Automated B2B Lead Extraction (Verified Decision Maker Emails & Phones)
2. Instant CRM / Odoo Integration (Zero Manual Entry)
3. Smart Follow-up Automation (Twilio SMS / Email Sync)

Would you be open to a quick 5-minute video call or demo tomorrow to see how this works for {company}?

Best regards,
Mohamed Yasar
AI & Enterprise Automation Architect | Independent Software Consultant
Website: https://github.com/mdyasar49
GitHub: https://github.com/mdyasar49
Email: mdyasardeveloper786@gmail.com
"""

LINKEDIN_TEMPLATE = """Hi {name}, came across your profile while researching top {niche} companies in {location}.

We just launched a 24-hour Automated Lead & CRM Integration Pipeline that delivers verified B2B leads directly to your team's CRM without manual work.

If you're open to seeing a 1-minute live demo, let me know where to send it over!

Best regards,
Mohamed Yasar | https://github.com/mdyasar49
"""

SAMPLE_TARGET_PROSPECTS = [
    {"name": "Director of Operations", "company": "Sydney Solar Systems", "niche": "Solar & Renewable Energy", "location": "Australia", "email": "contact@sydneysolar.example"},
    {"name": "Managing Director", "company": "Apex Logistics Ltd", "niche": "Supply Chain & Logistics", "location": "Melbourne", "email": "info@apexlogistics.example"},
    {"name": "Sales Head", "company": "B2B Tech Services", "niche": "Enterprise IT Services", "location": "Global", "email": "sales@b2btech.example"}
]

def main():
    print("=" * 80)
    print(" 🚀 48-HOUR CLIENT ACQUISITION OUTREACH ENGINE")
    print("=" * 80)
    
    out_dir = os.path.join(BASE_DIR, "scratch", "48hr_outreach")
    os.makedirs(out_dir, exist_ok=True)
    
    print("\n[+] Generating Cold Email & LinkedIn Pitch Messages...")
    
    generated = []
    for p in SAMPLE_TARGET_PROSPECTS:
        email_msg = EMAIL_TEMPLATE.format(
            name=p["name"],
            company=p["company"],
            niche=p["niche"],
            location=p["location"]
        )
        linkedin_msg = LINKEDIN_TEMPLATE.format(
            name=p["name"],
            company=p["company"],
            niche=p["niche"],
            location=p["location"]
        )
        generated.append({
            "prospect": p,
            "email_message": email_msg,
            "linkedin_message": linkedin_msg
        })
        
    # Save outreach campaign files
    out_csv = os.path.join(out_dir, "client_outreach_list.csv")
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Company", "Niche", "Location", "Email", "Cold Email Message", "LinkedIn Message"])
        for item in generated:
            p = item["prospect"]
            writer.writerow([p["name"], p["company"], p["niche"], p["location"], p["email"], item["email_message"], item["linkedin_message"]])
            
    print(f"  [✓] Saved campaign templates & prospect list to: {out_csv}")

    print("\n" + "=" * 80)
    print(" 📊 48-HOUR ACTION CHECKLIST TO CLOSE 2 CLIENTS TODAY & TOMORROW")
    print("=" * 80)
    print("""
1. Run LinkedIn Scraper & Local Lead Scraper to get 50 decision-maker emails.
2. Send 25 Personalized Cold Emails (Template generated above).
3. Send 20 Direct Messages on LinkedIn / WhatsApp.
4. Schedule 30-second live demos for responding prospects.
5. Offer 24-hour turnaround on Odoo Sync or Lead Automation to close 2 deals!
""")
    print("=" * 80)

if __name__ == "__main__":
    main()
