import asyncio
import logging
from aiogram import Bot

from database.db import get_active_swaps, update_swap_status
from services.simpleswap import get_exchange

logger = logging.getLogger(__name__)

CHECK_INTERVAL = 180  # 3 минуты

STATUS_MESSAGES = {
    "waiting":    "⏳ Ожидаем входящую транзакцию...",
    "confirming": "🔄 Транзакция найдена, ждём подтверждения сети...",
    "exchanging": "💱 Обмен выполняется...",
    "sending":    "📤 Отправляем на твой кошелёк...",
    "finished":   "✅ Обмен завершён! Монеты отправлены на кошелёк.",
    "failed":     "❌ Обмен не удался. Напиши /start чтобы попробовать снова.",
    "refunded":   "↩️ Средства возвращены на исходный адрес.",
    "expired":    "⌛ Время обмена истекло. Напиши /start чтобы создать новый.",
}

NOTIFY_ON = {"confirming", "exchanging", "sending", "finished", "failed", "refunded", "expired"}
FINAL_STATUSES = {"finished", "failed", "refunded", "expired"}


async def check_swaps(bot: Bot):
    """Background task — checks active swaps every 3 minutes."""
    logger.info("Background swap checker started")
    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        try:
            swaps = await get_active_swaps()
            if not swaps:
                continue

            logger.info(f"Checking {len(swaps)} active swap(s)...")

            for swap in swaps:
                try:
                    result = await get_exchange(swap["exchange_id"])
                    if not result:
                        continue

                    new_status = result.get("status")
                    if not new_status or new_status == swap["status"]:
                        continue

                    # Статус изменился — обновляем БД
                    await update_swap_status(swap["exchange_id"], new_status)
                    logger.info(
                        f"Swap {swap['exchange_id']}: "
                        f"{swap['status']} → {new_status}"
                    )

                    # Уведомляем пользователя только при важных статусах
                    if new_status not in NOTIFY_ON:
                        continue

                    message = STATUS_MESSAGES.get(new_status)
                    if not message:
                        continue

                    # Для финального статуса добавляем детали
                    if new_status == "finished":
                        amount_to = result.get("amountTo") or swap.get("amount_to", "")
                        ticker_to = result.get("tickerTo") or swap.get("currency_to", "")
                        text = (
                            f"✅ <b>Обмен завершён!</b>\n\n"
                            f"ID: <code>{swap['exchange_id']}</code>\n"
                            f"Получено: <b>{amount_to} {ticker_to.upper()}</b>\n\n"
                            f"Спасибо что воспользовался ботом 🙌"
                        )
                    else:
                        text = (
                            f"{message}\n\n"
                            f"ID: <code>{swap['exchange_id']}</code>"
                        )

                    await bot.send_message(
                        chat_id=swap["user_id"],
                        text=text,
                        parse_mode="HTML"
                    )

                except Exception as e:
                    logger.error(f"Error checking swap {swap.get('exchange_id')}: {e}")
                    continue

        except Exception as e:
            logger.error(f"check_swaps loop error: {e}")