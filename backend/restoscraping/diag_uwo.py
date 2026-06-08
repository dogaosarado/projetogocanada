from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
    )
    page = context.new_page()

    print("Navigating to UWO...")
    try:
        page.goto(
            "https://grad.uwo.ca/admissions/programs/",
            wait_until="domcontentloaded",
            timeout=30000,
        )
    except Exception as e:
        print(f"Navigation error: {e}")

    time.sleep(5)

    html = page.content()
    print(f"HTML length: {len(html)}")

    # check for MASTERS/DOCTORAL elements
    for sel in ["#MASTERS", "#DOCTORAL", "[id*='MASTER']", "[id*='master']", "a[href*='program.cfm']"]:
        el = page.query_selector(sel)
        print(f"  {sel}: {'FOUND' if el else 'not found'}")

    links = page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
    prog_links = [l for l in links if "program.cfm" in l]
    print(f"\nprogram.cfm links: {len(prog_links)}")
    for l in prog_links[:10]:
        print(" ", l)

    input("Press Enter to close...")
    browser.close()
