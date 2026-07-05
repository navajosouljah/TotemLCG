# Totem LCG

Partner-facing pitch deck and member newsletter wireframe delivered as a single static HTML site on Vercel. No build step. No framework. No dependencies.

## What this codebase is

`index.html` is the entire product — ~4,300 lines of HTML, CSS, and minimal JavaScript. What you edit is what ships. `index_1.html` is a prior backup; never edit it. Before any large edit, run `cp index.html index_1.html` to refresh the backup.

Vercel deploys automatically on every push to `main` — no manual deploy step.

## Page structure

| Page | HTML ID | Contents |
|---|---|---|
| 0 — Cover | `#page-0` | Market Pulse ticker, hero statement |
| 1 — Thesis | `#page-1` | Buffett Indicator, CAPE, S&P 500, M2 narrative |
| 2 — Category | `#page-2` | The Totem reframe ("not an alternative investment") |
| 3 — Product | `#page-3` | Structure, Allianz insurance, return mechanics |
| 4 — Proof | `#page-4` | Transaction history, 0.00% default rate, 90-day cycle data |
| 5 — Closer | `#page-5` | Wealth Preservation Blueprint, six-question scorecard |
| 6 — Newsletter | `#page-6` | The Totem Challenge mockup |

Navigation is handled by `goPage(n)` in the JavaScript block at the bottom of the file. Never touch `goPage()` — it controls all page transitions and keyboard navigation.

## CSS variables

Color and spacing tokens live at the top of the `<style>` block, inside `:root { }`. Key variables:

```css
--gold:       #A6791A
--gold-deep:  #7A550E
--gold-tint:  #F5EDD9
--ink:        #1C1A17
--white:      #FAF8F4
```

Color changes always go here, never inline. Never rename a CSS variable — it will silently break every element that references it.

## The Market Pulse ticker

**How to find it:** Search for `BUFFETT INDICATOR` in the file. The ticker block appears twice in sequence — both copies are required for the CSS infinite scroll animation.

The four values, each appearing in both copies:

```html
BUFFETT INDICATOR <strong>238%</strong>
SHILLER CAPE <strong>39.8</strong>
M2 GROWTH <strong>+78% (10Y)</strong>
S&P 500 <strong>+252% (10Y)</strong>
```

**Body copy sync:** Page 1 contains prose sentences that must stay in sync with the ticker. Search for `sat at 230% as of December 31` to find the Buffett body line. Search for `was at 39.8 in` for the CAPE line. Search for `The S&amp;P 500 rose` for the S&P line. Search for `M2 money supply rose` for the M2 line. Always update all four body lines when you update the ticker.

## The Wealth Preservation Blueprint (Page 5)

The six scorecard questions — used on Page 5 and in every Totem Challenge issue — are fixed and always in this order:

1. **Principal Protection** — Is 100% of invested capital protected from loss?
2. **Return Protection** — Is the stated return contractually guaranteed and insured?
3. **Cycle Clarity** — Is there a fixed, defined return-of-capital event?
4. **Verification Path** — Can the investor verify the counterparty and structure before capital moves?
5. **Accessibility** — Minimum, accreditation requirements, liquidity
6. **Track Record Transparency** — Transaction-level public performance history

Totem's answers: 100% principal insured by Allianz trade credit policy + first-position guarantee; 5% origination fee insured under the same structure; 90–100 day fixed cycle; live calls with Allianz broker, Fortune 100 buyer contacts, and Totem partners; withdrawals every 90 days, zero fees; 2,000+ transactions, 0.00% defaults.

## Automation

`scripts/update_market_pulse.py` fetches live data and patches both the ticker and body copy, then commits directly to `main`. The GitHub Actions workflow (`.github/workflows/market-pulse.yml`) runs it every weekday at 10:00 UTC (6 AM EDT / 5 AM EST).

**Data sources — all free, no API keys required:**
- S&P 500 10Y return: Yahoo Finance via yfinance, fallback FRED CSV (`SP500`)
- M2 10Y growth: FRED public CSV (`M2SL`)
- Shiller CAPE: multpl.com scrape
- Buffett Indicator: longtermtrends.net → currentmarketvaluation.com → FRED WILL5000PRFC/GDP calculation

If a source fails, that value is skipped and the existing HTML value is kept. The script never writes a blank value.

## The Totem Challenge

Weekly newsletter series in Page 6. Each issue: one named expert, a walkthrough of their analysis, a six-question scorecard comparing their recommended product to Totem, the outreach email sent verbatim, and their reply or silence.

Issue No. 01 (Pompliano, May 2026) is the format template, starting at `<!-- ============= NEWSLETTER MOCKUP ============= -->` in the file.

## Editing rules

- **Never** add a build step, `package.json`, or any JavaScript framework
- **Never** touch `goPage(n)` — it controls all navigation
- **Never** rename a CSS variable — silent breakage across the whole file
- **Never** add external resource references (`<script src>`, `<link href>` to a CDN) — this is a self-contained file
- **Always** update the ticker values in **both** occurrences — search for `BUFFETT INDICATOR` to confirm you find two blocks
- **Always** keep ticker values and Page 1 body copy in sync — four separate prose sentences must match the four ticker values
- **Always** edit `index_1.html` → never; it is the backup, not the working file
- The Buffett Indicator calibration anchor in `scripts/update_market_pulse.py` (`_CALIB_DATE`, `_CALIB_BI`) must be updated together when you have a verified new reference value
