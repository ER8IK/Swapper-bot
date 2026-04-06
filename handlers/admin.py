from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from database.db import get_all_swaps, get_stats
from config import ADMIN_ID

import logging

logger = logging.getLogger(__name__)
router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Нет доступа.")
        return

    stats = await get_stats()
    await message.answer(
        f"👑 <b>Админ панель</b>\n\n"
        f"📊 Всего обменов: <b>{stats['total']}</b>\n"
        f"✅ Завершено: <b>{stats['finished']}</b>\n"
        f"⏳ В процессе: <b>{stats['pending']}</b>\n"
        f"❌ Ошибок: <b>{stats['failed']}</b>\n\n"
        f"Последние 10 обменов: /admin_swaps\n"
        f"Все пользователи: /admin_users"
    )


@router.message(Command("admin_swaps"))
async def cmd_admin_swaps(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Нет доступа.")
        return

    swaps = await get_all_swaps(limit=10)

    if not swaps:
        await message.answer("📭 Обменов пока нет.")
        return

    text = "📋 <b>Последние обмены:</b>\n\n"
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
        await message.answer("⛔ Нет доступа.")
        return

    swaps = await get_all_swaps(limit=100)
    users = {}
    for swap in swaps:
        uid = swap["user_id"]
        users[uid] = users.get(uid, 0) + 1

    if not users:
        await message.answer("📭 Пользователей пока нет.")
        return

    text = f"👥 <b>Пользователи ({len(users)}):</b>\n\n"
    for uid, count in sorted(users.items(), key=lambda x: -x[1]):
        text += f"<code>{uid}</code> — {count} обмен(ов)\n"

    await message.answer(text)