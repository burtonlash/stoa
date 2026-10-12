#!/usr/bin/env python3
"""Search the bundled Stoic texts and print matching passages verbatim.

Usage examples:
    python3 scripts/find_passage.py "anger"
    python3 scripts/find_passage.py "in our power" --file epictetus --max 3
    python3 scripts/find_passage.py "anger" "patience"      (passages containing BOTH words)
    python3 scripts/find_passage.py "griev*|grief|mourn*" --file seneca
Words match whole words only; add * for any ending; use | for "or".
    python3 scripts/find_passage.py --list

Texts are plain .txt files in references/texts/ (see that folder's README).
A "passage" is a paragraph (text between blank lines). Each result shows its
location (book, work or chapter title, and section number) so it can be cited.
"""
import argparse
import re
import sys
from pathlib import Path

ROMAN = r"[IVXLC]{1,12}"
PAGE_MARK = re.compile(r"^\s*\{\d+\}\s*$")              # Gutenberg page numbers like {76}
ROMAN_ALONE = re.compile(rf"^\s*({ROMAN})\.?\s*$")
SUBBOOK = re.compile(rf"^\s*Book\s+({ROMAN})\.?\s*$", re.IGNORECASE)
ROMAN_LEAD = re.compile(rf"^\s*({ROMAN})\.\s+\S")       # paragraph that starts "IV. text..."
ARABIC_LEAD = re.compile(r"^\s*(\d{1,3})\.\s+\S")        # paragraph that starts "12. text..."
SECTION_LEAD = re.compile(r"^\s*§(\d{1,3})\.\s")           # Gummere letters: "§12. text..."


def roman_to_int(r):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    total = 0
    for a, b in zip(r, r[1:] + " "):
        v = vals[a]
        total += -v if b != " " and vals.get(b, 0) > v else v
    return total

# Editorial matter (not the ancient author's words) is never returned.
SKIP = re.compile(
    r"^(THE )?(CONTENTS|INTRODUCTION|PREFACE|NOTES?|FOOTNOTES|INDEX|APPENDIX|GLOSSARY|"
    r"BIBLIOGRAPHY|CORRESPONDENCE|TRANSLATOR|LIFE OF|THE PHILOSOPHY OF|EPICTETUS$|BIOGRAPHICAL|BIOGRAPHICAL|ADVERTISEMENT|ERRATA|ARGUMENT|SUMMARY|ANALYSIS)\b"
)
CHAPTER_LEAD = re.compile(r"^([A-Z][A-Z0-9 ,;:'’“”\"()\-]{8,}[.?!])\s*—")

NAMES = {
    "marcus": "Marcus Aurelius",
    "epictetus": "Epictetus",
    "seneca": "Seneca",
}


def default_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "references" / "texts"


def is_caps_title(lines):
    text = " ".join(lines)
    letters = [c for c in text if c.isalpha()]
    return (
        len(lines) <= 4
        and len(letters) >= 4
        and all(c.isupper() for c in letters)
    )


ORDINALS = ["FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH",
            "EIGHTH", "NINTH", "TENTH", "ELEVENTH", "TWELFTH"]


def tidy(s):
    s = re.sub(r"\s+", " ", s).strip().rstrip(".")
    if s == "THE THOUGHTS OF MARCUS AURELIUS ANTONINUS":
        return "Meditations"
    if s == "AEBUTIUS LIBERALIS":          # dedication line that opens On Benefits
        return "On Benefits"
    # Seneca: "THE FOURTH BOOK OF THE DIALOGUES OF L. ANNAEUS SENECA, ADDRESSED TO NOVATUS"
    m = re.match(r"THE (\w+) BOOK OF THE DIALOGUES? OF L\. ANNAEUS SENECA, ADDRESSED TO (.+)", s)
    if m:
        n = ORDINALS.index(m.group(1)) + 1 if m.group(1) in ORDINALS else m.group(1)
        return f"Dialogue {n} (to {m.group(2).title()})"
    # Long: "BOOK IV" -> "Book 4"
    m = re.match(r"BOOK ([IVXLC]+)$", s)
    if m:
        return f"Book {roman_to_int(m.group(1))}"
    # Marcus: "THE FIRST BOOK" -> "Book 1"
    m = re.match(r"THE (\w+) BOOK$", s)
    if m and m.group(1) in ORDINALS:
        return f"Book {ORDINALS.index(m.group(1)) + 1}"
    # Long double titles: keep the short name after ", OR,"
    m = re.search(r"\bOR,? (.+)$", s)
    if m and len(s) > 50:
        s = m.group(1)
    return s.strip(" “”\"").rstrip(".")


