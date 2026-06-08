import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"})

for name, url in [
    ("uRegina", "https://www.uregina.ca/academics/programs/"),
    ("Memorial", "https://www.mun.ca/become/graduate/programs-and-courses/"),
    ("UNB", "https://www.unb.ca/gradstudies/programs/"),
]:
    r = SESSION.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [(a.get_text(strip=True), a["href"]) for a in soup.find_all("a", href=True) if a.get_text(strip=True)]
    print(f"\n=== {name}: {r.status_code} | {len(links)} links ===")
    for text, href in links[:20]:
        print(f"  {text[:50]:<50} {href}")
