#!/usr/bin/env python3
"""
Fill Google Sheet to 800+ COMPLETE Australian Facebook leads:
  - Company Name
  - Email AND Phone (both mandatory)
  - AU verified
  - Notes with Facebook link
Age/date does NOT matter. Accuracy does.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
load_dotenv(SCRIPT_DIR / ".env", override=True)

import facebook_scraper as fs  # noqa: E402
from sheets_sync import (  # noqa: E402
    append_new_records,
    filter_eligible_leads,
    is_australian_lead,
    open_worksheet,
)

LOG = SCRIPT_DIR.parent / "logs" / "fill_800_complete.log"
TARGET = 800
BATCH = 150


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def has(s: pd.Series) -> pd.Series:
    return s.notna() & (s.astype(str).str.strip() != "") & (
        ~s.astype(str).str.lower().isin(["nan", "none"])
    )


def complete_local_count() -> int:
    df = fs.enrich_year(pd.read_csv(fs.OUTPUT_DETAILS_CSV))
    email = has(df["Email"])
    phone = has(df["Phone_number"]) & ~df["Phone_number"].map(
        lambda v: bool(fs.is_junk_phone(v)) if pd.notna(v) else False
    )
    name = has(df["Page_Name"])
    au = df.apply(is_australian_lead, axis=1)
    return int((email & phone & name & au).sum())


def sheet_count() -> int:
    try:
        return max(0, len(open_worksheet().get_all_values()) - 1)
    except Exception as exc:
        log(f"sheet_count error: {exc}")
        return -1


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log(f"START complete-fill target={TARGET} batch={BATCH}")

    # Rebuild sheet with complete rows only (email+phone+AU)
    from sheets_sync import force_resync_local_output

    try:
        force_resync_local_output()
    except Exception as exc:
        # fallback: append path may still work
        log(f"force_resync note: {exc}")

    while True:
        local_n = complete_local_count()
        sheet_n = sheet_count()
        log(f"complete_local={local_n} sheet_rows={sheet_n}")
        if sheet_n >= TARGET and local_n >= TARGET:
            log(f"TARGET REACHED sheet={sheet_n} local={local_n}")
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
            log("No pending pages left — need more discovery")
            break

        # Fill blank page names from URL slug before sync
        if "Page_Name" in scraped.columns:
            blank = ~has(scraped["Page_Name"])
            scraped.loc[blank, "Page_Name"] = scraped.loc[blank, "Facebook_url"].map(
                lambda u: (str(u).rstrip("/").split("/")[-1].replace("-", " ").replace(".", " ") if pd.notna(u) else "")
            )

        eligible = filter_eligible_leads(scraped)
        log(
            f"batch both_contacts={int((has(scraped['Email']) & has(scraped['Phone_number'])).sum())} "
            f"eligible={len(eligible)}"
        )
        appended = append_new_records(scraped)
        log(f"sheet_append={appended}")

    log(f"DONE sheet={sheet_count()} complete_local={complete_local_count()}")


if __name__ == "__main__":
    main()
