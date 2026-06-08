from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

FACULTY_IDS = [14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 30, 31]
BASE = "https://www.mcgill.ca"

def collect_program_links(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if "/gradapplicants/program/" in href and text:
            full = BASE + href if href.startswith("/") else href
            results.append((full, text))
    return results

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    )
    page = context.new_page()

    # single navigation — stay on this page forever
    page.goto("https://www.mcgill.ca/gradapplicants/programs", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    print(f"Loaded: {page.url}")
    print(f"Title: {page.title()}")

    all_links = set()

    # collect programs visible on initial load
    html = page.content()
    initial = collect_program_links(html)
    print(f"\nInitial load: {len(initial)} program links")
    for h, t in initial:
        all_links.add((h, t))

    # now click each faculty filter link (staying on same page)
    for fid in FACULTY_IDS:
        selector = f"a[href*='field_faculty_interest%3A{fid}']"
        link = page.query_selector(selector)
        if not link:
            print(f"\nFaculty {fid}: filter link not found")
            continue

        label = link.inner_text().strip()
        print(f"\nFaculty {fid} ({label}): clicking...")
        link.click()
        time.sleep(3)  # wait for AJAX to reload the list

        html = page.content()
        found = collect_program_links(html)
        print(f"  Found {len(found)} program links")
        for h, t in found[:5]:
            print(f"    {t[:50]:<50} {h}")
        for item in found:
            all_links.add(item)

        # go back to full list for next click
        back = page.query_selector("a[href='/gradapplicants/programs']")
        if back:
            back.click()
            time.sleep(2)

    print(f"\n\nTotal unique program links: {len(all_links)}")
    for h, t in sorted(all_links):
        print(f"  {t[:50]:<50} {h}")

    input("\nPress Enter to close...")
    browser.close()
