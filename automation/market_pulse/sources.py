"""Data fetchers for the Market Pulse newsletter.

Free sources, no paid plans required:
  * Stooq      - indices, futures, FX-quoted metals (no key)
  * CoinGecko  - crypto spot + 24h change (no key)
  * FRED       - Treasury yields, mortgage rate (free key: FRED_API_KEY)

Every fetch is best-effort: a failure for one metric returns ``None`` for that
metric and is logged, so a single dead symbol never sinks the whole run. The
caller (generate.py) falls back to overrides.yaml for anything that comes back
empty.
"""
from __future__ import annotations

import csv
import io
import logging
import os
from typing import Optional

import requests

from . import config

log = logging.getLogger("market_pulse.sources")

HTTP_TIMEOUT = 20
USER_AGENT = "TotemLCG-MarketPulse/1.0 (+https://github.com/navajosouljah/TotemLCG)"


def _get(url: str, **kwargs) -> requests.Response:
    headers = kwargs.pop("headers", {})
    headers.setdefault("User-Agent", USER_AGENT)
    resp = requests.get(url, timeout=HTTP_TIMEOUT, headers=headers, **kwargs)
    resp.raise_for_status()
    return resp


# ---------------------------------------------------------------------------
# Stooq: daily history CSV -> last close + % change vs prior close
# ---------------------------------------------------------------------------
def fetch_stooq(symbol: str) -> Optional[dict]:
    """Return {'value': float, 'change': float} or None.

    Uses the daily history endpoint and computes the percentage change from the
    last two available closes, which is more reliable than the snapshot feed.
    """
    url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
    try:
        text = _get(url).text
        rows = list(csv.DictReader(io.StringIO(text)))
        closes = [float(r["Close"]) for r in rows if r.get("Close") not in (None, "", "N/D")]
        if not closes:
            log.warning("stooq: no closes for %s", symbol)
            return None
        last = closes[-1]
        prev = closes[-2] if len(closes) >= 2 else last
        change = ((last - prev) / prev * 100.0) if prev else 0.0
        return {"value": last, "change": change}
    except Exception as exc:  # noqa: BLE001 - best-effort by design
        log.warning("stooq fetch failed for %s: %s", symbol, exc)
        return None


# ---------------------------------------------------------------------------
# CoinGecko: spot price + 24h change
# ---------------------------------------------------------------------------
def fetch_coingecko(ids: list[str], vs: str = config.COINGECKO_VS) -> dict:
    """Return {coingecko_id: {'value', 'change'}} for all ids in one call."""
    if not ids:
        return {}
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(ids),
        "vs_currencies": vs,
        "include_24hr_change": "true",
    }
    key = os.getenv("COINGECKO_API_KEY")
    headers = {"x-cg-demo-api-key": key} if key else {}
    out: dict = {}
    try:
        data = _get(url, params=params, headers=headers).json()
        for cid in ids:
            row = data.get(cid)
            if not row:
                continue
            out[cid] = {
                "value": row.get(vs),
                "change": row.get(f"{vs}_24h_change"),
            }
    except Exception as exc:  # noqa: BLE001
        log.warning("coingecko fetch failed: %s", exc)
    return out


# ---------------------------------------------------------------------------
# FRED: latest observation for a series
# ---------------------------------------------------------------------------
def fetch_fred(series_id: str) -> Optional[dict]:
    """Return {'value': float} (latest valid obs) or None. Requires FRED_API_KEY."""
    key = os.getenv("FRED_API_KEY")
    if not key:
        log.warning("FRED_API_KEY not set; skipping %s", series_id)
        return None
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 12,
    }
    try:
        obs = _get(url, params=params).json().get("observations", [])
        for o in obs:  # newest first; skip missing values marked "."
            if o.get("value") not in (None, "", "."):
                return {"value": float(o["value"])}
        return None
    except Exception as exc:  # noqa: BLE001
        log.warning("fred fetch failed for %s: %s", series_id, exc)
        return None


# ---------------------------------------------------------------------------
# Orchestrator: fetch every configured live metric
# ---------------------------------------------------------------------------
def fetch_all() -> dict:
    """Fetch all METRICS. Returns {metric_id: {'value','change'}} (may be partial)."""
    results: dict = {}

    # Group CoinGecko ids into a single request.
    cg_ids = [m["symbol"] for m in config.METRICS.values() if m["source"] == "coingecko"]
    cg = fetch_coingecko(cg_ids)

    for mid, meta in config.METRICS.items():
        src = meta["source"]
        if src == "stooq":
            res = fetch_stooq(meta["symbol"])
        elif src == "coingecko":
            res = cg.get(meta["symbol"])
        elif src == "fred":
            res = fetch_fred(meta["symbol"])
        else:
            res = None
        if res and res.get("value") is not None:
            results[mid] = res
        else:
            log.info("no live data for %s (%s); will use override if present", mid, src)
    return results