def passages(path: Path):
    """Yield (location, paragraph_text) for each paragraph in the file."""
    top = title = sub = section = ""
    first_after_book = False
    block = []

    def flush(block):
        nonlocal top, title, sub, section, first_after_book
        lines = [l for l in block if not PAGE_MARK.match(l)]
        if not lines:
            return None
        if len(lines) == 1 and ROMAN_ALONE.match(lines[0]):
            section = ROMAN_ALONE.match(lines[0]).group(1)
            return None
        if len(lines) == 1 and SUBBOOK.match(lines[0]):
            sub = "Book " + str(roman_to_int(SUBBOOK.match(lines[0]).group(1).upper()))
            section = ""
            first_after_book = True
            return None
        if is_caps_title(lines):
            t = tidy(" ".join(lines))
            if t.startswith("LETTER "):
                top, title, sub, section = t, "", "", ""
            elif re.match(r"(Book|Dialogue) ", t) or (re.search(r"\bBOOK\b", t) and not t.startswith("A SELECTION")):
                top, title, sub, section = t, "", "", ""
            else:
                title, sub, section = t, "", ""
            return None
        if any(SKIP.match(x) for x in (top, title)):
            return None
        m = SECTION_LEAD.match(lines[0]) or ROMAN_LEAD.match(lines[0]) or ARABIC_LEAD.match(lines[0])
        if not m and first_after_book and not section:
            section = "1"          # Long's Meditations leaves the first section of each book unnumbered
        first_after_book = False
        if m:
            section = ("§" if lines[0].lstrip().startswith("§") else "") + m.group(1)
        c = CHAPTER_LEAD.match(" ".join(l.strip() for l in lines))
        if c:
            title, sub = tidy(c.group(1)), ""
        loc = " > ".join(x for x in (top, title, sub, section) if x)
        # drop printed-page markers like {61} that sit inside sentences
        # and footnote markers like [12]
        text = "\n".join(re.sub(r"\[\d+\]", "", re.sub(r"\s*\{\d+\}\s*", " ", l)) for l in lines)
        loc = re.sub(r"\[\d+\]", "", loc).replace(".)", ")")
        return loc, text

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip() == "":
            if block:
                r = flush(block)
                if r:
                    yield r
                block = []
        else:
            block.append(line)
    if block:
        r = flush(block)
        if r:
            yield r


def author_for(name, loc=""):
    if "CLEANTHES" in loc.upper():
        return "Cleanthes"
    for key, val in NAMES.items():
        if key in name.lower():
            return val
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="*", help="one or more words/phrases/regexes; a passage must match all of them")
    ap.add_argument("--file", help="only search files whose name contains this (e.g. marcus, seneca, benefits)")
    ap.add_argument("--max", type=int, default=5, help="maximum passages to show (default 5)")
    ap.add_argument("--dir", type=Path, default=default_dir(), help="folder of .txt files")
    ap.add_argument("--list", action="store_true", help="list available text files and exit")
    args = ap.parse_args()

    files = sorted(args.dir.glob("*.txt")) if args.dir.is_dir() else []
    if args.file:
        files = [f for f in files if args.file.lower() in f.name.lower()]

    if args.list:
        if not files:
            print("No text files found. See references/texts/README.md")
            return 1
        for f in files:
            print(f.name)
        return 0

    if not args.query:
        ap.error("give a search query, or use --list")
    if not files:
        print("No text files found in", args.dir, "- see references/texts/README.md")
        return 1

    # Whole-word matching, so "anger" does not match "danger".
    # Add * to a word to allow endings: "grate*" matches grateful, gratitude is separate.
    patterns = []
    for q in args.query:
        q2 = q.replace("*", r"\w*")
        try:
            patterns.append(re.compile(rf"\b(?:{q2})\b", re.IGNORECASE))
        except re.error:
            patterns.append(re.compile(rf"\b{re.escape(q)}\b", re.IGNORECASE))

    # Collect matches per file, then alternate between files so every author gets a turn.
    per_file = []
    for f in files:
        hits = []
        for loc, para in passages(f):
            flat = " ".join(para.split())
            if all(p.search(flat) for p in patterns):
                hits.append((f, loc, para))
        if hits:
            per_file.append(hits)
    total = sum(len(h) for h in per_file)
    if total == 0:
        print("No matching passages. Try different or fewer words.")
        return 1

    shown = 0
    row = 0
    while shown < min(args.max, total):
        for hits in per_file:
            if row < len(hits) and shown < args.max:
                f, loc, para = hits[row]
                who = author_for(f.name, loc)
                print(f"--- {who + ' | ' if who else ''}{f.name} | {loc or '(location not found)'}")
                print(para)
                print()
                shown += 1
        row += 1
    print(f"(showing {shown} of {total} matching passages; use --max or --file to see more)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
