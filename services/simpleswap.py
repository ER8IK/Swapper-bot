import httpx
from config import SIMPLESWAP_API_KEY
import logging
import time


logger = logging.getLogger(__name__)

BASE_URL = "https://api.simpleswap.io"

NETWORKS = {
    "btc": "btc",
    "eth": "eth",
    "usdt": "eth",
    "sol": "sol",
    "bnb": "bsc",
    "trx": "trx",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _request_with_retry(method: str, url: str, retries: int = 3, **kwargs) -> dict | None:
    for attempt in range(retries):
        try:
            start = time.monotonic()
            async with httpx.AsyncClient() as client:
                resp = await client.request(method, url, timeout=10, **kwargs)
                elapsed = round((time.monotonic() - start) * 1000)
                resp.raise_for_status()
                data = resp.json()
                logger.info(f"[API] {method} {url} → {resp.status_code} ({elapsed}ms)")
                return data
        except httpx.TimeoutException:
            logger.warning(f"[API] Timeout attempt {attempt + 1} — {url}")
            if attempt == retries - 1:
                logger.error(f"[API] All {retries} attempts failed: {url}")
                return None
        except httpx.HTTPStatusError as e:
            logger.error(
                f"[API] HTTP {e.response.status_code} — {url} "
                f"| body: {e.response.text[:200]}"
            )
            return None
        except Exception as e:
            logger.error(f"[API] Request error: {e}")
            return None
    return None


def _get_network_for_ticker(ticker: str, pairs: list) -> str | None:
    key = ticker.lower()
    if key in NETWORKS:
        return NETWORKS[key]
    for p in pairs:
        if not isinstance(p, dict):
            continue
        if p.get("ticker", "").lower() == key:
            if p.get("network"):
                return p["network"]
            networks = p.get("networks")
            if isinstance(networks, list) and networks:
                return networks[0]
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def get_pairs(fixed: bool = False) -> list:
    """Get all available currencies from SimpleSwap."""
    data = await _request_with_retry(
        "GET",
        f"{BASE_URL}/v3/currencies",
        params={"api_key": SIMPLESWAP_API_KEY, "fixed": fixed},
    )
    if not data:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("result") or data.get("data") or []
    return []


async def get_estimated(
    ticker_from: str,
    network_from: str,
    ticker_to: str,
    network_to: str,
    amount: str,
    fixed: bool = False
) -> dict | None:
    try:
        ticker_from = ticker_from.lower()
        # Для фиата ВСЕГДА ставим fixed=True, так как платежные шлюзы не работают с плавающим курсом
        is_fiat = ticker_from in ["usd", "eur", "gbp"]
        if is_fiat:
            fixed = True

        params = {
            "tickerFrom": ticker_from,
            "networkFrom": network_from.lower() if network_from else "",
            "tickerTo": ticker_to.lower(),
            "networkTo": network_to.lower() if network_to else "",
            "amount": amount,
            "fixed": str(fixed).lower(),
        }

        data = await _request_with_retry(
            "GET",
            f"{BASE_URL}/v3/estimates",
            params=params,
            headers={"x-api-key": SIMPLESWAP_API_KEY},
        )

        # Если API выдало ошибку (например, из-за лимита), мы увидим это в логах
        if not data or "result" not in data:
            logger.error(f"QUOTE ERROR: {data}") # Смотри сюда в терминале!
            return None

        result = data["result"]
        estimated = result.get("estimatedAmount") or result.get("amountTo") or result.get("estimatedAmountTo")

        if estimated is None:
            return None

        return {
            "estimatedAmountTo": float(estimated),
            "rateId": result.get("rateId"),
        }

    except Exception as e:
        logger.error(f"get_estimated error: {e}")
        return None


async def create_exchange(
    ticker_from: str,
    network_from: str,
    ticker_to: str,
    network_to: str,
    amount: str,
    address_to: str,
    fixed: bool = False,
    rate_id: str | None = None,
) -> dict | None:
    payload = {
        "tickerFrom": ticker_from,
        "networkFrom": network_from,
        "tickerTo": ticker_to,
        "networkTo": network_to,
        "amount": amount,
        "addressTo": address_to,
        "fixed": fixed,
    }
    if rate_id:
        payload["rateId"] = rate_id

    data = await _request_with_retry(
        "POST",
        f"{BASE_URL}/v3/exchanges",
        json=payload,
        headers={"x-api-key": SIMPLESWAP_API_KEY},
    )

    if not data:
        return None

    if isinstance(data, dict) and isinstance(data.get("result"), dict):
        return data["result"]

    return data


async def get_exchange(public_id: str) -> dict | None:
    """Get exchange status by ID."""
    data = await _request_with_retry(
        "GET",
        f"{BASE_URL}/v3/exchanges/{public_id}",
        headers={"x-api-key": SIMPLESWAP_API_KEY},
    )

    if not data:
        return None

    if isinstance(data, dict) and isinstance(data.get("result"), dict):
        return data["result"]

    return data