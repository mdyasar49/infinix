import os
import sys
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

file_id = "1XVn_M-PqFl5Afw6bDtnOEakQAOJj2rbv"
print(f"[*] Accessing file: {file_id}")

# 1. Direct download attempt
try:
    url = f"https://docs.google.com/document/d/{file_id}/export?format=txt"
    r = requests.get(url, timeout=10)
    if r.status_code == 200 and len(r.content) > 50 and not b"accounts.google.com" in r.content:
        with open("d:/infonix/extracted_keywords.txt", "wb") as f:
            f.write(r.content)
        print(f"[+] Downloaded via Google Docs direct export! Bytes: {len(r.content)}")
        sys.exit(0)
except Exception as e:
    print(f"[-] Direct export error: {e}")

# 2. Service Account API
try:
    creds_path = "d:/infonix/credentials.json"
    if os.path.exists(creds_path):
        creds = service_account.Credentials.from_service_account_file(
            creds_path, 
            scopes=['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/documents.readonly']
        )
        drive_service = build('drive', 'v3', credentials=creds)
        meta = drive_service.files().get(fileId=file_id, fields='id, name, mimeType').execute()
        print(f"[+] Drive Meta: {meta}")
        
        mime = meta.get("mimeType", "")
        if "document" in mime:
            content = drive_service.files().export(fileId=file_id, mimeType='text/plain').execute()
        elif "spreadsheet" in mime:
            content = drive_service.files().export(fileId=file_id, mimeType='text/csv').execute()
        elif "presentation" in mime:
            content = drive_service.files().export(fileId=file_id, mimeType='text/plain').execute()
        else:
            req = drive_service.files().get_media(fileId=file_id)
            content = req.execute()
            
        out_path = f"d:/infonix/{meta.get('name', 'extracted_keywords.txt')}"
        with open(out_path, "wb") as f:
            f.write(content if isinstance(content, bytes) else content.encode("utf-8"))
        print(f"[+] Successfully saved file to: {out_path} ({len(content)} bytes)")
except Exception as e:
    print(f"[-] Service account error: {e}")
