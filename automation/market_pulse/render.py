"""Render the assembled data + narrative into the Market Pulse HTML."""
from __future__ import annotations

import logging
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config

log = logging.getLogger("market_pulse.render")

TEMPLATE_DIR = Path(__file__).parent / "templates"


# ---------------------------------------------------------------------------
# Value + change formatting
# ---------------------------------------------------------------------------
def format_value(value: float, fmt: str) -> str:
    if value is None:
        return "—"
    if fmt == "int":
        return f"{value:,.0f}"
    if fmt == "num2":
        return f"{value:,.2f}"
    if fmt == "usd2":
        return f"${value:,.2f}"
    if fmt == "usd_int":
        return f"${value:,.0f}"
    if fmt == "pct":
        return f"{value:.2f}%"
    return f"{value}"


def format_change(change: float) -> str:
    """'+0.13%' / '−0.70%' using a real minus sign to match the house style."""
    if change is None:
        return ""
    sign = "+" if change >= 0 else "−"  # U+2212 minus
    return f"{sign}{abs(change):.2f}%"


def change_class(change: float, polarity: str) -> str:
    """Map sign + editorial polarity to one of up/down-green/red.

    Favourable move -> green, unfavourable -> red. For a GOOD-polarity metric a
    rise is favourable; for a BAD-polarity metric a rise is unfavourable.
    """
    up = change >= 0
    if polarity == config.GOOD:
        favourable = up
    else:  # BAD
        favourable = not up
    colour = "green" if favourable else "red"
    arrow = "up" if up else "down"
    return f"{arrow}-{colour}"


def build_metric_line(mid: str, data_point: dict) -> dict:
    meta = config.METRICS[mid]
    value_str = format_value(data_point.get("value"), meta["fmt"])
    line = {"label": meta["label"], "value": value_str, "change": "", "cls": ""}
    if not meta.get("no_change") and data_point.get("change") is not None:
        line["change"] = format_change(data_point["change"])
        line["cls"] = change_class(data_point["change"], meta["polarity"])
    return line


# ---------------------------------------------------------------------------
# Assemble the full template context
# ---------------------------------------------------------------------------
def build_context(*, date_str, live, overrides, narrative, footer_legal) -> dict:
    """Merge live metrics, manual overrides, and narrative into one context.

    Precedence for a metric value: live data -> override line. Narrative
    (intros / bottom lines / news / quick read) comes from ``narrative`` which
    may itself be sourced from the LLM or from overrides fallbacks.
    """
    ov_sections = overrides.get("sections", {})
    nar_sections = narrative.get("sections", {})

    sections = []
    for sdef in config.SECTIONS:
        sid = sdef["id"]
        ov = ov_sections.get(sid, {})
        nar = nar_sections.get(sid, {})

        lines: list[dict] = []
        # Optional override lines that come *before* the live metrics.
        if sdef.get("prepend_override_lines"):
            lines.extend(ov.get("lines", []))

        # Live metric lines (fall back to an override line of the same id).
        for mid in sdef.get("metrics", []):
            if mid in live:
                lines.append(build_metric_line(mid, live[mid]))
            else:
                fb = (ov.get("metric_fallbacks") or {}).get(mid)
                if fb:
                    lines.append(fb)
                else:
                    log.warning("metric %s missing and no fallback in overrides", mid)

        # Sections whose body is entirely manual.
        if sdef.get("override_lines"):
            lines.extend(ov.get("lines", []))
        # Optional override lines appended *after* the live metrics.
        if sdef.get("append_override_lines"):
            lines.extend(ov.get("lines", []))

        sections.append({
            "id": sid,
            "title": sdef["title"],
            "intro": nar.get("intro") or ov.get("intro", ""),
            "lines": lines,
            "bottom_line": nar.get("bottom_line") or ov.get("bottom_line", []),
        })

    return {
        "date_str": date_str,
        "news_intro": narrative.get("news_intro") or overrides.get("news_intro", ""),
        "news": narrative.get("news") or overrides.get("news", []),
        "quick_read": narrative.get("quick_read") or overrides.get("quick_read", []),
        "sections": sections,
        "events_intro": overrides.get("events_intro", ""),
        "events": overrides.get("events", []),
        "footer_legal": footer_legal,
    }


def render_html(context: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=False,
        lstrip_blocks=False,
    )
    return env.get_template("newsletter.html.j2").render(**context)
