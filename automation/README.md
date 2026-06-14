# Market Pulse — newsletter automation

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
