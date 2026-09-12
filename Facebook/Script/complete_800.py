#!/usr/bin/env python3
"""
Build 800+ COMPLETE AU Facebook leads:
  Company Name + Email + Phone (both) + AU verified + FB link in Notes.

Strategy:
  1) Re-scrape pages that already have email XOR phone (likely to complete)
  2) Scrape remaining pending page_list URLs
  3) Sync complete rows to Google Sheet until >= 800
"""

from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
load_dotenv(SCRIPT_DIR / ".env", override=True)

import facebook_scraper as fs  # noqa: E402
from sheets_sync import (  # noqa: E402
    append_new_records,
    force_resync_local_output,
    is_australian_lead,
    open_worksheet,
)

LOG = ROOT / "logs" / "complete_800.log"
TARGET = 800
BATCH = 120
RESCRAPE_CSV = ROOT / "Output" / "rescrape_incomplete.csv"


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def has(s: pd.Series) -> pd.Series:
    return s.notna() & (s.astype(str).str.strip() != "") & (
        ~s.astype(str).str.lower().isin(["nan", "none"])
    )


def load_details() -> pd.DataFrame:
    return fs.enrich_year(pd.read_csv(fs.OUTPUT_DETAILS_CSV))


def fill_blank_names(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    blank = ~has(out["Page_Name"])

    def slug(u):
        if pd.isna(u):
            return ""
        s = str(u).rstrip("/").split("/")[-1]
        if not s or "profile.php" in s:
            return ""
        return s.replace("-", " ").replace(".", " ").replace("_", " ").strip()

    out.loc[blank, "Page_Name"] = out.loc[blank, "Facebook_url"].map(slug)
    return out


def complete_mask(df: pd.DataFrame) -> pd.Series:
    email = has(df["Email"])
    phone = has(df["Phone_number"]) & ~df["Phone_number"].map(
        lambda v: bool(fs.is_junk_phone(v)) if pd.notna(v) else False
    )
    name = has(df["Page_Name"])
    au = df.apply(is_australian_lead, axis=1)
    return email & phone & name & au


def complete_count() -> int:
    return int(complete_mask(fill_blank_names(load_details())).sum())


def sheet_count() -> int:
    try:
        return max(0, len(open_worksheet().get_all_values()) - 1)
    except Exception as exc:
        log(f"sheet error: {exc}")
        return -1


def prepare_rescrape_queue() -> int:
    df = fill_blank_names(load_details())
    email = has(df["Email"])
    phone = has(df["Phone_number"]) & ~df["Phone_number"].map(
        lambda v: bool(fs.is_junk_phone(v)) if pd.notna(v) else False
    )
    au = df.apply(is_australian_lead, axis=1)
    incomplete = df.loc[au & ((email & ~phone) | (phone & ~email))].copy()
    if incomplete.empty:
        return 0
    # Remove these URLs from master so skip_existing will pick them up again
    norms = set(incomplete["Facebook_url"].map(fs.normalize_facebook_url))
    master = load_details()
    keep = ~master["Facebook_url"].map(fs.normalize_facebook_url).isin(norms)
    master.loc[keep].to_csv(fs.OUTPUT_DETAILS_CSV, index=False)
    incomplete[["Page_Name", "Facebook_url", "Location"]].to_csv(RESCRAPE_CSV, index=False)
    # Also ensure they exist in page_list
    fs.save_page_links(incomplete[["Page_Name", "Facebook_url", "Location"]].to_dict("records"))
    log(f"queued rescrape incomplete={len(incomplete)} master_left={int(keep.sum())}")
    return len(incomplete)


def scrape_batch(limit: int) -> pd.DataFrame:
    last_exc = None
    for attempt in range(1, 4):
        try:
            scraped = fs.run_details_scrape(
                input_csv=fs.PAGE_LIST_CSV,
                output_csv=fs.OUTPUT_DETAILS_CSV,
                limit=limit,
                headless=True,
                login=True,
                skip_existing=True,
                profile_dir=SCRIPT_DIR / "credentials" / "chrome_profile_complete",
            )
            return fs.enrich_year(scraped)
        except Exception as exc:
            last_exc = exc
            log(f"scrape_batch attempt {attempt} failed: {exc}")
            time.sleep(5 * attempt)
    raise last_exc  # type: ignore[misc]


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log(f"START complete_800 target={TARGET}")

    # Clean local + sheet baseline
    df = fill_blank_names(load_details())
    junk = df["Phone_number"].map(lambda v: bool(fs.is_junk_phone(v)) if pd.notna(v) else False)
    df.loc[junk, "Phone_number"] = pd.NA
    df.to_csv(fs.OUTPUT_DETAILS_CSV, index=False)

    n = prepare_rescrape_queue()
    log(f"rescrape_ready={n} complete_now={complete_count()}")

    try:
        if sheet_count() < 1 or True:
            # Keep sheet aligned with complete-only filter
            force_resync_local_output()
    except Exception as exc:
        log(f"resync: {exc}")

    rounds = 0
    while complete_count() < TARGET or sheet_count() < TARGET:
        rounds += 1
        local_n = complete_count()
        sheet_n = sheet_count()
        log(f"ROUND {rounds} complete_local={local_n} sheet={sheet_n}")
        if local_n >= TARGET and sheet_n >= TARGET:
            break

        try:
            scraped = scrape_batch(BATCH)
        except Exception as exc:
            log(f"ROUND {rounds} scrape failed: {exc}")
            time.sleep(20)
            continue

        log(f"scraped={len(scraped)}")
        if scraped.empty:
            log("No pending URLs left")
            break

        scraped = fill_blank_names(scraped)
        if not scraped.empty:
            # rewrite last appended names in master file
            master = fill_blank_names(load_details())
            junk = master["Phone_number"].map(
                lambda v: bool(fs.is_junk_phone(v)) if pd.notna(v) else False
            )
            master.loc[junk, "Phone_number"] = pd.NA
            master.to_csv(fs.OUTPUT_DETAILS_CSV, index=False)

        try:
            appended = append_new_records(scraped)
            log(f"sheet_append={appended} complete_local={complete_count()}")
        except Exception as exc:
            log(f"append failed: {exc}")

        if rounds >= 40:
            log("safety stop after 40 rounds")
            break

    # Final full resync for clean sheet
    try:
        force_resync_local_output()
    except Exception as exc:
        log(f"final resync: {exc}")
    log(f"DONE complete_local={complete_count()} sheet={sheet_count()}")


if __name__ == "__main__":
    main()
