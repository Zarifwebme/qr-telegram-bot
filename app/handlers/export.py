"""Callback handlers for QR export and printable sticker generation."""

from __future__ import annotations

import asyncio

from aiogram import F, Router
from aiogram.types import BufferedInputFile, CallbackQuery

from app.database.crud import get_qrcode_for_user
from app.database.db import session_scope
from app.services.pdf_service import build_single_qr_pdf_bytes, build_sticker_sheet_pdf_bytes
from app.services.qr_service import build_jpg_bytes, build_png_bytes, build_svg_bytes
from app.utils.keyboards import build_export_keyboard


router = Router(name="export")


def _parse_callback_data(data: str) -> tuple[int, str]:
    """Parse callback payloads in the form action:qr_id:value."""

    _, qr_id_value, export_value = data.split(":", maxsplit=2)
    return int(qr_id_value), export_value


@router.callback_query(F.data.startswith("qr_export:"))
async def qr_export_callback(query: CallbackQuery) -> None:
    """Send the selected QR in the requested export format."""

    if query.from_user is None or query.data is None:
        return

    qr_id, export_format = _parse_callback_data(query.data)
    async with session_scope() as session:
        qr_code = await get_qrcode_for_user(session, query.from_user.id, qr_id)

    if qr_code is None:
        await query.answer("QR topilmadi.", show_alert=True)
        return

    if export_format == "png":
        data = await asyncio.to_thread(build_png_bytes, qr_code.content)
        file_name = f"qr_{qr_code.id}.png"
    elif export_format == "jpg":
        data = await asyncio.to_thread(build_jpg_bytes, qr_code.content)
        file_name = f"qr_{qr_code.id}.jpg"
    elif export_format == "svg":
        data = await asyncio.to_thread(build_svg_bytes, qr_code.content)
        file_name = f"qr_{qr_code.id}.svg"
    elif export_format == "pdf":
        data = await asyncio.to_thread(build_single_qr_pdf_bytes, qr_code.content)
        file_name = f"qr_{qr_code.id}.pdf"
    else:
        await query.answer("Noto‘g‘ri yuklab olish formati.", show_alert=True)
        return

    await query.answer("Yuklab olish fayli tayyorlandi.")
    await query.message.answer_document(
        document=BufferedInputFile(data, filename=file_name),
        caption=f"Format: {export_format.upper()}",
        reply_markup=build_export_keyboard(qr_code.id),
    )


@router.callback_query(F.data.startswith("qr_sticker:"))
async def qr_sticker_callback(query: CallbackQuery) -> None:
    """Generate and send a printable A4 sticker sheet for the selected QR."""

    if query.from_user is None or query.data is None:
        return

    _, qr_id_value, copies_value = query.data.split(":", maxsplit=2)
    qr_id = int(qr_id_value)
    copies = int(copies_value)

    async with session_scope() as session:
        qr_code = await get_qrcode_for_user(session, query.from_user.id, qr_id)

    if qr_code is None:
        await query.answer("QR topilmadi.", show_alert=True)
        return

    sheet_bytes = await asyncio.to_thread(build_sticker_sheet_pdf_bytes, qr_code.content, copies)
    await query.answer("Stiker varaqasi tayyorlandi.")
    await query.message.answer_document(
        document=BufferedInputFile(sheet_bytes, filename=f"qr_{qr_code.id}_sheet_{copies}x.pdf"),
        caption=f"Chop etish varaqasi: {copies}x",
        reply_markup=build_export_keyboard(qr_code.id),
    )