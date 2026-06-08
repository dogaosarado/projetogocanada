"""
cleanup_grad_programs.py

Applies targeted cleanup rules to a graduate programs JSON file.

Rules:
  - uOttawa: remove entries with "undergraduate" in name or URL (case-insensitive).
             Fix garbled names by taking only the first segment before repetition.
  - Manitoba, Dalhousie, Concordia: remove parenthetical degree suffix from name
             when degree_type is already known (not "Unknown").
  - McGill: extract degree type from parenthetical in name, set degree_type if
             it maps to a known type, then remove the parenthetical from name.

Usage:
    python cleanup_grad_programs.py input.json output.json
"""

import json
import re
import sys


# ---------------------------------------------------------------------------
# Degree type normalisation map (McGill uses abbreviations in parentheses)
# ---------------------------------------------------------------------------

DEGREE_MAP = {
    # PhD variants
    "phd": "PhD", "ph.d": "PhD", "ph.d.": "PhD",
    "d.c.l.": "PhD", "dcl": "PhD",
    "d.mus.": "PhD", "dmus": "PhD",
    "ed.d.": "PhD", "edd": "PhD",
    # Master variants
    "m.sc.": "MSc", "msc": "MSc", "m.sc.a.": "MSc", "msca": "MSc",
    "m.a.": "MA", "ma": "MA",
    "m.ed.": "MEd", "med": "MEd",
    "m.eng.": "MEng", "meng": "MEng",
    "m.asc.": "MASc", "masc": "MASc",
    "m.f.a.": "MFA", "mfa": "MFA",
    "m.b.a.": "MBA", "mba": "MBA",
    "emba": "MBA",
    "m.m.a.": "MBA", "mma": "MBA",
    "m.m.f.": "Master", "mmf": "Master",
    "m.m.r.": "Master", "mmr": "Master",
    "m.m.": "Master", "mm": "Master",
    "m.mus.": "Master", "mmus": "Master",
    "m.u.p.": "Master", "mup": "Master",
    "m.sw.": "MSW", "msw": "MSW",
    "ll.m.": "LLM", "llm": "LLM",
    "m.p.h.": "MPH", "mph": "MPH",
    "i.m.h.l.": "Master",
    "m.sc.a": "MSc",
    # Certificate / Diploma
    "grad. cert.": "Certificate", "grad.cert.": "Certificate",
    "grad. dip.": "Certificate", "grad.dip.": "Certificate",
    "post-grad. art. dip.": "Certificate",
    "graduate certificate": "Certificate",
    "graduate diploma": "Certificate",
}


def normalise_degree(raw: str) -> str | None:
    """Map a raw parenthetical string to a known degree_type, or None."""
    key = raw.strip().lower().rstrip(".")
    if key in DEGREE_MAP:
        return DEGREE_MAP[key]
    # try stripping trailing period variants
    key2 = key.replace(".", "").strip()
    return DEGREE_MAP.get(key2)


# ---------------------------------------------------------------------------
# uOttawa helpers
# ---------------------------------------------------------------------------

REPEAT_MARKERS = [
    "graduate studies", "master's", "doctoral", "undergraduate",
    "faculty of", "department of", "school of", "uottawa",
    "university of ottawa",
]

def fix_uottawa_name(name: str) -> str:
    """
    The real program name is the first segment before the text starts
    repeating navigational / faculty boilerplate.
    Strategy: find the earliest position where a repeat marker appears
    and truncate there.
    """
    lower = name.lower()
    cut = len(name)
    for marker in REPEAT_MARKERS:
        idx = lower.find(marker)
        if idx > 10:  # ignore if at the very start
            cut = min(cut, idx)
    return name[:cut].strip()


# ---------------------------------------------------------------------------
# Parenthetical cleanup helpers
# ---------------------------------------------------------------------------

# matches a trailing parenthetical: anything in () at end of string
PAREN_RE = re.compile(r"\s*\(([^)]+)\)\s*$")


def strip_paren_if_degree(name: str, degree_type: str) -> str:
    """Remove trailing parenthetical from name if degree_type is known."""
    if degree_type == "Unknown":
        return name
    return PAREN_RE.sub("", name).strip()


def extract_mcgill_degree(name: str):
    """
    For McGill entries: extract the parenthetical at the end of the name,
    try to map it to a degree_type. Returns (clean_name, degree_type_or_None).
    If no valid mapping, returns (original_name, None).
    """
    match = PAREN_RE.search(name)
    if not match:
        return name, None
    raw = match.group(1)
    dtype = normalise_degree(raw)
    if dtype is None:
        return name, None
    clean_name = name[:match.start()].strip()
    return clean_name, dtype


# ---------------------------------------------------------------------------
# Per-university processors
# ---------------------------------------------------------------------------

def process_uottawa(programs: list) -> list:
    cleaned = []
    for p in programs:
        name = p.get("name", "")
        url  = p.get("url", "")
        # drop undergraduate entries
        if "undergraduate" in name.lower() or "undergraduate" in url.lower():
            continue
        # drop MD (undergraduate medical) entries
        if re.search(r'\bMD\b', name) and p.get("degree_type") in ("MD", "Unknown"):
            # only drop if it looks like an undergrad MD
            if "undergraduate" in name.lower() or "doctor of medicine" not in name.lower():
                pass  # let it through if it's a legit grad MD
        # fix garbled name
        fixed_name = fix_uottawa_name(name)
        cleaned.append({**p, "name": fixed_name})
    return cleaned


def process_strip_paren(programs: list) -> list:
    """For Manitoba, Dalhousie, Concordia: strip trailing degree parenthetical."""
    return [
        {**p, "name": strip_paren_if_degree(p.get("name", ""), p.get("degree_type", "Unknown"))}
        for p in programs
    ]


def process_mcgill(programs: list) -> list:
    result = []
    for p in programs:
        name = p.get("name", "")
        dtype = p.get("degree_type", "Unknown")
        if dtype == "Unknown":
            clean_name, extracted = extract_mcgill_degree(name)
            if extracted:
                result.append({**p, "name": clean_name, "degree_type": extracted})
            else:
                result.append(p)
        else:
            result.append(p)
    return result


# ---------------------------------------------------------------------------
# University id → processor
# ---------------------------------------------------------------------------

PROCESSORS = {
    "uottawa":   process_uottawa,
    "mcgill":    process_mcgill,
    "umanitoba": process_strip_paren,
    "dalhousie": process_strip_paren,
    "concordia": process_strip_paren,
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print("Usage: python cleanup_grad_programs.py input.json output.json")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)

    result = []
    stats = {}

    for uni in data:
        uid = uni.get("id", "")
        programs = uni.get("programs", [])
        processor = PROCESSORS.get(uid)

        if processor:
            cleaned = processor(programs)
            stats[uid] = {"before": len(programs), "after": len(cleaned)}
            result.append({**uni, "programs": cleaned})
        else:
            result.append(uni)

    # print stats
    print(f"\n{'='*50}")
    print(f"  {'University':<20} {'Before':>8} {'After':>8} {'Removed':>8}")
    print(f"  {'-'*44}")
    for uid, s in stats.items():
        removed = s['before'] - s['after']
        print(f"  {uid:<20} {s['before']:>8} {s['after']:>8} {removed:>8}")
    print(f"{'='*50}\n")

    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Written to: {sys.argv[2]}")


if __name__ == "__main__":
    main()
