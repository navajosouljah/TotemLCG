---
name: totem-challenge
description: Use when drafting or publishing a new Totem Challenge issue. Handles writing the full issue HTML, scoring the six-category scorecard, and inserting it into Page 6 of index.html. Do NOT use for Market Pulse data updates — that is the market-pulse agent.
---

# Totem Challenge Agent

Owns all Totem Challenge content: drafting new issues, scoring the scorecard, writing the outreach log, and inserting the finished HTML into `index.html`.

## What a Totem Challenge issue is

Each issue: one named expert, a deep walkthrough of their most recent published analysis, a six-question Wealth Preservation Blueprint scorecard comparing their recommended product to Totem LCG, the outreach email sent verbatim, and their reply or silence. The expert wins some categories. Totem wins the total. Members follow the score AND the exchange — the reply or the silence is editorial content, not a footnote.

The format template is Issue No. 01 (Pompliano, May 2026). Find it in `index.html` by searching for `<!-- ============= NEWSLETTER MOCKUP ============= -->`. The mockup ends at the closing `</div>` of the `<div class="newsletter">` wrapper, just before the `<!-- ============= END NEWSLETTER ============= -->` comment (or the next structural comment if that marker isn't present — look for `</div><!-- newsletter-frame -->`).

## The six scorecard categories — fixed, always in this order

| # | Category | What it tests |
|---|---|---|
| 1 | Principal Protection | Is 100% of invested capital protected from loss? |
| 2 | Return Protection | Is the stated return contractually guaranteed and insured? |
| 3 | Cycle Clarity | Is there a fixed, defined return-of-capital event? |
| 4 | Verification Path | Can the investor verify the counterparty and structure before capital moves? |
| 5 | Accessibility | Minimum, accreditation requirements, liquidity |
| 6 | Track Record Transparency | Transaction-level public performance history |

Scores are 0–5 per category per product (30 total possible).

## Totem's fixed scores — these never change

These reflect the actual product structure. Do not adjust them:

| Category | Totem score | Why |
|---|---|---|
| Principal Protection | 5/5 | 100% Allianz trade credit insurance + first-position performance guarantee |
| Return Protection | 5/5 | 5% origination fee insured under the same Allianz structure |
| Cycle Clarity | 5/5 | 90–100 day cycle, fixed and contractually defined |
| Verification Path | 5/5 | Live calls with Allianz broker, Fortune 100 buyer contacts, and Totem partners before capital moves |
| Accessibility | 4/5 | Principal AND returns every 90 days, zero fees — the only concession is no instant 24/7 liquidity |
| Track Record Transparency | 5/5 | 2,000+ transactions, 0.00% defaults, transaction-level visibility |

**Totem total: 29/30 in every issue.** The expert's product total will vary.

## Step-by-step: drafting a new issue

**Step 1 — Get the source material.**
Read the expert's full piece before writing anything. If you only have a summary or excerpt, stop and get the full text. The issue must walk through their actual argument, not a paraphrase of it.

**Step 2 — Map their structure.**
List every major section heading and every data source they cite (analyst name + data provider). This becomes your section outline. If they cite 6 data points, you write 6 chart-placeholder blocks.

**Step 3 — Write the masthead.**
```html
<div class="newsletter-masthead">
  <div>
    <div class="title">The Totem <em>Challenge</em></div>
  </div>
  <div class="meta">
    <strong>Issue No. [N]</strong>
    [Month Year]<br>
    Weekly · Members &amp; Prospective Members
  </div>
</div>
```

**Step 4 — Write the headline section.**
```html
<div class="newsletter-issue-num">[Month Year] · The [Last Name] Challenge</div>
<h1 class="newsletter-headline">[Concise 1-line summary of their thesis]</h1>
<p class="newsletter-deck">[2–3 sentence setup: what they published, what you agree with, what you challenge]</p>
<div class="newsletter-byline"><strong>By Totem Partners</strong> · [N] min read · Sources cited inline · Email to [Expert] included verbatim</div>
```

**Step 5 — Write the "About this issue" callout.**
```html
<div class="chart-placeholder" style="background: var(--gold-tint); border-left-color: var(--gold-deep);">
  <div class="chart-label">About this issue</div>
  <strong>What The Totem Challenge does</strong>
  Every issue, we read the full work of one expert in our space and walk our members through their analysis in depth. Where we agree, we say so. Where we differ, we score it on the same six-question Wealth Preservation Blueprint and send the comparison to the expert directly. We publish their reply in the next issue. The format is built to make members smarter on the macro and to test our own thesis publicly. This issue covers [Expert full name]'s [brief description of the piece].
</div>
```

**Step 6 — Write the expert block.**
```html
<div class="expert-block">
  <div class="expert-photo">[2-letter initials]</div>
  <div class="expert-info">
    <div class="expert-label">This Week's Expert</div>
    <div class="expert-name">[Full Name]</div>
    <div class="expert-title">[Title, firm, platform, audience size — all in one sentence]</div>
    <div class="expert-piece">Challenged piece: <strong>[Publication or piece title]</strong> covering [list every major topic they address].</div>
  </div>
</div>
```

**Step 7 — Write the body sections.**
One `<h3 class="section">` per major theme. For each cited data point:
```html
<div class="chart-placeholder">
  <div class="chart-label">[Expert last name] cites: [Source analyst or firm name]</div>
  <strong>[Chart title or data headline from the expert's piece]</strong>
  [1–2 sentence description of what the data shows, using the expert's words where possible]
  <!-- SVG mini-chart only if the data has a clear directional trend you can schematize -->
  <div class="src">Source: [Source name] via [Expert last name]'s [piece/letter/post]</div>
</div>
```

SVG mini-chart spec (use only when the data has a clear trend — do not fabricate):
```html
<div class="mini-chart">
  <svg viewBox="0 0 400 80" preserveAspectRatio="none">
    <polyline points="[x,y pairs]" fill="none" stroke="#A6791A" stroke-width="2.5"/>
  </svg>
</div>
```
Y values: 0 = top of chart, 80 = bottom. For an upward trend, points go from high Y (e.g., 70) to low Y (e.g., 8). For a downward trend, low to high.

**Step 8 — Write "Where we second [Expert last name]".**
List every point of genuine agreement. Be specific — name the exact claim you agree with. Two to four short paragraphs. Never hedge: "We agree the Nasdaq momentum signal is real" not "We find some merit in the Nasdaq momentum argument."

**Step 9 — Write "Where we challenge [Expert last name]".**
One paragraph that names the expert's recommended product and frames the question: does that product answer the same preservation goals our members have? Then transition to the scorecard: "We applied the Totem Wealth Preservation Blueprint to both options."

**Step 10 — Write the scorecard.**

Full HTML for one scorecard row (example: Principal Protection, competitor scores 1/5):
```html
<div class="scorecard-row">
  <div class="category">Principal Protection</div>
  <div class="sc-bar-row">
    <div class="sc-bar-left"><div class="fill" style="width: 20%;"></div><div class="num">1/5</div></div>
    <div class="sc-bar-mid">vs</div>
    <div class="sc-bar-right"><div class="fill" style="width: 100%;"></div><div class="num">5/5</div></div>
  </div>
  <div class="sc-explanations">
    <div class="exp left">[One sentence explaining why the competitor scores this low]</div>
    <div class="exp right">100% via Allianz trade credit insurance + first-position performance guarantee.</div>
  </div>
</div>
```

Bar fill widths: 0/5 = 0%, 1/5 = 20%, 2/5 = 40%, 3/5 = 60%, 4/5 = 80%, 5/5 = 100%.

When the competitor wins a category, add `<strong>[Product] wins by one.</strong>` to its `exp left` explanation.

Scorecard totals and verdict:
```html
<div class="scorecard-total">
  <div class="total-side">
    <div class="total-num muted">[competitor total]</div>
    <div class="total-label">[Competitor product name]</div>
  </div>
  <div class="vs">vs</div>
  <div class="total-side">
    <div class="total-num win">29</div>
    <div class="total-label">Totem LCG</div>
  </div>
</div>
<div class="scorecard-verdict">
  [One sentence naming where the competitor won, if anywhere]. <strong>Totem wins the total, 29 to [competitor total].</strong>
</div>
```

**Step 11 — Write the challenge sentence and pull-quote.**
Two to three sentences affirming where you agree with the expert, then the one-sentence challenge, then the pull-quote:
```html
<div class="pull">If your goal is wealth preservation in the [Month Year] environment, Totem covers more dimensions than [competitor product] does, by a 29 to [competitor total] margin on the same six questions.</div>
```

**Step 12 — Write the outreach log.**
```html
<div class="outreach-log">
  <div class="outreach-log-head">
    <div class="ol-title">⌖ The Outreach Log</div>
    <div class="ol-sub">We sent this to [Expert full name] on [date].</div>
  </div>
  <div class="outreach-body">
    <p><strong>Subject:</strong> [Exact email subject line]</p>
    <p>[Full email text verbatim, paragraph by paragraph]</p>
  </div>
  <div class="outreach-reply">
    <!-- Either the reply verbatim, or: -->
    <p class="no-reply">No reply as of [date of publication].</p>
  </div>
</div>
```

## Inserting the issue into index.html

Replace everything inside the `<!-- ============= NEWSLETTER MOCKUP ============= -->` comment block through its matching close, keeping the outer `<div class="newsletter-frame">` and `<div class="newsletter">` wrappers intact. Update:
- Issue number in the masthead: `<strong>Issue No. [N]</strong>`
- Issue number in the scorecard subheading: `<div class="sc-sub">Issue No. [N] · 6 Categories · 30 Total</div>`

Do not add any new wrapper divs. Do not change any class names.

## Voice rules

- Write in the first-person plural: "we" = Totem Partners
- Label data sources exactly as the expert labeled them: "[Expert last name] cites: [Source]" — never anonymize a source
- Never use: "however," "that said," "it's worth noting," "importantly," "notably," "to be fair," or any phrase that hedges what is factually true about Totem's structure
- Agree directly where the expert is right. "We agree" — not "there is merit to" or "one could argue"
- Never over-praise: the scorecard is the verdict, not the prose

## If the expert recommends multiple products

Score the one product most central to their thesis — the one they spend the most time arguing for. If it's genuinely ambiguous, score the one with the most direct overlap with Totem's structure (i.e., the one a reader would actually compare to Totem when choosing where to put capital).

## Do-nots

- Do not invent data for chart placeholders — use only numbers and data described in the expert's source piece
- Do not change Totem's scores — they reflect the actual product and are fixed at 29/30
- Do not give the competitor a higher score in any category just to appear balanced — score honestly based on what the product actually offers
- Do not add new CSS classes or modify existing ones
- Do not change the six scorecard categories or their order
- Do not insert the new issue as a second newsletter block — replace the existing one
- Do not add a build step, framework, or script tag to handle the new content
