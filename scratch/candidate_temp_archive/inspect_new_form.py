import requests, re

url = 'https://docs.google.com/forms/d/e/1FAIpQLSdAffcQaR1oRuv_NwT5D-MrnGbjPq0EE_cka6jAZ5FjEgt0WA/viewform?usp=sharing'
r = requests.get(url)
print('Status:', r.status_code)
title = re.search(r'<title>(.*?)</title>', r.text)
if title:
    print('Title:', title.group(1))

# Check for FB_PUBLIC_LOAD_DATA_
match = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);\s*</script>', r.text)
if match:
    import json
    data = json.loads(match.group(1))
    print('Form Title:', data[1][8] if len(data[1]) > 8 else 'N/A')
    print('Form ID inside data:', data[14] if len(data) > 14 else 'N/A')
    print('Full array length:', len(data))
    # Look for items
    items = data[1][1]
    print(f'Total questions/items: {len(items)}')
    for it in items:
        # title
        t = it[1]
        print(f' - {t}')
