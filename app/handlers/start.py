"""Start and help handlers for the Telegram QR bot."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.crud import get_or_create_user
from app.database.db import session_scope
from app.handlers.my_qrcodes import my_qrcodes_command
from app.utils.keyboards import (
    START_MENU_HELP,
    START_MENU_MY_QR,
    START_MENU_QR_CREATE,
    START_MENU_QR_READ,
    build_start_menu,
)


router = Router(name="start")


async def _ensure_user(message: Message) -> None:
    """Persist the Telegram user in the database."""

    if message.from_user is None:
        return

    async with session_scope() as session:
        await get_or_create_user(session, message.from_user)


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """Show the main menu and register the user."""

    await _ensure_user(message)
    await message.answer(
        "Salom! Men professional QR botman.\n\n"
        "Matn yoki URL yuboring, men QR yarataman.\n"
        "Rasm yuborsangiz, uni decode qilaman.",
        reply_markup=build_start_menu(),
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Explain the bot capabilities in a short help message."""

    await message.answer(
        "Yordam:\n"
        f"- {START_MENU_QR_CREATE} - text yoki URL dan QR yaratish\n"
        f"- {START_MENU_QR_READ} - QR rasmni decode qilish\n"
        f"- {START_MENU_MY_QR} - saqlangan QR larni ko‘rish\n"
        f"- {START_MENU_HELP} - ushbu yordam matni",
        reply_markup=build_start_menu(),
    )


@router.message(F.text == START_MENU_QR_CREATE)
async def qr_create_hint_handler(message: Message) -> None:
    """Prompt the user to send content for QR generation."""

    await message.answer("QR yaratish uchun text yoki URL yuboring.", reply_markup=build_start_menu())


@router.message(F.text == START_MENU_QR_READ)
async def qr_read_hint_handler(message: Message) -> None:
    """Prompt the user to send an image for QR decoding."""

    await message.answer("QR o‘qish uchun rasm yuboring.", reply_markup=build_start_menu())


@router.message(F.text == START_MENU_MY_QR)
async def my_qr_hint_handler(message: Message) -> None:
    """Show the stored QR list when the menu button is pressed."""

    await my_qrcodes_command(message)


@router.message(F.text == START_MENU_HELP)
async def help_menu_handler(message: Message) -> None:
    """Repeat the help text when the reply keyboard button is pressed."""

    await help_handler(message)