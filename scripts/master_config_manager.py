"""
================================================================================
🌐 Master Global Configuration Manager
================================================================================
Provides a single source of truth for:
- Spreadsheet URL / ID
- Odoo CRM Credentials & URL
- Zoho CRM settings
When updated, automatically synchronizes across all repositories and scripts.
================================================================================
"""

import os
import sys
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_CONFIG_PATH = os.path.join(BASE_DIR, "master_config.json")

REPO_CONFIG_PATHS = [
    os.path.join(BASE_DIR, "odoo-sheets-auto-sync", "config.json"),
    os.path.join(BASE_DIR, "odoo_uploader", "config.json"),
    os.path.join(BASE_DIR, "Data-Scraping", "config.json"),
    os.path.join(BASE_DIR, "Social-Media-Data-Scraping", "config.json"),
    os.path.join(BASE_DIR, "LinkedIn-Data-Scraping", "config.json")
]

def extract_sheet_id(url_or_id):
    if not url_or_id:
        return ""
    match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url_or_id)
    if match:
        return match.group(1)
    return url_or_id.strip()

def get_master_config():
    default_config = {
        "spreadsheet_url": "https://docs.google.com/spreadsheets/d/1iIcE_TI17N2hgva99ylF_RPyUZtllZHQu-SOUprSpB4/edit",
        "spreadsheet_id": "1iIcE_TI17N2hgva99ylF_RPyUZtllZHQu-SOUprSpB4",
        "sheet_name": "",
        "odoo_url": "https://app.canadiancrystalline.info",
        "odoo_db": "app365",
        "odoo_username": "admin",
        "odoo_password": "admin",
        "poll_interval_seconds": 60,
        "port": 8080
    }
    if os.path.exists(MASTER_CONFIG_PATH):
        try:
            with open(MASTER_CONFIG_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
                default_config.update(saved)
        except Exception:
            pass
    return default_config

def update_master_config(new_values):
    cfg = get_master_config()
    cfg.update(new_values)
    
    if "spreadsheet_url" in new_values:
        cfg["spreadsheet_id"] = extract_sheet_id(new_values["spreadsheet_url"])
    elif "spreadsheet_id" in new_values:
        cfg["spreadsheet_url"] = f"https://docs.google.com/spreadsheets/d/{new_values['spreadsheet_id']}/edit"

    # Save to master_config.json
    try:
        with open(MASTER_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"[-] Error writing master_config.json: {e}")

    # Propagate to all repositories
    for p in REPO_CONFIG_PATHS:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
        except Exception as e:
            print(f"[-] Warning: Failed to propagate config to {p}: {e}")

    return cfg

if __name__ == "__main__":
    cfg = get_master_config()
    print("=== CURRENT MASTER CONFIG ===")
    print(json.dumps(cfg, indent=2))
