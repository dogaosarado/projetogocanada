import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"})

# UNB: try sitemap
print("=== UNB: sitemap ===")
for url in [
    "https://www.unb.ca/sitemap.xml",
    "https://www.unb.ca/gradstudies/sitemap.xml",
    "https://www.unb.ca/robots.txt",
]:
    r = SESSION.get(url, timeout=20)
    print(f"\n{url} → {r.status_code}")
    print(r.text[:800])

# Memorial: scrape the 4 sub-pages
print("\n\n=== Memorial: sub-pages ===")
base = "https://www.mun.ca"
subpages = [
    "/become/graduate/programs-and-courses/humanities-and-social-sciences/",
    "/become/graduate/programs-and-courses/interdisciplinary/",
    "/become/graduate/programs-and-courses/professional-programs/",
    "/become/graduate/programs-and-courses/sciences/",
]
for path in subpages:
    url = base + path
    r = SESSION.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [(a.get_text(strip=True), a["href"]) for a in soup.find_all("a", href=True)
             if "programs-and-courses" in a["href"] and a.get_text(strip=True)]
    print(f"\n{path} → {r.status_code} | {len(links)} program links")
    for text, href in links[:10]:
        print(f"  {text[:50]:<50} {href}")
