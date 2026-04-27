"""
Crypto price checker using CoinGecko free API.
No API key required.
"""

import httpx
import logging

logger = logging.getLogger(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

COIN_IDS = {
    "btc":  "bitcoin",
    "eth":  "ethereum",
    "usdt": "tether",
    "sol":  "solana",
    "bnb":  "binancecoin",
    "trx":  "tron",
}


async def get_prices() -> dict | None:
    """Fetch current prices in USD for all supported coins."""
    try:
        ids = ",".join(COIN_IDS.values())
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                COINGECKO_URL,
                params={
                    "ids":            ids,
                    "vs_currencies":  "usd",
                    "include_24hr_change": "true",
                },
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()

        result = {}
        for ticker, coin_id in COIN_IDS.items():
            if coin_id in data:
                result[ticker] = {
                    "usd":    data[coin_id].get("usd", 0),
                    "change": data[coin_id].get("usd_24h_change", 0),
                }
        return result
    except Exception as e:
        logger.error(f"get_prices error: {e}")
        return None


def format_prices(prices: dict) -> str:
    """Format prices dict into readable message."""
    LABELS = {
        "btc":  "Bitcoin (BTC)",
        "eth":  "Ethereum (ETH)",
        "usdt": "Tether (USDT)",
        "sol":  "Solana (SOL)",
        "bnb":  "BNB",
        "trx":  "Tron (TRX)",
    }
    lines = ["💹 <b>Crypto prices (USD)</b>\n"]
    for ticker, data in prices.items():
        label  = LABELS.get(ticker, ticker.upper())
        price  = data["usd"]
        change = data["change"]
        arrow  = "📈" if change >= 0 else "📉"
        sign   = "+" if change >= 0 else ""
        lines.append(
            f"{arrow} <b>{label}</b>\n"
            f"   ${price:,.4f}  ({sign}{change:.2f}%)\n"
        )
    lines.append("\n<i>Source: CoinGecko · Updates on request</i>")
    return "\n".join(lines)