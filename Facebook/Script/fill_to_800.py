#!/usr/bin/env python3
"""Scrape pending Facebook pages until ~800 email-or-phone AU leads are on the sheet."""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
load_dotenv(SCRIPT_DIR / ".env")

import facebook_scraper as fs  # noqa: E402
from sheets_sync import append_new_records, open_worksheet  # noqa: E402

LOG = SCRIPT_DIR.parent / "logs" / "fill_800.log"
TARGET = 800
BATCH = 200


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def sheet_count() -> int:
    try:
        return max(0, len(open_worksheet().get_all_values()) - 1)
    except Exception as exc:
        log(f"sheet_count error: {exc}")
        return -1


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log(f"START fill_to_800 target={TARGET} batch={BATCH}")
    while True:
        n = sheet_count()
        log(f"sheet_rows={n}")
        if n >= TARGET:
            log(f"TARGET REACHED {n}")
            break
        scraped = fs.run_details_scrape(
            input_csv=fs.PAGE_LIST_CSV,
            output_csv=fs.OUTPUT_DETAILS_CSV,
            limit=BATCH,
            headless=True,
            login=True,
            skip_existing=True,
        )
        scraped = fs.enrich_year(scraped)
        log(f"scraped={len(scraped)}")
        if scraped.empty:
            log("No more pending pages — stopping")
            break
        appended = append_new_records(scraped)
        log(f"sheet_append={appended}")
    log("DONE")


if __name__ == "__main__":
    main()
