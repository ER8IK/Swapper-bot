import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update

logger = logging.getLogger(__name__)


async def handle_webhook(request: web.Request) -> web.Response:
    """Handle incoming webhook updates from Telegram."""
    bot: Bot = request.app["bot"]
    dp: Dispatcher = request.app["dp"]

    try:
        data = await request.json()
        update = Update(**data)
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Webhook handler error: {e}")
        return web.Response(status=500)


async def health_check(request: web.Request) -> web.Response:
    """Simple health check endpoint."""
    return web.json_response({"status": "ok"})


def create_app(bot: Bot, dp: Dispatcher, webhook_path: str) -> web.Application:
    app = web.Application()
    app["bot"] = bot
    app["dp"] = dp
    app.router.add_post(webhook_path, handle_webhook)
    app.router.add_get("/health", health_check)
    return app