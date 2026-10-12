#!/usr/bin/env python3
"""Package Stoa as stoa.zip for uploading to the Claude app (Customize > Skills).

Usage:  python3 scripts/package_skill.py [output.zip]
Writes dist/stoa.zip with only the files Stoa needs at
run time: SKILL.md, the reference notes, the cleaned texts and the lookup
script. Leaves out setup scripts, READMEs, tests, raw downloads and your
private journal.
"""
import sys
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
# Default: dist/stoa.zip inside the project (this is the file published on GitHub).
out = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else root / "dist" / "stoa.zip"
out.parent.mkdir(parents=True, exist_ok=True)
# Only what Stoa needs while running. Setup tools, docs and tests stay in the repo.
include = [
    "SKILL.md",
    "references/core-concepts.md",
    "references/practices.md",
    "references/cbt-bridge.md",
    "references/modern-interpreters.md",
    "references/topic-index.md",
    "references/texts",
    "scripts/find_passage.py",
    "journal/situations.template.md",
    "LICENSE",
]
skip_parts = {"raw", "__pycache__", ".DS_Store", "README.md"}

texts = list((root / "references" / "texts").glob("*.txt"))
if not texts:
    raise SystemExit("No texts in references/texts/. Add them first (see references/texts/README.md).")

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for item in include:
        p = root / item
        files = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file())
        for f in files:
            if skip_parts & set(f.relative_to(root).parts):
                continue
            z.write(f, Path("stoa") / f.relative_to(root))
print(f"Wrote {out} ({out.stat().st_size // 1024} KB, {len(texts)} texts)")
