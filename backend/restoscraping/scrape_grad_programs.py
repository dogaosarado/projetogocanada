"""
scrape_grad_programs.py

Scrapes graduate program listings from 8 Canadian universities and outputs
a JSON array of program entries matching the structure:
    { "name": "...", "degree_type": "...", "url": "..." }

Usage:
    python scrape_grad_programs.py output.json

Dependencies:
    pip install requests beautifulsoup4 playwright
    python -m playwright install chromium

Notes:
- degree_type is inferred from the program name where possible; falls back to "Unknown".
- name is taken from the anchor text on the listing page.
- Run from your own machine — university servers block cloud IPs.
"""

import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# ---------------------------------------------------------------------------
# Shared session
# ---------------------------------------------------------------------------

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
})


def fetch(url, timeout=20):
    try:
        r = SESSION.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"  [WARN] fetch failed for {url}: {e}")
        return None


# ---------------------------------------------------------------------------
# Degree type inference
# ---------------------------------------------------------------------------

DEGREE_PATTERNS = [
    (r"\bPh\.?D\b|Doctor of Philosophy",                          "PhD"),
    (r"\bEdD\b|Doctor of Education",                              "PhD"),
    (r"\bDMA\b|Doctor of Musical Arts",                           "PhD"),
    (r"\bMD\b|Doctor of Medicine",                                "MD"),
    (r"\bMBA\b|Master of Business Administration",                "MBA"),
    (r"\bMSc\b|Master of Science",                                "MSc"),
    (r"\bMA\b|Master of Arts",                                    "MA"),
    (r"\bMEd\b|Master of Education",                              "MEd"),
    (r"\bMEng\b|MEL\b|Master of Engineering",                     "MEng"),
    (r"\bMASc\b|Master of Applied Science",                       "MASc"),
    (r"\bMFA\b|Master of Fine Arts",                              "MFA"),
    (r"\bLLM\b|Master of Laws",                                   "LLM"),
    (r"\bMPH\b|Master of Public Health",                          "MPH"),
    (r"\bMSW\b|Master of Social Work",                            "MSW"),
    (r"\bMArch\b|Master of Architecture",                         "Master"),
    (r"\bMaster\b",                                               "Master"),
    (r"\bCertificate\b|\bDiploma\b",                              "Certificate"),
]

def infer_degree_type(name):
    for pattern, dtype in DEGREE_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            return dtype
    return "Unknown"


def make_entry(name, url):
    name = name.strip()
    return {
        "name": name,
        "degree_type": infer_degree_type(name),
        "url": url,
    }


# ---------------------------------------------------------------------------
# Per-university scrapers
# ---------------------------------------------------------------------------

def scrape_mcgill():
    """
    McGill WAF blocks direct requests and new-page navigation.
    Strategy: load the listing page once, then click each faculty filter
    link (AJAX update, no navigation) and collect program links from the
    updated DOM. Deduplicate by URL and skip "Full program description" anchors.
    """
    base = "https://www.mcgill.ca"
    url  = "https://www.mcgill.ca/gradapplicants/programs"
    faculty_ids = [14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 30, 31]
    entries = []
    seen = set()

    def collect(html):
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            name = a.get_text(strip=True)
            if "/gradapplicants/program/" not in href:
                continue
            if not name or name.lower() == "full program description":
                continue
            full = base + href if href.startswith("/") else href
            if full in seen:
                continue
            seen.add(full)
            entries.append(make_entry(name, full))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(3)

        for fid in faculty_ids:
            selector = f"a[href*='field_faculty_interest%3A{fid}']"
            link = page.query_selector(selector)
            if not link:
                continue
            link.click()
            time.sleep(3)
            collect(page.content())

            # return to full list
            back = page.query_selector("a[href='/gradapplicants/programs']")
            if back:
                back.click()
                time.sleep(2)

        browser.close()
    return entries


