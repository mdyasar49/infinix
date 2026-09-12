import os
import sys
import shutil
import subprocess

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

brain_dir = r"C:\Users\HP\.gemini\antigravity-ide\brain\51026764-4558-48d2-b272-a018ce0ad279"
workspace_dir = r"d:\infonix"

projects_map = {
    "Data-Scraping": {
        "md": "DOC_Data_Scraping.md",
        "docx": "DOC_Data_Scraping.docx"
    },
    "LinkedIn-Data-Scraping": {
        "md": "DOC_LinkedIn_Data_Scraping.md",
        "docx": "DOC_LinkedIn_Data_Scraping.docx"
    },
    "Social-Media-Data-Scraping": {
        "md": "DOC_Social_Media_Data_Scraping.md",
        "docx": "DOC_Social_Media_Data_Scraping.docx"
    },
    "odoo_uploader": {
        "md": "DOC_odoo_uploader.md",
        "docx": "DOC_odoo_uploader.docx"
    },
    "odoo-sheets-auto-sync": {
        "md": "DOC_odoo_sheets_auto_sync.md",
        "docx": "DOC_odoo_sheets_auto_sync.docx"
    },
    "odoo-lead-generator": {
        "md": "DOC_odoo_lead_generator.md",
        "docx": "DOC_odoo_lead_generator.docx"
    },
    "zoho-lead-generator": {
        "md": "DOC_zoho_lead_generator.md",
        "docx": "DOC_zoho_lead_generator.docx"
    }
}

master_txt_source = os.path.join(workspace_dir, "scraping_keywords_master.txt")

print("Distributing technical documents and committing across all repositories...\n")

for project_name, doc_files in projects_map.items():
    proj_dir = os.path.join(workspace_dir, project_name)
    if not os.path.exists(proj_dir):
        os.makedirs(proj_dir, exist_ok=True)
        print(f"Created folder: {project_name}")
        # Initialize git if not present
        subprocess.run(["git", "init"], cwd=proj_dir, capture_output=True)

    # Source files
    src_md = os.path.join(brain_dir, doc_files["md"])
    if not os.path.exists(src_md):
        src_md = os.path.join(workspace_dir, doc_files["md"])
        
    src_docx = os.path.join(workspace_dir, doc_files["docx"])
    
    # Destination files
    dst_md = os.path.join(proj_dir, "TECHNICAL_DOCUMENTATION.md")
    dst_docx = os.path.join(proj_dir, "TECHNICAL_DOCUMENTATION.docx")
    dst_txt = os.path.join(proj_dir, "SCRAPING_KEYWORDS.txt")
    
    # Copy files
    if os.path.exists(src_md):
        shutil.copy2(src_md, dst_md)
    if os.path.exists(src_docx):
        shutil.copy2(src_docx, dst_docx)
    if os.path.exists(master_txt_source):
        shutil.copy2(master_txt_source, dst_txt)
        
    print(f"✓ Files copied to {project_name}/")
    
    # Git add and commit
    git_dir = os.path.join(proj_dir, ".git")
    if os.path.exists(git_dir):
        subprocess.run(["git", "add", "TECHNICAL_DOCUMENTATION.md", "TECHNICAL_DOCUMENTATION.docx", "SCRAPING_KEYWORDS.txt"], cwd=proj_dir, capture_output=True)
        commit_res = subprocess.run(["git", "commit", "-m", "docs: add technical documentation and scraping keywords manual"], cwd=proj_dir, capture_output=True, text=True)
        if "nothing to commit" in commit_res.stdout or "nothing to commit" in commit_res.stderr:
            print(f"  [-] Git Commit ({project_name}): Already up to date.")
        else:
            print(f"  [✓] Git Commit ({project_name}): Success!")

print("\nDistribution and commit completed successfully!")
