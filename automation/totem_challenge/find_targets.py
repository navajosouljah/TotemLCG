#!/usr/bin/env python3
"""The Totem Challenge — weekly target finder.

Every Wednesday, search the web for the most notable, "challenge-worthy" finance
figures and claims of the week, and produce a ranked Target Brief the editorial
team can review before deciding who to run The Totem Challenge against.

"Worthy" targets (per editorial direction) are:
  1. Anyone making a notable / contrarian / viral finance claim that week, AND
  2. Figures championing a competing vehicle (index funds, T-bills, public
     equities, private credit, etc.) that Totem's insured, contracted,
     transaction-level PO structure can be positioned against.

Already-covered people (data/done.yaml) are excluded so the series keeps moving.

Requires ANTHROPIC_API_KEY (uses Claude's server-side web_search tool). There is
no offline mode — the whole point is fresh weekly research.

Usage:
  python find_targets.py                       # -> output/totem_challenge_targets_<date>.{html,md}
  python find_targets.py --date 2026-06-24
  python find_targets.py --count 5             # number of candidates
  python find_targets.py --mark "Jeffrey Gundlach"   # add a name to done.yaml and exit
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("totem_challenge")

HERE = Path(__file__).parent
DONE_FILE = HERE / "data" / "done.yaml"
TEMPLATE_DIR = HERE / "templates"
OUTPUT_DIR = HERE.parent / "output"

MODEL = os.getenv("TOTEM_CHALLENGE_MODEL", "claude-opus-4-8")

SYSTEM_PROMPT = """You are the research desk for "The Totem Challenge", a weekly issue from Totem LC Group.

Totem's product: a contracted, insured, transaction-level commercial loan structure tied to verified Fortune 100 purchase orders — pitched as having 100% of principal AND 100% of returns insured by Allianz. The Challenge picks a prominent finance voice each week and positions Totem's structure against their public claim (past targets: Jamie Dimon, Charlie Bilello).

Your job: find this week's most notable, challenge-worthy targets. A worthy target is EITHER:
  (a) someone making a notable, contrarian, or viral finance claim this week, OR
  (b) someone publicly championing a competing vehicle (index funds, T-bills, public equities, private credit, money-market funds, etc.) that Totem can contrast its insured, uncorrelated, principal-and-return-protected structure against.

Use web search to ground every candidate in something real and RECENT (ideally this week). Prefer named, prominent people with a specific, quotable claim and a live source URL. Exclude anyone in the provided "already covered" list.

For each candidate provide a sharp "totem_angle": one or two sentences on how Totem's structure answers, rebuts, or contrasts with their claim. Be concrete, not generic.

After any searching, output ONLY a single JSON object (no prose, no markdown fences) with this shape:
{
  "week_of": "<the Monday or date string you were given>",
  "recommended": "<name of your top pick>",
  "candidates": [
    {
      "name": "Full Name",
      "title": "role / why they matter",
      "claim": "the specific recent claim or stance, with what/when",
      "totem_angle": "how Totem is positioned against it",
      "category": "notable_claim | champions_alternative",
      "notability": 1-10,
      "sources": [{"title": "...", "url": "https://..."}]
    }
  ]
}
Rank candidates by notability, most notable first. Base everything on real search results only; do not fabricate quotes or URLs."""


def load_done() -> list[dict]:
    if not DONE_FILE.exists():
        return []
    data = yaml.safe_load(DONE_FILE.read_text(encoding="utf-8")) or {}
    return data.get("done", [])


def mark_done(name: str) -> None:
    data = yaml.safe_load(DONE_FILE.read_text(encoding="utf-8")) if DONE_FILE.exists() else {}
    data = data or {}
    done = data.setdefault("done", [])
    if any(d.get("name", "").lower() == name.lower() for d in done):
        log.info("%s already in done.yaml", name)
        return
    done.append({"name": name, "note": f"added {dt.date.today().isoformat()}"})
    DONE_FILE.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    log.info("added %s to done.yaml", name)


def find_targets(week_of: str, count: int, done: list[dict]) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set — this tool needs it for web search.")
        sys.exit(2)
    import anthropic

    excluded = ", ".join(d.get("name", "") for d in done) or "(none yet)"
    user_msg = (
        f"Week of: {week_of}. Find the {count} most notable, challenge-worthy targets for "
        f"The Totem Challenge this week. Already covered (exclude these): {excluded}. "
        f"Search the web for recent, specific, sourced claims, then return the JSON object."
    )

    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        tools=[{"type": "web_search_20250305", "name": "web_search", "max_uses": 6}],
        messages=[{"role": "user", "content": user_msg}],
    )
    # The final assistant text holds the JSON; search happens server-side.
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text").strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1].lstrip("json").strip()
    # Be forgiving: grab the outermost JSON object.
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        log.error("model did not return JSON:\n%s", text[:500])
        sys.exit(1)
    return json.loads(text[start : end + 1])


def render(brief: dict, week_of: str) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=True)
    return env.get_template("target_brief.html.j2").render(brief=brief, week_of=week_of)


def to_markdown(brief: dict, week_of: str) -> str:
    lines = [f"# The Totem Challenge — Target Brief", f"*Week of {week_of}*", ""]
    rec = brief.get("recommended", "")
    if rec:
        lines += [f"**Recommended target: {rec}**", ""]
    for i, c in enumerate(brief.get("candidates", []), 1):
        lines.append(f"## {i}. {c.get('name','?')} — {c.get('title','')}")
        lines.append(f"- **Claim:** {c.get('claim','')}")
        lines.append(f"- **Totem angle:** {c.get('totem_angle','')}")
        lines.append(f"- **Category:** {c.get('category','')} · **Notability:** {c.get('notability','')}/10")
        for s in c.get("sources", []):
            lines.append(f"  - [{s.get('title','source')}]({s.get('url','')})")
        lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Find weekly Totem Challenge targets.")
    p.add_argument("--date", help="Reference date (YYYY-MM-DD); default today.")
    p.add_argument("--count", type=int, default=4, help="Number of candidates (default 4).")
    p.add_argument("--mark", help="Add a name to done.yaml and exit.")
    p.add_argument("--output", help="Output base path (without extension).")
    args = p.parse_args(argv)

    if args.mark:
        mark_done(args.mark)
        return 0

    ref = dt.date.fromisoformat(args.date) if args.date else dt.date.today()
    week_of = ref.strftime("%B ") + str(ref.day) + ref.strftime(", %Y")

    done = load_done()
    log.info("excluding %d already-covered targets", len(done))
    brief = find_targets(week_of, args.count, done)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    base = Path(args.output) if args.output else OUTPUT_DIR / f"totem_challenge_targets_{ref.isoformat()}"
    html_path = base.with_suffix(".html")
    md_path = base.with_suffix(".md")
    html_path.write_text(render(brief, week_of), encoding="utf-8")
    md_path.write_text(to_markdown(brief, week_of), encoding="utf-8")
    log.info("wrote %s", html_path)
    log.info("wrote %s", md_path)
    log.info("recommended target: %s", brief.get("recommended", "(none)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
