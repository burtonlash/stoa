# Stoa coverage test: Reddit questions (2026-10-12)

**Method.** Recurring questions were gathered from r/Stoicism (front page, the
advice wiki and its FAQ) and topic data for r/Stoicism and r/StoicSupport.
Each became a test case in `reddit_questions.json` with search terms written
the way the old translators phrase things. `run_coverage.py` runs them all.
For about a dozen cases, the top passages were read to judge whether they
actually answer the question, not just share a keyword.

Rerun anytime: `python3 tests/run_coverage.py` (or add an id, e.g. `anger`).

## Results

| Question theme | Passages found | Best fit (verified by reading) | Verdict |
|---|---|---|---|
| Anger | 122 | Seneca, Of Anger II.XXIX ("greatest remedy for anger is delay") | Strong |
| Difficult boss / coworker | 80+ | Marcus Bk 1.XV morning passage (Casaubon numbering) | Strong |
| Grief, death of a parent | 32 | Seneca, Consolations to Marcia, Helvia, Polybius | Strong |
| Pet with terminal illness | 26 | Epictetus, Enchiridion XI ("I have restored it") | Strong |
| Breakup / losing someone | 30 | Enchiridion III; Discourses "fig in winter" | Strong |
| Anxiety about the future | 26 | Epictetus, On Anxiety; Seneca dialogues | Strong |
| Staying calm / unbothered | 22 | Marcus Bk 4.III (retreat into oneself) | Strong |
| What's in my control | 20 | Enchiridion I; Discourses I.1 | Strong |
| No motivation / can't get up | 1 | Marcus Bk 5.I ("unwilling to rise") | Strong (one passage) |
| Wasting time | 54 | Seneca, Of the Shortness of Life | Strong |
| Fear of death | 67 | Many across all authors | Strong |
| What others think | 19 | Epictetus, On Anxiety (lute player); Marcus 2.XV | Strong |
| Insults | 48 | Seneca, Firmness of the Wise Man | Strong |
| Envy | 34 | Spread across authors | Good (not all read) |
| Courage / cowardice | 30 | Spread across authors | Good (not all read) |
| Desire | 17 | Epictetus only | Good (one author) |
| Family conflict | 48 | Many "brother" hits; relevance mixed | Moderate |
| Effort vs outcome | 15 | Epictetus, confidence and caution | Moderate |
| Gratitude | 57 | Marcus Book 1; On Benefits | Strong |
| Stoicism without faith | 2 | Marcus 4.III and 9.XXXVIII (providence or atoms) | Strong (few passages) |
| Wealth and ambition | 26 | Seneca dialogues, On Benefits | Good |
| Are humans good? | 17 | Marcus 1.XV; Epictetus, Of Inconsistency | Good |
| Noise (neighbor's loud music) | 41 hits, none on point | None. The classic passage is Seneca, Letter 56 (not installed) | Gap |
| Crisis ("my problems are killing me") | n/a | No quote; crisis rule applies | Guardrail |

## Issues found and fixed during testing

1. The Casaubon Meditations file included Marcus and Fronto's letters (with
   Fronto's own words). Now excluded from search.
2. Footnote markers like [12] appeared in quotes and labels. Now removed.
3. Keyword matches are not always relevant. SKILL.md now requires reading the
   passage and searching again if it only shares a word.
4. The Casaubon text has scanning typos ("md", "guest" for "goest"). SKILL.md
   now says to avoid or cut around them; adding Long's translation
   (Gutenberg #6920) is recommended.
5. SKILL.md now states that the crisis rule overrides the quote rule, lists
   known gaps, and explains where modern framing comes from.

## Still open

- Add Seneca's Letters to Lucilius (covers noise, friendship, travel, reading,
  daily practice).
- Add Long's Meditations (standard numbering, cleaner text).
- Not every top result was read by hand; "Good" rows rest on hit counts and spot checks.

## Update: Long's Meditations and Seneca's Letters added (2026-10-12)

- Added `marcus-meditations-long.txt` (Gutenberg #6920, George Long). Spot
  checks confirm standard numbering: 2.1, 4.3, 4.49, 5.1, 6.6, 8.47.
- Added `seneca-letters-gummere.txt`: all 124 letters, converted from the
  Wikisource EPUB with `scripts/epub_to_text.py`, cited as "Letter N, §n".
- The noise gap is closed: Letter 56, "On Quiet and Study", §1 is found
  directly. Seneca's Letters now contribute to 23 of the 24 test questions.
- Best-search passage counts after the update: anger 148, boss 94, grief 33,
  pet 39, breakup 37, anxiety 33, unbothered 29, control 29, motivation 2,
  time 84, fear of death 124, reputation 30, insult 56, envy 52, courage 41,
  effort vs outcome 28, desire 19, family 49, gratitude 110, faith 26,
  noise 64, wealth 52, human nature 20.
- Fixed: Letter 46 ("On a New Book…") was mistaken for a book heading; the
  Long translation's unnumbered first section of each book is labeled 1.
