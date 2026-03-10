# Crypto Price Tracker with Volatility Notifications

A lightweight Python application that polls live cryptocurrency prices and **alerts you in real time when the market is volatile** — i.e., when a coin's price swings by a configurable percentage.

## Features

- Tracks multiple coins simultaneously (Bitcoin, Ethereum, Solana, BNB, XRP by default)
- Uses the free [CoinGecko public API](https://www.coingecko.com/en/api) — no API key required
- Calculates price change between each polling cycle
- Prints a clear console alert whenever a coin's price moves ≥ the volatility threshold
- Fully configurable: coins, currency, poll interval, and alert threshold

## Requirements

- Python 3.10+
- `requests` library

```bash
pip install -r requirements.txt
```

## Usage

```bash
python crypto_tracker.py
```

The tracker will poll prices every **60 seconds** by default and print a **VOLATILITY ALERT** whenever a coin's price changes by **5% or more** since the last check.

### Customise from code

```python
from crypto_tracker import run

run(
    coins=["bitcoin", "ethereum"],   # CoinGecko coin IDs
    currency="usd",                  # Target fiat currency
    interval=30,                     # Polling interval in seconds
    threshold=3.0,                   # Alert threshold in %
)
```

## Example output

```
2026-03-10 12:00:00 [INFO] BITCOIN         67432.1000 USD   (24h: +6.35%)
2026-03-10 12:00:00 [INFO] ETHEREUM         3521.8800 USD   (24h: -1.20%)

=======================================================
  🚨  VOLATILITY ALERT  🚨
  Coin    : BITCOIN
  Price   : 67,432.1000 USD
  Change  : ▲ 6.35%
  Time    : 2026-03-10 12:00:00
=======================================================
```
