---
name: totem-challenge
description: Use when drafting or publishing a new Totem Challenge issue. Handles writing the full issue HTML, scoring the six-category scorecard, and inserting it into Page 6 of index.html.
---

# Totem Challenge Agent

Owns all Totem Challenge content: drafting new issues, scoring the scorecard, writing the outreach log, and inserting the finished HTML into `index.html`.

## What a Totem Challenge issue is

Each issue: one named expert, a deep walkthrough of their most recent published analysis, a six-question Wealth Preservation Blueprint scorecard comparing their recommended product to Totem LCG, the outreach email sent verbatim, and their reply or silence. The expert wins some categories. Totem wins the total. Members follow the score and the exchange — the reply or the silence is part of the story.

The format template is Issue No. 01 (Pompliano, May 2026) in `index.html` starting at the `<!-- NEWSLETTER MOCKUP -->` comment, approximately line 3892.

## The six scorecard categories (always in this order)

| # | Category | What it tests |
|---|---|---|
| 1 | Principal Protection | Is 100% of invested capital protected from loss? |
| 2 | Return Protection | Is the stated return contractually guaranteed and insured? |
| 3 | Cycle Clarity | Is there a fixed, defined return-of-capital event? |
| 4 | Verification Path | Can the investor verify the counterparty and structure before capital moves? |
| 5 | Accessibility | Minimum, accreditation requirements, liquidity |
| 6 | Track Record Transparency | Transaction-level public performance history |

Scores are 0–5 per category per product (30 total). Score honestly — Bitcoin wins on Accessibility in Issue No. 01 and that stands. Never give Totem a perfect score on a category it does not earn.

**Totem's baseline scores for comparison:**
- Principal Protection: 5/5 (100% Allianz trade credit insurance + first-position guarantee)
- Return Protection: 5/5 (5% origination fee insured under the same Allianz structure)
- Cycle Clarity: 5/5 (90–100 day cycle, fixed)
- Verification Path: 5/5 (live calls with Allianz broker, Fortune 100 buyer contacts, Totem partners)
- Accessibility: 4/5 (principal AND returns every 90 days, zero fees; only concession is no instant liquidity)
- Track Record Transparency: 5/5 (2,000+ transactions, 0.00% defaults, transaction-level visibility)

## Step-by-step: how to draft a new issue

**1. Gather the source material.**
Get the full text of the expert's most recent piece. Read it completely before writing anything.

**2. Map the expert's structure.**
List every major section and key data source they cite (by analyst, by data provider). These become the issue sections and `chart-placeholder` blocks.

**3. Write the expert block.**
- Initials for the photo placeholder (2 characters)
- Full name
- One-line title/credentials sentence (firm, media presence, audience size)
- One paragraph describing the challenged piece, naming every major topic they cover

**4. Write the body sections.**
One `<h3 class="section">` per major theme from the expert's piece. Include:
- A `chart-placeholder` for every cited data point, with `<div class="chart-label">Pomp cites: [Source]</div>` (substitute the expert's name for "Pomp")
- SVG mini-charts only when you can construct a plausible schematic from the data described (do not fabricate numbers)
- Agree with the expert where they are right — acknowledge good analysis directly

**5. Write "Where we second [Expert]".**
List every point of agreement. Be specific. Never hedge genuine agreement into a waffle.

**6. Write "Where we challenge [Expert]".**
One crisp paragraph per difference. Name the product the expert is recommending. Frame the challenge as a question about whether that product answers the same preservation goal Totem answers. Then lead into the scorecard.

**7. Score the scorecard.**
Score the expert's recommended product on each of the six categories. Use the same bar-fill `width` CSS as a percentage of 5 (`1/5 = 20%`, `2/5 = 40%`, etc.). Write one-line explanations for both sides in each row. Call out where the expert's product wins with `<strong>[Product] wins by one.</strong>` in the left explanation.

**8. Write the challenge sentence.**
One short paragraph per section of agreement. Then the pull-quote: `<div class="pull">If your goal is wealth preservation in the [Month Year] environment, Totem covers more dimensions than [Product] does, by a [Totem total] to [Expert product total] margin on the same six questions.</div>`

**9. Write the outreach log.**
Full email text verbatim. Subject line, greeting, body, sign-off. Honest about what was sent and when.

## HTML structure for a new issue

Replace the existing newsletter mockup (everything inside `<!-- ============= NEWSLETTER MOCKUP ============= -->` through the closing `</div>`) with the new issue. Update the issue number in the masthead and in `<div class="sc-sub">`.

Keep all CSS classes exactly as they are in Issue No. 01. Do not add inline styles unless they match an existing pattern in the file (e.g., `background: var(--gold-tint)` for callouts, `background: var(--white); border: 2px solid var(--gold)` for data tables).

## Voice rules

- Write in the first-person plural ("we" = Totem Partners)
- Name sources the way the expert named them: "Pomp cites: Charlie Bilello" — never anonymize
- Never say "however" or "that said" — use "but" or start a new sentence
- Never hedge what is factually true about Totem's structure (insurance, 0.00% defaults, 90-day cycle)
- Never over-praise the expert — agree where correct, challenge where you differ, and let the scorecard be the verdict

## Do-nots

- Do not invent data for chart placeholders — use only data described in the expert's source piece
- Do not score Totem above 5 on any category
- Do not score Totem above what is honest — if the expert's pick genuinely wins a category, acknowledge it
- Do not add new CSS classes or rename existing ones
- Do not change the six scorecard categories or their order
- Do not add a build step, framework, or JavaScript logic to handle the new issue
- Do not insert the issue as a second newsletter mockup — replace the existing one
