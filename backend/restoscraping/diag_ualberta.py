from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(
        "https://www.ualberta.ca/en/graduate-programs/index.html#sort=%40ua__grad_sub%20ascending",
        wait_until="networkidle",
        timeout=60000,
    )
    time.sleep(3)  # extra wait for Coveo

    # print all unique hrefs containing 'graduate'
    links = page.eval_on_selector_all(
        "a[href]",
        "els => els.map(e => e.href)"
    )
    grad_links = [l for l in links if "graduate" in l.lower()]
    print(f"Total links: {len(links)}, grad-related: {len(grad_links)}")
    for l in grad_links[:20]:
        print(" ", l)

    # also dump a snippet of the page source around program content
    html = page.content()
    idx = html.lower().find("graduate-programs")
    if idx > 0:
        print("\n--- HTML snippet around 'graduate-programs' ---")
        print(html[max(0,idx-200):idx+500])

    browser.close()
