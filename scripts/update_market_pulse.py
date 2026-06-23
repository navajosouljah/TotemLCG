#!/usr/bin/env python3
"""
scripts/update_market_pulse.py

Fetches current market data and updates the Market Pulse ticker
and supporting body copy in index.html.

Runs automatically via GitHub Actions (see .github/workflows/market-pulse.yml):
  Mon–Thu : market pulse only
  Fri     : market pulse + Totem Challenge stub (--friday flag)

All data sources are free and require no API keys:
  S&P 500    : Yahoo Finance via yfinance (falls back to FRED public CSV)
  M2 growth  : FRED public CSV (M2SL)
  Shiller CAPE : multpl.com
  Buffett Ind : longtermtrends.net scrape → currentmarketvaluation.com → FRED calc
"""

import re
import sys
import logging
import argparse
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

# Calibration anchor used by the FRED-based Buffett Indicator fallback.
# Update this when you want to re-anchor the estimate to a more recent known value.
_CALIB_DATE = pd.Timestamp("2025-12-31")
_CALIB_BI   = 230.0   # Buffett Indicator (%) on that date


# ── Fetchers ──────────────────────────────────────────────────────────────────

def sp500_10y() -> float:
    """S&P 500 trailing 10-year price return (%). Tries yfinance, falls back to FRED."""
    try:
        hist = yf.Ticker("^GSPC").history(period="11y", interval="1mo")
        if hist.empty:
            raise RuntimeError("empty response")
        if hist.index.tz is not None:
            hist.index = hist.index.tz_convert("UTC").tz_localize(None)
        return _10y_pct(hist, "Close")
    except Exception as exc:
        log.warning(f"yfinance failed ({exc}) — falling back to FRED SP500")
        return _10y_pct(_fred_csv("SP500"), "SP500")


def m2_10y() -> float:
    """M2 money supply trailing 10-year growth (%) via FRED public CSV."""
    return _10y_pct(_fred_csv("M2SL"), "M2SL")


def shiller_cape() -> float:
    """Current Shiller CAPE from multpl.com."""
    r = requests.get("https://www.multpl.com/shiller-pe", headers=_HEADERS, timeout=15)
    r.raise_for_status()
    el = BeautifulSoup(r.text, "html.parser").find(id="current")
    if not el:
        raise ValueError("multpl.com: #current element not found")
    m = re.search(r"([\d.]+)", el.get_text())
    if not m:
        raise ValueError("multpl.com: no number in #current")
    return float(m.group(1))


def buffett() -> float:
    """
    Buffett Indicator (%). Cascades through three sources:
      1. longtermtrends.net  (scraped)
      2. currentmarketvaluation.com  (scraped)
      3. FRED WILL5000PRFC / GDP  (calculated, self-calibrated to _CALIB_DATE)
    """
    for fn in (_buffett_longtermtrends, _buffett_cmv, _buffett_calc):
        try:
            val = fn()
            if 100 < val < 500:
                log.info(f"  Buffett via {fn.__name__}: {val}%")
                return round(val, 1)
        except Exception as exc:
            log.warning(f"  {fn.__name__}: {exc}")
    raise RuntimeError("all Buffett Indicator sources failed")


