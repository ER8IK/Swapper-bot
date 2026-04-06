import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from handlers import start, exchange, status, admin
from database.db import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    await init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(start.router)
    dp.include_router(exchange.router)
    dp.include_router(status.router)
    dp.include_router(admin.router)

    logger.info("Бот запущен")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())