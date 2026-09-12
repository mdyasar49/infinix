#!/usr/bin/env python3
"""
Daily Facebook scrape runner (cron-ready).

Flow:
  1) Run scraper
  2) Check duplicates (local Output + Google Sheet)
  3) Append only new records locally
  4) Append only new records to the SAME Google Sheet
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
LOG_DIR = PROJECT_DIR / "logs"

# Allow "python daily_run.py" from Script/
sys.path.insert(0, str(SCRIPT_DIR))

load_dotenv(SCRIPT_DIR / ".env")

from facebook_scraper import (  # noqa: E402
    INPUT_PAGES_CSV,
    OUTPUT_DETAILS_CSV,
    PAGE_LIST_CSV,
    enrich_year,
    ensure_dirs,
    filter_new_records,
    load_existing_urls,
    run_details_scrape,
)
from sheets_sync import append_new_records, existing_facebook_urls, open_worksheet  # noqa: E402


def default_input_csv() -> Path:
    env_path = os.environ.get("DAILY_INPUT_CSV", "").strip()
    if env_path:
        p = Path(env_path)
        if not p.is_absolute():
            p = SCRIPT_DIR / p
        if p.exists() and p.stat().st_size > 0:
            return p
    if PAGE_LIST_CSV.exists() and PAGE_LIST_CSV.stat().st_size > 0:
        return PAGE_LIST_CSV
    return INPUT_PAGES_CSV


def log(msg: str) -> None:
    ensure_dirs()
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    print(line)
    log_file = LOG_DIR / f"daily_run_{datetime.now().strftime('%Y%m%d')}.log"
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def run_daily(
    limit: int | None = None,
    input_csv: Path | None = None,
    output_csv: Path = OUTPUT_DETAILS_CSV,
    headless: bool = True,
    login: bool = False,
    sync_sheet: bool = True,
) -> None:
    ensure_dirs()
    input_csv = input_csv or default_input_csv()
    limit = limit if limit is not None else (
        int(os.environ["DAILY_SCRAPE_LIMIT"]) if os.environ.get("DAILY_SCRAPE_LIMIT") else 25
    )
    log(f"Starting daily run (limit={limit}, input={input_csv.name})")

    # 1) Scrape (also skips URLs already in local output)
    scraped = run_details_scrape(
        input_csv=input_csv,
        output_csv=output_csv,
        limit=limit,
        headless=headless,
        login=login or bool(os.environ.get("FACEBOOK_EMAIL")),
        skip_existing=True,
    )
    scraped = enrich_year(scraped)
    log(f"Scrape finished: {len(scraped)} row(s) this run")

    if scraped.empty:
        log("No scraped rows; nothing to append.")
        return

    # Local duplicate check
    local_existing = load_existing_urls(output_csv)
    new_for_sheet = filter_new_records(scraped, set())
    log(f"Local output now has {len(local_existing)} unique URL(s)")

    # Google Sheet: CRM filters (3-month + email+phone) applied inside append_new_records
    if not sync_sheet or os.environ.get("SKIP_GOOGLE_SHEETS", "").lower() in {"1", "true", "yes"}:
        log("Google Sheets sync skipped.")
        return

    try:
        worksheet = open_worksheet()
        sheet_urls = existing_facebook_urls(worksheet)
        appended = append_new_records(new_for_sheet, existing_urls=sheet_urls)
        log(f"Google Sheet append complete: {appended} eligible new row(s)")
    except SystemExit as exc:
        log(f"Google Sheets not configured yet: {exc}")
    except Exception as exc:
        log(f"Google Sheets sync failed: {exc}")
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Daily Facebook scrape + Google Sheet append")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=OUTPUT_DETAILS_CSV)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--login", action="store_true")
    parser.add_argument("--skip-sheets", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_daily(
        limit=args.limit,
        input_csv=args.input,
        output_csv=args.output,
        headless=not args.headed,
        login=args.login,
        sync_sheet=not args.skip_sheets,
    )


if __name__ == "__main__":
    main()
