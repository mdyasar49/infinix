import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
import requests

post_url = 'https://docs.google.com/forms/d/e/1FAIpQLSdAffcQaR1oRuv_NwT5D-MrnGbjPq0EE_cka6jAZ5FjEgt0WA/formResponse'

form_data = {
    'emailAddress': 'infogenx.dm@gmail.com',
    'entry.1962508159': 'Mohamed Yasar',
    # Date of Birth (Type 9)
    'entry.2094768511_year': '2001',
    'entry.2094768511_month': '01',
    'entry.2094768511_day': '15',
    'entry.560105994': '9087659164',
    'entry.565364655': 'Chennai',
    'entry.1499919333': 'UG',
    'entry.1611960530': 'Anna University',
    'entry.296852601': 'Computer Science and Engineering',
    'entry.1114402762': '2023',
    'entry.1469288896': 'IT',
    'entry.1060836287': 'React, Node.js, Python, JavaScript',
    'entry.22600333': 'Full Stack Web Development Certification',
    'entry.1540746504': 'Previous internship experience',
    'entry.1762623825': 'Infogenx Systems',
    'entry.1690561841': 'https://drive.google.com/file/d/1example/view?usp=sharing',
    'entry.142739096': 'https://linkedin.com/in/mohamedyasar',
    # Work Start Date (Type 9)
    'entry.1553391135_year': '2026',
    'entry.1553391135_month': '09',
    'entry.1553391135_day': '15',
    'entry.53166621': 'Full-Time'
}

resp = requests.post(post_url, data=form_data)
print('Form Submit HTTP Status:', resp.status_code)
if resp.status_code == 200:
    print('✅ Form submission successful! Submitted to Google Form.')
else:
    print('❌ Submission failed, response text snippet:', resp.text[:300])