def _buffett_longtermtrends() -> float:
    r = requests.get(
        "https://www.longtermtrends.net/market-cap-to-gdp-the-buffett-indicator/",
        headers=_HEADERS, timeout=15,
    )
    r.raise_for_status()
    text = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True)
    for pat in [
        r"currently (?:at |)([\d.]+)\s*%",
        r"(?:Buffett Indicator|Market Cap to GDP)[^%\d]*([\d.]+)\s*%",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return float(m.group(1))
    raise ValueError("pattern not matched")


def _buffett_cmv() -> float:
    r = requests.get(
        "https://www.currentmarketvaluation.com/models/buffett-indicator.php",
        headers=_HEADERS, timeout=15,
    )
    r.raise_for_status()
    text = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True)
    for pat in [
        r"currently (?:at |)([\d.]+)\s*%",
        r"Buffett[^%\d]*([\d.]+)\s*%",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return float(m.group(1))
    raise ValueError("pattern not matched")


def _buffett_calc() -> float:
    """
    Approximates Buffett Indicator from FRED data.

    Uses Wilshire 5000 Full Cap Price Index (WILL5000PRFC) divided by US GDP,
    scaled by a factor K that is derived self-consistently from the known
    (_CALIB_DATE, _CALIB_BI) anchor so no external calibration constant is needed.
    """
    will = _fred_csv("WILL5000PRFC")
    gdp  = _fred_csv("GDP")

    will_c = will["WILL5000PRFC"].iloc[(will.index - _CALIB_DATE).abs().argmin()]
    gdp_c  = gdp["GDP"].iloc[(gdp.index   - _CALIB_DATE).abs().argmin()]
    K = _CALIB_BI / (will_c / gdp_c)   # scaling factor (dimensionless)

    return will["WILL5000PRFC"].iloc[-1] / gdp["GDP"].iloc[-1] * K


# ── Helpers ───────────────────────────────────────────────────────────────────

def _fred_csv(series: str) -> pd.DataFrame:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
    df = pd.read_csv(url, parse_dates=["DATE"]).dropna()
    return df.set_index("DATE").sort_index()


def _10y_pct(df: pd.DataFrame, col: str) -> float:
    """(latest − value 10 years prior) / value 10 years prior × 100."""
    current = df[col].iloc[-1]
    target  = df.index[-1] - pd.DateOffset(years=10)
    base    = df[col].iloc[(df.index - target).abs().argmin()]
    return round((current - base) / base * 100, 1)


# ── HTML patching ─────────────────────────────────────────────────────────────

def patch_html(values: dict, month_year: str) -> bool:
    """
    Writes updated market values into index.html.
    Only modifies keys present in `values` — failed fetches are skipped.
    Returns True if the file changed.
    """
    src = HTML.read_text("utf-8")
    out = src

    def sub(pat, repl):
        nonlocal out
        out = re.sub(pat, repl, out)

    if "buffett" in values:
        v = f"{round(values['buffett'])}%"
        sub(r'(BUFFETT INDICATOR <strong>)[^<]*(</strong>)', rf'\g<1>{v}\2')
        sub(
            r'(sat at 230% as of December 31, 2025 and )(?:reached )?\d+% in \w+ \d{4}',
            rf'\g<1>reached {v} in {month_year}',
        )

    if "cape" in values:
        v = f"{values['cape']:.1f}"
        sub(r'(SHILLER CAPE <strong>)[^<]*(</strong>)', rf'\g<1>{v}\2')
        sub(r'(was at )[\d.]+ in \w+ \d{4}', rf'\g<1>{v} in {month_year}')

    if "sp500" in values:
        pct = round(values["sp500"])
        sub(r'(S&amp;P 500 <strong>)[^<]*(</strong>)', rf'\g<1>+{pct}% (10Y)\2')
        sub(
            r'The S&amp;P 500 rose [\d.]+% from \w+ \d{4} to \w+ \d{4}',
            f'The S&amp;P 500 rose {pct}% from June 2016 to {month_year}',
        )

    if "m2" in values:
        pct = round(values["m2"])
        sub(r'(M2 GROWTH <strong>)[^<]*(</strong>)', rf'\g<1>+{pct}% (10Y)\2')
        sub(
            r'M2 money supply rose [\d.]+% over the same period',
            f'M2 money supply rose {pct}% over the same period',
        )

    if out == src:
        log.info("No changes — already up to date.")
        return False

    HTML.write_text(out, "utf-8")
    log.info("index.html updated.")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Update the Totem LCG Market Pulse.")
    ap.add_argument("--friday", action="store_true",
                    help="Friday run: market pulse + Totem Challenge")
    args = ap.parse_args()

    today      = datetime.today()
    month_year = today.strftime("%B %Y")

    log.info(f"=== Market Pulse — {today.strftime('%A, %B %d %Y')} ===")

    fetchers = {
        "sp500":   sp500_10y,
        "m2":      m2_10y,
        "cape":    shiller_cape,
        "buffett": buffett,
    }

    values = {}
    for key, fn in fetchers.items():
        try:
            values[key] = fn()
            log.info(f"  {key}: {values[key]}")
        except Exception as exc:
            log.error(f"  {key} FAILED — {exc} — existing value kept")

    if not values:
        log.error("All fetches failed. Aborting.")
        sys.exit(1)

    patch_html(values, month_year)

    if args.friday:
        log.info("=== Totem Challenge (Friday) ===")
        # TODO: implement weekly Totem Challenge content pull.
        # This runs every Friday alongside the standard market pulse.
        # Likely sources: Notion, Google Doc, or a YAML file that specifies
        # the week's featured expert and their latest analysis URL.
        log.info("  (Totem Challenge automation pending specification — see TODO above)")

    log.info("Done.")


if __name__ == "__main__":
    main()
