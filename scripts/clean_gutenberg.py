#!/usr/bin/env python3
"""Clean a text file downloaded from Project Gutenberg.

Removes the Gutenberg license header and footer and normalizes line endings,
then writes the result into references/texts/ (or wherever you point it).

Usage:
    python3 scripts/clean_gutenberg.py ~/Downloads/pg2680.txt marcus-meditations-long.txt

The second argument is the output file name. Name files so the author appears
in the name (marcus, epictetus, seneca): find_passage.py --file uses that.
"""
import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src = Path(sys.argv[1]).expanduser()
    out_name = sys.argv[2]
    if not src.is_file():
        print(f"Cannot find {src}")
        return 1

    text = src.read_text(encoding="utf-8-sig", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    start = re.search(r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*\n", text, re.S)
    end = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK", text)
    body = text[start.end():] if start else text
    if end:
        body = body[: end.start() - (start.end() if start else 0)]
    if not start or not end:
        print("Warning: could not find the Gutenberg start/end markers; kept the whole file.")

    dest_dir = Path(__file__).resolve().parent.parent / "references" / "texts"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / out_name
    dest.write_text(body.strip() + "\n", encoding="utf-8")
    print(f"Wrote {dest} ({len(body.split())} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
