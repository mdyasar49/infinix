#!/usr/bin/env python3
"""Reliable scraper to reach 800 complete AU leads (name+email+phone)."""

from __future__ import annotations

import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
load_dotenv(SCRIPT_DIR / ".env", override=True)

import facebook_scraper as fs
from sheets_sync import append_new_records, is_australian_lead, open_worksheet, force_resync_local_output

LOG = SCRIPT_DIR.parent / "logs" / "reliable_800.log"
PROFILE = SCRIPT_DIR / "credentials" / "chrome_profile_complete"
TARGET = 800
BATCH = 50


def log(msg: str) -> None:
    line = "[{}] {}".format(datetime.now().strftime("%H:%M:%S"), msg)
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def has(s: pd.Series) -> pd.Series:
    return s.notna() & (s.astype(str).str.strip() != "") & (~s.astype(str).str.lower().isin(["nan", "none"]))


def complete_n() -> int:
    df = fs.enrich_year(pd.read_csv(fs.OUTPUT_DETAILS_CSV))
    email = has(df["Email"])
    phone = has(df["Phone_number"]) & ~df["Phone_number"].map(
        lambda v: bool(fs.is_junk_phone(v)) if pd.notna(v) else False
    )
    name = has(df["Page_Name"])
    au = df.apply(is_australian_lead, axis=1)
    return int((email & phone & name & au).sum())


def sheet_n() -> int:
    try:
        return max(0, len(open_worksheet().get_all_values()) - 1)
    except Exception as exc:
        log("sheet_n error: {}".format(exc))
        return -1


def fill_names(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    blank = ~has(out["Page_Name"])

    def slug(u):
        if pd.isna(u):
            return ""
        s = str(u).rstrip("/").split("/")[-1]
        if (not s) or ("profile.php" in s):
            return ""
        return s.replace("-", " ").replace(".", " ").replace("_", " ").strip()

    out.loc[blank, "Page_Name"] = out.loc[blank, "Facebook_url"].map(slug)
    return out


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    log("START reliable_800 target={} batch={}".format(TARGET, BATCH))
    log("baseline complete={} sheet={}".format(complete_n(), sheet_n()))

    for rnd in range(1, 50):
        c = complete_n()
        s = sheet_n()
        log("ROUND {} complete={} sheet={}".format(rnd, c, s))
        if c >= TARGET and s >= TARGET:
            log("TARGET REACHED")
            break
        try:
            for lock in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
                try:
                    (PROFILE / lock).unlink(missing_ok=True)
                except Exception:
                    pass
            scraped = fs.run_details_scrape(
                input_csv=fs.PAGE_LIST_CSV,
                output_csv=fs.OUTPUT_DETAILS_CSV,
                limit=BATCH,
                headless=True,
                login=True,
                skip_existing=True,
                profile_dir=PROFILE,
            )
            scraped = fill_names(fs.enrich_year(scraped))
            log("scraped={}".format(len(scraped)))
            if scraped.empty:
                log("no pending pages left")
                break
            both = int((has(scraped["Email"]) & has(scraped["Phone_number"])).sum())
            log("batch_both_contacts={}".format(both))
            appended = append_new_records(scraped)
            log("sheet_append={}".format(appended))
        except Exception as exc:
            log("ROUND {} ERROR: {}".format(rnd, exc))
            log(traceback.format_exc()[-500:])
            time.sleep(15)
            continue

    try:
        force_resync_local_output()
    except Exception as exc:
        log("final resync error: {}".format(exc))
    log("DONE complete={} sheet={}".format(complete_n(), sheet_n()))


if __name__ == "__main__":
    main()
