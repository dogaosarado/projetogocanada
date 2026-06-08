from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(
        "https://www.ualberta.ca/en/graduate-programs/index.html",
        wait_until="networkidle",
        timeout=60000,
    )
    time.sleep(5)

    # look for pagination / show more elements
    pager_classes = page.eval_on_selector_all(
        "[class]",
        "els => [...new Set(els.flatMap(e => [...e.classList]))].filter(c => /pager|next|more|page|load/i.test(c))"
    )
    print("Pagination-related classes:")
    for c in pager_classes:
        print(" ", c)

    # look for a total results count
    summary = page.query_selector(".coveo-summary-section, .CoveoQuerySummary, [class*='summary']")
    if summary:
        print(f"\nSummary text: {summary.inner_text()}")

    # check if there's a "load more" or pager button
    for selector in [".coveo-pager-next", ".CoveoPager", "[class*='pager']", "button[class*='next']"]:
        el = page.query_selector(selector)
        if el:
            print(f"\nFound pager element '{selector}': {el.inner_text()[:80]}")

    # how many result items are currently rendered
    results = page.query_selector_all(".CoveoResult, [class*='coveo-result']")
    print(f"\nCurrently rendered result items: {len(results)}")

    input("Press Enter to close...")
    browser.close()
