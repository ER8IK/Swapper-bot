# Все доступные валюты и их настройки

CRYPTO_CURRENCIES = [
    {"ticker": "btc",      "network": "btc",   "label": "BTC",           "min": 0.0001},
    {"ticker": "eth",      "network": "eth",   "label": "ETH",           "min": 0.005},
    {"ticker": "usdt",     "network": "trx",   "label": "USDT (TRC20)",  "min": 1.0},
    {"ticker": "usdt",     "network": "eth",   "label": "USDT (ERC20)",  "min": 10.0},
    {"ticker": "sol",      "network": "sol",   "label": "SOL",           "min": 0.1},
    {"ticker": "bnb",      "network": "bsc",   "label": "BNB",           "min": 0.01},
    {"ticker": "trx",      "network": "trx",   "label": "TRX",           "min": 50.0},
]

FIAT_CURRENCIES = [
    {"ticker": "usd", "network": "usd", "label": "💵 USD", "min": 20.0},
    {"ticker": "eur", "network": "eur", "label": "💶 EUR", "min": 20.0},
]

# Словарь для быстрого поиска сети по тикеру (первая попавшаяся)
NETWORK_MAP: dict[str, str] = {}
for c in CRYPTO_CURRENCIES + FIAT_CURRENCIES:
    key = f"{c['ticker']}_{c['network']}"
    NETWORK_MAP[key] = c["network"]

# Уникальный ключ валюты: ticker + network
def currency_key(ticker: str, network: str) -> str:
    return f"{ticker}_{network}"

def get_currency(ticker: str, network: str) -> dict | None:
    for c in CRYPTO_CURRENCIES + FIAT_CURRENCIES:
        if c["ticker"] == ticker and c["network"] == network:
            return c
    return None

def get_min_amount(ticker: str, network: str) -> float:
    c = get_currency(ticker, network)
    return c["min"] if c else 0.0