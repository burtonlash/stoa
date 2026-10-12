#!/usr/bin/env python3
"""Coverage test: for each question, run its searches and report how many passages
each author/work offers, plus the top locations. Usage: python3 tests/run_coverage.py [id]"""
import json, subprocess, sys, re
from pathlib import Path
root = Path(__file__).resolve().parent.parent
cases = json.loads((root/"tests"/"reddit_questions.json").read_text())
only = sys.argv[1] if len(sys.argv) > 1 else None
for c in cases:
    if only and c["id"] != only: continue
    print(f"\n### {c['id']}: {c['q']}")
    for terms in c["searches"]:
        out = subprocess.run([sys.executable, str(root/"scripts"/"find_passage.py"), *terms, "--max", "999"],
                             capture_output=True, text=True).stdout
        heads = [l for l in out.splitlines() if l.startswith("--- ")]
        works = {}
        for h in heads:
            w = h.split(" | ")[1].replace(".txt","")
            works[w] = works.get(w, 0) + 1
        print(f"  search {terms}: {len(heads)} passages  " + ", ".join(f"{k}:{v}" for k,v in sorted(works.items())))
        for h in heads[:3]:
            print("     " + h[4:][:140])
