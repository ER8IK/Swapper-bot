import httpx
from config import SIMPLESWAP_API_KEY
import logging

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
    """Make an HTTP request with retry on timeout."""
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.request(method, url, timeout=10, **kwargs)
                resp.raise_for_status()
                return resp.json()
        except httpx.TimeoutException:
            logger.warning(f"Timeout on attempt {attempt + 1} for {url}")
            if attempt == retries - 1:
                logger.error(f"All {retries} attempts failed (timeout): {url}")
                return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} for {url}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Request error: {e}")
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
    ticker_to: str,
    amount: str,
    fixed: bool = False
) -> dict | None:
    """Get exchange quote from SimpleSwap."""
    try:
        pairs = await get_pairs()
        network_from = _get_network_for_ticker(ticker_from, pairs)
        network_to = _get_network_for_ticker(ticker_to, pairs)

        if not network_from or not network_to:
            logger.error(f"Unknown network for {ticker_from} or {ticker_to}")
            return None

        data = await _request_with_retry(
            "GET",
            f"{BASE_URL}/v3/estimates",
            params={
                "tickerFrom": ticker_from,
                "networkFrom": network_from,
                "tickerTo": ticker_to,
                "networkTo": network_to,
                "amount": amount,
                "fixed": fixed,
            },
            headers={"x-api-key": SIMPLESWAP_API_KEY},
        )

        if not data:
            return None

        result = data.get("result") if isinstance(data, dict) else None
        if not result or not isinstance(result, dict):
            logger.error(f"Unexpected estimate response: {data}")
            return None

        estimated = result.get("estimatedAmount") or result.get("estimated")
        if estimated is None:
            logger.error(f"No estimated amount in response: {result}")
            return None

        return {
            "estimatedAmountTo": float(estimated),
            "rateId": result.get("rateId"),
            "validUntil": result.get("validUntil"),
        }

    except Exception as e:
        logger.error(f"get_estimated error: {e}")
        return None


async def create_exchange(
    ticker_from: str,
    ticker_to: str,
    amount: str,
    address_to: str,
    fixed: bool = False,
    rate_id: str | None = None,
) -> dict | None:
    """Create an exchange on SimpleSwap."""
    network_from = NETWORKS.get(ticker_from.lower())
    network_to = NETWORKS.get(ticker_to.lower())

    if not network_from or not network_to:
        logger.error(f"Unknown network for {ticker_from} or {ticker_to}")
        return None

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