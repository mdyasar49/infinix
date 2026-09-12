import os
import sys
import json
from datetime import datetime
import pytz

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Target Forward Numbers from Twilio Dialer configuration
FORWARD_SMS_NUMBERS = ["+61403339424", "+919787806366"]
OWNER_EMAIL = "admin@infogenx.in"

def get_candidate_sms_text(candidate):
    """
    Format GSM-7 compatible plain text SMS for Twilio SMS forwarders.
    """
    try:
        bne_tz = pytz.timezone('Australia/Brisbane')
        now_dt = datetime.now(bne_tz)
    except Exception:
        now_dt = datetime.now()

    date_str = now_dt.strftime("%d %b %Y")

    sms = (
        f"INFOGENX CANDIDATE ALERT ({date_str})\n"
        f"----------------------------------\n"
        f"Assessment & Task Completed!\n\n"
        f"Name : {candidate.get('name', 'N/A')}\n"
        f"Contact Number and WhatsappNo.: {candidate.get('phone', 'N/A')}\n"
        f"Location: {candidate.get('location', 'N/A')}\n"
        f"Any Experience: {candidate.get('experience', 'Fresher')}\n"
        f"Qualification: {candidate.get('qualification', 'N/A')}\n"
        f"Certification: {candidate.get('certification', 'None')}\n"
        f"LinkedIn profile URL : {candidate.get('linkedin', 'N/A')}\n"
        f"Resume Google Drive Link: {candidate.get('resumeLink', 'N/A')}\n"
        f"Work Duration & timings you can work : {candidate.get('workTimings', 'Full Time / Flexible')}\n"
        f"Start Date: {candidate.get('startDate', 'Immediate')}\n"
        f"Your Current Monthly Take Home Salary or Hourly rate if u r working: {candidate.get('currentSalary', 'N/A')}\n"
        f"Your Current Work Status: {candidate.get('workStatus', 'Not working')}\n"
        f"If Working then: {candidate.get('workMode', 'WFH all days with Fixed Day/hrs')}\n"
        f"Preferred Availability: {candidate.get('availability', 'Flexible (Weekday and Weekend Slots)')}\n"
        f"Score: {candidate.get('score', 50)}/50 ({candidate.get('percentage', 100)}%) - PASSED\n"
        f"Task: {candidate.get('taskStatus', 'Submitted & Verified')}\n"
        f"----------------------------------\n"
        f"Portal: https://candidates.infogenx.com"
    )
    return sms

def get_candidate_email_text(candidate):
    """
    Format Clean Plain Text & Executive Email for Company Owner.
    """
    date_str = datetime.now().strftime("%d %b %Y, %I:%M %p")
    name = candidate.get('name', 'Mohamed Yasar')
    score = candidate.get('score', 50)
    total = candidate.get('total', 50)
    pct = candidate.get('percentage', 100)

    email_body = f"""Subject: [CANDIDATE ONBOARDING COMPLETED] {name} - Assessment Score: {score}/{total} ({pct}%)

Dear HR Team,

This candidate has successfully completed all stages of the HR Training Process & and Practical Task. Below are the Candidate details for your review:

=======================================================
               CANDIDATE PROFILE DETAILS
=======================================================
Name : {candidate.get('name', 'N/A')}
Contact Number and WhatsappNo.: {candidate.get('phone', 'N/A')}
Email Address: {candidate.get('email', 'N/A')}
Location: {candidate.get('location', 'N/A')}
Any Experience: {candidate.get('experience', 'Fresher')}
Qualification: {candidate.get('qualification', 'N/A')}
Certification: {candidate.get('certification', 'None')}
LinkedIn profile URL : {candidate.get('linkedin', 'N/A')}
Resume Google Drive Link: {candidate.get('resumeLink', 'N/A')}
Work Duration & timings you can work : {candidate.get('workTimings', 'Full Time / Flexible')}
Start Date: {candidate.get('startDate', 'Immediate')}
Your Current Monthly Take Home Salary or Hourly rate if u r working: {candidate.get('currentSalary', 'N/A')}
Your Current Work Status: {candidate.get('workStatus', 'Not working')}
If Working then: {candidate.get('workMode', 'WFH all days with Fixed Day/hrs')}
Preferred Availability (Weekday and Weekend Time Slots): {candidate.get('availability', 'Flexible')}

=======================================================
ASSESSMENT & TASK EVALUATION
=======================================================
- 50 MCQ Assessment Score: {score}/{total} ({pct}%) - PASSED
- Step 1 (SOP Guide)     : Completed & Verified
- Step 2 (Orientation)   : Reviewed
- Step 4 (Practical Task): Proof Submitted & Verified
- Completed Timestamp    : {date_str}

=======================================================
ACTION REQUIRED
=======================================================
- Review in Portal : https://candidates.infogenx.com/admin
- Schedule Final Interview / Issue Offer Letter

-------------------------------------------------------
Infogenx Candidate Onboarding System
Portal: https://candidates.infogenx.com
=======================================================
"""
    return email_body

if __name__ == "__main__":
    demo_candidate = {
        "name": "Mohamed Yasar",
        "email": "mohamed.yasar@infogenx.com",
        "phone": "+91 97878 06366",
        "location": "Trichy / Chennai, Tamil Nadu",
        "experience": "1.5 Years in Web & Backend Development",
        "qualification": "B.E. Computer Science & Engineering",
        "certification": "AWS Certified Cloud Practitioner, Full Stack Web Dev",
        "linkedin": "https://linkedin.com/in/mdyasar49",
        "resumeLink": "https://drive.google.com/file/d/1example-drive-link/view",
        "workTimings": "8 Hours / Day (Flexible Morning/Evening)",
        "startDate": "Immediate (Within 1 week)",
        "currentSalary": "25,000 INR / Month",
        "workStatus": "Working in a Organisation",
        "workMode": "WFH all days with Fixed Day/hrs",
        "availability": "Weekday (9:00 AM - 6:00 PM IST) & Weekend on request",
        "score": 50,
        "total": 50,
        "percentage": 100,
        "taskStatus": "Submitted (Poster & Google Form Proof Verified)"
    }

    print("=======================================================")
    print(" 1. SMS FORMAT (To be sent to Twilio Dialer Numbers):")
    print(f" Target Numbers: {FORWARD_SMS_NUMBERS}")
    print("=======================================================")
    print(get_candidate_sms_text(demo_candidate))

    print("\n=======================================================")
    print(" 2. EMAIL FORMAT (To be sent to Company Owner):")
    print(f" Target Owner Email: {OWNER_EMAIL}")
    print("=======================================================")
    print(get_candidate_email_text(demo_candidate))
