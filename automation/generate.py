#!/usr/bin/env python3
"""Generate the Totem LC Group "Market Pulse" newsletter.

Pipeline:
  1. Fetch live market data from free APIs (Stooq / CoinGecko / FRED).
  2. Merge in manual figures from data/overrides.yaml (the stats no free API
     exposes: foreclosures, BNPL, crop progress, CD specials, upcoming events).
  3. Write the editorial narrative with Claude (optional; falls back to the
     intros / bottom lines in overrides.yaml when no ANTHROPIC_API_KEY).
  4. Render to HTML matching the house template, and optionally a PDF.

Usage:
  python generate.py                         # -> output/market_pulse_<date>.html
  python generate.py --date 2026-06-02       # date shown in the masthead (Monday of the week)
  python generate.py --no-narrative          # skip the LLM, use overrides text
  python generate.py --pdf                   # also render a PDF (needs playwright)
  python generate.py --output path.html
"""
from __future__ import annotations

import argparse
import datetime as dt
import logging
import sys
from pathlib import Path

import yaml

# Allow running as a plain script (python generate.py) or as a module.
sys.path.insert(0, str(Path(__file__).parent))
from market_pulse import narrative, render, sources  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("market_pulse")

HERE = Path(__file__).parent
DEFAULT_OVERRIDES = HERE / "data" / "overrides.yaml"
OUTPUT_DIR = HERE / "output"

FOOTER_LEGAL_TMPL = (
    "A free weekly snapshot for the Totem community. General information only — "
    "not investment advice or a recommendation to buy or sell anything. Figures "
    "reflect the latest readings available as of {as_of} and may change."
)


def monday_of_week(d: dt.date) -> dt.date:
    return d - dt.timedelta(days=d.weekday())


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Generate the Market Pulse newsletter.")
    p.add_argument("--date", help="Reference date (YYYY-MM-DD); masthead uses that week's Monday. Default: today.")
    p.add_argument("--overrides", default=str(DEFAULT_OVERRIDES), help="Path to overrides.yaml.")
    p.add_argument("--output", help="Output HTML path. Default: output/market_pulse_<date>.html")
    p.add_argument("--no-narrative", action="store_true", help="Skip LLM narrative; use overrides text.")
    p.add_argument("--no-fetch", action="store_true", help="Skip live fetch; use overrides only (offline/test).")
    p.add_argument("--pdf", action="store_true", help="Also render a PDF (requires playwright + chromium).")
    return p.parse_args(argv)


def load_overrides(path: str) -> dict:
    f = Path(path)
    if not f.exists():
        log.warning("overrides file %s not found; continuing with live data only", path)
        return {}
    with open(f, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def render_pdf(html_path: Path) -> Path | None:
    """Render <name>.pdf next to the HTML using Playwright's headless Chromium."""
    pdf_path = html_path.with_suffix(".pdf")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log.warning("playwright not installed; skipping PDF. `pip install playwright && playwright install chromium`")
        return None
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
            page.pdf(path=str(pdf_path), format="A4", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            browser.close()
        return pdf_path
    except Exception as exc:  # noqa: BLE001
        log.warning("PDF render failed: %s", exc)
        return None


def main(argv=None) -> int:
    args = parse_args(argv)

    ref = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    monday = monday_of_week(ref)
    date_str = "Week of " + monday.strftime("%A, %B ") + str(monday.day) + monday.strftime(", %Y")
    as_of = (monday + dt.timedelta(days=1)).strftime("%B ") + str((monday + dt.timedelta(days=1)).day) + ", " + str(monday.year)

    overrides = load_overrides(args.overrides)

    live = {} if args.no_fetch else sources.fetch_all()
    log.info("live metrics fetched: %d/%d", len(live), len(sources.config.METRICS))

    # Narrative falls back to overrides.yaml text when disabled or no API key.
    nar = {} if args.no_narrative else narrative.generate(
        live=live, overrides=overrides, date_str=date_str)

    context = render.build_context(
        date_str=date_str,
        live=live,
        overrides=overrides,
        narrative=nar,
        footer_legal=FOOTER_LEGAL_TMPL.format(as_of=as_of),
    )
    html = render.render_html(context)

    out = Path(args.output) if args.output else OUTPUT_DIR / f"market_pulse_{monday.isoformat()}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    log.info("wrote %s", out)

    if args.pdf:
        pdf = render_pdf(out)
        if pdf:
            log.info("wrote %s", pdf)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
