"""Keyboard factories for the Telegram QR bot interface."""

from __future__ import annotations

from collections.abc import Sequence

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.database.models import QRCode
from app.utils.text import shorten_text


START_MENU_QR_CREATE = "📌 QR Yaratish"
START_MENU_QR_READ = "📷 QR O‘qish"
START_MENU_MY_QR = "📁 Mening QRlarim"
START_MENU_HELP = "ℹ️ Yordam"


def build_start_menu() -> ReplyKeyboardMarkup:
    """Create the main reply keyboard for the bot home screen."""

    builder = ReplyKeyboardBuilder()
    builder.button(text=START_MENU_QR_CREATE)
    builder.button(text=START_MENU_QR_READ)
    builder.button(text=START_MENU_MY_QR)
    builder.button(text=START_MENU_HELP)
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)


def build_export_keyboard(qr_id: int) -> InlineKeyboardMarkup:
    """Create export buttons for a stored QR code."""

    builder = InlineKeyboardBuilder()
    builder.button(text="PNG", callback_data=f"qr_export:{qr_id}:png")
    builder.button(text="JPG", callback_data=f"qr_export:{qr_id}:jpg")
    builder.button(text="SVG", callback_data=f"qr_export:{qr_id}:svg")
    builder.button(text="PDF", callback_data=f"qr_export:{qr_id}:pdf")
    builder.button(text="Stiker 1x", callback_data=f"qr_sticker:{qr_id}:1")
    builder.button(text="Stiker 4x", callback_data=f"qr_sticker:{qr_id}:4")
    builder.button(text="Stiker 9x", callback_data=f"qr_sticker:{qr_id}:9")
    builder.button(text="Stiker 16x", callback_data=f"qr_sticker:{qr_id}:16")
    builder.adjust(2, 2, 2, 2)
    return builder.as_markup()


def build_open_link_keyboard(url: str) -> InlineKeyboardMarkup:
    """Create a single button keyboard that opens a decoded URL."""

    builder = InlineKeyboardBuilder()
    builder.button(text="Havolani ochish", url=url)
    return builder.as_markup()


def build_qrcode_list_keyboard(items: Sequence[QRCode]) -> InlineKeyboardMarkup:
    """Create a compact keyboard for the latest QR code records."""

    builder = InlineKeyboardBuilder()
    for qr_code in items:
        builder.button(
            text=f"#{qr_code.id} {shorten_text(qr_code.content, 24)}",
            callback_data=f"qr_details:{qr_code.id}",
        )
    builder.adjust(1)
    return builder.as_markup()