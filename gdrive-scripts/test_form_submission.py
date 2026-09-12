import requests

FORM_RESPONSE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdAffcQaR1oRuv_NwT5D-MrnGbjPq0EE_cka6jAZ5FjEgt0WA/formResponse"

def test_submission():
    payload = {
        "emailAddress": "test.candidate@infogenx.com",
        "entry.1962508159": "Mohamed Yasar",
        
        # Date of Birth
        "entry.2094768511_year": "2000",
        "entry.2094768511_month": "08",
        "entry.2094768511_day": "15",

        "entry.560105994": "9787806366",
        "entry.565364655": "Chennai, Tamil Nadu",
        "entry.1499919333": "UG",
        "entry.1611960530": "Anna University",
        "entry.296852601": "Computer Science & Engineering",
        "entry.1114402762": "2024",
        "entry.1469288896": "IT",
        "entry.1060836287": "HTML, JavaScript, React, Node.js, Python",
        "entry.22600333": "AWS Cloud Practitioner",
        "entry.1540746504": "Fresher",
        "entry.1762623825": "NA",
        "entry.1690561841": "https://drive.google.com/file/d/test-resume-link/view?usp=sharing",
        "entry.142739096": "https://linkedin.com/in/mohamed-yasar",
        
        # Work Start Date
        "entry.1553391135_year": "2026",
        "entry.1553391135_month": "09",
        "entry.1553391135_day": "15",

        "entry.53166621": "10:00 AM - 07:00 PM (Full-Time)"
    }

    print("[*] Submitting Test Application to HR Intern Google Form...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    r = requests.post(FORM_RESPONSE_URL, data=payload, headers=headers)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("✅ Google Form submission successful!")
    else:
        print(f"[!] Response status: {r.status_code}")

if __name__ == "__main__":
    test_submission()
