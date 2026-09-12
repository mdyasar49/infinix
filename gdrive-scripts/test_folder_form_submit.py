import requests
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSccc1FMu_lahzcR82sd1sRx6JKjt7LUd9hr-CV7iLAmKinj9Q/formResponse"

payload = {
    "entry.1032654986": "Infogenx QA Student",
    # Date of birth (type 9)
    "entry.2042877645_year": "2000",
    "entry.2042877645_month": "01",
    "entry.2042877645_day": "15",
    "entry.1046730135": "infogenx.jobs@gmail.com",
    "entry.34502397": "+919787806366",
    "entry.1247019162": "Chennai",
    "entry.7054084": "UG",
    "entry.2097140284": "Anna University",
    "entry.1792403442": "Computer Science",
    "entry.746569042": "2024",
    "entry.281727459": "IT",
    "entry.824047167": "React, Node.js, Python",
    "entry.89068927": "Fresher",
    "entry.956473909": "NA",
    "entry.1821849415": "0",
    "entry.29251381": "NA",
    "entry.1798328528": "35000",
    "entry.1233814069": "https://drive.google.com/test-resume",
    "entry.2002060636": "Full Time",
    "entry.709081998": "Full Stack Certification",
    "entry.1532916716": "https://linkedin.com/in/infogenx",
    "entry.1425564401": "General (9 AM - 6 PM)",
    # Start date (type 9)
    "entry.2052507023_year": "2026",
    "entry.2052507023_month": "09",
    "entry.2052507023_day": "15",
    "entry.904412918": "NA",
    "entry.850582346": "Not working",
    "entry.1627445891": "Flexible",
    "entry.1271723367": "Immediate"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

res = requests.post(form_url, data=payload, headers=headers)
print("Form Submit HTTP Status:", res.status_code)
if res.status_code == 200:
    print("[SUCCESS] Form submission successfully registered in Google Form!")
else:
    print("[FAIL] Status:", res.status_code)
