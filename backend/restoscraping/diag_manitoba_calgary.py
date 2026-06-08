from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time, re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    )

    # --- Manitoba ---
    print("=== Manitoba ===")
    page = context.new_page()
    page.goto("https://umanitoba.ca/graduate-studies/admissions/programs-of-study", wait_until="networkidle", timeout=60000)
    time.sleep(5)
    print(f"Title: {page.title()}")

    # try to get links from results-wrapper
    container = page.query_selector("#results-wrapper")
    if container:
        print(f"#results-wrapper found")
        html = container.inner_html()
        soup = BeautifulSoup(html, "html.parser")
        links = [(a["href"], a.get_text(strip=True)) for a in soup.find_all("a", href=True) if a.get_text(strip=True)]
        print(f"Links inside container: {len(links)}")
        for href, text in links[:10]:
            print(f"  {text[:50]:<50} {href}")
    else:
        print("#results-wrapper NOT found")
        # try atomic-result elements
        results = page.query_selector_all("atomic-result")
        print(f"atomic-result elements: {len(results)}")
        if results:
            print("First result HTML snippet:")
            print(results[0].inner_html()[:500])

    # count total visible program links matching the pattern
    all_links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
    prog = [(h, t) for h, t in all_links if "programs-of-study/" in h and t]
    print(f"\nProgram links matching 'programs-of-study/': {len(prog)}")
    for h, t in prog[:5]:
        print(f"  {t[:50]:<50} {h}")
    page.close()

    # --- Calgary ---
    print("\n\n=== Calgary ===")
    page = context.new_page()
    page.goto("https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs", wait_until="networkidle", timeout=60000)
    time.sleep(5)
    print(f"Title: {page.title()}")

    # check for show all button
    for sel in ["button", "[class*='show-all']", "[class*='show_all']", "a[class*='all']"]:
        els = page.query_selector_all(sel)
        for el in els:
            txt = el.inner_text().strip().lower()
            if "all" in txt or "show" in txt:
                print(f"Possible 'show all' button: '{el.inner_text().strip()[:60]}' [{sel}]")

    # check pagination xpath
    nav = page.query_selector("xpath=/html/body/main/div[5]/div/div/div[1]/div/div/div[2]/div/div/div/div[6]/div[2]/nav")
    if nav:
        print(f"\nPagination nav found: {nav.inner_text()[:200]}")
    else:
        print("\nPagination nav NOT found at that xpath")

    # count program links
    all_links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
    prog = [(h, t) for h, t in all_links if "explore-programs/" in h and t]
    print(f"\nProgram links matching 'explore-programs/': {len(prog)}")
    for h, t in prog[:10]:
        print(f"  {t[:50]:<50} {h}")
    page.close()

    input("\nPress Enter to close...")
    browser.close()
