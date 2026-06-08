from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import re, time

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
    links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
    prog = [(h, t) for h, t in links if "graduate-studies/admissions/programs-of-study/" in h]
    print(f"Total matching links: {len(prog)}")
    # show ones being excluded (no hyphen in slug)
    excluded = [(h, t) for h, t in prog if "-" not in urlparse(h).path.rstrip("/").split("/")[-1]]
    kept = [(h, t) for h, t in prog if "-" in urlparse(h).path.rstrip("/").split("/")[-1]]
    print(f"Kept (slug has hyphen): {len(kept)}")
    print(f"Excluded (no hyphen): {len(excluded)}")
    print("Excluded sample:")
    for h, t in excluded[:10]:
        print(f"  {t[:50]:<50} {h}")
    print("Kept sample:")
    for h, t in kept[:5]:
        print(f"  {t[:50]:<50} {h}")
    page.close()

    # --- Calgary ---
    print("\n=== Calgary ===")
    page = context.new_page()
    page.goto("https://grad.ucalgary.ca/future-students/graduate/discover-opportunities/explore-programs", wait_until="networkidle", timeout=60000)
    time.sleep(3)

    # find show all
    for sel in ["[class*='show-all']", "a[class*='all']", "button"]:
        els = page.query_selector_all(sel)
        for el in els:
            txt = el.inner_text().strip()
            if "all" in txt.lower() or "show" in txt.lower():
                cls = el.get_attribute("class") or ""
                tag = el.evaluate("e => e.tagName")
                print(f"Show-all candidate: <{tag}> class='{cls[:60]}' text='{txt}'")

    # count before click
    links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
    prog = [(h, t) for h, t in links if "explore-programs/" in h and t]
    print(f"Before click: {len(prog)} program links")

    # click show all
    show_all = page.query_selector("[class*='show-all']")
    if show_all:
        show_all.click()
        print("Clicked show-all, waiting...")
        time.sleep(5)
        links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
        prog = [(h, t) for h, t in links if "explore-programs/" in h and t]
        print(f"After click: {len(prog)} program links")
        for h, t in prog[:10]:
            print(f"  {t[:50]:<50} {h}")
    page.close()

    input("\nPress Enter to close...")
    browser.close()
