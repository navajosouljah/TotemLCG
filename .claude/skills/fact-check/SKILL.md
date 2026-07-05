---
name: fact-check
description: Verify a factual claim before it ships — especially a Totem Challenge target's public statement, or any number, quote, date, or event going into Market Pulse or Totem copy. Use before publishing anything that attributes a claim to a named person, or that states a market figure as fact. Produces a verdict record (CONFIRMED / UNCONFIRMED / MISQUOTED / OUTDATED) with the primary source and the exact wording.
---

# Fact-check

Totem names real, prominent people and states real market figures every week. A
misquote or a stale number is a legal and reputational problem, not a typo. This
skill is the gate a claim passes through before it's allowed into published copy.

## When to use

- **Always** before a Totem Challenge issue ships — verify the target actually
  made the claim, in roughly those words, recently, in a real venue.
- Before stating any market figure, event date, or attributed quote as fact in
  Market Pulse or any Totem copy.
- When someone hands you a claim with no source, or a source that's a screenshot,
  a paraphrase, or a secondary outlet reporting on a primary statement.

Do **not** use it to fact-check internal drafts of *opinion* (the house voice's
skepticism is fine) — only claims of fact and attributed statements.

## What counts as a primary source

Ranked best to worst. Always climb as high as you can:
1. The person's own words in a durable venue — their post/thread, their letter,
   an on-the-record interview transcript, an official filing or press release.
2. A full-quote report in a reputable outlet that names the venue and date.
3. A paraphrase in a reputable outlet (usable only to *find* the primary; never
   quote it as if it were the person's words).

Never acceptable as the sole basis: a screenshot with no link, an unattributed
aggregator, a social post *about* what someone said, or your own memory.

## Process

1. **State the claim in one sentence** exactly as the copy will present it,
   including any quotation marks and any date/number.
2. **Locate the primary source.** Search for the person's own words. Climb the
   source ladder above as high as it goes. Record the URL and the publication date.
3. **Compare word-for-word.** Does the copy's wording match? Is anything in
   quotation marks a *verbatim* quote? Is the number/date right? Is it recent
   enough to still be true (rates, prices, and positions go stale fast)?
4. **Assign a verdict** (see below) and capture the exact source quote.
5. **Return the verdict record.** If anything is short of CONFIRMED, say what
   would fix it — do not soften a fail into a pass.

## Output format

Return exactly this block, nothing before or after:

```
CLAIM:      <the claim as the copy states it>
VERDICT:    CONFIRMED | UNCONFIRMED | MISQUOTED | OUTDATED
SOURCE:     <URL>  (<venue>, <YYYY-MM-DD>)
EXACT QUOTE: "<verbatim words from the primary source>"
NOTES:      <what matches, what doesn't, and — if not CONFIRMED — the exact fix>
```

Verdicts:
- **CONFIRMED** — primary source found; wording, number, and date all check out.
- **MISQUOTED** — they said something like it, but the copy's wording (esp. inside
  quotation marks) doesn't match. Give the correct wording in NOTES.
- **OUTDATED** — it was true but isn't now (position reversed, number moved).
- **UNCONFIRMED** — no primary source found. Default here when in doubt.

## Do-nots (hard stops)

- **Never mark CONFIRMED without a primary-source URL and its date.** No URL → not
  confirmed, full stop.
- **Never treat a paraphrase as a quote.** If the primary source paraphrases, the
  copy may not put it in quotation marks.
- **Never let "it's probably right" pass.** Uncertain defaults to UNCONFIRMED.
- **Never fix a bad claim by softening the copy silently** — surface the verdict so
  a human decides. This skill reports; it doesn't quietly rewrite published claims.
- **Never rely on your training memory for a current figure or a recent quote.**
  Search for it.

## Worked examples

**A great CONFIRMED record:**
```
CLAIM:      Jamie Dimon called private credit "worse than people think."
VERDICT:    CONFIRMED
SOURCE:     https://www.example.com/dimon-letter-2026  (JPMorgan annual letter, 2026-04-08)
EXACT QUOTE: "Some of this stuff is worse than people think."
NOTES:      Wording matches in substance; the copy paraphrases slightly, so present
            it as a paraphrase (no quotation marks) or use the exact quote above.
```

**A great catch (MISQUOTED — this is the value of the skill):**
```
CLAIM:      Gundlach said private credit is "a bubble that will burst in 2026."
VERDICT:    MISQUOTED
SOURCE:     https://x.com/TruthGundlach/status/...  (X, 2026-05-14)
EXACT QUOTE: "The opacity in private credit worries me more than the spreads do."
NOTES:      He never said "bubble" or gave a 2026 date. Do NOT run the quoted line.
            If we want his stance, quote the verbatim line above and drop the date.
```

**Bad (do not produce) — a false confirm:**
```
CLAIM:      Buffett is moving to private credit.
VERDICT:    CONFIRMED
SOURCE:     (a tweet someone screenshotted)
```
Why it fails: no primary URL, no date, sourced from a screenshot — this is exactly
the mistake the skill exists to stop. Correct verdict: UNCONFIRMED.
