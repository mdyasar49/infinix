import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SELENIUM_SCRIPT_TEMPLATE = """import os
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

LINKEDIN_USER = os.environ.get("LINKEDIN_USER", "")
LINKEDIN_PASS = os.environ.get("LINKEDIN_PASS", "")

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

def run_headless_update():
    print("=" * 80)
    print(" 🤖 SILENT HEADLESS PYTHON AUTOMATION FOR LINKEDIN PROFILE UPDATE")
    print("=" * 80)

    if not LINKEDIN_USER or not LINKEDIN_PASS:
        print("  [!] LINKEDIN_USER or LINKEDIN_PASS environment variables not set.")
        return

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        print("[+] Navigating silently to LinkedIn Login...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        # Fallback selectors for Username & Password fields
        email_input = None
        for selector in ["#username", "#session_key", "input[name='session_key']", "input[name='username']"]:
            try:
                email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                if email_input:
                    break
            except Exception:
                continue

        pass_input = None
        for selector in ["#password", "#session_password", "input[name='session_password']", "input[name='password']"]:
            try:
                pass_input = driver.find_element(By.CSS_SELECTOR, selector)
                if pass_input:
                    break
            except Exception:
                continue

        if not email_input or not pass_input:
            print("  [!] Could not locate login form fields on page.")
            print(f"  [i] Current URL: {driver.current_url}")
            return

        print("[+] Entering credentials silently...")
        email_input.clear()
        email_input.send_keys(LINKEDIN_USER)
        pass_input.clear()
        pass_input.send_keys(LINKEDIN_PASS)
        pass_input.send_keys(Keys.RETURN)

        time.sleep(5)
        print(f"[+] Current URL after login submission: {driver.current_url}")

        if "checkpoint" in driver.current_url or "challenge" in driver.current_url:
            print("  [!] LinkedIn requested Security Verification / Captcha Code.")
            print("  [i] Check your email or SMS for verification prompt.")
            return

        print("[+] Navigating to Profile Page...")
        driver.get("https://www.linkedin.com/in/mohamed-yasar-4674ba223/")
        time.sleep(4)

        print("  [🎉] SUCCESS: Headless Session authenticated successfully!")
    except Exception as e:
        print(f"  [!] Automation error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_headless_update()
"""

def main():
    script_path = os.path.join(r"d:\infonix", "scripts", "automate_linkedin_headless.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(SELENIUM_SCRIPT_TEMPLATE)
    print(f"[✓] Fixed and updated headless script: {script_path}")

if __name__ == "__main__":
    main()
