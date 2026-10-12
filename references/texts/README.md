# Source texts

Stoa quotes only from the texts in this folder. The cleaned texts are
included in this repo, so you do not need to download anything to use Stoa.
The steps below are for rebuilding them from the original sources or adding
new ones. All of the
translations below were first published long ago and are in the public
domain in the United States. Check the status in your own country if you
are outside the US.

## Texts to download

Download each as plain text and save into `references/texts/raw/`.

| Work | Translator | Plain-text link | Save as |
|---|---|---|---|
| Meditations (Marcus Aurelius) | Meric Casaubon (1634) | https://www.gutenberg.org/ebooks/2680.txt.utf-8 | `marcus-meditations-casaubon.txt` |
| Meditations, preferred translation (*Thoughts of Marcus Aurelius*) | George Long (1862), standard modern numbering | https://www.gutenberg.org/ebooks/6920.txt.utf-8 | `marcus-meditations-long.txt` |
| Discourses (selection) + Enchiridion (Epictetus) | George Long | https://www.gutenberg.org/ebooks/10661.txt.utf-8 | `epictetus-discourses-enchiridion-long.txt` |
| Golden Sayings of Epictetus, with the Hymn of Cleanthes | Hastings Crossley | https://www.gutenberg.org/ebooks/871.txt.utf-8 | `epictetus-golden-sayings-crossley.txt` |
| Minor Dialogues (Seneca): On Anger, Shortness of Life, Tranquility of Mind, Providence, Consolations, Clemency and more | Aubrey Stewart | https://www.gutenberg.org/ebooks/64576.txt.utf-8 | `seneca-dialogues-stewart.txt` |
| On Benefits (Seneca) | Aubrey Stewart | https://www.gutenberg.org/ebooks/3794.txt.utf-8 | `seneca-benefits-stewart.txt` |
| Moral Letters to Lucilius (Seneca) | Richard Gummere | Not on Gutenberg. Download the EPUB from Wikisource's "Moral letters to Lucilius" page, then run `python3 scripts/epub_to_text.py <file>.epub seneca-letters-gummere.txt` | `seneca-letters-gummere.txt` |

## Notes on these editions

- Gutenberg #2680 is Casaubon's 1634 translation (archaic English, a few
  scanning typos, and section numbers that differ from modern editions in
  places). Long's translation (#6920) uses the standard numbering and is
  preferred; Casaubon is kept as a second wording.
- Long's text leaves the first section of each book unnumbered; the lookup
  script labels it as section 1.
- The Gummere letters come from Wikisource. The converter keeps each letter's
  title and Gummere's § section numbers and drops page numbers, footnotes,
  the introduction and the subject index.
- In the Golden Sayings file, the table of contents was removed and the
  "Appendix A/B" headings were turned into FRAGMENTS ATTRIBUTED TO EPICTETUS
  and THE HYMN OF CLEANTHES so the lookup script can label passages.
- The lookup script skips prefaces, introductions, contents and notes, so
  only the ancient authors' own words are quoted.

## How to get them (one time)

1. Go to https://www.gutenberg.org and search for each title and translator
   above. Gutenberg has Long's Meditations and Epictetus. If the Seneca
   letters in Gummere's translation are not on Gutenberg, Wikisource has
   them; copy the text into a plain `.txt` file.
2. On each book's page, download the "Plain Text UTF-8" version.
3. Clean and save each one with the helper script, from the `stoa` folder:

   ```
   python3 scripts/clean_gutenberg.py ~/Downloads/pg2680.txt marcus-meditations-long.txt
   ```

   (Your downloaded file name will differ.) Keep the author's name in the
   output file name, since the lookup script filters on it.
4. Check that it works:

   ```
   python3 scripts/find_passage.py --list
   python3 scripts/find_passage.py "anger" --file marcus
   ```

## A note on licensing

The cleaned texts are public domain, but the Project Gutenberg name and
license apply to its own edition headers. The cleaning script strips those.
If you choose to commit the texts to a public repo, keep a line in your
README crediting the translators and Project Gutenberg as the source.
