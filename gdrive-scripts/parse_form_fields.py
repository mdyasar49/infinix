import requests
import json
import re

URL = "https://docs.google.com/forms/d/e/1FAIpQLSdAffcQaR1oRuv_NwT5D-MrnGbjPq0EE_cka6jAZ5FjEgt0WA/viewform"

def parse_form():
    r = requests.get(URL, timeout=15)
    text = r.text

    # Extract FB_PUBLIC_LOAD_DATA_
    match = re.search(r"FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);\s*</script>", text, re.DOTALL)
    if not match:
        print("[!] FB_PUBLIC_LOAD_DATA_ not found.")
        return

    data = json.loads(match.group(1))
    title = data[1][8] if len(data) > 1 and len(data[1]) > 8 else "Unknown"
    description = data[1][0] if len(data) > 1 and len(data[1]) > 0 else ""
    questions = data[1][1] if len(data) > 1 and len(data[1]) > 1 else []

    print(f"=== FORM DETAILS ===")
    print(f"Title: {title}")
    print(f"Description: {description[:200]}...")
    print(f"\n=== QUESTIONS ({len(questions)}) ===")
    
    parsed_fields = []
    for q in questions:
        if not q or len(q) < 5:
            continue
        q_title = q[1]
        q_desc = q[2]
        q_type = q[3]
        entry_id = None
        if q[4] and len(q[4]) > 0 and q[4][0] and len(q[4][0]) > 0:
            entry_id = q[4][0][0]
        
        parsed_fields.append({
            "title": q_title,
            "entry_id": entry_id,
            "type": q_type
        })
        print(f"  - [{entry_id}] {q_title}")

    return parsed_fields

if __name__ == "__main__":
    parse_form()
