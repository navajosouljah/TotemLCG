# Totem LC Group — newsletter automation

This folder holds two automations:

1. **Market Pulse** (`generate.py` + `market_pulse/`) — the weekly markets memo, below.
2. **The Totem Challenge target finder** (`totem_challenge/find_targets.py`) — every
   Wednesday, web-searches the week's most notable challenge-worthy finance figures
   and writes a ranked **Target Brief** (HTML + Markdown) to `output/` for editorial
   review. Targets are notable/contrarian finance claims *and* champions of competing
   vehicles (index funds, T-bills, private credit) that Totem can be positioned
   against. Already-covered names live in `totem_challenge/data/done.yaml`
   (seed: Jamie Dimon, Charlie Bilello) and are excluded.

   ```bash
   export ANTHROPIC_API_KEY=...        # required (uses Claude's web_search tool)
   python totem_challenge/find_targets.py --count 4
   python totem_challenge/find_targets.py --mark "Jeffrey Gundlach"   # mark covered
   ```
   Scheduled weekly via `.github/workflows/totem-challenge-targets.yml` (Wednesdays).
   The brief is committed for review; nothing publishes automatically.

   **What a brief looks like** — `output/totem_challenge_targets_<date>.{html,md}`, a
   ranked list. Each candidate carries: `name`, `title`, the specific recent
   `claim` (with what/when), a one-line `totem_angle` (how Totem's insured PO
   structure answers it), a `category` (`notable_claim` or `champions_alternative`),
   a `notability` 1–10, and live `sources`. Example top entry:

   > **#1 Jeffrey Gundlach** — DoubleLine CEO · notable claim · 9/10
   > **Claim:** Publicly warning on private-credit opacity and unrealized losses (this week).
   > **Totem angle:** Totem's contracted, Allianz-insured, transaction-level PO structure is a direct answer to exactly the opacity he's flagging.
   > **Sources:** [link], [link]

## Guardrails (read before running or publishing)

**Do**
- Keep the manual figures in `overrides.yaml` current — they're the numbers no
  free feed exposes, and stale ones are the #1 source of a wrong issue.
- Review every generated issue/brief in `output/` before it goes out. These are
  drafts, not sends.
- Add a Totem Challenge name to `done.yaml` **only after** it actually ships.

**Don't**
- **Never invent numbers, tickers, quotes, or events.** If a live feed is down,
  fall back to `overrides.yaml` or leave it — do not fabricate.
- **Never publish a Totem Challenge target without verifying the claim and its
  source URL by hand.** We name real people; a misquote is a legal/reputational
  problem, not a typo.
- **Never commit secrets.** API keys live in env vars / Actions secrets only.
- **Never hand-edit files in `output/`** — they're regenerated and your edits are
  lost. Change the source (`overrides.yaml`, templates, config) instead.
- Nothing in `automation/` sends email or posts anywhere. Publishing is a
  separate, human step.

---

# Market Pulse — markets memo

Regenerates the Totem LC Group **Market Pulse** weekly markets memo. It fetches
live market data from free APIs, merges in the hand-curated stats that no free
API exposes, optionally writes the editorial narrative with Claude, and renders
the house-styled HTML (and optionally a PDF) — the same layout as
`market_pulse_june2_2026.html`.

## What's automated vs. manual

| Section | Source |
| --- | --- |
| Stock Market (S&P, Dow, Nasdaq, Russell, VIX) | **Live** — Stooq |
| Energy oil (WTI, Brent) | **Live** — Stooq |
| Commodities (gold, silver, copper, corn, soybeans, cattle) | **Live** — Stooq |
| Crypto (BTC, ETH, SOL, XRP) | **Live** — CoinGecko |
| Around the World (Japan, China) | **Live** — Stooq |
| Interest Rates (2y/10y/30y, 30y mortgage) | **Live** — FRED (free key) |
| Fed policy rate, Savings & CD, gas prices, Crop, Real Estate, Household Finance, Europe/EM, Upcoming Events | **Manual** — `data/overrides.yaml` |
| News headlines, Quick Read, section intros, "Bottom Line" bullets | **Claude** (optional) or `overrides.yaml` fallbacks |

