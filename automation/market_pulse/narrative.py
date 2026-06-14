"""Editorial narrative generation via the Claude API.

Given the week's fetched numbers and the manual context (crop, real estate,
events), Claude writes the prose Market Pulse is known for: the "This Week in
the News" headlines, "The Quick Read" paragraphs, each section's italic intro,
and the gold "BOTTOM LINE" bullets.

If ANTHROPIC_API_KEY is absent (or the call fails) we return an empty dict and
the renderer falls back to whatever intros / bottom lines exist in
overrides.yaml — so the generator still produces a complete newsletter offline.
"""
from __future__ import annotations

import json
import logging
import os

from . import config

log = logging.getLogger("market_pulse.narrative")

DEFAULT_MODEL = os.getenv("MARKET_PULSE_MODEL", "claude-sonnet-4-6")

# Stable, cacheable instruction block (kept verbatim across runs so prompt
# caching hits). The variable per-week data goes in a separate, uncached block.
SYSTEM_PROMPT = """You are the editor of "Market Pulse", a weekly markets memo from Totem LC Group.

Voice and rules:
- Plain-spoken, confident, slightly skeptical of consensus. Short declarative sentences.
- Educational, never hype. This is general information, not investment advice; never tell the reader to buy or sell.
- Use the exact figures provided. Do not invent numbers, tickers, or events.
- "Bottom line" bullets explain what a number MEANS for an ordinary investor — the so-what, not a restatement.
- Use a real minus sign (−) for negatives and keep it tight.

You will receive a JSON object with this week's data and manual context. Return ONLY a JSON object (no prose, no markdown fences) with this exact shape:
{
  "news_intro": "one short italic sentence",
  "news": [{"label": "Headline phrase", "text": "2-3 sentence explanation"}],          // 3-5 items
  "quick_read": ["paragraph", "..."],                                                    // 3-5 paragraphs
  "sections": {
    "<section_id>": {"intro": "one italic sentence", "bottom_line": ["bullet", "..."]}   // 2-4 bullets each
  }
}
Section ids you must cover: stocks, rates, savings, energy, commodities, crop, realestate, household, crypto, world.
Base every claim on the supplied data and context only."""


def _section_ids() -> list[str]:
    return [s["id"] for s in config.SECTIONS]


def generate(*, live: dict, overrides: dict, date_str: str) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.info("ANTHROPIC_API_KEY not set; using overrides.yaml narrative fallbacks")
        return {}

    try:
        import anthropic
    except ImportError:
        log.warning("anthropic SDK not installed; using narrative fallbacks")
        return {}

    # Compact, labelled view of the numbers so the model anchors on them.
    live_readable = {
        mid: {"label": config.METRICS[mid]["label"], **vals}
        for mid, vals in live.items()
    }
    payload = {
        "date": date_str,
        "live_metrics": live_readable,
        "manual_context": {
            "sections": overrides.get("sections", {}),
            "events": overrides.get("events", []),
        },
        "section_ids": _section_ids(),
    }

    client = anthropic.Anthropic(api_key=api_key)
    try:
        resp = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=4096,
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},  # cache the static instructions
            }],
            messages=[{
                "role": "user",
                "content": "Here is this week's data. Write the newsletter narrative as specified.\n\n"
                           + json.dumps(payload, indent=2),
            }],
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1].lstrip("json").strip()
        return json.loads(text)
    except Exception as exc:  # noqa: BLE001
        log.warning("narrative generation failed (%s); using fallbacks", exc)
        return {}
