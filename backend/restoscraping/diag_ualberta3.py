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

    # dump all class names that contain 'coveo' or 'result'
    classes = page.eval_on_selector_all(
        "[class]",
        "els => [...new Set(els.flatMap(e => [...e.classList]))].filter(c => /coveo|result|program/i.test(c))"
    )
    print("Relevant CSS classes found:")
    for c in classes[:40]:
        print(" ", c)

    # dump any links that appeared after JS ran
    links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
    grad = [l for l in links if "graduate-program" in l]
    print(f"\nGrad program links: {len(grad)}")
    for l in grad[:10]:
        print(" ", l)

    # dump innerHTML of the main content area
    main = page.query_selector("#main")
    if main:
        html = main.inner_html()
        print(f"\n#main innerHTML length: {len(html)}")
        print(html[:1000])

    input("Press Enter to close...")
    browser.close()
