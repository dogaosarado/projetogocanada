import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36"})

# uRegina: show ALL links containing 'academics/programs'
print("\n=== uRegina: links containing 'academics/programs' ===")
r = SESSION.get("https://www.uregina.ca/academics/programs/", timeout=20)
soup = BeautifulSoup(r.text, "html.parser")
links = [(a.get_text(strip=True), a["href"]) for a in soup.find_all("a", href=True) if "academics/programs" in a["href"]]
print(f"Total: {len(links)}")
for text, href in links[:40]:
    print(f"  {text[:50]:<50} {href}")

# Memorial: try the actual grad programs index
print("\n=== Memorial: trying /graduate/programs-and-courses/ ===")
for url in [
    "https://www.mun.ca/become/graduate/programs-and-courses/",
    "https://www.mun.ca/sgs/programs/",
    "https://www.mun.ca/graduate/programs/",
]:
    r = SESSION.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [(a.get_text(strip=True), a["href"]) for a in soup.find_all("a", href=True) if a.get_text(strip=True)]
    prog_links = [x for x in links if "program" in x[1].lower() or "graduate" in x[1].lower()]
    print(f"\n  {url} → {r.status_code} | {len(links)} total links | {len(prog_links)} program-ish links")
    for text, href in prog_links[:10]:
        print(f"    {text[:50]:<50} {href}")

# UNB: try alternate URLs
print("\n=== UNB: trying alternate URLs ===")
for url in [
    "https://www.unb.ca/gradstudies/programs/",
    "https://www.unb.ca/gradstudies/programs/index.html",
    "https://www.unb.ca/gradstudies/",
]:
    r = SESSION.get(url, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    links = [(a.get_text(strip=True), a["href"]) for a in soup.find_all("a", href=True) if a.get_text(strip=True)]
    prog_links = [x for x in links if "program" in x[1].lower() or "gradstud" in x[1].lower()]
    print(f"\n  {url} → {r.status_code} | {len(links)} total links | {len(prog_links)} program-ish links")
    for text, href in prog_links[:10]:
        print(f"    {text[:50]:<50} {href}")
