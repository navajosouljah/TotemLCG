# Totem LCG

Partner-facing pitch deck and member newsletter wireframe delivered as a single static HTML site on Vercel. No build step. No framework. No dependencies.

## What this codebase is

`index.html` is the entire product — ~3,400 lines of HTML, CSS, and minimal JavaScript. What you edit is what ships. `index_1.html` is a prior backup; never edit it.

## Page structure

| Page | HTML ID | Contents |
|---|---|---|
| 0 — Cover | `#page-0` | Market Pulse ticker, hero statement |
| 1 — Thesis | `#page-1` | Buffett Indicator, CAPE, S&P 500, M2 narrative |
| 2 — Category | `#page-2` | The Totem reframe ("not an alternative investment") |
| 3 — Product | `#page-3` | Structure, Allianz insurance, return mechanics |
| 4 — Proof | `#page-4` | Transaction history, default rate, cycle data |
| 5 — Closer | `#page-5` | Wealth Preservation Blueprint, six-question scorecard |
| 6 — Newsletter | `#page-6` | The Totem Challenge mockup |

Navigation is handled by `goPage(n)` JavaScript at the bottom of the file. CSS variables (colors, spacing) live at the top of the `<style>` block — color changes go there, never inline.

## The Market Pulse ticker

Lines ~2917–2936. Four indicators, each listed twice (the duplicate is required for the CSS infinite scroll animation):

```html
BUFFETT INDICATOR <strong>238%</strong>
SHILLER CAPE <strong>39.8</strong>
M2 GROWTH <strong>+78% (10Y)</strong>
S&P 500 <strong>+252% (10Y)</strong>
```

Matching body copy lives on Page 1 (~line 2955 and ~line 2959) and must always stay in sync with the ticker. When you update the ticker, update the body copy too.

## Automation

`scripts/update_market_pulse.py` fetches live data and patches both the ticker and body copy, then commits directly to `main`. The GitHub Actions workflow (`.github/workflows/market-pulse.yml`) runs it every weekday at 6 AM ET (10:00 UTC).

**Data sources — all free, no API keys required:**
- S&P 500 10Y return: Yahoo Finance via yfinance, fallback FRED CSV (`SP500`)
- M2 10Y growth: FRED public CSV (`M2SL`)
- Shiller CAPE: multpl.com
- Buffett Indicator: longtermtrends.net → currentmarketvaluation.com → FRED WILL5000PRFC/GDP calculation

If a source fails, that value is skipped and the existing HTML value is kept.

## The Totem Challenge

Weekly newsletter series in Page 6. Each issue: one named expert, a walkthrough of their analysis, a six-question scorecard comparing their recommended product to Totem, the outreach email sent to the expert verbatim, and their reply or silence. The chase is the hook — members follow the exchange, not just the score.

Issue No. 01 (Pompliano, May 2026) is mocked up in the HTML as the format template.

The automation script's `--friday` flag is wired and ready for Totem Challenge content automation once the data source is defined.

## Editing rules

- Never add a build step, `package.json`, or any JavaScript framework
- Always update the ticker values in BOTH occurrences (lines ~2919–2926 and ~2927–2934)
- Always keep ticker values and Page 1 body copy in sync
- The Buffett Indicator calibration anchor in `scripts/update_market_pulse.py` (`_CALIB_DATE`, `_CALIB_BI`) should be updated when the known reference value is refreshed
- Vercel deploys automatically on every push to `main` — no manual deploy step needed
