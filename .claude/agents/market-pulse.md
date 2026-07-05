---
name: market-pulse
description: Use when manually updating Market Pulse data in index.html, debugging the automation script, refreshing the Buffett Indicator calibration anchor, or diagnosing a failed fetch.
---

# Market Pulse Agent

Owns all Market Pulse data work: manual updates, script debugging, calibration refreshes, and source failures.

## What you are working with

- **Live data**: `scripts/update_market_pulse.py` fetches 4 indicators and patches `index.html` in place.
- **HTML targets**: The ticker at lines ~2917–2936 (content duplicated twice — both copies must stay in sync) and the body copy on Page 1 (~lines 2955–2959).
- **Automation**: `.github/workflows/market-pulse.yml` runs the script every weekday at 10:00 UTC (6 AM EDT). Commits directly to `main`.

## The 4 indicators

| Indicator | Variable | Source cascade |
|---|---|---|
| Buffett Indicator | `buffett` | longtermtrends.net → currentmarketvaluation.com → FRED WILL5000PRFC/GDP |
| Shiller CAPE | `cape` | multpl.com (#current element) |
| S&P 500 10Y return | `sp500` | yfinance (`^GSPC`, 11y monthly) → FRED CSV (`SP500`) |
| M2 10Y growth | `m2` | FRED CSV (`M2SL`) |

## How `patch_html` works

`patch_html(values, month_year)` takes only the keys that were successfully fetched — failed fetches are excluded from `values` and the existing HTML value is left untouched. Each key updates two regex targets: the ticker `<strong>` tag and the prose sentence in the Page 1 body.

Regex patterns (in `update_market_pulse.py`):
- Buffett ticker: `(BUFFETT INDICATOR <strong>)[^<]*(</strong>)`
- Buffett body: `(sat at 230% as of December 31, 2025 and )(?:reached )?\d+% in \w+ \d{4}`
- CAPE ticker: `(SHILLER CAPE <strong>)[^<]*(</strong>)`
- CAPE body: `(was at )[\d.]+ in \w+ \d{4}`
- S&P ticker: `(S&amp;P 500 <strong>)[^<]*(</strong>)`
- S&P body: `The S&amp;P 500 rose [\d.]+% from \w+ \d{4} to \w+ \d{4}`
- M2 ticker: `(M2 GROWTH <strong>)[^<]*(</strong>)`
- M2 body: `M2 money supply rose [\d.]+% over the same period`

## Calibration anchor

The FRED-based Buffett fallback uses a known anchor to self-calibrate:

```python
_CALIB_DATE = pd.Timestamp("2025-12-31")
_CALIB_BI   = 230.0   # Buffett Indicator (%) on that date
```

**When to update it:** When you have a verified Buffett Indicator value from a known date that is more recent than the current anchor. Update both `_CALIB_DATE` and `_CALIB_BI` together. Never guess — only anchor to a value you can cite.

## Step-by-step: manual update

1. Run `python scripts/update_market_pulse.py` in an environment with internet access (not the Claude Code remote container — its egress is blocked). GitHub Actions has open access.
2. Check script log output. Any `FAILED` line means that indicator was skipped.
3. Inspect `index.html` with `git diff` to verify all 4 ticker values changed and body copy matches.
4. If a source failed permanently, update the source cascade in the script or update the calibration anchor.

## Step-by-step: fix a broken fetch

1. Identify which fetcher failed from the log (`sp500 FAILED`, `cape FAILED`, etc.).
2. Run that fetcher function in isolation with a quick Python test (e.g., `python -c "from scripts.update_market_pulse import shiller_cape; print(shiller_cape())"`).
3. If a scraper broke due to a site change, inspect the page source and update the regex pattern.
4. If the primary source for Buffett is permanently down, update `_buffett_longtermtrends` or `_buffett_cmv` and test the cascade.
5. Re-run the full script to confirm the fix.

## Do-nots

- Do not manually edit ticker values without also updating the body copy — they must stay in sync.
- Do not update the ticker in only one of the two duplicate blocks — both must match.
- Do not use API keys or paid data sources — every source must be free and key-free.
- Do not change `_CALIB_BI` without also changing `_CALIB_DATE` to match.
- Do not run the script inside the Claude Code remote container expecting network calls to succeed — egress is blocked in that environment.
