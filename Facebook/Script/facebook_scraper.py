"""
Facebook Australian business page scraper.

Extracts contact details and page creation date from Facebook business pages.
Outputs are written under the project Output/ folder.
"""

from __future__ import annotations

import argparse
import codecs
import os
import random
import re
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# ---------------------------------------------------------------------------
# Paths / config
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
load_dotenv(SCRIPT_DIR / ".env")
PROJECT_DIR = SCRIPT_DIR.parent
INPUT_DIR = SCRIPT_DIR / "input"
OUTPUT_DIR = PROJECT_DIR / "Output"
LOG_DIR = PROJECT_DIR / "logs"

LGA_CSV = INPUT_DIR / "australian_lga_regions.csv"
INPUT_PAGES_CSV = INPUT_DIR / "sydney1.csv"
OUTPUT_DETAILS_CSV = OUTPUT_DIR / "facebook_business_leads.csv"
PAGE_LIST_CSV = OUTPUT_DIR / "page_list.csv"
CITIES_CSV = INPUT_DIR / "australia_major_cities.csv"

# Skip non-page Facebook paths when discovering links
_SKIP_PATH_PREFIXES = (
    "/search",
    "/login",
    "/watch",
    "/reel",
    "/reels",
    "/groups",
    "/events",
    "/marketplace",
    "/stories",
    "/story.php",
    "/photo",
    "/video",
    "/posts",
    "/permalink",
    "/share",
    "/hashtag",
    "/pages/category",
    "/privacy",
    "/policies",
    "/help",
    "/settings",
    "/dialog",
    "/recover",
    "/reg",
)

CHROMEDRIVER_CANDIDATES = [os.environ.get("CHROMEDRIVER_PATH")]
FACEBOOK_EMAIL = os.environ.get("FACEBOOK_EMAIL", "")
FACEBOOK_PASSWORD = os.environ.get("FACEBOOK_PASSWORD", "")

FIELD_PATTERN = re.compile(
    r'"text"\s*:\s*"((?:\\.|[^"\\])*)"\s*\}\s*,\s*"field_type"\s*:\s*"([^"]+)"'
)
ID_PATTERN = re.compile(r"[?&]id=\d+")

# Canonical output columns for local CSV
OUTPUT_COLUMNS = [
    "Page_Name",
    "Facebook_url",
    "Page_Created_date",
    "Year",
    "Phone_number",
    "Email",
    "Website_url",
    "Address",
    "Location",
    "Industry",
    "Managed_From_Country",
]

DETAIL_COLUMNS = OUTPUT_COLUMNS  # alias

# Digit strings seen on nearly every page (Facebook markup, not businesses)
JUNK_PHONE_DIGITS = {
    "0231659310",
    "610231659310",
}

