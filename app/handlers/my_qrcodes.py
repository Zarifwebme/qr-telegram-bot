"""Handlers for browsing the user's saved QR history."""

from __future__ import annotations

import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, CallbackQuery, Message

from app.database.crud import get_or_create_user, get_qrcode_for_user, list_recent_qrcodes
from app.database.db import session_scope
from app.services.qr_service import build_png_bytes
from app.utils.keyboards import build_export_keyboard, build_qrcode_list_keyboard
from app.utils.text import shorten_text


router = Router(name="my_qrcodes")


@router.message(Command("my_qrcodes"))
async def my_qrcodes_command(message: Message) -> None:
    """List the latest QR codes created by the current user."""

    if message.from_user is None:
        await message.answer("Foydalanuvchi aniqlanmadi.")
        return

    async with session_scope() as session:
        await get_or_create_user(session, message.from_user)
        items = await list_recent_qrcodes(session, message.from_user.id, limit=10)

    if not items:
        await message.answer("Hozircha saqlangan QR kodlar yo‘q.")
        return

    lines = ["Sizning so‘nggi QR kodlaringiz:"]
    for qr_code in items:
        lines.append(f"#{qr_code.id} - {shorten_text(qr_code.content, 60)}")

    await message.answer("\n".join(lines), reply_markup=build_qrcode_list_keyboard(items))


@router.callback_query(F.data.startswith("qr_details:"))
async def qr_details_callback(query: CallbackQuery) -> None:
    """Show a stored QR code preview with export actions."""

    if query.from_user is None or query.data is None:
        return

    _, qr_id_value = query.data.split(":", maxsplit=1)
    qr_id = int(qr_id_value)

    async with session_scope() as session:
        qr_code = await get_qrcode_for_user(session, query.from_user.id, qr_id)

    if qr_code is None:
        await query.answer("QR topilmadi.", show_alert=True)
        return

    preview_bytes = await asyncio.to_thread(build_png_bytes, qr_code.content)
    await query.answer()
    await query.message.answer_photo(
        photo=BufferedInputFile(preview_bytes, filename=f"qr_{qr_code.id}.png"),
        caption=f"QR #{qr_code.id}\n{shorten_text(qr_code.content, 100)}",
        reply_markup=build_export_keyboard(qr_code.id),
    )