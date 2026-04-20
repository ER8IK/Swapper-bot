from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from database.db import (
    get_all_swaps, get_stats, get_recent_logs,
    get_top_pairs, get_average_amount, get_volume_by_period
)
from config import ADMIN_ID
import logging

logger = logging.getLogger(__name__)
router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return

    stats = await get_stats()
    avg = await get_average_amount()

    await message.answer(
        f"👑 <b>Admin Panel</b>\n\n"

        f"📊 <b>Overall</b>\n"
        f"Total exchanges: <b>{stats['total']}</b>\n"
        f"Unique users: <b>{stats['users']}</b>\n"
        f"Avg amount: <b>{avg}</b>\n\n"

        f"📅 <b>By period</b>\n"
        f"Today: <b>{stats['today']}</b>\n"
        f"This week: <b>{stats['week']}</b>\n"
        f"This month: <b>{stats['month']}</b>\n\n"

        f"⚙️ <b>By status</b>\n"
        f"✅ Finished: <b>{stats['finished']}</b>\n"
        f"⏳ Pending: <b>{stats['pending']}</b>\n"
        f"❌ Failed: <b>{stats['failed']}</b>\n\n"

        f"📋 Commands:\n"
        f"/admin_swaps — last 10 exchanges\n"
        f"/admin_users — user list\n"
        f"/admin_pairs — top pairs\n"
        f"/admin_logs — recent logs"
    )


@router.message(Command("admin_pairs"))
async def cmd_admin_pairs(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return

    pairs = await get_top_pairs()

    if not pairs:
        await message.answer("📭 No finished exchanges yet.")
        return

    text = "📈 <b>Top pairs:</b>\n\n"
    medals = ["🥇", "🥈", "🥉", "4.", "5."]

    for i, pair in enumerate(pairs):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        text += (
            f"{medal} <b>{pair['currency_from'].upper()} → "
            f"{pair['currency_to'].upper()}</b>\n"
            f"   Exchanges: {pair['count']} | "
            f"Volume: {round(pair['volume'], 4)}\n\n"
        )

    await message.answer(text)


@router.message(Command("admin_swaps"))
async def cmd_admin_swaps(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return

    swaps = await get_all_swaps(limit=10)

    if not swaps:
        await message.answer("📭 No exchanges yet.")
        return

    text = "📋 <b>Last exchanges:</b>\n\n"
    for swap in swaps:
        text += (
            f"👤 <code>{swap['user_id']}</code> | "
            f"{swap['amount_from']} {swap['currency_from'].upper()} → "
            f"{swap['currency_to'].upper()} | "
            f"{swap['status']}\n"
            f"   <code>{swap['exchange_id']}</code>\n\n"
        )

    await message.answer(text)


@router.message(Command("admin_users"))
async def cmd_admin_users(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return

    swaps = await get_all_swaps(limit=100)
    users = {}
    for swap in swaps:
        uid = swap["user_id"]
        users[uid] = users.get(uid, 0) + 1

    if not users:
        await message.answer("📭 No users yet.")
        return

    text = f"👥 <b>Users ({len(users)}):</b>\n\n"
    for uid, count in sorted(users.items(), key=lambda x: -x[1]):
        text += f"<code>{uid}</code> — {count} exchange(s)\n"

    await message.answer(text)


@router.message(Command("admin_logs"))
async def cmd_admin_logs(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ No access.")
        return

    lines = await get_recent_logs(20)

    if not lines:
        await message.answer("📭 No logs yet.")
        return

    text = "\n".join(lines)
    chunks = [text[i:i+3500] for i in range(0, len(text), 3500)]

    for chunk in chunks:
        await message.answer(
            f"📋 <b>Recent logs:</b>\n\n"
            f"<pre>{chunk}</pre>"
        )