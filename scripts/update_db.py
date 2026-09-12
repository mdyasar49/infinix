import json
from enrich_and_update_odoo_master import ENRICHED_LEADS

india_leads = [l for l in ENRICHED_LEADS if 'india' in l['country'].lower()]
aus_leads = [l for l in ENRICHED_LEADS if 'australia' in l['country'].lower()]
global_leads = [l for l in ENRICHED_LEADS if 'australia' not in l['country'].lower() and 'india' not in l['country'].lower()]

header = '''"""
Comprehensive enriched database of companies using Odoo in India, Australia, and Global.
Derived from technographic scraping, partner networks, customer directories, and dork footprints.
Enriched with Decision Makers, Verified Work Emails, Direct Phone Numbers, and LinkedIn profiles.
"""
'''

body = f"""
{header}

INDIA_COMPANIES = {json.dumps(india_leads, indent=4, ensure_ascii=False)}

AUSTRALIA_COMPANIES = {json.dumps(aus_leads, indent=4, ensure_ascii=False)}

GLOBAL_COMPANIES = {json.dumps(global_leads, indent=4, ensure_ascii=False)}

def get_companies_by_region(region="all"):
    reg = region.lower().strip()
    if reg in ["in", "india"]:
        return INDIA_COMPANIES
    elif reg in ["au", "aus", "australia"]:
        return AUSTRALIA_COMPANIES
    elif reg in ["global", "europe", "world"]:
        return GLOBAL_COMPANIES
    else:
        return INDIA_COMPANIES + AUSTRALIA_COMPANIES + GLOBAL_COMPANIES
"""

with open("d:/infonix/odoo-lead-generator/database.py", "w", encoding="utf-8") as f:
    f.write(body.strip() + "\n")

print("Successfully updated database.py with all 50 enriched leads!")
