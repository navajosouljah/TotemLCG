# CLAUDE.md — TotemLCG

Operating guide for anyone (human or Claude) working in this repo. Read it before
you touch anything under `automation/` or the workflows.

## What this repo is

The publishing engine for **Totem LC Group**'s two weekly editorial products:

- **Market Pulse** — a house-styled weekly markets memo. Live data (Stooq /
  CoinGecko / FRED) + hand-curated figures + a Claude-written narrative, rendered
  to HTML/PDF. Code: `automation/generate.py` + `automation/market_pulse/`.
- **The Totem Challenge** — a weekly issue that picks a prominent finance voice
  and positions Totem's structure against their public claim. A Wednesday job
  produces a ranked **Target Brief** for editorial review. Code:
  `automation/totem_challenge/find_targets.py`.

The public site is `index.html` / `index_1.html` at the repo root and deploys via
Vercel (previews per PR). Editorial review happens in a separate app,
`totem-editorial-review.vercel.app`, which is **backed by a different repo not in
this session** — this repo does not publish there.

**Totem's positioning (the through-line of all copy):** a contracted, insured,
transaction-level commercial-loan structure tied to verified Fortune 100 purchase
orders — principal and returns insured by Allianz; uncorrelated to public markets.
Every editorial angle contrasts that against whatever the week's target claims.

## The weekly cadence

| Day | Job | Output | Human step |
| --- | --- | --- | --- |
| Mon 11:00 UTC | `market-pulse.yml` | `automation/output/market_pulse_<mon>.{html,pdf}` | Review, then send |
| Wed 13:00 UTC | `totem-challenge-targets.yml` | `automation/output/totem_challenge_targets_<date>.{html,md}` | Pick a target, verify the claim, mark it in `done.yaml` after it ships |

Both jobs commit **only** to `automation/output/` and **never publish** — sending
is always a separate human action.

## Commands

```bash
cd automation
pip install -r requirements.txt

python generate.py                         # Market Pulse for this week -> output/
python generate.py --no-fetch --no-narrative   # offline known-good baseline (smoke test)
python generate.py --pdf                   # also render PDF (needs playwright)

python totem_challenge/find_targets.py --count 4          # this week's target brief
python totem_challenge/find_targets.py --mark "Name"      # mark a target covered (after it ships)
```

Model IDs are pinned in code and overridable by env var
(`MARKET_PULSE_MODEL`, `TOTEM_CHALLENGE_MODEL`). Default to the latest Claude
models; don't hardcode an older one.

## Guardrails — the do-nots

These are hard rules. When one conflicts with a request, stop and flag it.

1. **Never fabricate a number, ticker, quote, event, or source URL.** If a feed is
   down, fall back to `overrides.yaml` or omit — never invent. Market Pulse copy
   must use the exact figures supplied.
2. **Never publish a Totem Challenge target without a human verifying the claim
   and its live source.** We name real, prominent people. A misquote is a legal
   and reputational problem.
3. **This is general information, never investment advice.** No "buy" / "sell".
4. **Never commit secrets.** Keys live in env vars / Actions secrets only. Don't
   echo them in logs or workflow output.
5. **Never hand-edit `automation/output/`** — it's regenerated; edit the source
   (`overrides.yaml`, templates, `config.py`) instead.
6. **Automated jobs commit only `automation/output/`** — never `git add -A`, never
   push to a contributor's branch.
7. **Nothing here auto-sends or auto-posts.** Publishing is out of band.

## House voice (all editorial copy)

Plain-spoken, confident, lightly skeptical of consensus. Short declarative
sentences. Educational, never hype. The "so-what" over the restatement — tell the
reader what a number *means* for them. Use a real minus sign (−). The canonical,
machine-enforced version of this lives in `market_pulse/narrative.py`
(`SYSTEM_PROMPT`) and in the `house-style` skill (`.claude/skills/house-style/`) —
keep those three in sync if you change the voice.

**Good bottom-line bullet:** "A 30-year mortgage back near 7% means a $400k loan
costs ~$300/month more than it did in 2021 — the freeze in existing-home sales
isn't ending soon."
**Bad (restatement, no so-what):** "The 30-year mortgage rate is 6.9%, up from
last week."

## Layout

```
index.html, index_1.html      # public site (Vercel)
automation/
  generate.py                 # Market Pulse orchestrator
  totem_challenge/            # Totem Challenge target finder + templates + done.yaml
  market_pulse/               # fetchers, narrative, render, templates
  data/overrides.yaml         # manual figures + narrative fallbacks (edit weekly)
  output/                     # generated issues (do not hand-edit)
  README.md                   # detailed automation docs
.github/workflows/            # Monday + Wednesday scheduled jobs
.claude/skills/               # authored skills (see house-style)
```

See `automation/README.md` for the full data-source map, setup, and
troubleshooting.
