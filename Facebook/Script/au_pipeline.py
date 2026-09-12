#!/usr/bin/env python3
"""
Australia-wide pipeline (Yasar rules):
  1) Discover Facebook page URLs by AU city
  2) Scrape page details
  3) Append only eligible rows to Google Sheet
     (created last 3 months + email + phone/mobile)
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
load_dotenv(SCRIPT_DIR / ".env")

from facebook_scraper import (  # noqa: E402
    PAGE_LIST_CSV,
    OUTPUT_DETAILS_CSV,
    enrich_year,
    run_details_scrape,
    run_page_discovery,
)
from sheets_sync import append_new_records  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="AU discover → scrape → CRM sheet")
    parser.add_argument("--locations-limit", type=int, default=5)
    parser.add_argument("--keyword", type=str, default="business")
    parser.add_argument("--scrape-limit", type=int, default=25)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--login", action="store_true")
    parser.add_argument("--skip-discover", action="store_true")
    parser.add_argument("--skip-sheets", action="store_true")
    args = parser.parse_args()

    headless = not args.headed
    login = args.login or bool(os.environ.get("FACEBOOK_EMAIL"))

    if not args.skip_discover:
        run_page_discovery(
            limit_locations=args.locations_limit,
            keyword=args.keyword,
            headless=headless,
            login=login,
            output_csv=PAGE_LIST_CSV,
        )

    if not PAGE_LIST_CSV.exists() or PAGE_LIST_CSV.stat().st_size == 0:
        print(f"No discovered pages at {PAGE_LIST_CSV}. Stopping.")
        return

    scraped = run_details_scrape(
        input_csv=PAGE_LIST_CSV,
        output_csv=OUTPUT_DETAILS_CSV,
        limit=args.scrape_limit,
        headless=headless,
        login=login,
        skip_existing=True,
    )
    scraped = enrich_year(scraped)
    print(f"Scraped {len(scraped)} page(s) this run")

    if args.skip_sheets or os.environ.get("SKIP_GOOGLE_SHEETS", "").lower() in {"1", "true", "yes"}:
        print("Sheet sync skipped.")
        return

    if scraped.empty:
        print("Nothing to sync.")
        return

    appended = append_new_records(scraped)
    print(f"Sheet eligible append: {appended}")


if __name__ == "__main__":
    main()
