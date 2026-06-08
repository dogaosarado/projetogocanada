"""
count_programs.py

Usage:
    python count_programs.py input.json
"""

import json
import sys

with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)

total = 0
print(f"\n{'='*45}")
print(f"  {'University':<30} {'Programs':>8}")
print(f"  {'-'*38}")
for uni in data:
    count = len(uni.get("programs", []))
    total += count
    print(f"  {uni.get('name', uni['id'])[:30]:<30} {count:>8}")
print(f"  {'-'*38}")
print(f"  {'TOTAL':<30} {total:>8}")
print(f"{'='*45}\n")
