from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # opens a visible window
    page = browser.new_page()

    print("Navigating...")
    try:
        page.goto(
            "https://www.ualberta.ca/en/graduate-programs/index.html",
            wait_until="domcontentloaded",
            timeout=30000,
        )
    except Exception as e:
        print(f"Navigation error: {e}")

    time.sleep(5)  # watch the browser window

    html = page.content()
    print(f"Page HTML length: {len(html)}")
    print("First 500 chars:")
    print(html[:500])

    links = page.eval_on_selector_all("a", "els => els.map(e => e.outerHTML)")
    print(f"\nTotal <a> tags: {len(links)}")
    for l in links[:10]:
        print(" ", l[:120])

    input("Press Enter to close browser...")
    browser.close()
