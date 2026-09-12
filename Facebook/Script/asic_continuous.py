#!/usr/bin/env python3
"""
Continuous ASIC → Facebook discovery + scrape loop toward 800+ recent leads.

Cycles:
  1) Discover N company names on Facebook
  2) Scrape matched pages for email/phone
  3) Append eligible rows to Google Sheet
  4) Repeat until target sheet count or queue exhausted
"""

from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
load_dotenv(SCRIPT_DIR / ".env")

import asic_fb_pipeline as pipe  # noqa: E402
from sheets_sync import open_worksheet  # noqa: E402

LOG = ROOT / "logs" / "asic_continuous.log"


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def sheet_count() -> int:
    try:
        ws = open_worksheet()
        return max(0, len(ws.get_all_values()) - 1)
    except Exception as exc:
        log(f"sheet_count error: {exc}")
        return -1


def main() -> None:
    target = int(os.environ.get("ASIC_TARGET_LEADS", "800"))
    discover_batch = int(os.environ.get("ASIC_DISCOVER_BATCH", "80"))
    scrape_batch = int(os.environ.get("ASIC_SCRAPE_BATCH", "80"))
    pause = int(os.environ.get("ASIC_LOOP_PAUSE_SEC", "20"))

    log(f"CONTINUOUS start target={target} discover={discover_batch} scrape={scrape_batch}")
    round_no = 0
    while True:
        round_no += 1
        current = sheet_count()
        log(f"ROUND {round_no} sheet_rows={current}")
        if current >= target:
            log(f"TARGET REACHED {current} >= {target}")
            break

        try:
            pipe.run_discovery(limit=discover_batch, offset=0, headed=False)
        except Exception as exc:
            log(f"discover error: {exc}")

        try:
            pipe.run_scrape(limit=scrape_batch)
        except Exception as exc:
            log(f"scrape error: {exc}")

        current = sheet_count()
        log(f"ROUND {round_no} done sheet_rows={current}")
        if current >= target:
            log(f"TARGET REACHED {current} >= {target}")
            break
        time.sleep(pause)

    log("CONTINUOUS DONE")


if __name__ == "__main__":
    main()
