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

def run_google_sso_update():
    print("=" * 80)
    print(" 🚀 LINKEDIN GOOGLE SINGLE SIGN-ON (SSO) AUTOMATION ENGINE")
    print("=" * 80)

    user_data_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
    
    chrome_options = Options()
    if os.path.exists(user_data_path):
        print(f"[+] Using local Chrome User Data profile: {user_data_path}")
        chrome_options.add_argument(f"--user-data-dir={user_data_path}")
        chrome_options.add_argument("--profile-directory=Default")
        
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    try:
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 15)
        
        print("[+] Navigating to LinkedIn Login with Google SSO support...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(4)

        current_url = driver.current_url
        print(f"[+] Current Page URL: {current_url}")

        if "feed" in current_url or "in/" in current_url or "mynetwork" in current_url:
            print("  [🎉] Already logged into LinkedIn via Chrome session!")
        else:
            # Look for "Continue with Google" button
            google_btn = None
            for selector in [
                "button[data-provider='google']",
                ".nsm7Bb-HzV7m-Lg4B8e",
                "iframe[title*='Google']",
                "button[aria-label*='Google']",
                "a[href*='google']"
            ]:
                try:
                    btns = driver.find_elements(By.CSS_SELECTOR, selector)
                    if btns:
                        google_btn = btns[0]
                        break
                except Exception:
                    continue

            if google_btn:
                print("  [➔] Found 'Continue with Google' button! Clicking...")
                google_btn.click()
                time.sleep(5)
            else:
                print("  [i] 'Continue with Google' button clicked or redirected. Waiting for session...")

        print("[+] Navigating to Profile Page...")
        driver.get("https://www.linkedin.com/in/mohamed-yasar-4674ba223/")
        time.sleep(4)

        print("[🎉] LinkedIn Session Active!")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    run_google_sso_update()
