import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

API_URL = "https://api.infogenx.com/api/offer-letter/request-approval"

print("--- TEST 1: Candidate FAILS (passed = false) ---")
payload_fail = {
    "candidateName": "Test Failed Candidate",
    "candidateEmail": "test_failed_candidate@infogenx.com",
    "phone": "+919876543210",
    "location": "Chennai",
    "passed": False,
    "score": "Not Passed (Failed)",
    "requestedRole": "HR Intern",
    "department": "Human Resources"
}

r1 = requests.post(API_URL, json=payload_fail)
print("Status:", r1.status_code)
print("Response:", r1.json())

print("\n--- TEST 2: Candidate PASSES (passed = true) ---")
payload_pass = {
    "candidateName": "Mohamed Yasar",
    "candidateEmail": "infogenx.dm@gmail.com",
    "phone": "+919087659164",
    "location": "Chennai",
    "experience": "Fresher",
    "qualification": "B.E Computer Science and Engineering",
    "certification": "Full Stack Web Development",
    "linkedin": "https://linkedin.com/in/mohamedyasar",
    "resumeLink": "https://drive.google.com/file/d/1example/view?usp=sharing",
    "workTimings": "8 Hours / Day",
    "startDate": "Immediate",
    "currentSalary": "Fresher",
    "workStatus": "Not working",
    "workMode": "WFH all days with Fixed Day/hrs",
    "availability": "Weekday & Weekend Slots",
    "passed": True,
    "score": "Selected (Passed)",
    "requestedRole": "HR Intern",
    "department": "Human Resources"
}

r2 = requests.post(API_URL, json=payload_pass)
print("Status:", r2.status_code)
print("Response:", r2.json())
