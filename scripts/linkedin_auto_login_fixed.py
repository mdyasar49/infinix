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

def run_login_fixed():
    print("=" * 80)
    print(" 🚀 FIXED ROCK-SOLID LINKEDIN PROFILE AUTOMATION ENGINE")
    print("=" * 80)

    user = os.environ.get("LINKEDIN_USER", "mohamedyasar081786@gmail.com")
    password = os.environ.get("LINKEDIN_PASS", "")

    if not password:
        import getpass
        print(f"User Email: {user}")
        password = getpass.getpass("Enter your LinkedIn Password: ").strip()

    if not password:
        print("[!] Password is required.")
        return

    # Use a custom temporary profile directory to prevent Chrome locking errors
    temp_profile_dir = os.path.join(r"d:\infonix", "scratch", "chrome_temp_profile")
    os.makedirs(temp_profile_dir, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        print("[+] Navigating to LinkedIn Login...")
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        # Locate visible interactive fields
        wait = WebDriverWait(driver, 10)
        
        email_el = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        pass_el = wait.until(EC.visibility_of_element_located((By.ID, "password")))

        print("[+] Entering credentials into visible fields...")
        driver.execute_script("arguments[0].scrollIntoView(true);", email_el)
        email_el.clear()
        email_el.send_keys(user)

        driver.execute_script("arguments[0].scrollIntoView(true);", pass_el)
        pass_el.clear()
        pass_el.send_keys(password)
        pass_el.send_keys(Keys.RETURN)

        time.sleep(5)
        print(f"[+] Current Page URL: {driver.current_url}")

        if "checkpoint" in driver.current_url or "challenge" in driver.current_url:
            print("  [!] Security Checkpoint requested by LinkedIn.")
            print("  [i] Please check your email or phone for verification code.")
            return

        print("[+] Navigating to Profile Page...")
        driver.get("https://www.linkedin.com/in/mohamed-yasar-4674ba223/")
        time.sleep(4)

        print("[🎉] SUCCESS: Authenticated & Session Ready!")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_login_fixed()
