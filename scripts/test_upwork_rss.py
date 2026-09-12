import requests
import xml.etree.ElementTree as ET
import email.utils

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
url = "https://www.upwork.com/ab/feed/jobs/rss?q=python&sort=recency"

try:
    res = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        root = ET.fromstring(res.content)
        items = root.findall("./channel/item")
        print(f"Found {len(items)} RSS items!")
        for item in items[:3]:
            title = item.find("title").text if item.find("title") is not None else ""
            link = item.find("link").text if item.find("link") is not None else ""
            pubDate = item.find("pubDate").text if item.find("pubDate") is not None else ""
            print(f"Title   : {title}")
            print(f"Link    : {link}")
            print(f"PubDate : {pubDate}")
            if pubDate:
                dt = email.utils.parsedate_to_datetime(pubDate)
                print(f"Formatted Date: {dt.strftime('%d/%m/%Y')}")
            print("-" * 50)
except Exception as e:
    print(f"Error: {e}")
