from playwright.sync_api import sync_playwright
import time

FACULTY_IDS = [14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 30, 31]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    )

    for fid in FACULTY_IDS[:3]:  # just first 3 to see the pattern
        url = f"https://www.mcgill.ca/gradapplicants/programs?f%5B0%5D=field_faculty_interest%3A{fid}"
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        links = page.eval_on_selector_all("a[href]", "els => els.map(e => [e.href, e.innerText.trim()])")
        prog = [(h, t) for h, t in links if "gradapplicants/program/" in h and t]
        print(f"\nFaculty {fid}: {len(prog)} program links")
        for h, t in prog[:10]:
            print(f"  {t[:50]:<50} {h}")
        page.close()

    input("\nPress Enter to close...")
    browser.close()
