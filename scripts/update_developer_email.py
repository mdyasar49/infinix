import urllib.request
import json
import subprocess
import os
import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_GITHUB_TOKEN"
USER_NAME = "mdyasar49"
DEV_EMAIL = "mdyasardeveloper786@gmail.com"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Python"
}

def update_user_profile():
    print(f"[+] Updating GitHub Profile email & bio for '{DEV_EMAIL}'...")
    url = "https://api.github.com/user"
    payload = json.dumps({
        "name": "Mohamed Yasar",
        "company": "Independent Software Consultant",
        "blog": f"mailto:{DEV_EMAIL}",
        "location": "Chennai, India / Remote Worldwide",
        "bio": f"⚡ Senior AI & Enterprise Software Architect | Web Crawlers, Twilio Telephony & Full-Stack Apps. Contact: {DEV_EMAIL}",
        "hireable": True
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=HEADERS, method="PATCH")
    try:
        with urllib.request.urlopen(req) as resp:
            print("  [✓] GitHub Profile updated with developer email!")
    except Exception as e:
        print(f"  [!] Profile update output: {e}")

def update_profile_readme():
    print(f"[+] Updating Profile README with developer email '{DEV_EMAIL}'...")
    readme_dir = os.path.join(r"d:\infonix", "scratch", "profile_readme")
    readme_path = os.path.join(readme_dir, "README.md")
    
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace old email with new email
        new_content = re.sub(r"[a-zA-Z0-9._%+-]+@gmail\.com", DEV_EMAIL, content)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        auth_remote = f"https://{USER_NAME}:{TOKEN}@github.com/{USER_NAME}/{USER_NAME}.git"
        clean_remote = f"https://github.com/{USER_NAME}/{USER_NAME}.git"

        subprocess.run(["git", "add", "."], cwd=readme_dir, check=True)
        subprocess.run(["git", "commit", "-m", f"Update contact email to {DEV_EMAIL}"], cwd=readme_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        res = subprocess.run(["git", "push", "-u", auth_remote, "main", "--force"], cwd=readme_dir, capture_output=True, text=True)
        subprocess.run(["git", "remote", "set-url", "origin", clean_remote], cwd=readme_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if res.returncode == 0:
            print("  [🎉] SUCCESS: Profile README updated and pushed!")
        else:
            print(f"  [!] Push Error: {res.stderr}")

def update_script_templates():
    print(f"[+] Updating Outreach Engines with developer email '{DEV_EMAIL}'...")
    script_paths = [
        os.path.join(r"d:\infonix", "scripts", "resume_client_acquisition_engine.py"),
        os.path.join(r"d:\infonix", "scripts", "48hr_client_acquisition_engine.py")
    ]
    for sp in script_paths:
        if os.path.exists(sp):
            with open(sp, "r", encoding="utf-8") as f:
                txt = f.read()
            txt = re.sub(r"[a-zA-Z0-9._%+-]+@gmail\.com", DEV_EMAIL, txt)
            with open(sp, "w", encoding="utf-8") as f:
                f.write(txt)
            print(f"  [✓] Updated: {os.path.basename(sp)}")

def main():
    print("=" * 80)
    print(f" 🚀 UPDATING DEVELOPER EMAIL TO: {DEV_EMAIL}")
    print("=" * 80)

    update_user_profile()
    update_profile_readme()
    update_script_templates()

    print("=" * 80)

if __name__ == "__main__":
    main()
