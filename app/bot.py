import logging
import qrcode
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Logger sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),  # Loglarni faylga yozish
        logging.StreamHandler()  # Konsolda ko‘rsatish
    ]
)
logger = logging.getLogger(__name__)


# QR kodni yaratish funksiyasi
def generate_qr(data, size=10, color="black", background="white"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color=background)
    return img


# /start komandasini ishlatish
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Assalomu alaykum! Men QR kod generator botman.\n"
        "Menga matn yoki URL yuboring (200 belgidan oshmasligi kerak), men esa siz uchun QR kod yarataman!"
    )


# QR kodni yaratish va yuborish
async def generate_qr_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_input = update.message.text
        if len(user_input) > 200:
            await update.message.reply_text(
                "Xatolik: Matn 200 belgidan oshmasligi kerak! Iltimos, qisqaroq matn yuboring."
            )
            return

        # QR kodni yaratish
        img = generate_qr(user_input)

        # QR kodni vaqtinchalik fayl sifatida saqlash
        file_path = "qr_code.png"
        img.save(file_path)

        # QR kodni foydalanuvchiga yuborish
        await update.message.reply_photo(photo=open(file_path, "rb"))
        await update.message.reply_text("QR kodingiz tayyor!")
    except Exception as e:
        logger.error(f"QR kod yaratishda xatolik: {e}", exc_info=True)
        await update.message.reply_text(
            "Kutilmagan xatolik yuz berdi! Iltimos, qayta urinib ko‘ring."
        )


# Botdagi global xatolarni qayta ishlash
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Global xatolik: {context.error}", exc_info=True)
    if update and update.effective_user:
        try:
            await context.bot.send_message(
                chat_id=update.effective_user.id,
                text="Kutilmagan xatolik yuz berdi! Admin bilan bog‘laning."
            )
        except Exception as e:
            logger.error(f"Foydalanuvchiga xatolik haqida xabar yuborishda muammo: {e}")


# Botni ishga tushirish
def main():
    try:
        # Telegram bot tokenini bu yerda o'zgartiring
        TOKEN = "Bot_tokken"

        # Botni sozlash
        application = ApplicationBuilder().token(TOKEN).build()

        # Komanda va xabarlar uchun handlerlar
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr_handler))

        # Global xatolar uchun handler
        application.add_error_handler(error_handler)

        # Botni ishga tushirish
        application.run_polling()
    except Exception as e:
        logger.critical(f"Botni ishga tushirishda xatolik: {e}", exc_info=True)


if __name__ == "__main__":
    main()
