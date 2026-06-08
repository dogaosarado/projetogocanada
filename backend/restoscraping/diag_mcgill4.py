from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time, re

FACULTY_IDS = [14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 30, 31]
BASE = "https://www.mcgill.ca"

def get_html(context, url, retries=2):
    """Navigate and return page HTML, retrying if context is destroyed."""
    for attempt in range(retries + 1):
        page = context.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
            time.sleep(2)
            html = page.content()
            page.close()
            return html
        except Exception as e:
            page.close()
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return ""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    )

    all_program_links = set()

    for fid in FACULTY_IDS:
        url = f"{BASE}/gradapplicants/programs?f%5B0%5D=field_faculty_interest%3A{fid}"
        print(f"\nFaculty {fid}: {url}")
        html = get_html(context, url)
        if not html:
            print("  No HTML retrieved")
            continue

        soup = BeautifulSoup(html, "html.parser")
        links = [(a["href"], a.get_text(strip=True)) for a in soup.find_all("a", href=True)]
        prog = [(h, t) for h, t in links if "/gradapplicants/program/" in h and t]
        print(f"  Found {len(prog)} program links")
        for h, t in prog[:5]:
            full = BASE + h if h.startswith("/") else h
            all_program_links.add((full, t))
            print(f"    {t[:50]:<50} {h}")
        time.sleep(1)

    print(f"\n\nTotal unique program links: {len(all_program_links)}")
    for h, t in sorted(all_program_links)[:20]:
        print(f"  {t[:50]:<50} {h}")

    input("\nPress Enter to close...")
    browser.close()
