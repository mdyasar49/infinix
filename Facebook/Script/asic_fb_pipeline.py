#!/usr/bin/env python3
"""
Find Facebook pages for ASIC companies registered in the last 3 months.

Strategy:
  1) ASIC official register gives Exact registration dates (last 3 months)
  2) Search Facebook Pages for each company name
  3) Scrape About / Transparency / Contact for email + phone
  4) Push to Google Sheet when email+phone+AU + (page created OR company registered) within 3 months
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus, urlparse

import pandas as pd
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
load_dotenv(SCRIPT_DIR / ".env")

import facebook_scraper as fs  # noqa: E402
from sheets_sync import append_new_records  # noqa: E402

QUEUE_CSV = ROOT / "Output" / "asic_fb_search_queue.csv"
MATCH_CSV = ROOT / "Output" / "asic_fb_matches.csv"
LOG = ROOT / "logs" / f"asic_fb_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG.parent.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def name_similarity(query: str, page_name: str) -> float:
    q = set(re_tokens(query))
    p = set(re_tokens(page_name))
    if not q or not p:
        return 0.0
    return len(q & p) / max(len(q), 1)


def re_tokens(text: str) -> List[str]:
    import re

    stop = {
        "pty",
        "ltd",
        "limited",
        "the",
        "and",
        "of",
        "for",
        "au",
        "australia",
        "group",
        "services",
        "service",
        "company",
        "co",
    }
    toks = re.findall(r"[a-z0-9]+", (text or "").lower())
    return [t for t in toks if t not in stop and len(t) > 1]


def discover_page_for_company(
    driver,
    company_name: str,
    acn: str = "",
    reg_date: str = "",
    scroll_rounds: int = 2,
) -> List[Dict[str, str]]:
    """Search Facebook Pages for an exact company name and keep close matches."""
    query = company_name.strip()
    if not query:
        return []
    # Try exact name first; append Australia only as a second pass if needed.
    queries = [query, f"{query} Australia"]
    links = []
    seen_urls = set()
    for q in queries:
        url = f"https://www.facebook.com/search/pages/?q={quote_plus(q)}"
        driver.get(url)
        fs.random_sleep(3.0, 4.5)
        fs.dismiss_blocking_dialogs(driver)
        for _ in range(scroll_rounds):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            fs.random_sleep(1.2, 2.0)
        for name, link in fs.extract_page_links_from_html(driver.page_source or ""):
            norm = fs.normalize_facebook_url(link)
            if norm and norm not in seen_urls:
                seen_urls.add(norm)
                links.append((name, link))
        # If we already have a strong candidate, skip second query
        if any(name_similarity(query, n or "") >= 0.7 for n, _ in links):
            break

    q_toks = re_tokens(query)
    if not q_toks:
        return []

    scored: List[Tuple[float, str, str]] = []
    seen = set()
    for name, link in links[:25]:
        norm = fs.normalize_facebook_url(link)
        if not norm or norm in seen:
            continue
        seen.add(norm)
        hay_name = (name or "").strip()
        hay_url = urlparse(norm).path.strip("/").replace("-", " ").replace("_", " ")
        # Must have an extractable page name OR a readable URL slug
        if not hay_name and ("profile.php" in norm or not hay_url):
            continue
        score_name = name_similarity(query, hay_name) if hay_name else 0.0
        score_url = name_similarity(query, hay_url) if hay_url else 0.0
        score = max(score_name, score_url)
        # Every query token (except very short) should appear in name or URL
        hay = f"{hay_name} {hay_url}".lower()
        missing = [t for t in q_toks if len(t) > 2 and t not in hay]
        if len(q_toks) == 1:
            token = q_toks[0]
            # Short brand tokens are too ambiguous (e.g. "SNY", "MJ")
            if len(token) < 5 or token not in hay:
                continue
            score = max(score, 0.9)
        else:
            # Require majority of meaningful tokens + decent score
            meaningful = [t for t in q_toks if len(t) > 2]
            if not meaningful:
                continue
            present = [t for t in meaningful if t in hay]
            if len(present) < max(2, int(round(len(meaningful) * 0.6))):
                continue
            if score < 0.55:
                continue
        scored.append((score, hay_name or query, norm))

    scored.sort(key=lambda x: x[0], reverse=True)
    rows: List[Dict[str, str]] = []
    for score, name, norm in scored[:2]:
        rows.append(
            {
                "Page_Name": name,
                "Facebook_url": norm,
                "Location": f"ASIC:{reg_date}",
                "ASIC_Name": query,
                "ASIC_ACN": acn,
                "ASIC_RegDate": reg_date,
                "Match_Score": f"{score:.2f}",
            }
        )
    return rows


def save_matches(rows: List[Dict[str, str]]) -> int:
    if not rows:
        return 0
    df = pd.DataFrame(rows)
    existing = set()
    if MATCH_CSV.exists() and MATCH_CSV.stat().st_size > 0:
        old = pd.read_csv(MATCH_CSV)
        if "Facebook_url" in old.columns:
            existing = {fs.normalize_facebook_url(u) for u in old["Facebook_url"].dropna()}
    norms = df["Facebook_url"].map(fs.normalize_facebook_url)
    df = df.loc[~norms.isin(existing) & norms.ne("")].copy()
    if df.empty:
        return 0
    write_header = not MATCH_CSV.exists() or MATCH_CSV.stat().st_size == 0
    df.to_csv(MATCH_CSV, mode="a", header=write_header, index=False)
    # Also feed the common page list for scraping
    fs.save_page_links(
        [
            {
                "Page_Name": r["Page_Name"],
                "Facebook_url": r["Facebook_url"],
                "Location": r["Location"],
            }
            for r in df.to_dict("records")
        ],
        fs.PAGE_LIST_CSV,
    )
    return len(df)


def already_searched_names() -> set:
    if not MATCH_CSV.exists() or MATCH_CSV.stat().st_size == 0:
        return set()
    old = pd.read_csv(MATCH_CSV)
    if "ASIC_Name" not in old.columns:
        return set()
    return {str(x).strip().lower() for x in old["ASIC_Name"].dropna()}


def run_discovery(limit: int = 200, offset: int = 0, headed: bool = False) -> None:
    queue = pd.read_csv(QUEUE_CSV, dtype=str)
    queue = queue.rename(columns={"Date of Registration": "RegDate"})
    done = already_searched_names()
    queue = queue[~queue["Query_Name"].astype(str).str.strip().str.lower().isin(done)]
    queue = queue.iloc[offset : offset + limit]
    log(f"DISCOVER start names={len(queue)} offset={offset} already_matched_file={MATCH_CSV.exists()}")

    driver = fs.build_driver(
        headless=not headed,
        profile_dir=SCRIPT_DIR / "credentials" / "chrome_profile_asic",
    )
    saved = 0
    tried = 0
    try:
        driver.get("https://www.facebook.com/")
        fs.random_sleep(2, 3)
        if not fs.is_logged_in(driver):
            log("Login required...")
            ok = fs.optional_login(driver)
            log(f"login_ok={ok}")
        else:
            log("Already logged in via Chrome profile")

        for row in queue.itertuples(index=False):
            name = str(getattr(row, "Query_Name", "") or "").strip()
            acn = str(getattr(row, "ACN", "") or "")
            reg = str(getattr(row, "RegDate", "") or "")
            if reg in {"nan", "None"}:
                reg = ""
            tried += 1
            try:
                rows = discover_page_for_company(driver, name, acn=acn, reg_date=reg)
                n = save_matches(rows)
                saved += n
                log(f"[{tried}/{len(queue)}] {name} hits={len(rows)} new={n} reg={reg}")
            except Exception as exc:
                log(f"[{tried}/{len(queue)}] ERROR {name}: {exc}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass
    log(f"DISCOVER done tried={tried} new_matches={saved} log={LOG}")


def run_scrape(limit: int = 150) -> None:
    if not MATCH_CSV.exists():
        log("No matches CSV yet — run discover first")
        return
    matches = pd.read_csv(MATCH_CSV)
    # Prefer only ASIC-sourced pages for this scrape
    input_csv = ROOT / "Output" / "asic_fb_scrape_input.csv"
    matches[["Page_Name", "Facebook_url", "Location"]].drop_duplicates(
        subset=["Facebook_url"]
    ).to_csv(input_csv, index=False)
    log(f"SCRAPE start input={len(matches)} limit={limit}")
    scraped = fs.run_details_scrape(
        input_csv=input_csv,
        output_csv=fs.OUTPUT_DETAILS_CSV,
        limit=limit,
        headless=True,
        login=True,
        skip_existing=True,
    )
    scraped = fs.enrich_year(scraped)
    log(f"scraped={len(scraped)}")
    if scraped.empty:
        log("No new scraped rows")
        return

    # Attach ASIC reg date into Notes via Location already (ASIC:dd/mm/yyyy)
    def has(s):
        return s.notna() & (s.astype(str).str.strip() != "") & (
            ~s.astype(str).str.lower().isin(["nan", "none"])
        )

    dates = fs.normalize_created_dates(scraped.get("Page_Created_date", pd.Series(dtype=object)))
    recent_page = dates.notna() & (
        dates >= pd.Timestamp(datetime.now()) - pd.DateOffset(months=3)
    )
    log(
        f"batch email={int(has(scraped['Email']).sum())} "
        f"phone={int(has(scraped['Phone_number']).sum())} "
        f"date={int(has(scraped['Page_Created_date']).sum())} "
        f"page_last3m={int(recent_page.sum())} "
        f"both={int((has(scraped['Email']) & has(scraped['Phone_number'])).sum())}"
    )
    appended = append_new_records(scraped)
    log(f"sheet_append={appended}")
    log("SCRAPE done")


def main(argv: Optional[List[str]] = None) -> None:
    p = argparse.ArgumentParser(description="ASIC → Facebook recent-business pipeline")
    p.add_argument("command", choices=["discover", "scrape", "run"])
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--scrape-limit", type=int, default=150)
    p.add_argument("--headed", action="store_true")
    args = p.parse_args(argv)

    if args.command == "discover":
        run_discovery(limit=args.limit, offset=args.offset, headed=args.headed)
    elif args.command == "scrape":
        run_scrape(limit=args.scrape_limit)
    else:
        run_discovery(limit=args.limit, offset=args.offset, headed=args.headed)
        run_scrape(limit=args.scrape_limit)


if __name__ == "__main__":
    main()
