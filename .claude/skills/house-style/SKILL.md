---
name: house-style
description: Write or edit any Totem LC Group editorial copy — Market Pulse memos, Totem Challenge issues, section intros, "Bottom Line" bullets, headlines, social blurbs — in the house voice and format. Use whenever drafting, rewriting, tightening, or fact-checking reader-facing prose for Totem. Enforces the voice, the compliance do-nots (no fabricated numbers/quotes, no investment advice), and the exact output shapes.
---

# Totem house style

Codifies how every reader-facing word from Totem LC Group reads and what it may
never say. This is the single source of truth for voice; the machine-enforced
copy in `automation/market_pulse/narrative.py` (`SYSTEM_PROMPT`) and the
positioning in `CLAUDE.md` must stay in sync with it.

## When to use

Use this any time you are producing or changing copy a reader will see:
- A Market Pulse section intro, "Quick Read" paragraph, headline, or Bottom Line.
- A Totem Challenge issue, hook, or the `totem_angle` line in a target brief.
- Any social post, email subject, or blurb representing Totem.

Do **not** use it for internal notes, code comments, or commit messages.

## The voice (non-negotiable)

- **Plain-spoken and confident.** Short declarative sentences. No throat-clearing.
- **Lightly skeptical of consensus** — we question the herd, we don't sneer.
- **Educational, never hype.** No "massive", "huge", "to the moon", no exclamation
  points. Explain, don't sell.
- **Lead with the so-what.** Every claim answers "what does this mean for an
  ordinary investor?" — not a restatement of the number.
- **Typography:** real minus sign (−) for negatives; keep figures tight (`6.9%`,
  `$1.2T`); one space, no em-dash pileups.

## The through-line (positioning)

Totem's structure is contracted, insured, transaction-level lending against
verified Fortune 100 purchase orders — principal and returns insured by Allianz,
uncorrelated to public markets. When copy contrasts Totem with a target's claim,
name the specific fear their claim implies (opacity, volatility, correlation,
default risk) and show how Totem's structure answers *that specific fear*. Keep it
concrete; never generic ("a smarter way to invest").

## Process

1. **Identify the artifact and its shape** (see Output formats below). If it's a
   Totem Challenge angle, get the target's exact recent claim and a live source
   first.
2. **Anchor on real inputs.** Use only the figures, quotes, and events supplied or
   verifiable. If a number is missing, ask for it or omit the line — never guess.
3. **Draft in the voice.** Short sentences. So-what first.
4. **Run the do-not checklist** (below) against every sentence.
5. **Return only the requested artifact** in the exact format — no preamble,
   no "Here's your copy", no markdown fences unless the format calls for them.

## The so-what test

Before any sentence ships, ask: **"So what — what does this change for the
reader's money or decisions?"** If the sentence only restates a number already in
the table, it fails. The so-what is the second half of the sentence, after the
number: *the number* → *what it means*. Every Bottom Line and Quick Read line must
pass this test.

## Output formats

Match these shapes exactly. Lengths are ceilings, not targets — shorter is better.

**Bottom Line bullets** — 2–4 per section, each one sentence, each a so-what:
```
- A 30-year mortgage near 7% adds ~$300/month to a $400k loan versus 2021 —
  the freeze in existing-home sales isn't thawing on this rate.
```

**Section intro** — one italic sentence, scene-setting, no numbers repeated from
the table:
```
_Rates drifted higher again as the market gave up on a near-term cut._
```

**Quick Read paragraph** — 2–4 sentences, ≤55 words, plain text. Opens with the
week's single most important move, closes with the so-what for an ordinary
investor. No bullet, no heading:
```
The Fed held again and the market finally stopped pricing a summer cut. Two-year
yields pushed back toward 4.8%, and mortgage rates followed. If you're waiting to
refinance, this isn't the week — and it may not be the quarter.
```

**News headline item** — a `label` (≤8-word noun phrase, no verb-of-being) plus a
2–3 sentence `text` that explains why it matters:
```
label: "Oil slips under $70"
text:  "WTI closed the week below $70 for the first time since spring. Traders
        read it as softening demand more than added supply. Cheap gas now, but a
        demand signal worth watching."
```

**Totem Challenge angle** — 1–2 sentences, target's fear → Totem's answer:
```
Gundlach is warning on private-credit opacity and marks nobody can verify.
Totem's contracted, Allianz-insured, transaction-level PO structure is the
answer to exactly that: every dollar tied to a named Fortune 100 receivable.
```

**Market Pulse JSON** (full narrative, generated programmatically) — return ONLY
the JSON object, no fences. This is the canonical shape (source of truth is
`SYSTEM_PROMPT` in `automation/market_pulse/narrative.py` — if the two disagree,
narrative.py wins and this block must be updated to match):
```json
{
  "news_intro": "one short italic sentence",
  "news": [{"label": "Headline phrase", "text": "2-3 sentence explanation"}],
  "quick_read": ["paragraph", "..."],
  "sections": {
    "<section_id>": {"intro": "one italic sentence", "bottom_line": ["bullet", "..."]}
  }
}
```
Section ids you must cover: `stocks, rates, savings, energy, commodities, crop,
realestate, household, crypto, world`.

## Do-nots (compliance — hard stops)

- **Never invent** a number, ticker, quote, date, event, or source URL. Missing
  data → ask or omit.
- **Never give investment advice.** No "buy", "sell", "you should", price targets,
  or return promises. This is general information.
- **Never misquote or paraphrase a named person as a direct quote.** A Totem
  Challenge target's claim must be verifiable against a live source before it ships.
- **Never overstate the insurance.** Say what's actually contracted ("principal and
  returns insured by Allianz"); don't drift into "risk-free" or "guaranteed profit".
- **No hype words, no exclamation points, no emoji** in reader-facing copy.
- **Don't restate the number as the insight** — if the bullet just re-reads the
  table, it's wrong.

## Two worked examples

**Great — Bottom Line, energy section:**
> WTI slipping under $70 is quiet relief at the pump, but it's also the market
> pricing in weaker demand — good for drivers, a caution flag for growth.

Why it's great: so-what first, both sides named, no advice, tight.

**Great — Totem Challenge hook, target = an index-fund maximalist:**
> "Just buy the index" works right up until the index is down 20% and you needed
> the money at 19. Totem's returns don't move with the S&P — they move with
> invoices Fortune 100 buyers have already agreed to pay.

Why it's great: concrete contrast, names the specific weakness (correlation/
sequence risk), lands the structure without a sales pitch.

**Bad (do not produce):**
> Markets are booming and Totem offers HUGE guaranteed returns you should get into
> now! The S&P is up so buy while it's hot.

Why it fails: hype, exclamation, "guaranteed", explicit advice, no substance.
