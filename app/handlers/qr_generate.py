"""Text and URL message handler for QR generation."""

from __future__ import annotations

import asyncio

from aiogram import F, Router
from aiogram.types import BufferedInputFile, Message

from app.config import load_settings
from app.database.crud import create_qrcode, get_or_create_user
from app.database.db import session_scope
from app.services.qr_service import build_png_bytes
from app.utils.keyboards import (
    START_MENU_HELP,
    START_MENU_MY_QR,
    START_MENU_QR_CREATE,
    START_MENU_QR_READ,
    build_export_keyboard,
    build_start_menu,
)


router = Router(name="qr_generate")
settings = load_settings()


@router.message(F.text)
async def qr_generate_handler(message: Message) -> None:
    """Generate a QR code from arbitrary text content."""

    if message.text is None:
        return

    content = message.text.strip()
    if not content or content.startswith("/"):
        return

    if content in {
        START_MENU_QR_CREATE,
        START_MENU_QR_READ,
        START_MENU_MY_QR,
        START_MENU_HELP,
    }:
        return

    if len(content) > settings.max_qr_content_length:
        await message.answer(
            f"Matn juda uzun. Maksimum {settings.max_qr_content_length} belgigacha ruxsat beriladi.",
            reply_markup=build_start_menu(),
        )
        return

    if message.from_user is None:
        await message.answer("Foydalanuvchi aniqlanmadi.")
        return

    async with session_scope() as session:
        user = await get_or_create_user(session, message.from_user)
        qr_code = await create_qrcode(session, user, content)

    png_bytes = await asyncio.to_thread(build_png_bytes, content)
    preview = BufferedInputFile(png_bytes, filename=f"qr_{qr_code.id}.png")
    caption = f"QR tayyor. ID: {qr_code.id}\nMatn: {content[:120]}"
    await message.answer_photo(
        photo=preview,
        caption=caption,
        reply_markup=build_export_keyboard(qr_code.id),
    )