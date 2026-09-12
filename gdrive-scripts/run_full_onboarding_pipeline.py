import json
import sys
import os
import requests
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

SPREADSHEET_ID = "1tEjn1hJ0rd2pNV3kaLyv4SitFyoRLwCKb5loAdEvjoM"
CLASPRC_PATH = Path(os.path.expanduser("~/.clasprc.json"))

PORTAL_URL = "https://candidates.infogenx.com/login"
DIALER_SMS_URL = "https://twilliodialer.infogenx.com/dialer/send-sms/"
DIALER_API_KEY = "infogenx-secret-2026"
CANDIDATE_API_URL = "https://api.infogenx.com/api/candidate-auth/users"

def get_auth_token():
    with open(CLASPRC_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    token_dict = data.get("tokens", {}).get("default", {})
    if not token_dict and "token" in data:
        token_dict = data.get("token", {})
    if not token_dict:
        token_dict = data
        
    access_token = token_dict.get("access_token")
    refresh_token = token_dict.get("refresh_token")
    client_id = token_dict.get("client_id")
    client_secret = token_dict.get("client_secret")

    if refresh_token and client_id and client_secret:
        refresh_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        try:
            r = requests.post("https://oauth2.googleapis.com/token", data=refresh_data, timeout=15)
            if r.status_code == 200:
                access_token = r.json().get("access_token", access_token)
        except Exception as e:
            print(f"Token refresh note: {e}")
            
    return access_token

def generate_password(full_name, dob):
    clean_name = "".join(c for c in full_name.upper() if c.isalpha())
    if len(clean_name) < 4:
        clean_name = (clean_name + "INFO")[:4]
    else:
        clean_name = clean_name[:4]
    
    year = "2000"
    if dob:
        digits = "".join(c for c in dob if c.isdigit())
        if len(digits) >= 4:
            year = digits[:4] if int(digits[:4]) > 1950 and int(digits[:4]) < 2030 else digits[-4:]
    return f"{clean_name}{year}"

def send_gmail(to_email, full_name, password):
    token = get_auth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    subject = "Application Received Successfully - Infogenx Candidate Assessment Portal"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="margin: 0; padding: 0; background-color: #F8FAFC; font-family: 'Segoe UI', Arial, sans-serif;">
      <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #F8FAFC; padding: 40px 10px;">
        <tr>
          <td align="center">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 640px; background-color: #FFFFFF; border-radius: 14px; overflow: hidden; box-shadow: 0 10px 30px rgba(0, 18, 60, 0.08); border: 1px solid #E2E8F0;">
              <tr>
                <td align="center" style="background: linear-gradient(135deg, #00123C 0%, #000E68 55%, #E65525 100%); padding: 34px 20px; color: #FFFFFF;">
                  <a href="https://candidates.infogenx.com" target="_blank" style="text-decoration: none; display: inline-block;">
                    <img src="https://candidates.infogenx.com/logo_white.png" alt="INFOGENX" width="180" style="width: 180px; max-width: 180px; height: auto; display: block; margin: 0 auto 8px auto; border: 0;" />
                  </a>
                  <p style="margin: 0; font-size: 13px; opacity: 0.95; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; color: #FFFFFF;">Candidate Onboarding & Assessment Portal</p>
                </td>
              </tr>
              <tr>
                <td style="padding: 36px 32px; color: #00123C;">
                  <h2 style="margin: 0 0 16px 0; font-size: 22px; font-weight: 800; color: #00123C;">Application Received Successfully 🎉</h2>
                  <p style="margin: 0 0 20px 0; font-size: 15px; line-height: 1.6; color: #334155;">Dear <strong>{full_name}</strong>,</p>
                  <p style="margin: 0 0 24px 0; font-size: 15px; line-height: 1.6; color: #334155;">Thank you for submitting your HR Intern candidate application to Infogenx. Your candidate onboarding account is now active.</p>
                  
                  <div style="background-color: #FFF8F3; border: 1.5px solid rgba(230, 85, 37, 0.25); border-radius: 12px; padding: 22px; margin-bottom: 26px;">
                    <h3 style="margin: 0 0 14px 0; font-size: 16px; font-weight: 800; color: #E65525;">Your Login Credentials</h3>
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="font-size: 14px;">
                      <tr>
                        <td style="padding: 6px 0; color: #5C6A86; font-weight: 600; width: 140px;">Registered Email:</td>
                        <td style="padding: 6px 0; color: #00123C; font-weight: 700;">{to_email}</td>
                      </tr>
                      <tr>
                        <td style="padding: 6px 0; color: #5C6A86; font-weight: 600;">Generated Password:</td>
                        <td style="padding: 6px 0; color: #E65525; font-weight: 800; font-family: monospace; font-size: 18px; letter-spacing: 0.05em;">{password}</td>
                      </tr>
                      <tr>
                        <td style="padding: 6px 0; color: #5C6A86; font-weight: 600;">Exam Attempts:</td>
                        <td style="padding: 6px 0; color: #00123C; font-weight: 700;">Strictly 1 Attempt Allowed</td>
                      </tr>
                    </table>
                  </div>

                  <p style="margin: 0 0 28px 0; font-size: 15px; line-height: 1.6; color: #334155;">Thanks for filling out this form, Please login to the HR Training Applicaiton with below user name and password and complete all training Process</p>
                  
                  <div align="center" style="margin: 30px 0 24px 0;">
                    <a href="{PORTAL_URL}" target="_blank" style="background: linear-gradient(90deg, #00123C 0%, #E65525 100%); color: #FFFFFF !important; text-decoration: none; padding: 15px 36px; border-radius: 10px; font-weight: 700; font-size: 15px; display: inline-block; box-shadow: 0 8px 22px rgba(0, 18, 60, 0.16); text-align: center;">Access Candidate Assessment Portal →</a>
                  </div>
                  <p style="margin: 0; font-size: 13px; color: #94A3B8; text-align: center;">Portal URL: <a href="{PORTAL_URL}" style="color: #E65525;">{PORTAL_URL}</a></p>
                </td>
              </tr>
              <!-- Unified Footer -->
              <tr>
                <td align="center" style="background-color: #F8FAFC; border-top: 1px solid #E2E8F0; padding: 24px 20px; color: #64748B; font-size: 12px; line-height: 1.6;">
                  <p style="margin: 0 0 6px 0; font-weight: 700; color: #00123C; font-size: 13px;">Infogenx Talent Acquisition & HR Operations</p>
                  <p style="margin: 0 0 6px 0;">This is an automated operational email from Infogenx Recruitment Management System.</p>
                  <p style="margin: 0; color: #94A3B8;">&copy; 2026 Infogenx Pvt. Ltd. All Rights Reserved. • <a href="https://infogenx.com" target="_blank" style="color: #E65525; text-decoration: none; font-weight: 600;">infogenx.com</a></p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["To"] = to_email
    msg["From"] = "infogenx.jobs@gmail.com"
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    
    send_url = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
    r = requests.post(send_url, headers=headers, json={"raw": raw_message})
    print(f"[*] Gmail API dispatch status: {r.status_code}")
    if r.status_code == 200:
        print(f"✅ Welcome email delivered to {to_email} successfully!")
        return True
    else:
        print(f"[!] Gmail API response: {r.text}")
        return False

def register_in_cpanel_db(candidate_data, password):
    payload = {
        "name": candidate_data["fullName"],
        "email": candidate_data["email"],
        "password": password,
        "role": "candidate",
        "max_attempts": 1,
        "mobile": candidate_data.get("mobile", ""),
        "location": candidate_data.get("city", ""),
        "qualification": candidate_data.get("qualification", "")
    }
    r = requests.post(CANDIDATE_API_URL, json=payload, timeout=10)
    print(f"[*] cPanel MySQL Candidate User Registration status: {r.status_code}")
    if r.status_code == 200:
        print(f"✅ User registered in cPanel DB: {r.json().get('message')}")
        return True
    return False

def process_candidate_onboarding(candidate):
    print("=" * 60)
    print("INFOGENX FULL ONBOARDING PIPELINE EXECUTION")
    print("=" * 60)
    print(f"Candidate: {candidate['fullName']}")
    print(f"Email:     {candidate['email']}")
    print(f"Mobile:    {candidate['mobile']}")
    print("=" * 60)

    # 1. Generate Password
    pwd = generate_password(candidate["fullName"], candidate["dob"])
    print(f"[+] Generated Password: {pwd}")

    # 2. Register in cPanel MySQL DB for Candidate Portal Login
    register_in_cpanel_db(candidate, pwd)

    # 3. Dispatch Official Welcome Email from infogenx.jobs@gmail.com
    send_gmail(candidate["email"], candidate["fullName"], pwd)

    print("\n" + "=" * 60)
    print("🎉 FULL ONBOARDING & ASSESSMENT TEST ACCESS COMPLETE!")
    print("=" * 60)
    print(f"1. Login Portal:     {PORTAL_URL}")
    print(f"2. Registered Email: {candidate['email']}")
    print(f"3. Password:         {pwd}")
    print(f"4. Attempt Rule:     Strictly 1 Attempt")
    print(f"5. Google Sheet:     https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
    print("=" * 60)
    return {
        "email": candidate["email"],
        "password": pwd,
        "portal": PORTAL_URL,
        "status": "SUCCESS"
    }

if __name__ == "__main__":
    # Test candidate execution
    test_cand = {
        "fullName": "Mohamed Yasar",
        "dob": "2000-08-15",
        "email": "infogenx.jobs@gmail.com",
        "mobile": "+919787806366",
        "city": "Chennai, Tamil Nadu",
        "qualification": "B.E. Computer Science & Engineering",
        "college": "Anna University",
        "department": "Computer Science",
        "yearOfPassing": "2024"
    }
    process_candidate_onboarding(test_cand)
