"""Configuration loading for the bot application."""

from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    """Application settings loaded from environment variables."""

    bot_token: str
    database_url: str
    max_qr_content_length: int = 2048


def load_settings() -> Settings:
    """Load and validate runtime settings from environment variables."""

    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set")

    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./data/qrbot.db",
    ).strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    return Settings(bot_token=bot_token, database_url=database_url)