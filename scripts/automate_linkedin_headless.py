import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Support testing multiple potential credential pairs if provided
CREDENTIAL_PAIRS = [
    (os.environ.get("LINKEDIN_USER", ""), os.environ.get("LINKEDIN_PASS", "")),
    ("mohamedyasar081786@gmail.com", os.environ.get("LINKEDIN_PASS", "")),
    ("mdyasardeveloper786@gmail.com", os.environ.get("LINKEDIN_PASS", ""))
]

HEADLINE = "⚡ Senior AI & Enterprise Software Architect | B2B Web Scrapers, Twilio Cloud Telephony & React/Node SaaS Apps | Helping Businesses Automate & Scale | 📧 mdyasardeveloper786@gmail.com"

ABOUT_TEXT = '''👋 Hi, I'm Mohamed Yasar — Senior AI & Enterprise Software Architect.

I help founders, agencies, and enterprise businesses build automated, high-margin software systems — from custom B2B lead scraping engines and cloud telephony dialers to multimodal AI voice agents and full-stack web applications.

🛠️ CORE SERVICES & TECHNICAL SOLUTIONS I PROVIDE:
1️⃣ Custom B2B Lead Scraping & Data Extraction Engines
2️⃣ Twilio Cloud Telephony & Custom Dialer Applications
3️⃣ Conversational AI & Multimodal Gemini Voice Agents
4️⃣ Full-Stack Web Development & Enterprise SaaS

💼 HIGHLIGHTED CASE STUDY:
⚡ Infogenx Cloud Telephony & AI Voice Engine: Engineered an enterprise Twilio WebRTC dialer app and real-time Gemini AI voice assistant for high-volume client operations.

📬 LET'S WORK TOGETHER:
📧 Email: mdyasardeveloper786@gmail.com
💻 GitHub Portfolio: https://github.com/mdyasar49
🤝 Available For: Direct Freelance Contracts, Technical Consultations & Software Retainers.'''

def try_login_with_driver(driver, user, password):
    if not user or not password:
        return False
        
    print(f"\n[+] Testing Login Credentials for user: {user}...")
    
    # Try direct login page
    urls = [
        "https://www.linkedin.com/login",
        "https://www.linkedin.com/uas/login",
        "https://www.linkedin.com/checkpoint/lg/login"
    ]
    
    for login_url in urls:
        try:
            print(f"  [➔] Loading: {login_url}")
            driver.get(login_url)
            time.sleep(3)
            
            # Find input elements
            inputs = driver.find_elements(By.TAG_NAME, "input")
            email_field = None
            pass_field = None
            
            for inp in inputs:
                inp_type = inp.get_attribute("type") or ""
                inp_name = inp.get_attribute("name") or ""
                inp_id = inp.get_attribute("id") or ""
                
                if inp_type in ["text", "email"] or "user" in inp_name or "session" in inp_name or "username" in inp_id or "session_key" in inp_id:
                    if not email_field:
                        email_field = inp
                elif inp_type == "password" or "pass" in inp_name or "password" in inp_id:
                    if not pass_field:
                        pass_field = inp

            if email_field and pass_field:
                print(f"  [✓] Located login input fields on {login_url}!")
                email_field.clear()
                email_field.send_keys(user)
                pass_field.clear()
                pass_field.send_keys(password)
                pass_field.send_keys(Keys.RETURN)
                
                time.sleep(5)
                current_url = driver.current_url
                print(f"  [i] Redirect URL after submit: {current_url}")
                
                if "feed" in current_url or "in/" in current_url or "mynetwork" in current_url or "dashboard" in current_url:
                    print(f"  [🎉] SUCCESS: Authenticated successfully with {user}!")
                    return True
                elif "checkpoint" in current_url or "challenge" in current_url:
                    print(f"  [⚠️] Security Checkpoint / Verification code required for {user}.")
                    print("  [i] Please check your email or phone SMS for verification code.")
                    return True
                elif "login" in current_url or "error" in current_url:
                    print(f"  [!] Login failed for {user} (Incorrect password or username).")
                    continue
        except Exception as e:
            print(f"  [!] Error during login attempt on {login_url}: {e}")
            
    return False

def main():
    print("=" * 80)
    print(" 🤖 MULTI-CREDENTIAL HEADLESS LINKEDIN AUTOMATION ENGINE")
    print("=" * 80)

    chrome_options = Options()
    # Stealth options for LinkedIn compatibility
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    # Bypass navigator.webdriver detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        user_env = os.environ.get("LINKEDIN_USER", "")
        pass_env = os.environ.get("LINKEDIN_PASS", "")

        pairs = []
        if user_env and pass_env:
            pairs.append((user_env, pass_env))
        pairs.extend([
            ("mohamedyasar081786@gmail.com", pass_env),
            ("mdyasardeveloper786@gmail.com", pass_env)
        ])

        success = False
        for u, p in pairs:
            if u and p:
                if try_login_with_driver(driver, u, p):
                    success = True
                    break

        if not success:
            print("\n[!] None of the provided credential pairs were able to log in successfully.")
            print("[i] Please check that the password entered is correct.")

    except Exception as e:
        print(f"[!] Engine Exception: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