def scrape_concordia():
    """
    Listing page: https://www.concordia.ca/academics/graduate.html
    Keep links matching /academics/graduate/<program>.
    """
    base = "https://www.concordia.ca"
    url  = "https://www.concordia.ca/academics/graduate.html"
    html = fetch(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    entries = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(base, href)
        path = urlparse(full).path.rstrip("/")
        if re.search(r"/academics/graduate/[^/]+$", path) and full not in seen:
            seen.add(full)
            name = a.get_text(" ", strip=True)
            if name:
                entries.append(make_entry(name, full))
    return entries


def scrape_ualberta():
    """
    Page is JS-rendered with a Coveo search index (5 pages).
    Wait for networkidle + 5s, collect links, then click each page span.
    """
    base = "https://www.ualberta.ca"
    url  = "https://www.ualberta.ca/en/graduate-programs/index.html"
    entries = []
    seen = set()

    def collect(page):
        links = page.eval_on_selector_all(
            "a[href]", "els => els.map(e => [e.href, e.innerText.trim()])"
        )
        for full, name in links:
            path = urlparse(full).path
            if re.match(r"^/en/graduate-programs/[^/]+\.html$", path) and full not in seen:
                seen.add(full)
                if not name:
                    slug = path.split("/")[-1].replace(".html", "")
                    name = slug.replace("-", " ").title()
                entries.append(make_entry(name, full))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        )
        pg = context.new_page()
        pg.goto(url, wait_until="networkidle", timeout=60000)
        time.sleep(5)

        # collect page 1
        collect(pg)

        # click pages 2–5 by aria-label
        for page_num in range(2, 6):
            btn = pg.query_selector(f"span[aria-label='Page {page_num}']")
            if not btn:
                break
            btn.click()
            pg.wait_for_load_state("networkidle")
            time.sleep(3)
            collect(pg)

        browser.close()
    return entries


