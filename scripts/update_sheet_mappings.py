import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Update Odoo Scraper -> Sheet 1: 1X_8LbsHisyvoCfjSuTX5yRVsRgXPDEmu3W5RWXuAC1o
odoo_script = r"d:\infonix\scripts\live_odoo_partner_tn_india_scraper.py"
with open(odoo_script, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'SPREADSHEET_ID = "18oHqPuo6BhAgI5e_GLSSps5fSc_DpzYEYofgPKxBv9o"',
    'SPREADSHEET_ID = "1X_8LbsHisyvoCfjSuTX5yRVsRgXPDEmu3W5RWXuAC1o"'
)

with open(odoo_script, "w", encoding="utf-8") as f:
    f.write(content)
print("✓ Updated live_odoo_partner_tn_india_scraper.py -> Sheet 1 (Odoo Leads)")

# 2. Update Zoho Scraper -> Sheet 2: 18oHqPuo6BhAgI5e_GLSSps5fSc_DpzYEYofgPKxBv9o
zoho_script = r"d:\infonix\scripts\live_zoho_partner_tn_india_scraper.py"
with open(zoho_script, "r", encoding="utf-8") as f:
    z_content = f.read()

z_content = z_content.replace(
    'SPREADSHEET_ID_ZOHO = "1X_8LbsHisyvoCfjSuTX5yRVsRgXPDEmu3W5RWXuAC1o"',
    'SPREADSHEET_ID_ZOHO = "18oHqPuo6BhAgI5e_GLSSps5fSc_DpzYEYofgPKxBv9o"'
)

with open(zoho_script, "w", encoding="utf-8") as f:
    f.write(z_content)
print("✓ Updated live_zoho_partner_tn_india_scraper.py -> Sheet 2 (Zoho Leads)")
