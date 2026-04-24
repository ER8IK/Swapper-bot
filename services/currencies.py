"""
Currency helpers.

Currencies are now stored in the `currencies` DB table and managed
via the admin panel (/admin_currencies).

This module provides async helpers that read from the DB,
plus sync fallbacks for places that still need them.
"""

from database.db import get_currencies as _get_currencies_db


# ── Async helpers (use these in handlers) ─────────────────────────────────────

async def get_crypto_currencies() -> list:
    """Return active crypto currencies from DB."""
    return await _get_currencies_db(crypto_only=True, active_only=True)


async def get_fiat_currencies() -> list:
    """Return active fiat currencies from DB."""
    return await _get_currencies_db(fiat_only=True, active_only=True)


async def get_all_active_currencies() -> list:
    """Return all active currencies (crypto + fiat) from DB."""
    return await _get_currencies_db(active_only=True)


# ── Lookup helpers ─────────────────────────────────────────────────────────────

def get_currency_from_list(currencies: list, ticker: str, network: str) -> dict | None:
    """Find currency dict in a pre-fetched list."""
    for c in currencies:
        if c["ticker"] == ticker and c["network"] == network:
            return c
    return None


def get_min_from_list(currencies: list, ticker: str, network: str) -> float:
    """Get min_amount from a pre-fetched list."""
    c = get_currency_from_list(currencies, ticker, network)
    return c["min_amount"] if c else 0.0


async def get_currency(ticker: str, network: str) -> dict | None:
    """Async: find a single currency by ticker + network."""
    all_currencies = await _get_currencies_db(active_only=False)
    return get_currency_from_list(all_currencies, ticker, network)


async def get_min_amount(ticker: str, network: str) -> float:
    """Async: get min_amount for ticker + network."""
    c = await get_currency(ticker, network)
    return c["min_amount"] if c else 0.0


# ── currency_key helper ────────────────────────────────────────────────────────

def currency_key(ticker: str, network: str) -> str:
    return f"{ticker}_{network}"