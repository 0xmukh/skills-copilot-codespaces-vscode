"""
Crypto Price Tracker with Volatility Notifications

Tracks cryptocurrency prices and notifies the user when the market
is volatile with heavy price swings.
"""

import time
import logging
from datetime import datetime
from typing import Optional

import requests

# --- Configuration ---
COINS = ["bitcoin", "ethereum", "solana", "binancecoin", "ripple"]
CURRENCY = "usd"
POLL_INTERVAL_SECONDS = 60          # How often to fetch prices
VOLATILITY_THRESHOLD_PERCENT = 5.0  # Alert when price swings ≥ this %
COINGECKO_API_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
)

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def fetch_prices(coins: list[str], currency: str) -> Optional[dict]:
    """Fetch current prices from the CoinGecko public API."""
    params = {
        "ids": ",".join(coins),
        "vs_currencies": currency,
        "include_24hr_change": "true",
    }
    try:
        response = requests.get(COINGECKO_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exc:
        logger.error("Failed to fetch prices: %s", exc)
        return None


def calculate_change(old_price: float, new_price: float) -> float:
    """Return the percentage change between two prices."""
    if old_price == 0:
        return 0.0
    return ((new_price - old_price) / old_price) * 100


def notify(coin: str, price: float, change_pct: float, currency: str) -> None:
    """Print a volatility alert to the console."""
    direction = "▲" if change_pct > 0 else "▼"
    print(
        f"\n{'=' * 55}\n"
        f"  🚨  VOLATILITY ALERT  🚨\n"
        f"  Coin    : {coin.upper()}\n"
        f"  Price   : {price:,.4f} {currency.upper()}\n"
        f"  Change  : {direction} {abs(change_pct):.2f}%\n"
        f"  Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{'=' * 55}\n"
    )


def run(
    coins: list[str] = COINS,
    currency: str = CURRENCY,
    interval: int = POLL_INTERVAL_SECONDS,
    threshold: float = VOLATILITY_THRESHOLD_PERCENT,
) -> None:
    """
    Main tracking loop.

    Polls prices every `interval` seconds and triggers a notification
    whenever a coin's price moves more than `threshold` percent since
    the previous reading.
    """
    logger.info(
        "Starting crypto tracker | coins: %s | currency: %s | "
        "interval: %ds | threshold: %.1f%%",
        coins,
        currency.upper(),
        interval,
        threshold,
    )

    previous_prices: dict[str, float] = {}

    while True:
        data = fetch_prices(coins, currency)

        if data is None:
            logger.warning("Skipping this cycle due to fetch error.")
            time.sleep(interval)
            continue

        for coin in coins:
            coin_data = data.get(coin)
            if coin_data is None:
                logger.warning("No data returned for '%s', skipping.", coin)
                continue

            current_price: float = coin_data.get(currency, 0.0)
            change_24h: float = coin_data.get(f"{currency}_24h_change", 0.0) or 0.0

            logger.info(
                "%-15s %12.4f %-4s  (24h: %+.2f%%)",
                coin.upper(),
                current_price,
                currency.upper(),
                change_24h,
            )

            # Compare against our last recorded price if available
            if coin in previous_prices:
                change_pct = calculate_change(previous_prices[coin], current_price)
                if abs(change_pct) >= threshold:
                    notify(coin, current_price, change_pct, currency)
            else:
                # On first run, use the 24h change from the API as a proxy
                if abs(change_24h) >= threshold:
                    notify(coin, current_price, change_24h, currency)

            previous_prices[coin] = current_price

        logger.info("Next check in %d seconds...\n", interval)
        time.sleep(interval)


if __name__ == "__main__":
    run()
