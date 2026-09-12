#!/usr/bin/env python3
"""Validate Facebook deployment config before going live."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv
import os

SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(SCRIPT_DIR / ".env")

ok = True


def check(name: str, passed: bool, detail: str = "") -> None:
    global ok
    status = "OK  " if passed else "FAIL"
    if not passed:
        ok = False
    print(f"[{status}] {name}" + (f" — {detail}" if detail else ""))


def main() -> None:
    print("Facebook deployment check\n")

    env_path = SCRIPT_DIR / ".env"
    check(".env exists", env_path.exists(), str(env_path))

    sheet_id = os.environ.get("GOOGLE_SHEET_ID", "").strip()
    check("GOOGLE_SHEET_ID set", bool(sheet_id), sheet_id[:12] + "..." if len(sheet_id) > 12 else sheet_id or "missing")

    tab = os.environ.get("GOOGLE_SHEET_TAB", "Leads").strip() or "Leads"
    check("GOOGLE_SHEET_TAB", True, tab)

    cred_env = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "credentials/google_service_account.json")
    cred_path = Path(cred_env)
    if not cred_path.is_absolute():
        cred_path = SCRIPT_DIR / cred_path
    check("Service account JSON exists", cred_path.exists(), str(cred_path))

    client_email = ""
    if cred_path.exists():
        try:
            data = json.loads(cred_path.read_text())
            client_email = data.get("client_email", "")
            check("JSON has client_email", bool(client_email), client_email)
            check("JSON has private_key", bool(data.get("private_key")))
        except Exception as exc:
            check("JSON readable", False, str(exc))

    out = SCRIPT_DIR.parent / "Output" / "facebook_business_leads.csv"
    check("Output CSV exists", out.exists(), str(out))

    # Optional live Sheets access
    if sheet_id and cred_path.exists():
        try:
            sys.path.insert(0, str(SCRIPT_DIR))
            from sheets_sync import open_worksheet, existing_facebook_urls

            ws = open_worksheet()
            urls = existing_facebook_urls(ws)
            check("Google Sheet accessible", True, f"tab={ws.title}, existing_urls={len(urls)}")
        except Exception as exc:
            check("Google Sheet accessible", False, str(exc))
            print("\nTip: share the sheet with the service account email as Editor.")
            if client_email:
                print(f"     {client_email}")
    else:
        print("\nSkipped live Sheets test (ID or credentials missing).")

    print()
    if ok:
        print("All required checks passed. Ready to install cron.")
        print("See Documentation/DEPLOYMENT.md step 7.")
        sys.exit(0)
    print("Fix the FAIL items above, then re-run: python3 deploy_check.py")
    sys.exit(1)


if __name__ == "__main__":
    main()
