"""Configuration for the Market Pulse newsletter generator.

Defines every live-fetched metric (label, formatting, source symbol, and
editorial polarity) plus the ordered section layout. Anything that cannot be
pulled from a free API lives in ``data/overrides.yaml`` instead.
"""

# Editorial polarity controls the colour of the change figure.
#   GOOD  -> a rise is favourable (green when up, red when down)   e.g. an index
#   BAD   -> a rise is unfavourable (red when up, green when down)  e.g. VIX, oil
GOOD = "good"
BAD = "bad"

# ---------------------------------------------------------------------------
# Live metrics. Each entry:
#   source : "stooq" | "coingecko" | "fred"
#   symbol : provider-specific identifier
#   fmt    : how to render the value (see render.format_value)
#   polarity, label
# ---------------------------------------------------------------------------
METRICS = {
    # --- Stock Market (Stooq daily history, % change vs prior close) ---
    "sp500":   {"label": "S&P 500",                "source": "stooq", "symbol": "^spx",   "fmt": "int",   "polarity": GOOD},
    "dow":     {"label": "Dow Jones",              "source": "stooq", "symbol": "^dji",   "fmt": "int",   "polarity": GOOD},
    "nasdaq":  {"label": "Nasdaq",                 "source": "stooq", "symbol": "^ndq",   "fmt": "int",   "polarity": GOOD},
    "russell": {"label": "Russell 2000 (small caps)", "source": "stooq", "symbol": "^rut", "fmt": "int", "polarity": GOOD},
    "vix":     {"label": "Fear gauge (VIX)",       "source": "stooq", "symbol": "^vix",   "fmt": "num2", "polarity": BAD},

    # --- Energy (Stooq futures) ---
    "wti":     {"label": "WTI oil / barrel",       "source": "stooq", "symbol": "cl.f",   "fmt": "usd2", "polarity": BAD},
    "brent":   {"label": "Brent oil / barrel",     "source": "stooq", "symbol": "cb.f",   "fmt": "usd2", "polarity": BAD},

    # --- Commodities (Stooq) ---
    "gold":    {"label": "Gold / oz",              "source": "stooq", "symbol": "xauusd", "fmt": "usd_int", "polarity": GOOD},
    "silver":  {"label": "Silver / oz",            "source": "stooq", "symbol": "xagusd", "fmt": "usd2",    "polarity": GOOD},
    "copper":  {"label": "Copper / lb",            "source": "stooq", "symbol": "hg.f",   "fmt": "usd2",    "polarity": GOOD},
    "corn":    {"label": "Corn / bushel",          "source": "stooq", "symbol": "zc.f",   "fmt": "usd2",    "polarity": GOOD},
    "soybeans":{"label": "Soybeans / bushel",      "source": "stooq", "symbol": "zs.f",   "fmt": "usd2",    "polarity": GOOD},
    "cattle":  {"label": "Cattle / lb (live)",     "source": "stooq", "symbol": "le.f",   "fmt": "usd2",    "polarity": BAD},

    # --- Crypto (CoinGecko, 24h change) ---
    "btc":     {"label": "Bitcoin (BTC)", "source": "coingecko", "symbol": "bitcoin",  "fmt": "usd_int", "polarity": GOOD},
    "eth":     {"label": "Ethereum (ETH)","source": "coingecko", "symbol": "ethereum", "fmt": "usd_int", "polarity": GOOD},
    "sol":     {"label": "Solana",        "source": "coingecko", "symbol": "solana",   "fmt": "usd2",    "polarity": GOOD},
    "xrp":     {"label": "XRP",           "source": "coingecko", "symbol": "ripple",   "fmt": "usd2",    "polarity": GOOD},

    # --- Around the World (Stooq) ---
    "nikkei":  {"label": "Japan", "source": "stooq", "symbol": "^nkx",   "fmt": "int", "polarity": GOOD},
    "ftse":    {"label": "FTSE 100", "source": "stooq", "symbol": "^ukx", "fmt": "int", "polarity": GOOD},
    "shanghai":{"label": "China", "source": "stooq", "symbol": "^shc",   "fmt": "int", "polarity": GOOD},

    # --- Interest Rates (FRED, latest level; no change shown) ---
    "ust2":    {"label": "2-year Treasury",  "source": "fred", "symbol": "DGS2",       "fmt": "pct", "polarity": GOOD, "no_change": True},
    "ust10":   {"label": "10-year Treasury", "source": "fred", "symbol": "DGS10",      "fmt": "pct", "polarity": GOOD, "no_change": True},
    "ust30":   {"label": "30-year Treasury", "source": "fred", "symbol": "DGS30",      "fmt": "pct", "polarity": GOOD, "no_change": True},
    "mortgage30": {"label": "30-year mortgage (avg.)", "source": "fred", "symbol": "MORTGAGE30US", "fmt": "pct", "polarity": BAD, "no_change": True},
}

# CoinGecko vs_currency
COINGECKO_VS = "usd"

# ---------------------------------------------------------------------------
# Section layout. ``metrics`` lists live metric ids in display order.
# ``override`` pulls the whole section body (lines / events) from overrides.yaml.
# Narrative fields (intro, bottom_line) are written by narrative.py when an
# ANTHROPIC_API_KEY is present, otherwise taken from overrides.yaml fallbacks.
# ---------------------------------------------------------------------------
SECTIONS = [
    {"id": "stocks",    "title": "Stock Market",        "metrics": ["sp500", "dow", "nasdaq", "russell", "vix"]},
    {"id": "rates",     "title": "Interest Rates",      "metrics": ["ust2", "ust10", "ust30", "mortgage30"], "prepend_override_lines": True},
    {"id": "savings",   "title": "Savings & CD Rates",  "override_lines": True},
    {"id": "energy",    "title": "Energy & Gas Prices", "metrics": ["wti", "brent"], "append_override_lines": True},
    {"id": "commodities","title": "Commodities",        "metrics": ["gold", "silver", "copper", "corn", "soybeans", "cattle"]},
    {"id": "crop",      "title": "Crop Weather",        "override_lines": True},
    {"id": "realestate","title": "Real Estate",         "override_lines": True},
    {"id": "household", "title": "Household Finance",    "override_lines": True},
    {"id": "crypto",    "title": "Crypto",              "metrics": ["btc", "eth", "sol", "xrp"]},
    {"id": "world",     "title": "Around the World",    "metrics": ["nikkei", "shanghai"], "append_override_lines": True},
]
