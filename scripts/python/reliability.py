"""
reliability.py
Krippendorff's alpha (nominal) for two coders, one code at a time.

Thresholds from the coding framework:
    speech act (Primary act)  alpha >= .80
    everything else           alpha >= .70

Usage:
    python reliability.py coderA.csv coderB.csv
Both CSVs: one row per speech act, a 'Speech act ID' column, and one column
per code (the Coding tab exported as CSV). Only IDs in both files are compared.
"""

import csv
import sys
from collections import Counter
from itertools import permutations

CODES = ["Clause type", "Primary act", "Directness", "Presup Y/N", "Trigger type",
         "Presup direction", "Leading construction", "Evaluative Y/N", "Polarity",
         "Target", "Stance disclosure Y/N", "Disclosure direction",
         "Relation to prev model turn"]


def alpha_nominal(pairs):
    """pairs: list of (a, b) values for units both coders coded."""
    units = [(a, b) for a, b in pairs if a not in ("", None) and b not in ("", None)]
    if not units:
        return None
    o = Counter()  # coincidence matrix
    for a, b in units:
        for x, y in permutations([a, b], 2):
            o[(x, y)] += 1
    n_c = Counter()
    for (x, _), v in o.items():
        n_c[x] += v
    n = sum(n_c.values())
    d_o = sum(v for (x, y), v in o.items() if x != y)
    d_e = sum(n_c[x] * n_c[y] for x in n_c for y in n_c if x != y) / (n - 1)
    return 1.0 if d_e == 0 else 1 - d_o / d_e


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {r["Speech act ID"]: r for r in csv.DictReader(f) if r.get("Speech act ID")}


def main(a_path, b_path):
    a, b = load(a_path), load(b_path)
    shared = sorted(set(a) & set(b))
    print(f"{len(shared)} shared speech acts\n")
    print(f"{'Code':32} {'alpha':>7}  target  pass")
    for code in CODES:
        if code not in next(iter(a.values()), {}):
            continue
        al = alpha_nominal([(a[i][code].strip().lower(), b[i][code].strip().lower()) for i in shared])
        target = 0.80 if code == "Primary act" else 0.70
        if al is None:
            print(f"{code:32} {'n/a':>7}")
        else:
            print(f"{code:32} {al:7.3f}  {target:.2f}    {'yes' if al >= target else 'NO'}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python reliability.py coderA.csv coderB.csv")
    main(*sys.argv[1:])
