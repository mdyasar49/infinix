import os
import sys
import subprocess
import getpass

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    print("=" * 80)
    print(" 🚀 LINKEDIN AUTOMATED MULTI-CREDENTIAL PROFILE UPDATER")
    print("=" * 80)
    
    user = input("Enter LinkedIn Email/Username [Default: mohamedyasar081786@gmail.com]: ").strip()
    if not user:
        user = "mohamedyasar081786@gmail.com"
        
    password = getpass.getpass("Enter your LinkedIn Password: ").strip()
    if not password:
        print("[!] Password cannot be empty.")
        return

    os.environ["LINKEDIN_USER"] = user
    os.environ["LINKEDIN_PASS"] = password

    script_path = os.path.join(r"d:\infonix", "scripts", "automate_linkedin_headless.py")
    subprocess.run([sys.executable, script_path])

if __name__ == "__main__":
    main()
