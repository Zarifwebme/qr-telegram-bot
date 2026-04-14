"""Async database engine and session management."""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import load_settings
from app.database.models import Base


settings = load_settings()
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _normalize_database_url(database_url: str) -> str:
    """Resolve relative SQLite paths against the project root."""

    url = make_url(database_url)
    if not url.drivername.startswith("sqlite"):
        return database_url

    database_path = url.database
    if not database_path or database_path == ":memory:":
        return database_url

    sqlite_path = Path(database_path).expanduser()
    if not sqlite_path.is_absolute():
        sqlite_path = (PROJECT_ROOT / sqlite_path).resolve()
    else:
        sqlite_path = sqlite_path.resolve()

    normalized_url = url.set(database=sqlite_path.as_posix())
    return normalized_url.render_as_string(hide_password=False)


def _ensure_sqlite_directory(database_url: str) -> None:
    """Create the parent directory for a file-based SQLite database if needed."""

    url = make_url(database_url)
    if not url.drivername.startswith("sqlite"):
        return

    database_path = url.database
    if not database_path or database_path == ":memory:":
        return

    Path(database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


database_url = _normalize_database_url(settings.database_url)
_ensure_sqlite_directory(database_url)

engine = create_async_engine(database_url, echo=False, pool_pre_ping=True)
session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    """Create database tables if they do not already exist."""

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async SQLAlchemy session with automatic cleanup."""

    async with session_factory() as session:
        yield session