CATEGORY_PATTERNS = [
    re.compile(r'"category_name"\s*:\s*"((?:\\.|[^"\\])*)"', re.I),
    re.compile(r'"page_category"\s*:\s*"((?:\\.|[^"\\])*)"', re.I),
    re.compile(r'"category_list"\s*:\s*\[\s*\{\s*"id"\s*:\s*"[^"]*"\s*,\s*"name"\s*:\s*"((?:\\.|[^"\\])+)"', re.I),
    re.compile(r'"categories"\s*:\s*\[\s*"((?:\\.|[^"\\])+)"', re.I),
    re.compile(r'Page categories?[^<]{0,40}</[^>]+>\s*<[^>]+>\s*([^<]{2,80})', re.I),
    re.compile(r'"text"\s*:\s*"((?:\\.|[^"\\]){2,60})"\s*\}\s*,\s*"field_type"\s*:\s*"category"', re.I),
    re.compile(r'"category"\s*:\s*"((?:\\.|[^"\\]){2,80})"', re.I),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    INPUT_DIR.mkdir(parents=True, exist_ok=True)


def decode_fb_text(value: str) -> str:
    value = value.replace(r"\/", "/")
    try:
        return codecs.decode(value, "unicode_escape")
    except Exception:
        return value.replace("\\u0040", "@")


def extract_profile_fields(page_source: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    for raw_text, field_type in FIELD_PATTERN.findall(page_source):
        key = field_type.lower()
        if key in fields:
            continue
        text = decode_fb_text(raw_text).strip()
        if text:
            fields[key] = text
    return fields


def extract_emails_from_html(page_source: str) -> List[str]:
    blocked = {
        (FACEBOOK_EMAIL or "").strip().lower(),
        "facebook@facebook.com",
        "support@facebook.com",
        "noreply@facebook.com",
        "notification@facebookmail.com",
    }
    blocked = {b for b in blocked if b}
    found: List[str] = []
    for m in re.findall(r"mailto:([A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,})", page_source, re.I):
        email = m.strip().rstrip(".,;)")
        if looks_like_email(email) and email.lower() not in blocked and email.lower() not in {x.lower() for x in found}:
            if "facebook.com" in email.lower() or "fb.com" in email.lower() or "facebookmail.com" in email.lower():
                continue
            found.append(email)
    for m in re.findall(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", page_source, re.I):
        email = m.strip().rstrip(".,;)")
        low = email.lower()
        if low in blocked:
            continue
        if "facebook.com" in low or "fb.com" in low or "facebookmail.com" in low:
            continue
        if looks_like_email(email) and low not in {x.lower() for x in found}:
            found.append(email)
    return found


def extract_phones_from_html(page_source: str) -> List[str]:
    found: List[str] = []
    for m in re.findall(r"tel:([+\d][\d\-\s().]{6,})", page_source, re.I):
        phone = m.strip()
        if looks_like_phone(phone) and not is_junk_phone(phone) and phone not in found:
            found.append(phone)
    # AU-looking numbers in text
    for m in re.findall(
        r"(?:\+?61[\s\-]?(?:\(?0?[2-478]\)?[\s\-]?\d{4}[\s\-]?\d{4}|4\d{2}[\s\-]?\d{3}[\s\-]?\d{3})"
        r"|(?:\(?0[2-478]\)?[\s\-]?\d{4}[\s\-]?\d{4})|(?:04\d{2}[\s\-]?\d{3}[\s\-]?\d{3}))",
        page_source,
    ):
        phone = m.strip()
        # Unformatted digit runs are almost always internal IDs from scripts,
        # not phone numbers, so require a separator or a +61 prefix.
        if not re.search(r"[\s\-().]", phone) and not phone.startswith("+"):
            continue
        if looks_like_phone(phone) and not is_junk_phone(phone) and phone not in found:
            found.append(phone)
    return found


def is_junk_phone(value: Optional[str]) -> bool:
    """Numbers that come from Facebook's own markup, not the business."""
    digits = re.sub(r"\D", "", value or "")
    if not digits:
        return True
    if digits in JUNK_PHONE_DIGITS:
        return True
    return len(set(digits)) <= 2


def extract_creation_date_from_html(page_source: str) -> Optional[str]:
    patterns = [
        r'"creation_date"\s*:\s*"((?:\\.|[^"\\])+)"',
        r'"page_creation_date"\s*:\s*"((?:\\.|[^"\\])+)"',
        r"Page created\s*[-–—:]?\s*([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
        r"Created\s*[-–—:]?\s*([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})",
        r"([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4})\s*(?:</span>|</div>).*?(?:created|Page created)",
    ]
    for pat in patterns:
        m = re.search(pat, page_source, re.I | re.S)
        if m:
            text = decode_fb_text(m.group(1)).strip()
            if text:
                return text
    return None


def extract_manager_country_from_html(page_source: str) -> Optional[str]:
    """
    'Primary country location' of the people who manage the page, shown in the
    Page Transparency panel. Used to confirm the page is Australian.
    """
    marker = re.search(
        r"Primary country/region location for people who manage this Page[^<]*",
        page_source,
        re.I,
    )
    if not marker:
        return None

    # Countries are rendered as sibling spans right after the label, e.g.
    # <span ...>Australia (6)</span>
    window = page_source[marker.end() : marker.end() + 4000]
    banned = ("page", "ads", "advert", "see all", "close", "follower")
    countries: List[str] = []
    # The country list ends as soon as the next unrelated section starts, so
    # stop at the first span that does not look like a country name.
    for raw in re.findall(r">([A-Z][A-Za-z .'\-]{2,40}(?:\s*\(\d+\))?)<", window):
        text = decode_fb_text(raw).strip()
        low = text.lower()
        if not text or any(word in low for word in banned) or text.endswith("."):
            break
        if text not in countries:
            countries.append(text)
        if len(countries) >= 5:
            break
    return ", ".join(countries) if countries else None


def open_transparency_dialog(driver: webdriver.Chrome) -> bool:
    """
    Creation date and manager country often sit behind a 'See all' dialog in
    the Page Transparency panel. Click it so the details land in page_source.
    """
    for label in ("see all", "view all", "more details"):
        try:
            elements = driver.find_elements(
                By.XPATH,
                "//*[self::div or self::span or self::a]"
                f"[contains(translate(normalize-space(text()),"
                f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{label}')]",
            )
        except Exception:
            continue
        for el in elements[:4]:
            try:
                if not el.is_displayed():
                    continue
                before = len(driver.page_source or "")
                driver.execute_script("arguments[0].click();", el)
                random_sleep(2.5, 4)
                html = driver.page_source or ""
                if len(html) != before and re.search(
                    r"primary (?:country )?location|creation_date", html, re.I
                ):
                    return True
            except Exception:
                continue
    return False


def extract_industry(page_source: str) -> Optional[str]:
    """Best-effort Facebook page category / industry."""
    blocked = {
        "page",
        "profile",
        "facebook",
        "community",
        "public figure",
        "interest",
        "topic",
    }
    for pattern in CATEGORY_PATTERNS:
        match = pattern.search(page_source)
        if match:
            text = decode_fb_text(match.group(1)).strip()
            if text and text.lower() not in blocked and len(text) <= 80:
                return text
    return None


def looks_like_email(value: Optional[str]) -> bool:
    if not value:
        return False
    return bool(re.search(r"^[\w.+-]+@[\w.-]+\.\w{2,}$", value.strip()))


def looks_like_phone(value: Optional[str]) -> bool:
    if not value or looks_like_email(value):
        return False
    digits = re.sub(r"\D", "", value)
    return 7 <= len(digits) <= 15


def looks_like_website(value: Optional[str]) -> bool:
    if not value:
        return False
    return bool(re.search(r"(https?://|www\.)", value, re.I)) or (
        "." in value and " " not in value and "@" not in value
    )


def normalize_website(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    if value.startswith("//"):
        value = "https:" + value
    return value


def normalize_facebook_url(url: Optional[str]) -> str:
    """Normalize URL for duplicate checks."""
    if not url or (isinstance(url, float) and pd.isna(url)):
        return ""
    raw = str(url).strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    host = (parsed.netloc or "").lower().replace("www.", "")
    path = (parsed.path or "").rstrip("/")
    query = parsed.query
    # Keep profile.php?id=... identity
    if "profile.php" in path and query:
        qs = parse_qs(query)
        page_id = (qs.get("id") or [""])[0]
        if page_id:
            return f"https://{host}/profile.php?id={page_id}"
    return f"https://{host}{path}".rstrip("/")


def about_urls(page_url: str) -> Tuple[str, str, str]:
    """Return (about, transparency, contact_and_basic_info) URLs."""
    page_url = page_url.strip()
    parsed = urlparse(page_url)

    if "profile.php" in parsed.path or ID_PATTERN.search(page_url):
        query = parse_qs(parsed.query)
        contact_q = {k: v[0] for k, v in query.items() if k != "sk"}
        transp_q = dict(contact_q)
        basic_q = dict(contact_q)
        contact_q["sk"] = "about"
        transp_q["sk"] = "about_profile_transparency"
        basic_q["sk"] = "about_contact_and_basic_info"
        contact = urlunparse(parsed._replace(query=urlencode(contact_q)))
        transparency = urlunparse(parsed._replace(query=urlencode(transp_q)))
        basic = urlunparse(parsed._replace(query=urlencode(basic_q)))
        return contact, transparency, basic

    base = page_url.rstrip("/")
    return (
        f"{base}/about",
        f"{base}/about_profile_transparency",
        f"{base}/about_contact_and_basic_info",
    )


def random_sleep(low: float = 3.0, high: float = 5.0) -> None:
    time.sleep(random.uniform(low, high))


def _ensure_executable(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    if not os.access(path, os.X_OK):
        try:
            path.chmod(path.stat().st_mode | 0o111)
        except OSError:
            return None
    if path.name.lower().startswith("third_party") or path.suffix.lower() in {".txt", ".md"}:
        return None
    return str(path)


def resolve_chromedriver() -> Optional[str]:
    for candidate in CHROMEDRIVER_CANDIDATES:
        if candidate:
            resolved = _ensure_executable(Path(candidate))
            if resolved:
                return resolved
    try:
        from webdriver_manager.chrome import ChromeDriverManager

        installed = Path(ChromeDriverManager().install())
        resolved = _ensure_executable(installed)
        if resolved:
            return resolved
        sibling = installed.parent / "chromedriver"
        resolved = _ensure_executable(sibling)
        if resolved:
            return resolved
    except Exception as exc:
        print(f"webdriver-manager lookup failed: {exc}")

    wdm_root = Path.home() / ".wdm" / "drivers" / "chromedriver"
    if wdm_root.is_dir():
        candidates = sorted(wdm_root.rglob("chromedriver"), key=lambda p: p.stat().st_mtime, reverse=True)
        for path in candidates:
            if path.is_file() and path.name == "chromedriver":
                resolved = _ensure_executable(path)
                if resolved:
                    return resolved
    return None


def build_driver(headless: bool = True, profile_dir: Optional[Path] = None) -> webdriver.Chrome:
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280,900")
    chrome_options.add_argument(f"--remote-debugging-port={random.randint(20000, 40000)}")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
    )
    chrome_options.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 2}
    )
    # Persist cookies/session so one manual login can be reused
    profile = profile_dir or (SCRIPT_DIR / "credentials" / "chrome_profile")
    profile.mkdir(parents=True, exist_ok=True)
    for lock in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
        try:
            (profile / lock).unlink(missing_ok=True)
        except Exception:
            pass
    chrome_options.add_argument(f"--user-data-dir={profile}")
    chrome_options.add_argument("--profile-directory=Default")
    driver_path = resolve_chromedriver()
    last_exc: Optional[Exception] = None
    for attempt in range(1, 4):
        try:
            if driver_path:
                driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
            else:
                driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(60)
            return driver
        except Exception as exc:
            last_exc = exc
            time.sleep(2 * attempt)
            for lock in ("SingletonLock", "SingletonSocket", "SingletonCookie"):
                try:
                    (profile / lock).unlink(missing_ok=True)
                except Exception:
                    pass
    raise last_exc  # type: ignore[misc]


def is_logged_in(driver: webdriver.Chrome) -> bool:
    url = (driver.current_url or "").lower()
    if any(x in url for x in ("/login", "checkpoint", "two_factor", "recover")):
        return False
    html = (driver.page_source or "").lower()
    # Logged-in chrome usually has feed / account menu markers
    markers = (
        'aria-label="your profile"',
        'aria-label="account"',
        'aria-label="home"',
        '"vieweruserid"',
        "logout.php",
    )
    return any(m in html for m in markers)


def optional_login(driver: webdriver.Chrome) -> bool:
    if not FACEBOOK_EMAIL or not FACEBOOK_PASSWORD:
        print("No FACEBOOK_EMAIL/FACEBOOK_PASSWORD set; continuing without login.")
        return False
    driver.get("https://www.facebook.com/login/")
    time.sleep(3)
    try:
        driver.switch_to.alert.dismiss()
    except NoAlertPresentException:
        pass
    dismiss_blocking_dialogs(driver)
    time.sleep(1)

    def _first_visible(selectors: List[str]):
        for sel in selectors:
            for el in driver.find_elements(By.CSS_SELECTOR, sel):
                try:
                    if el.is_displayed() and el.is_enabled():
                        return el
                except Exception:
                    continue
        return None

    email_el = _first_visible(
        ["#email", "input[name='email']", "input[type='text'][name='email']"]
    )
    pass_el = _first_visible(
        ["#pass", "input[name='pass']", "input[type='password']"]
    )

    if not email_el or not pass_el:
        print("Login form not found; continuing without login.")
        return False

    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", email_el)
        time.sleep(0.4)
        try:
            email_el.clear()
            email_el.send_keys(FACEBOOK_EMAIL)
        except Exception:
            driver.execute_script(
                "arguments[0].focus(); arguments[0].value=arguments[1];"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
                email_el,
                FACEBOOK_EMAIL,
            )
        time.sleep(0.6)
        try:
            pass_el.clear()
            pass_el.send_keys(FACEBOOK_PASSWORD)
        except Exception:
            driver.execute_script(
                "arguments[0].focus(); arguments[0].value=arguments[1];"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
                pass_el,
                FACEBOOK_PASSWORD,
            )
        time.sleep(0.6)

        login_btn = _first_visible(
            ["button[name='login']", "#loginbutton", "button[type='submit']", "input[type='submit']"]
        )
        if login_btn:
            try:
                login_btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", login_btn)
        else:
            pass_el.submit()

        time.sleep(7)
        dismiss_blocking_dialogs(driver)
        url = (driver.current_url or "").lower()
        html = (driver.page_source or "").lower()
        if "checkpoint" in url or "two_factor" in url or "two-step" in html[:8000]:
            print("Login needs checkpoint / 2FA — complete it manually, then retry.")
            return False
        if "captcha" in html[:12000] or "security check" in html[:12000]:
            print("Login blocked by captcha/security check.")
            return False
        if "/login" in url or not is_logged_in(driver):
            # one more navigation check
            driver.get("https://www.facebook.com/")
            time.sleep(4)
            if not is_logged_in(driver):
                print("Login failed (not logged in).")
                return False
        print(f"Login OK (url={driver.current_url[:80]})")
        return True
    except Exception as exc:
        print(f"Login error: {exc}")
        return False


def dismiss_blocking_dialogs(driver: webdriver.Chrome) -> None:
    selectors = [
        "button[data-cookiebanner='accept_button']",
        "button[title='Allow all cookies']",
        "div[aria-label='Close']",
        "div[aria-label='Decline optional cookies']",
    ]
    for sel in selectors:
        try:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            if els:
                driver.execute_script("arguments[0].click();", els[0])
                time.sleep(0.5)
        except Exception:
            continue


def normalize_created_dates(series: pd.Series, default_year: Optional[int] = None) -> pd.Series:
    text = series.astype(str).str.strip()
    text = text.str.replace(r"<[^>]+>", " ", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()
    extracted = text.str.extract(
        r"(\d{4}-\d{2}-\d{2}|\d{1,2}\s+[A-Za-z]+\s+\d{4}|[A-Za-z]+\s+\d{1,2},?\s+\d{4}|\d{1,2}\s+[A-Za-z]+)",
        expand=False,
    )
    text = extracted.fillna(text)
    if default_year is not None:
        incomplete = text.str.match(r"^\d{1,2}\s+[A-Za-z]+$", na=False)
        text = text.where(~incomplete, text + f" {default_year}")
    iso_mask = text.str.match(r"^\d{4}-\d{2}-\d{2}", na=False)
    dates = pd.Series(pd.NaT, index=text.index, dtype="datetime64[ns]")
    if iso_mask.any():
        dates.loc[iso_mask] = pd.to_datetime(text.loc[iso_mask], errors="coerce")
    rest = ~iso_mask
    if rest.any():
        dates.loc[rest] = pd.to_datetime(text.loc[rest], errors="coerce", dayfirst=True)
        still_missing = rest & dates.isna()
        if still_missing.any():
            dates.loc[still_missing] = pd.to_datetime(text.loc[still_missing], errors="coerce")
    return dates


def enrich_year(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "Location" not in out.columns and "LGA_region" in out.columns:
        out["Location"] = out["LGA_region"]
    dates = normalize_created_dates(out.get("Page_Created_date", pd.Series(dtype=object)))
    out["Year"] = dates.dt.year.astype("Int64")
    # Keep only canonical columns when present
    for col in OUTPUT_COLUMNS:
        if col not in out.columns:
            out[col] = pd.NA
    return out[OUTPUT_COLUMNS]


def _merge_contacts_from_source(result: Dict[str, Any], page_source: str) -> None:
    fields = extract_profile_fields(page_source)

    email = fields.get("profile_email") or fields.get("email")
    phone = fields.get("profile_phone") or fields.get("phone") or fields.get("mobile")
    website = normalize_website(fields.get("website") or fields.get("website_url"))
    address = fields.get("address")
    created = fields.get("creation_date") or fields.get("page_creation_date")
    industry = extract_industry(page_source) or fields.get("category") or fields.get("page_category")

    if not email:
        emails = extract_emails_from_html(page_source)
        email = emails[0] if emails else None
    if not phone:
        phones = extract_phones_from_html(page_source)
        phone = phones[0] if phones else None
    if not created:
        created = extract_creation_date_from_html(page_source)
    country = extract_manager_country_from_html(page_source)

    if email and looks_like_email(email) and not result.get("Email"):
        if email.lower() != (FACEBOOK_EMAIL or "").strip().lower():
            result["Email"] = email
    if phone and looks_like_phone(phone) and not result.get("Phone_number"):
        result["Phone_number"] = phone
    if website and looks_like_website(website) and not result.get("Website_url"):
        result["Website_url"] = website
    if address and not result.get("Address"):
        result["Address"] = address
    if industry and not result.get("Industry"):
        result["Industry"] = industry
    if country and not result.get("Managed_From_Country"):
        result["Managed_From_Country"] = country
    if created and not result.get("Page_Created_date"):
        result["Page_Created_date"] = created
        parsed = normalize_created_dates(pd.Series([created]))
        if parsed.notna().iloc[0]:
            result["Year"] = int(parsed.iloc[0].year)


def scrape_page_details(
    driver: webdriver.Chrome,
    page_url: str,
    page_name: str = "",
    location: str = "",
) -> Dict[str, Any]:
    about_url, transparency_url, contact_basic_url = about_urls(page_url)
    result: Dict[str, Any] = {
        "Page_Name": page_name or None,
        "Facebook_url": page_url,
        "Page_Created_date": None,
        "Year": None,
        "Phone_number": None,
        "Email": None,
        "Website_url": None,
        "Address": None,
        "Location": location or None,
        "Industry": None,
        "Managed_From_Country": None,
    }

    for url in (about_url, contact_basic_url, transparency_url):
        try:
            driver.get(url)
            random_sleep(3.5, 5.5)
            dismiss_blocking_dialogs(driver)
            _merge_contacts_from_source(result, driver.page_source)
            # Transparency details are often only rendered after opening the
            # "See all" dialog, so retry there when we still lack them.
            if url == transparency_url and not (
                result.get("Page_Created_date") and result.get("Managed_From_Country")
            ):
                if open_transparency_dialog(driver):
                    _merge_contacts_from_source(result, driver.page_source)
        except Exception:
            continue
        if (
            result.get("Email")
            and result.get("Phone_number")
            and result.get("Page_Created_date")
            and result.get("Managed_From_Country")
        ):
            break

    if not result["Page_Name"]:
        title = (driver.title or "").replace(" | Facebook", "").strip()
        result["Page_Name"] = title or None

    return result


def append_details_rows(rows: List[Dict[str, Any]], output_path: Path = OUTPUT_DETAILS_CSV) -> None:
    if not rows:
        return
    ensure_dirs()
    df = enrich_year(pd.DataFrame(rows))
    write_header = not output_path.exists() or output_path.stat().st_size == 0
    df.to_csv(output_path, mode="a", header=write_header, index=False)


def load_existing_urls(csv_path: Path = OUTPUT_DETAILS_CSV) -> set:
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return set()
    df = pd.read_csv(csv_path)
    url_col = "Facebook_url" if "Facebook_url" in df.columns else None
    if not url_col:
        return set()
    return {normalize_facebook_url(u) for u in df[url_col].dropna().tolist() if normalize_facebook_url(u)}


def filter_new_records(df: pd.DataFrame, existing_urls: set) -> pd.DataFrame:
    if df.empty:
        return df
    out = enrich_year(df)
    norms = out["Facebook_url"].map(normalize_facebook_url)
    mask = ~norms.isin(existing_urls) & norms.ne("")
    return out.loc[mask].copy()


def load_input_pages(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Support legacy LGA_region column
    if "Location" not in df.columns and "LGA_region" in df.columns:
        df["Location"] = df["LGA_region"]
    required = {"Facebook_url"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input CSV missing columns: {sorted(missing)}")
    if "Page_Name" not in df.columns:
        df["Page_Name"] = ""
    if "Location" not in df.columns:
        df["Location"] = ""
    return df.dropna(subset=["Facebook_url"]).drop_duplicates(subset=["Facebook_url"])


def filter_recent_pages(details_df: pd.DataFrame, year_from: int = 2023) -> pd.DataFrame:
    enriched = enrich_year(details_df)
    mask = enriched["Year"].notna() & (enriched["Year"] >= year_from)
    return enriched.loc[mask].sort_values("Year", ascending=False)


def load_lga_regions(csv_path: Path = LGA_CSV) -> List[str]:
    df = pd.read_csv(csv_path)
    col = "LGA_region" if "LGA_region" in df.columns else df.columns[0]
    data_list = df[col].dropna().astype(str).tolist()
    expanded: List[str] = []
    for item in data_list:
        if "/" in item:
            expanded.extend(p.strip() for p in item.split("/") if p.strip())
        elif "-" in item:
            expanded.extend(p.strip() for p in item.split("-") if p.strip())
        else:
            expanded.append(item.strip())
    seen = set()
    ordered = []
    for name in expanded:
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def save_page_links(rows: List[Dict[str, str]], path: Path = PAGE_LIST_CSV) -> None:
    if not rows:
        return
    ensure_dirs()
    df = pd.DataFrame(rows)
    for col in ("Page_Name", "Facebook_url", "Location"):
        if col not in df.columns:
            df[col] = ""
    df = df[["Page_Name", "Facebook_url", "Location"]]
    existing: set = set()
    if path.exists() and path.stat().st_size > 0:
        old = pd.read_csv(path)
        if "Facebook_url" in old.columns:
            existing = {normalize_facebook_url(u) for u in old["Facebook_url"].dropna()}
    norms = df["Facebook_url"].map(normalize_facebook_url)
    df = df.loc[~norms.isin(existing) & norms.ne("")].copy()
    if df.empty:
        return
    write_header = not path.exists() or path.stat().st_size == 0
    df.to_csv(path, mode="a", header=write_header, index=False)
    print(f"Saved {len(df)} new page link(s) -> {path}")


def load_cities(csv_path: Path = CITIES_CSV) -> List[str]:
    if not csv_path.exists():
        return []
    df = pd.read_csv(csv_path)
    col = "Location" if "Location" in df.columns else df.columns[0]
    cities = [str(x).strip() for x in df[col].dropna().tolist() if str(x).strip()]
    seen = set()
    out: List[str] = []
    for c in cities:
        key = c.lower()
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out


def is_probable_page_url(url: str) -> bool:
    norm = normalize_facebook_url(url)
    if not norm or "facebook.com" not in norm:
        return False
    parsed = urlparse(norm)
    path = (parsed.path or "/").lower()
    if path in {"", "/"}:
        return False
    for prefix in _SKIP_PATH_PREFIXES:
        if path.startswith(prefix):
            return False
    if "profile.php" in path:
        return bool(parse_qs(parsed.query).get("id"))
    parts = [p for p in path.split("/") if p]
    if not parts:
        return False
    if parts[0] in {"people", "public", "ads", "business", "gaming"}:
        return False
    return True


def extract_page_links_from_html(html: str) -> List[Tuple[str, str]]:
    found: List[Tuple[str, str]] = []
    seen = set()
    hrefs = re.findall(r'href="(https://(?:www\.)?facebook\.com/[^"]+)"', html)
    hrefs += re.findall(r'"url"\s*:\s*"(https:\\/\\/www\.facebook\.com\\/[^"]+)"', html)
    for h in hrefs:
        h = h.replace("\\/", "/")
        if "profile.php" in h:
            parsed = urlparse(h)
            qs = parse_qs(parsed.query)
            pid = (qs.get("id") or [""])[0]
            h = f"https://www.facebook.com/profile.php?id={pid}" if pid else h
        else:
            h = h.split("?")[0]
        if not is_probable_page_url(h):
            continue
        norm = normalize_facebook_url(h)
        if not norm or norm in seen:
            continue
        seen.add(norm)
        path = urlparse(norm).path.strip("/")
        name = ""
        if path and "profile.php" not in path:
            name = path.split("/")[0].replace("-", " ").replace("_", " ")
        found.append((name, norm))
    return found


def discover_pages_for_location(
    driver: webdriver.Chrome,
    location: str,
    keyword: str = "business",
    scroll_rounds: int = 4,
) -> List[Dict[str, str]]:
    from urllib.parse import quote_plus

    query = f"{location} {keyword}".strip()
    search_url = f"https://www.facebook.com/search/pages/?q={quote_plus(query)}"
    print(f"Discover: {query}")
    driver.get(search_url)
    random_sleep(4, 6)
    dismiss_blocking_dialogs(driver)
    html = driver.page_source or ""
    if len(html) < 500 or "login" in (driver.current_url or "").lower():
        print(
            "  WARNING: Facebook search returned little/no content "
            "(login wall or block). Set FACEBOOK_EMAIL/PASSWORD and use --login."
        )
    for _ in range(scroll_rounds):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep(2, 3.5)
    links = extract_page_links_from_html(driver.page_source)
    rows = [
        {"Page_Name": name, "Facebook_url": url, "Location": location}
        for name, url in links
    ]
    print(f"  found {len(rows)} candidate page link(s)")
    return rows


def ad_library_url(keyword: str, country: str = "AU") -> str:
    from urllib.parse import quote_plus

    return (
        "https://www.facebook.com/ads/library/?active_status=all&ad_type=all"
        f"&country={country}&q={quote_plus(keyword)}"
        "&search_type=keyword_unordered&media_type=all"
    )


def extract_advertiser_pages_from_html(html: str) -> List[Tuple[str, str]]:
    """Pull advertiser page ids/handles out of an Ad Library results page."""
    found: List[Tuple[str, str]] = []
    seen = set()

    page_ids = re.findall(r"view_all_page_id[=\"':\s\\]+(\d{5,})", html)
    page_ids += re.findall(r'"page_id"\s*:\s*"?(\d{5,})"?', html)
    for pid in page_ids:
        url = f"https://www.facebook.com/profile.php?id={pid}"
        norm = normalize_facebook_url(url)
        if norm and norm not in seen:
            seen.add(norm)
            found.append(("", norm))

    for name, url in extract_page_links_from_html(html):
        if url not in seen:
            seen.add(url)
            found.append((name, url))
    return found


def discover_pages_from_ad_library(
    driver: webdriver.Chrome,
    keyword: str,
    country: str = "AU",
    scroll_rounds: int = 8,
) -> List[Dict[str, str]]:
    """
    Discover advertiser pages via Facebook Ad Library.

    Surfaces a different pool than normal search: Ad Library ranks by ad
    activity rather than follower count, so small/new businesses appear.
    """
    url = ad_library_url(keyword, country)
    print(f"AdLibrary: {keyword} ({country})")
    driver.get(url)
    random_sleep(5, 7)
    dismiss_blocking_dialogs(driver)

    for _ in range(scroll_rounds):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        random_sleep(2.5, 4)

    links = extract_advertiser_pages_from_html(driver.page_source or "")
    rows = [
        {"Page_Name": name, "Facebook_url": link, "Location": f"AU ads: {keyword}"}
        for name, link in links
    ]
    print(f"  found {len(rows)} advertiser page(s)")
    return rows


def run_ad_library_discovery(
    keywords: Optional[List[str]] = None,
    country: str = "AU",
    headless: bool = True,
    login: bool = True,
    output_csv: Path = PAGE_LIST_CSV,
    scroll_rounds: int = 8,
    profile_dir: Optional[Path] = None,
) -> pd.DataFrame:
    keywords = keywords or [
        "business",
        "cafe",
        "salon",
        "plumber",
        "electrician",
        "cleaning",
        "dentist",
        "gym",
        "photographer",
        "landscaping",
    ]
    driver = build_driver(headless=headless, profile_dir=profile_dir)
    all_rows: List[Dict[str, str]] = []
    try:
        if login and not is_logged_in(driver):
            optional_login(driver)
        for kw in keywords:
            try:
                rows = discover_pages_from_ad_library(
                    driver, kw, country=country, scroll_rounds=scroll_rounds
                )
                save_page_links(rows, output_csv)
                all_rows.extend(rows)
            except Exception as exc:
                print(f"  ERROR ad library {kw}: {exc}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass
    return pd.DataFrame(all_rows)


def run_page_discovery(
    locations: Optional[List[str]] = None,
    limit_locations: Optional[int] = None,
    keyword: str = "business",
    headless: bool = True,
    login: bool = False,
    output_csv: Path = PAGE_LIST_CSV,
    scroll_rounds: int = 4,
) -> pd.DataFrame:
    locations = locations or load_cities() or load_lga_regions()
    if limit_locations is not None:
        locations = locations[:limit_locations]
    if not locations:
        raise SystemExit("No locations found for discovery (check australia_major_cities.csv)")

    print(f"Discovering Facebook pages for {len(locations)} location(s)...")
    driver = build_driver(headless=headless)
    all_rows: List[Dict[str, str]] = []
    try:
        if login:
            optional_login(driver)
        for loc in locations:
            try:
                rows = discover_pages_for_location(
                    driver, loc, keyword=keyword, scroll_rounds=scroll_rounds
                )
                save_page_links(rows, output_csv)
                all_rows.extend(rows)
            except Exception as exc:
                print(f"  ERROR discovering {loc}: {exc}")
    finally:
        driver.quit()
    return pd.DataFrame(all_rows)


def run_details_scrape(
    input_csv: Path,
    output_csv: Path,
    limit: Optional[int] = None,
    offset: int = 0,
    headless: bool = True,
    login: bool = False,
    flush_every: int = 10,
    skip_existing: bool = True,
    profile_dir: Optional[Path] = None,
) -> pd.DataFrame:
    ensure_dirs()
    pages = load_input_pages(input_csv)
    existing = load_existing_urls(output_csv) if skip_existing else set()
    if existing:
        before = len(pages)
        pages = pages[~pages["Facebook_url"].map(normalize_facebook_url).isin(existing)]
        print(f"Skipping {before - len(pages)} URLs already in {output_csv.name}")

    if offset:
        pages = pages.iloc[offset:]
    if limit is not None:
        pages = pages.iloc[:limit]

    print(f"Scraping {len(pages)} pages from {input_csv.name} -> {output_csv.name}")
    if pages.empty:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)

    driver = build_driver(headless=headless, profile_dir=profile_dir)
    results: List[Dict[str, Any]] = []
    buffer: List[Dict[str, Any]] = []

    try:
        if login:
            optional_login(driver)

        for idx, row in enumerate(pages.itertuples(index=False), start=1):
            url = getattr(row, "Facebook_url")
            name = getattr(row, "Page_Name", "") or ""
            location = getattr(row, "Location", "") or getattr(row, "LGA_region", "") or ""
            print(f"[{idx}/{len(pages)}] {name or url}")
            try:
                detail = scrape_page_details(driver, url, page_name=name, location=location)
            except Exception as exc:
                print(f"  ERROR: {exc}")
                detail = {
                    "Page_Name": name,
                    "Facebook_url": url,
                    "Page_Created_date": None,
                    "Year": None,
                    "Phone_number": None,
                    "Email": None,
                    "Website_url": None,
                    "Address": None,
                    "Location": location,
                    "Industry": None,
                    "Managed_From_Country": None,
                }
            print(
                f"  phone={detail['Phone_number']} email={detail['Email']} "
                f"web={detail['Website_url']} created={detail['Page_Created_date']} "
                f"year={detail['Year']} country={detail['Managed_From_Country']}"
            )
            results.append(detail)
            buffer.append(detail)
            if len(buffer) >= flush_every:
                append_details_rows(buffer, output_csv)
                buffer.clear()

        if buffer:
            append_details_rows(buffer, output_csv)
    finally:
        driver.quit()

    return enrich_year(pd.DataFrame(results))


def run_verification(sample_limit: int = 4, headless: bool = True) -> pd.DataFrame:
    known_pages = [
        {
            "Page_Name": "Meat & Livestock Australia",
            "Facebook_url": "https://www.facebook.com/meatandlivestockaustralia",
            "Location": "Sydney",
            "expect_email": "info@mla.com.au",
            "expect_phone_substr": "+61",
        },
        {
            "Page_Name": "Mattrimony",
            "Facebook_url": "https://www.facebook.com/Mattrimony",
            "Location": "Sydney",
            "expect_email": "info@mattrimony.com.au",
            "expect_phone_substr": "+61",
        },
        {
            "Page_Name": "Merita A V",
            "Facebook_url": "https://www.facebook.com/merita.a.v20",
            "Location": "Sydney",
            "expect_email": "merita@meritaasv.com",
            "expect_phone_substr": "+61",
        },
        {
            "Page_Name": "Rashmi shrestha & co.",
            "Facebook_url": "https://www.facebook.com/profile.php?id=100089117367268",
            "Location": "Sydney",
            "expect_email": "namaste@rashmishrestha.com",
            "expect_phone_substr": None,
        },
    ][:sample_limit]

    driver = build_driver(headless=headless)
    rows: List[Dict[str, Any]] = []
    failures: List[str] = []
    try:
        for spec in known_pages:
            print(f"VERIFY {spec['Page_Name']}")
            detail = scrape_page_details(
                driver,
                spec["Facebook_url"],
                page_name=spec["Page_Name"],
                location=spec["Location"],
            )
            rows.append(detail)
            if spec.get("expect_email") and detail["Email"] != spec["expect_email"]:
                failures.append(f"{spec['Page_Name']}: email mismatch got {detail['Email']!r}")
            if spec.get("expect_phone_substr"):
                phone = detail["Phone_number"] or ""
                if spec["expect_phone_substr"] not in phone:
                    failures.append(f"{spec['Page_Name']}: phone mismatch got {phone!r}")
            if not detail.get("Page_Created_date"):
                failures.append(f"{spec['Page_Name']}: missing Page_Created_date")
            print(
                f"  OK phone={detail['Phone_number']} email={detail['Email']} "
                f"created={detail['Page_Created_date']} year={detail['Year']}"
            )
    finally:
        driver.quit()

    ensure_dirs()
    result_df = enrich_year(pd.DataFrame(rows))
    out = OUTPUT_DIR / "verification_results.csv"
    result_df.to_csv(out, index=False)
    print(f"Wrote {out}")
    if failures:
        print("VERIFICATION FAILURES:")
        for item in failures:
            print(" -", item)
        raise SystemExit(1)
    print("All verification checks passed.")
    return result_df


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Facebook AU business page scraper")
    parser.add_argument(
        "command",
        choices=["verify", "scrape", "filter-recent", "discover", "discover-ads"],
    )
    parser.add_argument("--input", type=Path, default=INPUT_PAGES_CSV)
    parser.add_argument("--output", type=Path, default=OUTPUT_DETAILS_CSV)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--login", action="store_true")
    parser.add_argument("--year-from", type=int, default=2023)
    parser.add_argument("--filter-output", type=Path, default=None)
    parser.add_argument("--sample-limit", type=int, default=4)
    parser.add_argument("--no-skip-existing", action="store_true", help="Do not skip URLs already in output CSV")
    parser.add_argument("--locations-limit", type=int, default=None, help="Max cities for discover")
    parser.add_argument("--keyword", type=str, default="business", help="Search keyword with location")
    parser.add_argument("--page-list", type=Path, default=PAGE_LIST_CSV, help="Discovered pages CSV")
    parser.add_argument("--country", type=str, default="AU", help="Ad Library country code")
    parser.add_argument(
        "--keywords",
        type=str,
        default=None,
        help="Comma-separated keywords for discover-ads",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> None:
    args = parse_args(argv)
    headless = not args.headed
    ensure_dirs()

    if args.command == "verify":
        run_verification(sample_limit=args.sample_limit, headless=headless)
    elif args.command == "discover":
        run_page_discovery(
            limit_locations=args.locations_limit,
            keyword=args.keyword,
            headless=headless,
            login=args.login,
            output_csv=args.page_list,
        )
        print(f"Discovery finished. Page list: {args.page_list}")
    elif args.command == "discover-ads":
        kws = (
            [k.strip() for k in args.keywords.split(",") if k.strip()]
            if args.keywords
            else None
        )
        run_ad_library_discovery(
            keywords=kws,
            country=args.country,
            headless=headless,
            login=True,
            output_csv=args.page_list,
        )
        print(f"Ad Library discovery finished. Page list: {args.page_list}")
    elif args.command == "scrape":
        df = run_details_scrape(
            input_csv=args.input,
            output_csv=args.output,
            limit=args.limit,
            offset=args.offset,
            headless=headless,
            login=args.login,
            skip_existing=not args.no_skip_existing,
        )
        with_contact = df[
            df["Phone_number"].notna() | df["Email"].notna() | df["Website_url"].notna()
        ]
        print(f"Done. {len(with_contact)}/{len(df)} rows have at least one contact field.")
    elif args.command == "filter-recent":
        if not args.output.exists():
            raise SystemExit(f"Missing details file: {args.output}")
        details = pd.read_csv(args.output)
        recent = filter_recent_pages(details, year_from=args.year_from)
        out = args.filter_output or (OUTPUT_DIR / f"filtered_data_{args.year_from}_plus.csv")
        recent.to_csv(out, index=False)
        print(f"Wrote {len(recent)} rows to {out}")


if __name__ == "__main__":
    main()
