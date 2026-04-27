"""
Channel posting service.

Set in .env:
  PUBLIC_CHANNEL_ID  = @yourchannel  or  -1001234567890
  PRIVATE_CHANNEL_ID = -1009876543210

If a channel ID is empty — posting to that channel is silently skipped.
"""

import logging
from aiogram import Bot
from config import PUBLIC_CHANNEL_ID, PRIVATE_CHANNEL_ID

logger = logging.getLogger(__name__)


async def post_to_public(bot: Bot, swap: dict, result: dict):
    """Post successful swap to public channel."""
    if not PUBLIC_CHANNEL_ID:
        return
    try:
        exchange_id  = result.get("id") or swap.get("exchange_id", "—")
        amount_from  = swap.get("amount_from", "?")
        currency_from = swap.get("currency_from", "?").upper()
        currency_to   = swap.get("currency_to", "?").upper()
        amount_to    = swap.get("amount_to", "?")

        text = (
            "✅ <b>Successful swap</b>\n\n"
            f"🔄 {amount_from} {currency_from} → {currency_to}\n"
            f"💰 Received: ~{amount_to} {currency_to}\n"
            f"🆔 <code>{exchange_id}</code>"
        )
        await bot.send_message(PUBLIC_CHANNEL_ID, text)
    except Exception as e:
        logger.error(f"Failed to post to public channel: {e}")


async def post_status_update(bot: Bot, exchange_id: str, old_status: str,
                              new_status: str, user_id: int):
    """Post status change to private admin channel."""
    if not PRIVATE_CHANNEL_ID:
        return
    try:
        STATUS_EMOJI = {
            "waiting":    "⏳",
            "confirming": "🔄",
            "exchanging": "💱",
            "sending":    "📤",
            "finished":   "✅",
            "failed":     "❌",
            "refunded":   "↩️",
            "expired":    "⌛",
        }
        e_old = STATUS_EMOJI.get(old_status, "❓")
        e_new = STATUS_EMOJI.get(new_status, "❓")
        text = (
            f"📊 <b>Status update</b>\n\n"
            f"🆔 <code>{exchange_id}</code>\n"
            f"👤 User: <code>{user_id}</code>\n"
            f"{e_old} {old_status} → {e_new} <b>{new_status}</b>"
        )
        await bot.send_message(PRIVATE_CHANNEL_ID, text)
    except Exception as e:
        logger.error(f"Failed to post to private channel: {e}")