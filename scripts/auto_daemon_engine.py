import os
import sys
import time
import subprocess
import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"d:\infonix"
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

def run_lead_acquisition_engine():
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{now_str}] 🚀 AUTOMATED CRON ENGINE: Running Resume Client Acquisition Engine...")
    
    script_path = os.path.join(SCRIPTS_DIR, "resume_client_acquisition_engine.py")
    if os.path.exists(script_path):
        res = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[{now_str}]  [🎉] Automated Run Successful!")
            print(res.stdout[:300])
        else:
            print(f"[{now_str}]  [!] Error running script: {res.stderr}")
    else:
        print(f"[{now_str}]  [!] Script not found: {script_path}")

def main():
    print("=" * 80)
    print(" 🤖 100% AUTOMATED BACKGROUND DAEMON ENGINE LAUNCHED")
    print("=" * 80)
    print("  • Automatically executing Lead Acquisition & Outreach Engine")
    print("  • Scheduled to run every 12 hours automatically")
    print("=" * 80)

    # Initial immediate run
    run_lead_acquisition_engine()

    INTERVAL_SECONDS = 12 * 3600  # 12 hours
    print(f"\n[i] Daemon is active. Next automated execution in 12 hours...")
    
    try:
        while True:
            time.sleep(INTERVAL_SECONDS)
            run_lead_acquisition_engine()
    except KeyboardInterrupt:
        print("\n[i] Daemon stopped by user.")

if __name__ == "__main__":
    main()
