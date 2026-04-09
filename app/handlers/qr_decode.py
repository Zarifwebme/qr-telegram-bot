"""Image handler for QR code decoding."""

from __future__ import annotations

import asyncio
from io import BytesIO

from aiogram import F, Router
from aiogram.types import Message

from app.services.decode_service import decode_qr_from_bytes
from app.utils.keyboards import build_open_link_keyboard
from app.utils.text import is_url


router = Router(name="qr_decode")


async def _download_file_bytes(message: Message, file_id: str) -> bytes:
    """Download a Telegram file into memory and return its bytes."""

    if message.bot is None:
        raise RuntimeError("Bot instance is not available")

    telegram_file = await message.bot.get_file(file_id)
    buffer = BytesIO()
    await message.bot.download(telegram_file, destination=buffer)
    return buffer.getvalue()


@router.message(F.photo)
async def qr_decode_photo_handler(message: Message) -> None:
    """Decode a QR code from a Telegram photo message."""

    if not message.photo:
        return

    photo = message.photo[-1]
    image_bytes = await _download_file_bytes(message, photo.file_id)
    decoded_items = await asyncio.to_thread(decode_qr_from_bytes, image_bytes)

    if not decoded_items:
        await message.answer("QR kod topilmadi yoki o‘qib bo‘lmadi. Iltimos, aniqroq rasm yuboring.")
        return

    content = decoded_items[0]
    reply_markup = build_open_link_keyboard(content) if is_url(content) else None
    await message.answer(f"Decoded content:\n{content}", reply_markup=reply_markup)


@router.message(F.document)
async def qr_decode_document_handler(message: Message) -> None:
    """Decode QR codes from image documents when users send files instead of photos."""

    if message.document is None or message.document.mime_type is None:
        return

    if not message.document.mime_type.startswith("image/"):
        return

    image_bytes = await _download_file_bytes(message, message.document.file_id)
    decoded_items = await asyncio.to_thread(decode_qr_from_bytes, image_bytes)

    if not decoded_items:
        await message.answer("QR kod topilmadi yoki o‘qib bo‘lmadi. Iltimos, boshqa rasm yuboring.")
        return

    content = decoded_items[0]
    reply_markup = build_open_link_keyboard(content) if is_url(content) else None
    await message.answer(f"Decoded content:\n{content}", reply_markup=reply_markup)