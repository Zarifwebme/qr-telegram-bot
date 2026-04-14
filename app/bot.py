"""aiogram 3 application entrypoint for the Telegram QR bot."""

from __future__ import annotations

import asyncio
import logging
import ssl

import certifi
from aiohttp import ClientSession, TCPConnector
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, ErrorEvent

from app.config import load_settings
from app.database.db import init_db
from app.handlers import routers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def _set_bot_commands(bot: Bot) -> None:
    """Publish a compact command list in Telegram."""

    commands = [
        BotCommand(command="start", description="Bot menyusini ochish"),
        BotCommand(command="help", description="Yordamni ko‘rsatish"),
        BotCommand(command="my_qrcodes", description="Saqlangan QR kodlarni ko‘rish"),
    ]
    await bot.set_my_commands(commands)


async def _startup(bot: Bot) -> None:
    """Initialize the database and bot metadata before polling starts."""

    await init_db()
    await _set_bot_commands(bot)
    logger.info("Bot started and database initialized")


async def _shutdown(bot: Bot) -> None:
    """Close resources when polling stops."""

    await bot.session.close()
    logger.info("Bot stopped")


async def _global_error_handler(event: ErrorEvent) -> None:
    """Log unexpected errors and keep the dispatcher running."""

    logger.error("Unhandled error: %s", event.exception, exc_info=True)


async def main() -> None:
    """Start the Telegram bot with the configured environment."""

    settings = load_settings()
    
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = TCPConnector(ssl_context=ssl_context)
    client_session = ClientSession(connector=connector)
    session = AiohttpSession(client=client_session)
    
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    dp.errors.register(_global_error_handler)

    async def on_startup() -> None:
        await _startup(bot)

    async def on_shutdown() -> None:
        await _shutdown(bot)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
