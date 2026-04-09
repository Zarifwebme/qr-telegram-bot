"""Database access helpers for Telegram users and QR codes."""

from __future__ import annotations

from collections.abc import Sequence

from aiogram.types import User as TelegramUser
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import QRCode, User


def _compose_full_name(user: TelegramUser) -> str:
    """Build a readable user name from Telegram profile fields."""

    parts = [user.first_name or ""]
    if user.last_name:
        parts.append(user.last_name)
    full_name = " ".join(part for part in parts if part).strip()
    return full_name or user.username or f"user_{user.id}"


async def get_or_create_user(session: AsyncSession, telegram_user: TelegramUser) -> User:
    """Create a user row if needed and refresh the stored name when it changes."""

    result = await session.execute(select(User).where(User.telegram_id == telegram_user.id))
    user = result.scalar_one_or_none()
    full_name = _compose_full_name(telegram_user)

    if user is None:
        user = User(telegram_id=telegram_user.id, full_name=full_name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    if user.full_name != full_name:
        user.full_name = full_name
        await session.commit()
        await session.refresh(user)

    return user


async def create_qrcode(session: AsyncSession, user: User, content: str) -> QRCode:
    """Persist a generated QR code payload for the given user."""

    qr_code = QRCode(user_id=user.id, content=content)
    session.add(qr_code)
    await session.commit()
    await session.refresh(qr_code)
    return qr_code


async def get_qrcode_for_user(session: AsyncSession, telegram_id: int, qr_id: int) -> QRCode | None:
    """Fetch a QR code only when it belongs to the given Telegram user."""

    statement = (
        select(QRCode)
        .join(User)
        .where(User.telegram_id == telegram_id, QRCode.id == qr_id)
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def list_recent_qrcodes(
    session: AsyncSession, telegram_id: int, limit: int = 10
) -> Sequence[QRCode]:
    """Return the latest QR codes created by the specified user."""

    statement = (
        select(QRCode)
        .join(User)
        .where(User.telegram_id == telegram_id)
        .order_by(QRCode.created_at.desc(), QRCode.id.desc())
        .limit(limit)
    )
    result = await session.execute(statement)
    return result.scalars().all()