import requests
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdAffcQaR1oRuv_NwT5D-MrnGbjPq0EE_cka6jAZ5FjEgt0WA/formResponse"

payload = {
    "emailAddress": "infogenx.jobs@gmail.com",
    "entry.1962508159": "HR Intern Candidate",
    "entry.2094768511_year": "2001",
    "entry.2094768511_month": "05",
    "entry.2094768511_day": "20",
    "entry.560105994": "+919787806366",
    "entry.565364655": "Chennai",
    "entry.1499919333": "UG",
    "entry.1611960530": "Madras University",
    "entry.296852601": "Human Resources",
    "entry.1114402762": "2024",
    "entry.1469288896": "Non IT",
    "entry.1060836287": "HR Operations, Talent Acquisition, Excel",
    "entry.22600333": "HR Management Certification",
    "entry.1540746504": "Fresher",
    "entry.1762623825": "NA",
    "entry.1690561841": "https://drive.google.com/test-resume",
    "entry.142739096": "https://linkedin.com/in/infogenx",
    "entry.1553391135_year": "2026",
    "entry.1553391135_month": "09",
    "entry.1553391135_day": "15",
    "entry.53166621": "Full-Time"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

res = requests.post(form_url, data=payload, headers=headers)
print("Form Submit Status Code:", res.status_code)
if res.status_code == 200:
    print("[SUCCESS] Form submission successfully registered in Google Form!")
else:
    print(f"[ERROR] HTTP {res.status_code}")
