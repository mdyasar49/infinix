import urllib.request
import re
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

URL = "https://www.linkedin.com/in/mohamed-yasar-4674ba223/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
}

def fetch_linkedin():
    print("=" * 80)
    print(f" 🔍 FETCHING LINKEDIN PROFILE FOR ANALYSIS: {URL}")
    print("=" * 80)
    
    req = urllib.request.Request(URL, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            
            # Extract meta tags (og:title, og:description, etc.)
            title_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', html) or re.search(r'<title>([^<]+)</title>', html)
            desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html) or re.search(r'<meta\s+property="og:description"\s+content="([^"]+)"', html)
            image_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)

            title = title_match.group(1) if title_match else "Mohamed Yasar"
            description = desc_match.group(1) if desc_match else "Profile details extracted"
            image = image_match.group(1) if image_match else "None"

            print(f"📌 Profile Title / Name : {title}")
            print(f"📝 Profile Meta Summary: {description}")
            print(f"🖼️ Profile Image URL   : {image}")
            print("=" * 80)

            return {
                "title": title,
                "description": description,
                "image": image,
                "url": URL
            }
    except Exception as e:
        print(f"  [!] Note: LinkedIn public wall response: {e}")
        return {
            "url": URL,
            "error": str(e)
        }

if __name__ == "__main__":
    fetch_linkedin()