def scrape_usask():
    """
    Listing page: https://grad.usask.ca/programs/
    Keep links matching /programs/<program>.php, exclude utility pages.
    """
    base     = "https://grad.usask.ca"
    url      = "https://grad.usask.ca/programs/"
    excluded = {"find-a-program", "find-a-supervisor"}
    html     = fetch(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    entries = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(base, href)
        path = urlparse(full).path
        match = re.match(r"^/programs/([^/]+)\.php$", path)
        if match and match.group(1) not in excluded and full not in seen:
            seen.add(full)
            name = a.get_text(" ", strip=True)
            if name:
                entries.append(make_entry(name, full))
    return entries


def scrape_uregina():
    """
    Listing page: https://www.uregina.ca/academics/programs/
    Keep links matching /academics/programs/<dept>/<program> where the
    path contains a graduate-level keyword (master, phd, msc, mba, etc.)
    or comes from known graduate departments (levene, graduate).
    Excludes undergraduate, certificate, diploma, and professional-development pages.
    """
    base = "https://www.uregina.ca"
    url  = "https://www.uregina.ca/academics/programs/"

    GRAD_KEYWORDS = re.compile(
        r"(master|phd|msc|mba|m\.sc|levene|graduate|doctoral|doctor)",
        re.IGNORECASE,
    )
    EXCLUDE_SEGMENTS = re.compile(
        r"/(professional-development|cce|cert-|dip-|bachelor|baccalaureat|"
        r"arts-science\.html|faculty-directory|federated-colleges)",
        re.IGNORECASE,
    )

    html = fetch(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    entries = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(base, href)
        path = urlparse(full).path.rstrip("/")

        if not re.match(r"^/academics/programs/[^/]+/.+$", path):
            continue
        if EXCLUDE_SEGMENTS.search(path):
            continue
        if not GRAD_KEYWORDS.search(path):
            continue
        if full in seen:
            continue

        seen.add(full)
        name = a.get_text(" ", strip=True)
        if name:
            entries.append(make_entry(name, full))
    return entries


def scrape_uwo():
    """
    All 163 program links are present on domcontentloaded — no tab interaction needed.
    Links match /admissions/programs/program.cfm?p=<number>.
    Uses non-headless to avoid bot detection on this server.
    """
    base = "https://grad.uwo.ca"
    url  = "https://grad.uwo.ca/admissions/programs/"
    entries = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
        for full, name in links:
            # normalise http → https
            full = full.replace("http://grad.uwo.ca", "https://grad.uwo.ca")
            parsed = urlparse(full)
            path_ok  = parsed.path == "/admissions/programs/program.cfm"
            query_ok = bool(re.match(r"^p=\d+$", parsed.query))
            if path_ok and query_ok and full not in seen:
                seen.add(full)
                if name:
                    entries.append(make_entry(name, full))

        browser.close()
    return entries


def scrape_memorial():
    """
    Scrapes the 4 graduate sub-pages on mun.ca using plain requests.
    Keeps links matching /become/graduate/programs-and-courses/<program>/
    excluding the category index slugs.
    """
    base = "https://www.mun.ca"
    subpages = [
        "/become/graduate/programs-and-courses/humanities-and-social-sciences/",
        "/become/graduate/programs-and-courses/interdisciplinary/",
        "/become/graduate/programs-and-courses/professional-programs/",
        "/become/graduate/programs-and-courses/sciences/",
    ]
    CATEGORY_SLUGS = {
        "humanities-and-social-sciences",
        "interdisciplinary",
        "professional-programs",
        "sciences",
        "programs-and-courses",
    }
    entries = []
    seen = set()

    for subpath in subpages:
        html = fetch(base + subpath)
        if not html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full = urljoin(base, href)
            path = urlparse(full).path.rstrip("/")
            match = re.match(r"^/become/graduate/programs-and-courses/([^/]+)$", path)
            if not match:
                continue
            slug = match.group(1)
            if slug in CATEGORY_SLUGS or full in seen:
                continue
            seen.add(full)
            name = a.get_text(" ", strip=True)
            if name:
                entries.append(make_entry(name, full))
        time.sleep(0.5)

    return entries


def scrape_unb():
    """
    Listing page is JS-rendered and returns nothing useful.
    Use the sitemap (static XML, not blocked) to extract URLs
    matching /gradstudies/programs/<program>.html
    Names derived from URL slugs since there is no anchor text.
    """
    import xml.etree.ElementTree as ET

    sitemap_url = "https://www.unb.ca/sitemap.xml"
    html = fetch(sitemap_url)
    if not html:
        return []

    entries = []
    seen = set()

    try:
        cleaned = re.sub(r' xmlns[^=]*="[^"]*"', "", html)
        root = ET.fromstring(cleaned)
        locs = [el.text.strip() for el in root.iter("loc") if el.text]
    except ET.ParseError:
        locs = re.findall(r"<loc>(.*?)</loc>", html)

    for full in locs:
        path = urlparse(full).path
        if re.match(r"^/gradstudies/programs/[^/]+\.html$", path) and full not in seen:
            seen.add(full)
            slug = path.split("/")[-1].replace(".html", "")
            name = slug.replace("-", " ").title()
            entries.append(make_entry(name, full))

    return entries


def scrape_manitoba():
    """
    Page renders via Atomic (web components / shadow DOM).
    eval_on_selector_all pierces shadow DOM and returns all links after
    networkidle + 5s. Keep URLs matching:
    /graduate-studies/admissions/programs-of-study/<slug>
    where slug contains at least one hyphen (excludes bare index pages).
    """
    base = "https://umanitoba.ca"
    url  = "https://umanitoba.ca/graduate-studies/admissions/programs-of-study"
    entries = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        time.sleep(5)
        # scroll to bottom to trigger any lazy-loaded results
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)

        links = page.eval_on_selector_all(
            "a[href]", "els => els.map(e => [e.href, e.innerText.trim()])"
        )
        browser.close()

    for full, name in links:
        path = urlparse(full).path.rstrip("/")
        if not re.match(r"^/graduate-studies/admissions/programs-of-study/.+$", path):
            continue
        if full in seen:
            continue
        seen.add(full)
        if name:
            entries.append(make_entry(name, full))

    return entries


def scrape_calgary():
    """
    Programs are paginated. Click the 'Show all' button to reveal all at once,
    then collect links matching:
    /future-students/graduate/discover-opportunities/explore-programs/<slug>
    """
    base = "https://grad.ucalgary.ca"
    url  = "https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs"
    entries = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        time.sleep(3)

        # click Show all
        show_all = page.query_selector("a.show-all-button")
        if show_all:
            show_all.click()
            time.sleep(3)

        links = page.eval_on_selector_all(
            "a[href]", "els => els.map(e => [e.href, e.innerText.trim()])"
        )
        browser.close()

    for full, name in links:
        path = urlparse(full).path.rstrip("/")
        if not re.match(r"^/future-students/graduate/discover-opportunities/explore-programs/.+$", path):
            continue
        if full in seen:
            continue
        seen.add(full)
        if name:
            entries.append(make_entry(name, full))

    return entries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

UNIVERSITIES = [
    ("McGill",    "mcgill",    scrape_mcgill),
    ("Concordia", "concordia", scrape_concordia),
    ("uAlberta",  "ualberta",  scrape_ualberta),
    ("USask",     "usask",     scrape_usask),
    ("uRegina",   "uregina",   scrape_uregina),
    ("UWO",       "uwo",       scrape_uwo),
    ("Memorial",  "memorial",  scrape_memorial),
    ("UNB",       "unb",       scrape_unb),
    ("Manitoba",  "umanitoba", scrape_manitoba),
    ("Calgary",   "ucalgary",  scrape_calgary),
]


def main():
    if len(sys.argv) != 2:
        print("Usage: python scrape_grad_programs.py output.json")
        sys.exit(1)

    output_path = sys.argv[1]
    all_results = []

    print(f"\n{'='*55}")
    for display_name, uni_id, scraper in UNIVERSITIES:
        print(f"  Scraping {display_name}...")
        entries = scraper()
        print(f"  → {len(entries)} programs found")
        all_results.append({
            "id": uni_id,
            "name": display_name,
            "programs": entries,
            "needs_manual_review": len(entries) == 0,
        })
        time.sleep(1)  # be polite

    total = sum(len(u["programs"]) for u in all_results)
    print(f"{'='*55}")
    print(f"  Total programs scraped: {total}")
    print(f"{'='*55}\n")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
