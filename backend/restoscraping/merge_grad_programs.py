"""
merge_grad_programs.py

Merges two JSON files of university graduate program data.
Universities present in the PATCH file overwrite their counterpart
in the BASE file (matched by 'id'). Universities only in the BASE
file are kept as-is.

Usage:
    python merge_grad_programs.py base.json patch.json output.json
"""

import json
import sys


def main():
    if len(sys.argv) != 4:
        print("Usage: python merge_grad_programs.py base.json patch.json output.json")
        sys.exit(1)

    base_path, patch_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(base_path, encoding="utf-8") as f:
        base = json.load(f)

    with open(patch_path, encoding="utf-8") as f:
        patch = json.load(f)

    # index patch by university id
    patch_by_id = {uni["id"]: uni for uni in patch}

    result = []
    replaced = []
    kept = []

    for uni in base:
        uid = uni["id"]
        if uid in patch_by_id:
            merged = {**uni, "programs": patch_by_id[uid]["programs"]}
            result.append(merged)
            replaced.append(uid)
        else:
            result.append(uni)
            kept.append(uid)

    # universities in patch but not in base — append them
    base_ids = {uni["id"] for uni in base}
    added = []
    for uni in patch:
        if uni["id"] not in base_ids:
            result.append(uni)
            added.append(uni["id"])

    # stats
    print(f"\n{'='*55}")
    print(f"  Base universities      : {len(base)}")
    print(f"  Patch universities     : {len(patch)}")
    print(f"  Replaced by patch      : {len(replaced)} — {replaced}")
    print(f"  Added from patch       : {len(added)}   — {added}")
    print(f"  Kept from base         : {len(kept)}")
    print(f"  Total in output        : {len(result)}")

    total_programs = sum(len(u.get("programs", [])) for u in result)
    print(f"  Total programs         : {total_programs}")
    print(f"{'='*55}\n")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
