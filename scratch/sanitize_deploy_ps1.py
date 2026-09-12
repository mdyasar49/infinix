import os
from pathlib import Path

targets = [
    Path(r"d:\infonix\cloudpanel-scripts\deploy.ps1"),
    Path(r"d:\infonix\cloudpanel-scripts\deploy.ps1.bak"),
    Path(r"d:\infonix\deploy.ps1")
]

secrets_map = {
    "YOUR_TWILIO_ACCOUNT_SID": "YOUR_TWILIO_ACCOUNT_SID",
    "YOUR_TWILIO_AUTH_TOKEN": "YOUR_TWILIO_AUTH_TOKEN",
    "YOUR_TWILIO_API_KEY": "YOUR_TWILIO_API_KEY",
    "YOUR_TWILIO_API_SECRET": "YOUR_TWILIO_API_SECRET",
    "YOUR_TWILIO_APP_SID": "YOUR_TWILIO_APP_SID",
    "YOUR_TWILIO_MESSAGING_SERVICE_SID": "YOUR_TWILIO_MESSAGING_SERVICE_SID"
}

for t in targets:
    if t.exists():
        text = t.read_text(encoding="utf-8")
        for secret, placeholder in secrets_map.items():
            text = text.replace(secret, placeholder)
        t.write_text(text, encoding="utf-8")
        print(f"Sanitized: {t}")
