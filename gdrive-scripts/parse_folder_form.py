import requests
import re
import json

r = requests.get('https://docs.google.com/forms/d/e/1FAIpQLSccc1FMu_lahzcR82sd1sRx6JKjt7LUd9hr-CV7iLAmKinj9Q/viewform')
match = re.search(r'FB_PUBLIC_LOAD_DATA_\s*=\s*(.*?);</script>', r.text, re.DOTALL)
if match:
    data = json.loads(match.group(1))
    print('Form Title:', data[1][8] if len(data[1]) > 8 else 'No title')
    print('Form Description:', data[1][0] if len(data[1]) > 0 else 'No desc')
    fields = data[1][1]
    print(f'Total Questions: {len(fields)}')
    for f in fields:
        if f and len(f) > 1:
            q_title = f[1]
            entry_id = f[4][0][0] if (len(f) > 4 and f[4] and f[4][0]) else ''
            print(f" - {q_title} -> entry.{entry_id}")