The manual figures are the ones with no clean free feed (foreclosure filings,
BNPL late rates, USDA crop progress, CD specials, the events calendar). Update
those in `overrides.yaml` each week; everything else fills itself in.

## Setup

```bash
cd automation
pip install -r requirements.txt          # core: requests, PyYAML, Jinja2
# optional narrative:  pip install anthropic
# optional PDF:        pip install playwright && playwright install chromium
```

### API keys (all free)

| Variable | Needed for | Get one |
| --- | --- | --- |
| `FRED_API_KEY` | Treasury yields + mortgage rate | https://fred.stlouisfed.org/docs/api/api_key.html |
| `ANTHROPIC_API_KEY` | LLM-written narrative (optional) | https://console.anthropic.com |
| `COINGECKO_API_KEY` | optional; raises CoinGecko rate limits | https://www.coingecko.com/en/api |

Stooq and CoinGecko need no key. Without `FRED_API_KEY` the rates section falls
back to `overrides.yaml`; without `ANTHROPIC_API_KEY` the prose falls back too.

> **Network note:** the data hosts (`stooq.com`, `api.coingecko.com`,
> `api.stlouisfed.org`, `api.anthropic.com`) must be reachable. On a restricted
> egress allowlist, add them first. GitHub Actions runners have open egress.

## Usage

```bash
python generate.py                    # today's week -> output/market_pulse_<monday>.html
python generate.py --date 2026-06-02  # masthead uses that week's Monday
python generate.py --pdf              # also write a PDF (needs playwright)
python generate.py --no-narrative     # skip the LLM, use overrides.yaml prose
python generate.py --no-fetch         # fully offline; reproduces the seeded sample
python generate.py --output path.html
```

`python generate.py --no-fetch --no-narrative` reproduces the seeded Week of
June 2, 2026 issue — a good smoke test.

## Weekly workflow

1. Edit `data/overrides.yaml`: refresh the manual `lines`, the `events` list,
   and (if the LLM is off) the `intro` / `bottom_line` prose.
2. `python generate.py --pdf`
3. Review `output/`, then send.

## Scheduled runs

`.github/workflows/market-pulse.yml` runs every Monday (11:00 UTC) and on
demand, committing the rendered issue to `automation/output/`. Add
`FRED_API_KEY`, `ANTHROPIC_API_KEY`, and optionally `COINGECKO_API_KEY` as repo
**Actions secrets**.

## Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| Rates section shows fallback values | `FRED_API_KEY` missing or FRED unreachable → set the key, or accept the `overrides.yaml` fallback. |
| Prose is generic / from overrides | `ANTHROPIC_API_KEY` missing or `anthropic` not installed → set the key and `pip install anthropic`, or you ran `--no-narrative`. |
| A live number looks stale | Stooq/CoinGecko throttled or returned nothing; the fetch is best-effort and falls back. Re-run, or update `overrides.yaml`. |
| Totem Challenge job fails immediately | `ANTHROPIC_API_KEY` not set — this tool has no offline mode by design. |
| Same target keeps appearing | It isn't in `done.yaml` yet. Run `find_targets.py --mark "Name"` after you publish. |
| PDF step fails | `playwright install chromium` not run, or no headless deps on the box. |

To reproduce a known-good baseline offline: `python generate.py --no-fetch --no-narrative`.

## Layout

```
automation/
├── generate.py                 # CLI orchestrator: fetch -> merge -> narrate -> render
├── requirements.txt
├── data/overrides.yaml         # manual figures + narrative fallbacks (edit weekly)
├── output/                     # generated issues
└── market_pulse/
    ├── config.py               # metrics (symbols, formatting, polarity) + section layout
    ├── sources.py              # Stooq / CoinGecko / FRED fetchers (best-effort)
    ├── narrative.py            # Claude narrative (prompt-cached) + graceful fallback
    ├── render.py               # value/colour formatting + Jinja context
    └── templates/newsletter.html.j2
```

### Adding or changing a metric

Add an entry to `METRICS` in `config.py` (label, `source`, `symbol`, `fmt`,
`polarity`) and list its id in the relevant `SECTIONS` entry. `polarity` is
`GOOD` (a rise is favourable → green) or `BAD` (a rise is unfavourable → red),
which is what drives the up/down-green/red colour on the change figure.
