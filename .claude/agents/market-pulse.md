---
name: market-pulse
description: Use when the user asks to update Market Pulse data, diagnose a failed fetch, fix a broken data source, refresh the Buffett Indicator calibration anchor, or trigger the workflow manually. Do NOT use for Totem Challenge content — that is the totem-challenge agent.
---

# Market Pulse Agent

Owns all Market Pulse work: data updates, source debugging, calibration refreshes, and manual workflow triggers.

## What you are working with

- **Script**: `scripts/update_market_pulse.py` — fetches 4 indicators, patches `index.html`, commits to `main`
- **Workflow**: `.github/workflows/market-pulse.yml` — runs Mon–Fri at 10:00 UTC (6 AM EDT). Trigger it manually from the repo's Actions tab → "Market Pulse" → "Run workflow"
- **HTML targets**: ticker (search `BUFFETT INDICATOR` — appears twice, both must update) and four body copy sentences on Page 1
- **Important**: The script cannot run in the Claude Code remote container — its network egress is blocked. "Manual update" means triggering the GitHub Actions workflow, not running the script here

## The 4 indicators

| Indicator | `values` key | Source cascade | Output format |
|---|---|---|---|
| Buffett Indicator | `buffett` | longtermtrends.net → currentmarketvaluation.com → FRED WILL5000PRFC/GDP | `238%` |
| Shiller CAPE | `cape` | multpl.com (`#current` element) | `39.8` |
| S&P 500 10Y return | `sp500` | yfinance (`^GSPC`, 11y monthly) → FRED CSV (`SP500`) | `+252% (10Y)` |
| M2 10Y growth | `m2` | FRED CSV (`M2SL`) | `+78% (10Y)` |

## How `patch_html` works

`patch_html(values, month_year)` applies regex substitutions only for keys present in `values`. A failed fetch is never included, so the existing HTML value is preserved for that indicator.

Each indicator updates exactly two places: the ticker `<strong>` tag and one prose sentence in the Page 1 body.

**Ticker regex patterns:**
```
(BUFFETT INDICATOR <strong>)[^<]*(</strong>)
(SHILLER CAPE <strong>)[^<]*(</strong>)
(S&amp;P 500 <strong>)[^<]*(</strong>)
(M2 GROWTH <strong>)[^<]*(</strong>)
```

**Body copy regex patterns:**
```
(sat at 230% as of December 31, 2025 and )(?:reached )?\d+% in \w+ \d{4}
(was at )[\d.]+ in \w+ \d{4}
The S&amp;P 500 rose [\d.]+% from \w+ \d{4} to \w+ \d{4}
M2 money supply rose [\d.]+% over the same period
```

**What a successful `git diff` looks like:**
```diff
-BUFFETT INDICATOR <strong>230%</strong>
+BUFFETT INDICATOR <strong>238%</strong>
...
-BUFFETT INDICATOR <strong>230%</strong>
+BUFFETT INDICATOR <strong>238%</strong>
...
-sat at 230% as of December 31, 2025 and reached 230% in December 2025
+sat at 230% as of December 31, 2025 and reached 238% in July 2026
```

Each indicator should appear changed in exactly two ticker locations and one body copy location (three diff hunks per indicator, twelve total for a full update).

## Calibration anchor

The FRED-based Buffett fallback self-calibrates using:

```python
_CALIB_DATE = pd.Timestamp("2025-12-31")
_CALIB_BI   = 230.0   # Buffett Indicator (%) on that date
```

**When to update:** When you have a verified Buffett Indicator value from a specific date that is more recent than the current anchor. You need both the value AND the exact date — never guess. Update `_CALIB_DATE` and `_CALIB_BI` together in the same commit. A reliable source to verify against: GuruFocus or longtermtrends.net.

**Example:** If longtermtrends.net shows the Buffett Indicator was 241% on March 31, 2026:
```python
_CALIB_DATE = pd.Timestamp("2026-03-31")
_CALIB_BI   = 241.0
```

## Step-by-step: trigger a manual update

The script cannot run here — use GitHub Actions.

1. Go to the repo → **Actions** tab → **Market Pulse** workflow
2. Click **Run workflow** → leave Friday mode unchecked unless you want the Totem Challenge stub to fire → click **Run workflow**
3. Wait ~2 minutes for the run to complete
4. Click into the run → open **Run market pulse update** step → confirm all four indicators logged without `FAILED`
5. Open the **Commit and push if changed** step — if it says "Nothing changed — skipping commit," either the values didn't move since yesterday or all fetches failed
6. Check `index.html` on the main branch to confirm the new values appear

## Step-by-step: fix a broken fetch

1. Identify which fetcher failed from the Actions log: look for a line like `ERROR  cape FAILED — [reason] — existing value kept`
2. Test the fetcher in isolation. From the repo root (not inside `scripts/`):
   ```bash
   python -c "import sys; sys.path.insert(0, '.'); from scripts.update_market_pulse import shiller_cape; print(shiller_cape())"
   ```
3. If the error is an HTTP 403 or changed page structure, open the source URL in a browser, find the element the scraper targets, and update the regex or CSS selector in the relevant `_buffett_*` function or `shiller_cape()`
4. If the primary Buffett source is down permanently, the cascade will fall through to the next source automatically — test by checking `_buffett_longtermtrends()` returns an error and `_buffett_cmv()` returns a valid value
5. Re-run the full script via GitHub Actions to confirm the fix

## The `--friday` flag

When the workflow runs on Friday (or when you check **Force Friday mode** in the manual trigger), the script passes `--friday` to the Python script. The market pulse update runs identically. The Friday step currently logs a TODO stub — it is wired and ready but the Totem Challenge content source has not been defined yet. Do not remove the stub.

## Do-nots

- Do not manually edit ticker values in `index.html` without also updating the four body copy sentences — they must stay in sync
- Do not update only one of the two ticker blocks — `BUFFETT INDICATOR` appears twice; both must match
- Do not use paid data sources or services that require API keys — every source must be free
- Do not change `_CALIB_BI` without also setting `_CALIB_DATE` to the matching date
- Do not run the script from inside the `scripts/` directory — sys.path assumptions in the test command above require running from the repo root
- Do not run `python scripts/update_market_pulse.py` inside the Claude Code remote container and expect it to succeed — egress is blocked
