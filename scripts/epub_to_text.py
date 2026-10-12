#!/usr/bin/env python3
"""Convert the Wikisource EPUB of Seneca's Moral Letters to Lucilius (Gummere)
into a plain-text file the lookup script can search.

Usage:
    python3 scripts/epub_to_text.py references/texts/raw/Moral_letters_to_Lucilius.epub seneca-letters-gummere.txt

Keeps: each letter's title and Gummere's section numbers (one paragraph per §).
Drops: page numbers, footnote markers and footnotes, the introduction and index.
"""
import html, re, sys, textwrap, zipfile
from pathlib import Path

ROMAN = [(100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def strip_tags(s):
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def convert_letter(raw):
    s = re.sub(r"<style.*?</style>", "", raw, flags=re.S)
    s = s[s.find("<body"):]
    # cut the footnote list at the end
    s = re.split(r'<ol[^>]*class="[^"]*references', s)[0]
    # drop footnote reference markers and page-number spans
    s = re.sub(r'<sup[^>]*class="[^"]*mw-ref[^"]*".*?</sup>', "", s, flags=re.S)
    s = re.sub(r'<span[^>]*class="[^"]*pagenum[^"]*"[^>]*/>', "", s)
    # turn Gummere's section numbers into paragraph starts: "\n\n§12. "
    s = re.sub(r'<span[^>]*wst-verse[^>]*>\s*<sup>\s*<b>\s*(\d+)\.\s*</b>\s*</sup>\s*</span>', r"\n\n@@\1@@ ", s)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", s, flags=re.S)
    text = "\n\n".join(strip_tags(p.replace("\n\n@@", "@@BREAK@@")) for p in paras)
    text = text.replace("@@BREAK@@", "\n\n@@")
    return text


def main():
    if len(sys.argv) != 3:
        print(__doc__); return 2
    src, out_name = Path(sys.argv[1]).expanduser(), sys.argv[2]
    z = zipfile.ZipFile(src)
    letters = []
    for name in z.namelist():
        m = re.search(r"_Letter_(\d+)\.xhtml$", name)
        if m:
            letters.append((int(m.group(1)), name))
    letters.sort()
    out = ["MORAL LETTERS TO LUCILIUS", "", "Seneca. Translated by Richard M. Gummere (Loeb, 1917-1925). Source: Wikisource.", ""]
    for num, name in letters:
        text = convert_letter(z.read(name).decode("utf-8"))
        blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
        # first block is the title, e.g. "LVI. ON QUIET AND STUDY"
        if blocks and blocks[0].upper().startswith("THE EPISTLES OF SENECA"):
            blocks = blocks[1:]          # Letter 1 carries the collection title first
        title = blocks[0] if blocks else ""
        title = re.sub(r"^[IVXLC]+\.\s*", "", title).upper()
        out += ["", f"LETTER {num}. {title}".rstrip(". ") , ""]
        for b in blocks[1:]:
            b = re.sub(r"^@@(\d+)@@\s*", r"§\1. ", b)
            b = b.replace("@@", "")
            out += textwrap.wrap(b, 76) + [""]
    dest = Path(__file__).resolve().parent.parent / "references" / "texts" / out_name
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote {dest}: {len(letters)} letters, {len(' '.join(out).split())} words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
