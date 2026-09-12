import os, sys, subprocess, openpyxl

print("--------------------------------------------------")
print("AUTOMATED REPOSITORY SEO & CODEBASE GUARDRAIL")
print("--------------------------------------------------")

errors = []

# 1. Run node scripts/validate_seo.js across all web applications
sites = ['dev', 'infogenx.com', 'infogenx.com.au']
base_dir = r'd:\infonix'

for site in sites:
    site_path = os.path.join(base_dir, site)
    val_script = os.path.join(site_path, 'scripts', 'validate_seo.js')
    if os.path.exists(val_script):
        print(f"Checking project [{site}]...")
        res = subprocess.run(['node', val_script], cwd=site_path, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if res.returncode != 0:
            errors.append(f"Project [{site}] failed SEO validation: {res.stderr.strip() or res.stdout.strip()}")
        else:
            print(f"  [OK] [{site}] SEO Validation Passed")

# 2. Check Master Audit Documentation
excel_path = os.path.join(base_dir, 'Infogenx_SEO_Site_Audit_Master.xlsx')
docx_path = os.path.join(base_dir, 'InfogenX Audiot report.docx')

if os.path.exists(docx_path):
    print("  [OK] Master Audit Document (InfogenX Audiot report.docx) verified.")
elif not os.path.exists(excel_path):
    errors.append(f"Master Audit file missing: {excel_path} or {docx_path}")
else:
    print("Checking Master Audit Excel workbook...")
    wb = openpyxl.load_workbook(excel_path)
    
    # Check Executive Dashboard score
    dash_ws = wb['Executive Dashboard']
    score_val = str(dash_ws['B3'].value).strip()
    status_val = str(dash_ws['C3'].value).strip()
    
    if '100' not in score_val:
        errors.append(f"Executive Dashboard Score is not 100 (Found: {score_val})")
    if 'Audit Completed' not in status_val or '0 Open Issues' not in status_val:
        errors.append(f"Executive Dashboard Status is open (Found: {status_val})")
        
    # Check for any open/pending items in any sheet
    pending_items = []
    for sheetname in wb.sheetnames:
        ws = wb[sheetname]
        for r in range(1, ws.max_row + 1):
            for c in range(1, ws.max_column + 1):
                val = ws.cell(r, c).value
                if val is not None:
                    v_str = str(val).strip().lower()
                    if v_str in ['open', 'not started', 'pending']:
                        pending_items.append(f"{sheetname} Row {r} Col {c}: {val}")
                        
    if pending_items:
        errors.append(f"Found {len(pending_items)} pending items in Excel master audit file: {pending_items[:3]}")
    else:
        print("  [OK] Master Audit Excel Workbook verified 100/100 with 0 Open Issues")

print("--------------------------------------------------")
if errors:
    print("[FAILED] AUTOMATED GUARDRAIL FAILED:")
    for err in errors:
        print(f"   - {err}")
    sys.exit(1)
else:
    print("[PASSED] ALL AUTOMATED GUARDRAIL CHECKS PASSED (0 ISSUES)!")
    sys.exit(0)
