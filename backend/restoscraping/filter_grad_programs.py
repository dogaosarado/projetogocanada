"""
filter_grad_programs.py

Usage:
    python filter_grad_programs.py input.json output.json

Structure expected:
    [
      { "id": "ubc", "name": "...", "programs": [ { "url": "...", ... }, ... ] },
      ...
    ]
"""

import json
import sys
import re
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Filter rules — return True to KEEP the program entry
# ---------------------------------------------------------------------------

def filter_uottawa(url):
    return "/en/graduate" in url

def filter_mcgill(url):
    return "gradapplicants/program" in url

def filter_concordia(url):
    path = urlparse(url).path.rstrip("/")
    return bool(re.search(r"/academics/graduate/[^/]+$", path))

def filter_ualberta(url):
    path = urlparse(url).path
    return bool(re.match(r"^/en/graduate-programs/[^/]+\.html$", path))

def filter_usask(url):
    path = urlparse(url).path
    excluded = {"find-a-program", "find-a-supervisor"}
    match = re.match(r"^/programs/([^/]+)\.php$", path)
    if not match:
        return False
    return match.group(1) not in excluded

def filter_uregina(url):
    path = urlparse(url).path.rstrip("/")
    return bool(re.match(r"^/academics/programs/[^/]+/.+$", path))

def filter_uwo(url):
    parsed = urlparse(url)
    path_ok = parsed.path == "/admissions/programs/program.cfm"
    query_ok = bool(re.match(r"^p=\d+$", parsed.query))
    return path_ok and query_ok

def filter_memorial(url):
    path = urlparse(url).path.rstrip("/")
    return bool(re.match(r"^/become/graduate/programs-and-courses/[^/]+$", path))

def filter_unb(url):
    path = urlparse(url).path
    return bool(re.match(r"^/gradstudies/programs/[^/]+\.html$", path))


# university id → filter function
FILTERS = {
    "uottawa":  filter_uottawa,
    "mcgill":   filter_mcgill,
    "concordia": filter_concordia,
    "ualberta": filter_ualberta,
    "usask":    filter_usask,
    "uregina":  filter_uregina,
    "uwo":      filter_uwo,
    "memorial": filter_memorial,
    "unb":      filter_unb,
}

# also match by domain fragment as fallback (id field may differ)
DOMAIN_FALLBACK = [
    ("uottawa.ca",   filter_uottawa),
    ("mcgill.ca",    filter_mcgill),
    ("concordia.ca", filter_concordia),
    ("ualberta.ca",  filter_ualberta),
    ("usask.ca",     filter_usask),
    ("uregina.ca",   filter_uregina),
    ("uwo.ca",       filter_uwo),
    ("mun.ca",       filter_memorial),
    ("unb.ca",       filter_unb),
]

def get_filter(uni_id, url):
    # try id first
    if uni_id in FILTERS:
        return uni_id, FILTERS[uni_id]
    # fallback to domain
    for domain, fn in DOMAIN_FALLBACK:
        if domain in url:
            return domain, fn
    return None, None


def main():
    if len(sys.argv) != 3:
        print("Usage: python filter_grad_programs.py input.json output.json")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("Error: expected a top-level JSON array.")
        sys.exit(1)

    stats = {}
    result = []

    for uni in data:
        uni_id = uni.get("id", "").lower()
        programs = uni.get("programs", [])
        kept = []

        uni_kept = 0
        uni_removed = 0

        for program in programs:
            url = program.get("url", "")
            key, fn = get_filter(uni_id, url)

            if fn is None:
                kept.append(program)
                uni_kept += 1
            elif fn(url):
                kept.append(program)
                uni_kept += 1
            else:
                uni_removed += 1

        stats[uni.get("name", uni_id)] = {"kept": uni_kept, "removed": uni_removed}
        result.append({**uni, "programs": kept})

    # print stats
    print(f"\n{'='*60}")
    print(f"  {'University':<35} {'Kept':>6} {'Removed':>8}")
    print(f"  {'-'*51}")
    total_kept = total_removed = 0
    for name, s in stats.items():
        print(f"  {name:<35} {s['kept']:>6} {s['removed']:>8}")
        total_kept += s['kept']
        total_removed += s['removed']
    print(f"  {'-'*51}")
    print(f"  {'TOTAL':<35} {total_kept:>6} {total_removed:>8}")
    print(f"{'='*60}\n")

    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Written to: {sys.argv[2]}")


if __name__ == "__main__":
    main()
