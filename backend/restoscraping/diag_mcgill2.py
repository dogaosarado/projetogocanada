from playwright.sync_api import sync_playwright
import time, re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    )
    page = context.new_page()
    page.goto("https://www.mcgill.ca/gradapplicants/programs", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    print(f"Final URL: {page.url}")
    print(f"Title: {page.title()}")

    links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
    grad = [(h, t) for h, t in links if "gradapplicants/program" in h]
    print(f"\ngradapplicants/program links: {len(grad)}")
    for h, t in grad:
        print(f"  {t[:50]:<50} {h}")

    # look for pagination
    pagers = page.query_selector_all("[class*='pager'], [class*='page'], [class*='next'], nav")
    print(f"\nPager-ish elements: {len(pagers)}")
    for el in pagers[:5]:
        print(f"  {el.inner_text()[:80]}")

    # total results indicator
    for sel in ["[class*='summary']", "[class*='result-count']", "[class*='total']"]:
        el = page.query_selector(sel)
        if el:
            print(f"\n{sel}: {el.inner_text()[:100]}")

    input("\nPress Enter to close...")
    browser.close()
