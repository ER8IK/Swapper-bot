from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from services.simpleswap import get_exchange
from database.db import get_user_swaps, update_swap_status
from keyboards.inline import back_to_menu

import logging

logger = logging.getLogger(__name__)
router = Router()

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


@router.message(F.text.regexp(r"^/status_(.+)$"))
async def cmd_status(message: Message):
    exchange_id = message.text.split("_", 1)[1].strip()

    await message.answer("⏳ Checking status...")

    result = await get_exchange(exchange_id)

    if not result:
        await message.answer("❌ Exchange not found. Check the ID and try again.")
        return

    status = result.get("status", "unknown")
    emoji = STATUS_EMOJI.get(status, "❓")

    await update_swap_status(exchange_id, status)

    address_from = result.get("addressFrom") or result.get("address_from", "—")
    amount_from = result.get("amountFrom") or result.get("amount_from", "—")
    amount_to = result.get("amountTo") or result.get("amount_to", "—")
    ticker_from = result.get("tickerFrom") or result.get("currency_from", "—")
    ticker_to = result.get("tickerTo") or result.get("currency_to", "—")

    await message.answer(
        f"{emoji} <b>Exchange Status</b>\n\n"
        f"ID: <code>{exchange_id}</code>\n"
        f"Status: <b>{status}</b>\n\n"
        f"You send: <b>{amount_from} {ticker_from.upper()}</b>\n"
        f"You receive: <b>{amount_to} {ticker_to.upper()}</b>\n\n"
        f"Send to address:\n<code>{address_from}</code>",
        reply_markup=back_to_menu()
    )


@router.message(Command("history"))
async def cmd_history(message: Message):
    swaps = await get_user_swaps(message.from_user.id)

    if not swaps:
        await message.answer(
            "📭 You have no exchanges yet.\n\nPress /start to begin."
        )
        return

    text = "📋 <b>Your recent exchanges:</b>\n\n"

    for swap in swaps:
        status = swap.get("status", "unknown")
        emoji = STATUS_EMOJI.get(status, "❓")
        text += (
            f"{emoji} <code>{swap['exchange_id']}</code>\n"
            f"   {swap['amount_from']} {swap['currency_from'].upper()} → "
            f"{swap['currency_to'].upper()}\n"
            f"   /status_{swap['exchange_id']}\n\n"
        )

    await message.answer(text, reply_markup=back_to_menu())