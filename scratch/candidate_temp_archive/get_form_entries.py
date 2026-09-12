import requests, re, json

url = 'https://docs.google.com/forms/d/e/1FAIpQLSdAffcQaR1oRuv_NwT5D-MrnGbjPq0EE_cka6jAZ5FjEgt0WA/viewform'
r = requests.get(url)
match = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);\s*</script>', r.text)
if match:
    data = json.loads(match.group(1))
    items = data[1][1]
    print(f"Total Questions: {len(items)}\n")
    for it in items:
        title = it[1]
        entry_id = None
        if len(it) > 4 and it[4] and len(it[4]) > 0 and len(it[4][0]) > 0:
            entry_id = it[4][0][0]
        print(f" - Title: {title} | Entry ID: entry.{entry_id}")
