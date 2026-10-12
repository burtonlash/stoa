# Stoa

A Claude skill that acts as a Stoic-style counselor. Bring it what you're
struggling with and it helps you sort what is in your control from what is
not, offers one practice to try, and grounds its advice in a **verbatim
quote** from the classic Stoic texts: Marcus Aurelius, Epictetus and Seneca.

> **Stoa is a philosophy practice tool, not therapy,** and not a substitute
> for professional help. If you are in crisis, call or text 988 (US) or your
> local emergency number.

## Example

> **You:** I can't stop getting angry at a coworker.
>
> **Stoa:** That sounds exhausting… Seneca's advice is almost practical to a
> fault: *"The greatest remedy for anger is delay: beg anger to grant you this
> at the first, not in order that it may pardon the offence, but that it may
> form a right judgment about it: if it delays, it will come to an end."*
> (Seneca, *Of Anger*, Book II, section XXIX, Stewart translation) …
> Try this: write the reply you want to send, then wait 24 hours.

## What it does

- **Listens first**, then helps you separate what's up to you from what isn't.
- **Always quotes the source.** Every quote comes word for word from the
  bundled public-domain texts, found with a lookup script rather than recalled
  from memory, and cited with work, location and translator.
- **Modern interpreters** (Ryan Holiday, Donald Robertson, Massimo Pigliucci,
  William Irvine, Pierre Hadot) are summarized and credited, never quoted.
- **Two voices.** Gentle by default; a direct, Epictetus-style mentor when you
  ask ("be blunt"). It challenges excuses, never your worth.
- **Remembers ongoing situations** (with your permission) so it can pick up
  where you left off.
- **Safety first.** It sets philosophy aside in a crisis, points to real help
  for abuse, and never diagnoses.
- **Triggers on its own** for about 60 everyday topics: stress, anxiety,
  self-worth, grief, anger, motivation, procrastination, burnout, breakups,
  family conflict, career setbacks and more. Or just say "use Stoa".

## Install (about a minute)

### Claude app (web, desktop, mobile)

1. Download **[`dist/stoa.zip`](dist/stoa.zip)** from this repo.
2. In Claude, turn on **Settings › Capabilities › Code execution and file
   creation**.
3. Go to **Customize › Skills**, click **+**, then **Create skill › Upload a
   skill**, and choose `stoa.zip`.
4. Start a new chat: "I've been dreading a hard conversation all week."

### Claude Code

Unzip `dist/stoa.zip` into `~/.claude/skills/` so you have
`~/.claude/skills/stoa/SKILL.md`. In Claude Code, Stoa keeps ongoing
situations in `journal/situations.md`, which stays on your machine.

## The texts

All translations are in the public domain in the United States. Check the
status in your own country if you are elsewhere.

| Author | Work | Translator | Source |
|---|---|---|---|
| Marcus Aurelius | *Meditations* (preferred) | George Long (1862) | Project Gutenberg #6920 |
| Marcus Aurelius | *Meditations* | Meric Casaubon (1634) | Project Gutenberg #2680 |
| Epictetus | *Discourses* (selection) and *Enchiridion* | George Long | Project Gutenberg #10661 |
| Epictetus | *Golden Sayings*, with the *Hymn of Cleanthes* | Hastings Crossley | Project Gutenberg #871 |
| Seneca | *Moral Letters to Lucilius* (all 124) | Richard M. Gummere | Wikisource |
| Seneca | *Minor Dialogues* (On Anger, Shortness of Life, Tranquility, Consolations…) | Aubrey Stewart | Project Gutenberg #64576 |
| Seneca | *On Benefits* | Aubrey Stewart | Project Gutenberg #3794 |

Thanks to Project Gutenberg and Wikisource volunteers. The texts were cleaned
(license headers, tables of contents, page numbers and footnote markers
removed); see `references/texts/README.md` for details.

## How it works

```
SKILL.md                     Stoa's instructions (voice, workflow, quote rule, guardrails)
references/                  Stoic concepts, practices, CBT bridge, modern interpreters, topic index
references/texts/            the seven cleaned source texts
scripts/find_passage.py      verbatim quote lookup with citations
scripts/package_skill.py     builds dist/stoa.zip
scripts/clean_gutenberg.py   prepares a Project Gutenberg download
scripts/epub_to_text.py      converts the Wikisource EPUB of Seneca's Letters
tests/                       coverage tests from common r/Stoicism questions
dist/stoa.zip                ready-to-install skill
```

Try the lookup yourself:

```
python3 scripts/find_passage.py "anger" "delay*"
python3 scripts/find_passage.py "grief|griev*|mourn*" --file letters --max 3
```

After changing anything, rebuild the installable file with
`python3 scripts/package_skill.py`.

## Testing

`tests/reddit_questions.json` holds 24 common questions from r/Stoicism and
r/StoicSupport. Run `python3 tests/run_coverage.py` to see how well the texts
cover each one. Results are in `tests/TEST_REPORT.md`.

## Contributing

Ideas, confirmed passages for the topic index, new practices and bug fixes
are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Code and original writing: MIT (see [LICENSE](LICENSE)). The Stoic texts are
in the public domain.
