import requests
import re
import json

URL1 = "https://forms.gle/xb6hcogsrkYZVNK47"
URL2 = "https://forms.gle/ZbDDiHP5gTqekwLp8"

def inspect_form(url):
    print(f"[*] Resolving URL: {url}")
    try:
        r = requests.get(url, allow_redirects=True, timeout=15)
        print(f"    Final URL: {r.url}")
        print(f"    Status Code: {r.status_code}")
        
        # Extract form ID
        match = re.search(r"/forms/d/(?:e/)?([a-zA-Z0-9_-]+)", r.url)
        form_id = match.group(1) if match else "Unknown"
        print(f"    Extracted Form ID: {form_id}")
        
        # Check title
        title_match = re.search(r"<title>(.*?)</title>", r.text)
        title = title_match.group(1) if title_match else "Unknown"
        print(f"    Form Page Title: {title}")
        
        return r.url, form_id, title
    except Exception as e:
        print(f"    Error: {e}")
        return None, None, None

if __name__ == "__main__":
    print("--- Testing Link 1 ---")
    inspect_form(URL1)
    print("\n--- Testing Link 2 ---")
    inspect_form(URL2)
