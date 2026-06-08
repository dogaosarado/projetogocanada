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

    # dump the full pager HTML
    pager = page.query_selector(".CoveoPager")
    if pager:
        print("Pager HTML:")
        print(pager.inner_html())

    # dump all buttons on the page
    buttons = page.query_selector_all("button, a[class*='pager'], li[class*='pager']")
    print(f"\nAll buttons/pager elements: {len(buttons)}")
    for b in buttons:
        txt = b.inner_text().strip()
        cls = b.get_attribute("class") or ""
        if txt or "pager" in cls.lower():
            print(f"  [{b.tag_name()}] class='{cls[:60]}' text='{txt[:40]}'")

    # dump the summary section fully
    for sel in [".CoveoQuerySummary", "[class*='QuerySummary']", "[class*='summary']"]:
        el = page.query_selector(sel)
        if el:
            print(f"\n{sel} HTML: {el.inner_html()[:300]}")

    input("Press Enter to close...")
    browser.close()
