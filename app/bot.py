"""aiogram 3 application entrypoint for the Telegram QR bot."""

from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError
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
    try:
        await _set_bot_commands(bot)
    except TelegramNetworkError:
        logger.warning("Could not set bot commands because Telegram is unreachable")
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
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    dp.errors.register(_global_error_handler)

    while True:
        bot = Bot(
            token=settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        try:
            await _startup(bot)
            await dp.start_polling(bot)
            break
        except TelegramNetworkError as error:
            logger.warning("Telegram unreachable, retrying in 10s: %s", error)
            await asyncio.sleep(10)
        except Exception:
            logger.exception("Unexpected polling failure, retrying in 10s")
            await asyncio.sleep(10)
        finally:
            await _shutdown(bot)


if __name__ == "__main__":
    asyncio.run(main())
