#!/usr/bin/env python3
"""
Deep AU collect run (client request):
  1) Discover more page URLs by city + keyword
  2) Scrape pending pages for email/phone/created date
  3) Append only eligible leads to Google Sheet (last 3 months + email + phone)
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
load_dotenv(SCRIPT_DIR / ".env")

import facebook_scraper as fs  # noqa: E402
from sheets_sync import append_new_records  # noqa: E402

LOG = SCRIPT_DIR.parent / "logs" / f"collect_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def main() -> None:
    discover_cities = int(os.environ.get("COLLECT_CITIES", "12"))
    scrape_limit = int(os.environ.get("COLLECT_SCRAPE_LIMIT", "120"))
    keywords = [
        "business",
        "cafe",
        "salon",
        "plumber",
        "restaurant",
        "electrician",
        "cleaning",
        "dentist",
        "gym",
        "new business",
    ]
    # fewer keywords if time-constrained; still deeper than before
    keywords = keywords[:6]

    cities = fs.load_cities()[:discover_cities]
    log(f"START collect cities={len(cities)} keywords={keywords} scrape_limit={scrape_limit}")

    # --- Discovery ---
    driver = fs.build_driver(headless=True)
    discovered = 0
    try:
        driver.get("https://www.facebook.com/")
        fs.random_sleep(2, 3)
        if not fs.is_logged_in(driver):
            log("Login required for discovery...")
            ok = fs.optional_login(driver)
            log(f"login_ok={ok}")
        else:
            log("Already logged in via Chrome profile")

        for city in cities:
            for kw in keywords:
                try:
                    rows = fs.discover_pages_for_location(
                        driver, city, keyword=kw, scroll_rounds=4
                    )
                    before = discovered
                    fs.save_page_links(rows, fs.PAGE_LIST_CSV)
                    discovered += len(rows)
                    log(f"discover {city}/{kw}: found={len(rows)}")
                except Exception as exc:
                    log(f"discover ERROR {city}/{kw}: {exc}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    log(f"Discovery pass candidates seen={discovered}")
    if fs.PAGE_LIST_CSV.exists():
        import pandas as pd

        pl = pd.read_csv(fs.PAGE_LIST_CSV)
        log(f"page_list total unique rows={len(pl)}")

    # --- Scrape pending ---
    log(f"Scraping up to {scrape_limit} pending pages...")
    scraped = fs.run_details_scrape(
        input_csv=fs.PAGE_LIST_CSV,
        output_csv=fs.OUTPUT_DETAILS_CSV,
        limit=scrape_limit,
        headless=True,
        login=True,
        skip_existing=True,
    )
    scraped = fs.enrich_year(scraped)
    log(f"Scraped rows this run={len(scraped)}")

    if not scraped.empty:
        def has(s):
            return s.notna() & (s.astype(str).str.strip() != "") & (
                ~s.astype(str).str.lower().isin(["nan", "none"])
            )

        log(
            "batch contacts: "
            f"email={int(has(scraped['Email']).sum())} "
            f"phone={int(has(scraped['Phone_number']).sum())} "
            f"date={int(has(scraped['Page_Created_date']).sum())} "
            f"both={int((has(scraped['Email']) & has(scraped['Phone_number'])).sum())}"
        )
        appended = append_new_records(scraped)
        log(f"Google Sheet eligible append={appended}")
    else:
        log("No new scraped rows")

    # Final snapshot
    import pandas as pd
    from facebook_scraper import normalize_created_dates

    df = fs.enrich_year(pd.read_csv(fs.OUTPUT_DETAILS_CSV))
    dates = normalize_created_dates(df["Page_Created_date"])
    now = pd.Timestamp(datetime.now())
    m3 = now - pd.DateOffset(months=3)
    r3 = dates.notna() & (dates >= m3)

    def has(s):
        return s.notna() & (s.astype(str).str.strip() != "") & (
            ~s.astype(str).str.lower().isin(["nan", "none"])
        )

    both = has(df["Email"]) & has(df["Phone_number"])
    log(
        f"SNAPSHOT total={len(df)} both={int(both.sum())} "
        f"last3m_pages={int(r3.sum())} last3m_both={int((r3 & both).sum())}"
    )
    log(f"LOG file: {LOG}")
    log("DONE")


if __name__ == "__main__":
    main()
