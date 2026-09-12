import os
import sys
import docx

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from docx.shared import Inches, Pt, RGBColor
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header_banner(doc, title, subtitle):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_title = p.add_run(title)
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0, 51, 102) # Dark Navy
    
    p_sub = doc.add_paragraph()
    run_sub = p_sub.add_run(subtitle)
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 100, 100)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_section_heading(doc, text):
    h = doc.add_heading(level=1)
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 51, 102)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)

def add_sub_heading(doc, text):
    h = doc.add_heading(level=2)
    run = h.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(51, 102, 153)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(2)

def add_bullet(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(0)
    
    r_bold = p.add_run(bold_prefix + ": ")
    r_bold.bold = True
    r_bold.font.name = 'Calibri'
    r_bold.font.size = Pt(10.5)
    r_bold.font.color.rgb = RGBColor(30, 30, 30)
    
    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = RGBColor(50, 50, 50)

def add_body_paragraph(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(40, 40, 40)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F2F4F7")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(30, 30, 30)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_custom_table(doc, headers, data):
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Format Header Row
    hdr_cells = tbl.rows[0].cells
    for idx, header_text in enumerate(headers):
        hdr_cells[idx].text = header_text
        set_cell_background(hdr_cells[idx], "003366")
        set_cell_margins(hdr_cells[idx], top=100, bottom=100, left=150, right=150)
        p = hdr_cells[idx].paragraphs[0]
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(10)
            
    # Format Data Rows
    for r_idx, row_data in enumerate(data):
        row_cells = tbl.rows[r_idx + 1].cells
        bg_color = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(40, 40, 40)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Output Paths
output_dir_workspace = r"d:\infonix"
output_dir_artifact = r"C:\Users\HP\.gemini\antigravity-ide\brain\51026764-4558-48d2-b272-a018ce0ad279"

print("Generating 7 Separate DOCX Technical Manuals...")

# ==============================================================================
# 1. DOC_odoo_lead_generator.docx
# ==============================================================================
doc1 = docx.Document()
add_header_banner(doc1, "Technical Documentation: odoo-lead-generator", "Automated Odoo ERP Technographic Discovery & Executive Contact Enrichment Engine")

add_section_heading(doc1, "1. Executive Summary & Purpose")
add_body_paragraph(doc1, "The odoo-lead-generator system automatically inspects web technologies, domain headers, and public directories to discover mid-market companies running Odoo ERP across Australia and international markets. It enriches discovered records with C-level executive details, verified work emails, and phone numbers.")

add_section_heading(doc1, "2. Execution Commands & Setup Guide")
add_sub_heading(doc1, "Prerequisites")
add_bullet(doc1, "Python Environment", "Python 3.10+ required")
add_bullet(doc1, "Dependencies", "pip install requests beautifulsoup4 openpyxl pandas google-genai")
add_bullet(doc1, "API Credentials", "SERPER_API_KEY and GEMINI_API_KEY configured in .env file")

add_sub_heading(doc1, "Manual Run Command")
add_code_block(doc1, "python d:\\infonix\\scripts\\enrich_and_update_odoo_master.py")

add_sub_heading(doc1, "Automated Task Scheduler Setup")
add_code_block(doc1, 'schtasks /create /tn "OdooLeadGeneratorCron" /tr "python d:\\infonix\\scripts\\enrich_and_update_odoo_master.py" /sc daily /st 09:00 /f /rl HIGHEST')

add_section_heading(doc1, "3. Execution Frequency & Schedule Interval")
add_bullet(doc1, "Schedule Interval", "Daily at 09:00 AM (Runs automatically once every 24 hours)")
add_bullet(doc1, "On-Demand Triggering", "Can be executed manually anytime new target domain batches or partner lists are added")

add_section_heading(doc1, "4. Scraping Keywords & Technographic Footprints")
add_sub_heading(doc1, "HTML/JS Code Signatures")
add_bullet(doc1, "Framework Signatures", "/web/static/, /web/login, odoo.define, web.assets_backend, website_sale, Odoo Session ID")
add_sub_heading(doc1, "Search Engine Dorks & Google Serper Queries")
add_bullet(doc1, "Search Dorks", '"Powered by Odoo", site:.com.au "Odoo ready partner", site:.co.in "Odoo implementation", "Odoo ERP Australia", "Odoo Gold Partner", inurl:/shop "Odoo"')

add_section_heading(doc1, "5. Scraped Data Schema")
headers = ["Field Name", "Description", "Example Value"]
data = [
    ["Company Name", "Normalized Legal Enterprise Name", "Apex Industrial Supplies"],
    ["Domain / Web URL", "Target Corporate Domain", "apexsupplies.com.au"],
    ["Contact Person", "Executive Decision-Maker", "Marcus Vance"],
    ["Job Title", "C-Level / Operational Title", "Director of Sales & Operations"],
    ["Work Email", "MX & DNS Validated Business Email", "m.vance@apexsupplies.com.au"],
    ["Phone Number", "Formatted International Phone", "+61 3 9580 4421"],
    ["Email Status", "Verification State", "Verified (MX Validated)"],
    ["Odoo Sourcing", "Technographic Signal Source", "Technographic Scraping (/web/static/)"]
]
add_custom_table(doc1, headers, data)

doc1.save(os.path.join(output_dir_workspace, "DOC_odoo_lead_generator.docx"))
doc1.save(os.path.join(output_dir_artifact, "DOC_odoo_lead_generator.docx"))
print("✓ DOC_odoo_lead_generator.docx created")

# ==============================================================================
# 2. DOC_zoho_lead_generator.docx
# ==============================================================================
doc2 = docx.Document()
add_header_banner(doc2, "Technical Documentation: zoho-lead-generator", "Automated Technographic Hunter for Zoho Ecosystem in Australia & India")

add_section_heading(doc2, "1. Executive Summary & Purpose")
add_body_paragraph(doc2, "The zoho-lead-generator engine discovers mid-market enterprises utilizing Zoho One, Zoho CRM, Zoho Books, or Deluge scripting. It targets key business hubs in Australia and India to build enriched lead pipelines.")

add_section_heading(doc2, "2. Execution Commands & Setup Guide")
add_sub_heading(doc2, "Prerequisites")
add_bullet(doc2, "Python & Zoho Access", "Python 3.10+ and Zoho CRM API v2 OAuth token / Deluge Manager access")
add_bullet(doc2, "Dependencies", "pip install requests beautifulsoup4 gspread google-auth")

add_sub_heading(doc2, "Manual Run Commands")
add_code_block(doc2, "python d:\\infonix\\Social-Media-Data-Scraping\\upload_all_sheets_direct_to_zoho.py")

add_sub_heading(doc2, "Deluge Script Execution")
add_body_paragraph(doc2, "Trigger ZOHO_CRM_DELUGE_SCHEDULED_FUNCTION_CLEAN.deluge inside Zoho CRM Scheduled Functions.")

add_sub_heading(doc2, "Automated Task Scheduler Setup")
add_code_block(doc2, 'schtasks /create /tn "ZohoLeadGeneratorCron" /tr "python d:\\infonix\\Social-Media-Data-Scraping\\upload_all_sheets_direct_to_zoho.py" /sc daily /st 09:00 /f /rl HIGHEST')

add_section_heading(doc2, "3. Execution Frequency & Schedule Interval")
add_bullet(doc2, "Scheduled Cron", "Daily at 08:00 AM & 09:00 AM (Runs once every 24 hours)")
add_bullet(doc2, "Real-Time Sync", "Zoho Flow webhooks listen continuously for Google Sheets row updates")

add_section_heading(doc2, "4. Scraping Keywords & Search Patterns")
add_bullet(doc2, "Product Keywords", "Zoho CRM, Zoho One, Zoho Books, Zoho Creator, Zoho Desk, Deluge Scripting, Zoho Flow")
add_bullet(doc2, "Search Queries", '"Zoho Advanced Partner" Sydney, "Zoho Authorized Partner" Melbourne, "Zoho CRM migration", site:zoho.com/partners "Australia"')

add_section_heading(doc2, "5. Scraped Data Schema")
data2 = [
    ["Lead Source", "Originating Directory", "Zoho Partner Directory / Google Search"],
    ["Company Name", "Target Business Name", "Apex Cloud Systems AU"],
    ["Customer Name", "Contact Representative", "Ethan Wright"],
    ["Work Email", "Validated Corporate Email", "ethan.wright@apexcloud.com.au"],
    ["Phone / Mobile", "Formatted Phone Number", "+61 2 8765 4321"],
    ["Industry", "Target Industry Vertical", "IT / Software"],
    ["Rating", "Lead Qualification State", "Verified Ecosystem User"]
]
add_custom_table(doc2, headers, data2)

doc2.save(os.path.join(output_dir_workspace, "DOC_zoho_lead_generator.docx"))
doc2.save(os.path.join(output_dir_artifact, "DOC_zoho_lead_generator.docx"))
print("✓ DOC_zoho_lead_generator.docx created")

# ==============================================================================
# 3. DOC_Social_Media_Data_Scraping.docx
# ==============================================================================
doc3 = docx.Document()
add_header_banner(doc3, "Technical Documentation: Social-Media-Data-Scraping", "Multi-Platform Social Media Lead Scraper & AI Business Intelligence Analyzer")

add_section_heading(doc3, "1. Executive Summary & Purpose")
add_body_paragraph(doc3, "This platform scans Instagram, Facebook, X (Twitter), YouTube, and Pinterest for pre-launch startups, new business announcements, and hiring intent. Gemini 3.1 Flash / 3.6 Flash AI parses captions and extracts buyer intent.")

add_section_heading(doc3, "2. Execution Commands & Setup Guide")
add_sub_heading(doc3, "Manual Execution Commands")
add_code_block(doc3, "python d:\\infonix\\Social-Media-Data-Scraping\\job_vacancy_scraper.py\npython d:\\infonix\\Social-Media-Data-Scraping\\social_scraper_serper.py\npython d:\\infonix\\Social-Media-Data-Scraping\\sync_to_google_sheet.py")

add_sub_heading(doc3, "Automated Task Scheduler Setup")
add_code_block(doc3, "cmd /c d:\\infonix\\Social-Media-Data-Scraping\\setup_schedule.bat")

add_section_heading(doc3, "3. Execution Frequency & Schedule Interval")
add_bullet(doc3, "Schedule Task Name", "SocialMediaLeadScraperCron")
add_bullet(doc3, "Schedule Interval", "Daily at 09:00 AM (Runs once every 24 hours)")

add_section_heading(doc3, "4. Scraping Keywords & Pre-Launch Triggers")
add_bullet(doc3, "Pre-Launch Triggers", "coming soon, launching soon, opening soon, new launch, pre-launch, website launching, getting ready to launch, grand opening, beta launch, early access, we are launching")
add_bullet(doc3, "Social Dorks", 'site:facebook.com "launching soon", site:instagram.com "coming soon", site:twitter.com "pre-launch"')

add_section_heading(doc3, "5. Scraped Data Schema")
data3 = [
    ["Scraped Date", "Timestamp", "YYYY-MM-DD"],
    ["Platform", "Source Network", "Instagram / Facebook / LinkedIn / X / YouTube"],
    ["Company / Page Name", "Brand Title", "TechFlow Systems"],
    ["Email & Phone", "Contact Information", "sarah.smith@techflow.io | +61 412 345 678"],
    ["Notes", "Gemini AI Summary", "AI generated summary of business launch requirements"]
]
add_custom_table(doc3, headers, data3)

doc3.save(os.path.join(output_dir_workspace, "DOC_Social_Media_Data_Scraping.docx"))
doc3.save(os.path.join(output_dir_artifact, "DOC_Social_Media_Data_Scraping.docx"))
print("✓ DOC_Social_Media_Data_Scraping.docx created")

# ==============================================================================
# 4. DOC_LinkedIn_Data_Scraping.docx
# ==============================================================================
doc4 = docx.Document()
add_header_banner(doc4, "Technical Documentation: LinkedIn-Data-Scraping", "Automated LinkedIn B2B Prospecting & Contact Intelligence Extractor with Anti-Detection Guard")

add_section_heading(doc4, "1. Executive Summary & Purpose")
add_body_paragraph(doc4, "LinkedIn-Data-Scraping executes stealthy B2B contact extraction using Selenium and Playwright with anti-detection guardrails (dynamic sleep intervals, user-agent rotation, and webdriver flag masking).")

add_section_heading(doc4, "2. Execution Commands & Setup Guide")
add_sub_heading(doc4, "Manual Execution Commands")
add_code_block(doc4, "python d:\\infonix\\LinkedIn-Data-Scraping\\linkedinScraper.py\npython d:\\infonix\\LinkedIn-Data-Scraping\\sync_to_google_sheet.py")

add_sub_heading(doc4, "Automated Task Scheduler Setup")
add_code_block(doc4, "cmd /c d:\\infonix\\LinkedIn-Data-Scraping\\setup_schedule.bat")

add_section_heading(doc4, "3. Execution Frequency & Schedule Interval")
add_bullet(doc4, "Schedule Task Name", "LinkedInLeadScraperCron")
add_bullet(doc4, "Schedule Interval", "Daily at 09:00 AM (Runs once every 24 hours)")

add_section_heading(doc4, "4. Scraping Keywords & Dorks")
add_bullet(doc4, "Search Dorks", 'site:linkedin.com/in/ "Full Stack Developer" "Australia", site:linkedin.com/company/ "Odoo partner"')
add_bullet(doc4, "Target Roles", "Managing Director, Director of IT, CEO, Founder, Full Stack Developer, React Developer, Python Developer, Senior AI Engineer")

add_section_heading(doc4, "5. Scraped Data Schema")
data4 = [
    ["Profile Link", "Direct Profile URL", "https://www.linkedin.com/in/marcus-vance/"],
    ["Customer Name", "Full Name", "Marcus Vance"],
    ["Designation", "Current Job Title", "Director of IT"],
    ["Company", "Employer Name", "Apex Cloud Systems"],
    ["Work Email", "MX Verified Email", "marcus.v@apexcloud.com.au"]
]
add_custom_table(doc4, headers, data4)

doc4.save(os.path.join(output_dir_workspace, "DOC_LinkedIn_Data_Scraping.docx"))
doc4.save(os.path.join(output_dir_artifact, "DOC_LinkedIn_Data_Scraping.docx"))
print("✓ DOC_LinkedIn_Data_Scraping.docx created")

# ==============================================================================
# 5. DOC_Data_Scraping.docx
# ==============================================================================
doc5 = docx.Document()
add_header_banner(doc5, "Technical Documentation: Data-Scraping", "Scalable Multi-Channel B2B Web Scraping Engine for Upwork, Freelancer, Clutch & DesignRush")

add_section_heading(doc5, "1. Executive Summary & Purpose")
add_body_paragraph(doc5, "Data-Scraping is a multi-platform contract job scraper targeting Upwork, Freelancer.com, Clutch.co, and DesignRush to discover web development, scraping, and software engineering leads.")

add_section_heading(doc5, "2. Execution Commands & Setup Guide")
add_sub_heading(doc5, "Manual Execution Commands")
add_code_block(doc5, "python d:\\infonix\\Data-Scraping\\run_all.py\npython d:\\infonix\\Data-Scraping\\Upwork\\upwork_new.py\npython d:\\infonix\\Data-Scraping\\sync_to_google_sheet.py")

add_sub_heading(doc5, "Automated Task Scheduler Setup")
add_code_block(doc5, "cmd /c d:\\infonix\\Data-Scraping\\setup_schedule.bat")

add_section_heading(doc5, "3. Execution Frequency & Schedule Interval")
add_bullet(doc5, "Schedule Task Name", "FreelancerUpworkLeadScraperCron")
add_bullet(doc5, "Schedule Interval", "Daily at 09:00 AM (Runs once every 24 hours)")

add_section_heading(doc5, "4. Scraping Intent Keywords")
add_bullet(doc5, "Contract Keywords", "scrap, scrape, scraping, extractor, data extraction, migration, migrate, redesign, upgrade, landing page, site link, web address")

add_section_heading(doc5, "5. Scraped Data Schema")
data5 = [
    ["Job Title", "Project Title", "Python Web Scraper for E-commerce"],
    ["Budget / Hourly Rate", "Financial Scope", "$500 Fixed / $35-$50 per hr"],
    ["Client Spent", "Total Platform Spend", "$10,000+ Spent"],
    ["Client Location", "Geographic Location", "Australia / USA / Global"]
]
add_custom_table(doc5, headers, data5)

doc5.save(os.path.join(output_dir_workspace, "DOC_Data_Scraping.docx"))
doc5.save(os.path.join(output_dir_artifact, "DOC_Data_Scraping.docx"))
print("✓ DOC_Data_Scraping.docx created")

# ==============================================================================
# 6. DOC_odoo_uploader.docx
# ==============================================================================
doc6 = docx.Document()
add_header_banner(doc6, "Technical Documentation: odoo_uploader", "High-Speed Bulk Odoo Lead & Sales Data Uploader Tool with Automated Validation Rules")

add_section_heading(doc6, "1. Executive Summary & Purpose")
add_body_paragraph(doc6, "odoo_uploader validates and streams bulk lead datasets from multi-tab Excel files and HTTP API webhooks into Odoo ERP CRM (crm.lead and res.partner) via XML-RPC protocols.")

add_section_heading(doc6, "2. Execution Commands & Setup Guide")
add_sub_heading(doc6, "Manual Execution Commands")
add_code_block(doc6, 'cmd /c d:\\infonix\\odoo_uploader\\run_uploader.bat\npython d:\\infonix\\odoo_uploader\\odoo_uploader.py "d:\\infonix\\odoo_leads.xlsx"')

add_sub_heading(doc6, "Start Webhook Server")
add_code_block(doc6, "python d:\\infonix\\odoo_uploader\\server.py")

add_section_heading(doc6, "3. Execution Frequency & Schedule Interval")
add_bullet(doc6, "Execution Mode", "On-Demand (Bulk Excel Processing) & Event-Driven (HTTP Webhooks listening on port 5000)")

add_section_heading(doc6, "4. Validation Rules & Field Mapping")
add_bullet(doc6, "Validation Rules", "RFC Email Syntax Check, Odoo XML-RPC search_count Duplicate Verification, Phone E.164 Formatting")
add_bullet(doc6, "Odoo Mapping", "partner_name -> Company, contact_name -> Contact Person, email_from -> Work Email, phone -> Phone")

doc6.save(os.path.join(output_dir_workspace, "DOC_odoo_uploader.docx"))
doc6.save(os.path.join(output_dir_artifact, "DOC_odoo_uploader.docx"))
print("✓ DOC_odoo_uploader.docx created")

# ==============================================================================
# 7. DOC_odoo_sheets_auto_sync.docx
# ==============================================================================
doc7 = docx.Document()
add_header_banner(doc7, "Technical Documentation: odoo-sheets-auto-sync", "Real-Time Two-Way Automated Sync Engine Between Odoo ERP & Google Sheets via REST API")

add_section_heading(doc7, "1. Executive Summary & Purpose")
add_body_paragraph(doc7, "odoo-sheets-auto-sync maintains real-time bidirectional synchronization between Google Sheets worksheets and Odoo ERP CRM using continuous polling and Google Apps Script triggers.")

add_section_heading(doc7, "2. Execution Commands & Setup Guide")
add_sub_heading(doc7, "Start Background Auto Poller")
add_code_block(doc7, "python d:\\infonix\\odoo-sheets-auto-sync\\auto_poller.py")

add_sub_heading(doc7, "Start Real-Time Sync Server")
add_code_block(doc7, "python d:\\infonix\\odoo-sheets-auto-sync\\server.py")

add_section_heading(doc7, "3. Execution Frequency & Schedule Interval")
add_bullet(doc7, "Polling Frequency", "Runs Continuously in Background, checking for un-synced leads every 60 Seconds (poll_interval_seconds: 60)")
add_bullet(doc7, "Webhook Frequency", "Instant real-time synchronization upon Google Sheets onChange edit events")

add_section_heading(doc7, "4. Synchronized Schema")
add_bullet(doc7, "Bi-directional Mapping", "Company <-> partner_name, Customer Name <-> contact_name, Email <-> email_from, Phone <-> phone, Synced Status <-> Metadata")

doc7.save(os.path.join(output_dir_workspace, "DOC_odoo_sheets_auto_sync.docx"))
doc7.save(os.path.join(output_dir_artifact, "DOC_odoo_sheets_auto_sync.docx"))
print("✓ DOC_odoo_sheets_auto_sync.docx created")

print("\nALL 7 DOCX TECHNICAL MANUALS SUCCESSFULLY GENERATED!")
