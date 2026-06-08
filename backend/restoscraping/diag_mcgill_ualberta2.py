from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import re, time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    )

    # --- McGill ---
    print("=== McGill ===")
    page = context.new_page()
    page.goto("https://www.mcgill.ca/gradapplicants/programs", wait_until="networkidle", timeout=30000)
    time.sleep(2)
    print(f"Final URL: {page.url}")
    print(f"Title: {page.title()}")

    links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
    print(f"Total links: {len(links)}")
    print("First 30 links:")
    for href, text in links[:30]:
        print(f"  {text[:45]:<45} {href[:80]}")
    page.close()

    # --- uAlberta ---
    print("\n=== uAlberta ===")
    page = context.new_page()
    page.goto("https://www.ualberta.ca/en/graduate-programs/index.html", wait_until="networkidle", timeout=60000)
    time.sleep(5)
    print(f"Final URL: {page.url}")
    links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
    grad = [(h, t) for h, t in links if re.match(r".*/en/graduate-programs/[^/]+\.html$", h)]
    print(f"Graduate program links found: {len(grad)}")
    for href, text in grad[:10]:
        print(f"  {text[:50]:<50} {href}")
    page.close()

    input("\nPress Enter to close...")
    browser.close()
