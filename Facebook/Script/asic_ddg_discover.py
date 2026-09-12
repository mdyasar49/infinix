#!/usr/bin/env python3
"""
Fast discovery: for each ASIC company name, use DuckDuckGo HTML to find
facebook.com page URLs (often more precise than FB search ranking).
"""

from __future__ import annotations

import argparse
import re
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import List, Set

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "Output" / "asic_fb_search_queue.csv"
MATCH = ROOT / "Output" / "asic_fb_matches.csv"
PAGE_LIST = ROOT / "Output" / "page_list.csv"
LOG = ROOT / "logs" / f"ddg_asic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG.parent.mkdir(parents=True, exist_ok=True)

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
    }
)

FB_URL_RE = re.compile(
    r"https?://(?:www\.)?facebook\.com/[A-Za-z0-9.\-_/%]+",
    re.I,
)
SKIP = (
    "/search/",
    "/login",
    "/share",
    "/watch",
    "/reel",
    "/groups/",
    "/events/",
    "/marketplace",
    "/ads/",
    "/privacy",
    "/help",
    "/policies",
)


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def tokens(text: str) -> List[str]:
    stop = {"pty", "ltd", "limited", "the", "and", "of", "for", "au", "australia", "co"}
    toks = re.findall(r"[a-z0-9]+", (text or "").lower())
    return [t for t in toks if t not in stop and len(t) > 1]


def normalize_fb(url: str) -> str:
    url = urllib.parse.unquote(url).split("?")[0].split("#")[0].rstrip("/")
    url = url.replace("http://", "https://").replace("://m.facebook.com", "://www.facebook.com")
    if "facebook.com" not in url:
        return ""
    for s in SKIP:
        if s in url.lower():
            return ""
    return url


def looks_like_match(query: str, url: str) -> bool:
    q = tokens(query)
    if not q:
        return False
    slug = urllib.parse.urlparse(url).path.strip("/").lower().replace("-", " ").replace("_", " ").replace(".", " ")
    if "profile.php" in slug:
        return False
    hay = slug
    if len(q) == 1:
        return q[0] in hay
    missing = [t for t in q if len(t) > 2 and t not in hay]
    return len(missing) <= max(1, len(q) // 3)


def ddg_facebook_urls(query: str) -> List[str]:
    q = f'site:facebook.com "{query}"'
    url = "https://html.duckduckgo.com/html/"
    try:
        r = SESSION.post(url, data={"q": q}, timeout=25)
        r.raise_for_status()
        html = r.text
    except Exception as exc:
        log(f"DDG error {query}: {exc}")
        return []

    found: List[str] = []
    seen: Set[str] = set()
    # DDG wraps redirects: uddg=encoded_url
    for m in re.findall(r"uddg=([^&\"']+)", html):
        decoded = urllib.parse.unquote(m)
        if "facebook.com" not in decoded:
            continue
        norm = normalize_fb(decoded)
        if not norm or norm in seen:
            continue
        if looks_like_match(query, norm):
            seen.add(norm)
            found.append(norm)
    for m in FB_URL_RE.findall(html):
        norm = normalize_fb(m)
        if not norm or norm in seen:
            continue
        if looks_like_match(query, norm):
            seen.add(norm)
            found.append(norm)
    return found[:2]


def already_done() -> Set[str]:
    if not MATCH.exists() or MATCH.stat().st_size == 0:
        return set()
    df = pd.read_csv(MATCH)
    if "ASIC_Name" not in df.columns:
        return set()
    return {str(x).strip().lower() for x in df["ASIC_Name"].dropna()}


def save_rows(rows: List[dict]) -> int:
    if not rows:
        return 0
    df = pd.DataFrame(rows)
    existing = set()
    if MATCH.exists() and MATCH.stat().st_size > 0:
        old = pd.read_csv(MATCH)
        existing = {str(u).rstrip("/") for u in old.get("Facebook_url", pd.Series(dtype=str)).dropna()}
    df = df[~df["Facebook_url"].isin(existing)].copy()
    if df.empty:
        return 0
    write_header = not MATCH.exists() or MATCH.stat().st_size == 0
    df.to_csv(MATCH, mode="a", header=write_header, index=False)

    # page_list
    pl = df[["Page_Name", "Facebook_url", "Location"]].copy()
    pe = set()
    if PAGE_LIST.exists() and PAGE_LIST.stat().st_size > 0:
        old = pd.read_csv(PAGE_LIST)
        pe = {str(u).rstrip("/") for u in old.get("Facebook_url", pd.Series(dtype=str)).dropna()}
    pl = pl[~pl["Facebook_url"].isin(pe)]
    if not pl.empty:
        write_header = not PAGE_LIST.exists() or PAGE_LIST.stat().st_size == 0
        pl.to_csv(PAGE_LIST, mode="a", header=write_header, index=False)
    return len(df)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=500)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=1.2)
    args = ap.parse_args()

    queue = pd.read_csv(QUEUE, dtype=str)
    done = already_done()
    queue = queue[~queue["Query_Name"].astype(str).str.strip().str.lower().isin(done)]
    queue = queue.iloc[args.offset : args.offset + args.limit]
    log(f"DDG discover start names={len(queue)}")

    saved = 0
    hits = 0
    for i, row in enumerate(queue.itertuples(index=False), start=1):
        name = str(getattr(row, "Query_Name", "") or "").strip()
        acn = str(getattr(row, "ACN", "") or "")
        reg = str(getattr(row, "Date of Registration", "") or "")
        urls = ddg_facebook_urls(name)
        rows = []
        for u in urls:
            slug = urllib.parse.urlparse(u).path.strip("/").split("/")[0]
            page_name = slug.replace("-", " ").replace("_", " ") if slug and "profile.php" not in slug else name
            rows.append(
                {
                    "Page_Name": page_name,
                    "Facebook_url": u,
                    "Location": f"ASIC:{reg}",
                    "ASIC_Name": name,
                    "ASIC_ACN": acn,
                    "ASIC_RegDate": reg,
                    "Match_Score": "ddg",
                }
            )
        n = save_rows(rows)
        saved += n
        if urls:
            hits += 1
        if i % 10 == 0 or n:
            log(f"[{i}/{len(queue)}] {name} urls={len(urls)} new={n}")
        time.sleep(args.sleep)

    log(f"DONE tried={len(queue)} companies_with_hit={hits} new_rows={saved}")


if __name__ == "__main__":
    main()
