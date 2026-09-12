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

def run_google_sso():
    print("=" * 80)
    print(" 🚀 LINKEDIN CONTINUE WITH GOOGLE (SSO) AUTOMATION ENGINE")
    print("=" * 80)
    print("  [i] Chrome window will open. Click 'Continue with Google' or log in with Google.")
    print("  [i] Once logged in, the script will automatically take over and update your profile!")
    print("=" * 80)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        print("[+] Navigating to LinkedIn Login...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        # Look for 'Continue with Google' button and click if present
        try:
            google_btns = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='Google'], .nsm7Bb-HzV7m-Lg4B8e, iframe[title*='Google']")
            if google_btns:
                print("  [➔] Found 'Continue with Google' button! Clicking...")
                google_btns[0].click()
                time.sleep(3)
        except Exception:
            pass

        print("\n[➔] Waiting for LinkedIn login completion...")
        print("[i] Please complete Google Sign-In in the opened Chrome window...")

        # Wait until user reaches feed or profile page
        max_wait = 120 # 2 minutes
        start_time = time.time()
        logged_in = False

        while time.sleep(2) or (time.time() - start_time < max_wait):
            current_url = driver.current_url
            if any(k in current_url for k in ["feed", "in/", "mynetwork", "messaging"]):
                print("\n  [🎉] SUCCESS: Google Sign-In Completed & LinkedIn Session Detected!")
                logged_in = True
                break

        if not logged_in:
            print("  [!] Login wait timed out. Please try running again once ready.")
            return

        print("[+] Navigating to Mohamed Yasar's Profile Page...")
        driver.get("https://www.linkedin.com/in/mohamed-yasar-4674ba223/")
        time.sleep(4)

        print("  [✓] Profile Page Loaded successfully!")
        time.sleep(5)
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_google_sso()
