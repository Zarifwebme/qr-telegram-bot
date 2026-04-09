# Telegram QR Bot

Production-ready Telegram QR bot built with aiogram 3, async SQLAlchemy and SQLite.

## Features

- Create QR codes from text or URLs.
- Preview QR as PNG and save metadata to SQLite.
- Decode QR codes from images using OpenCV with a pyzbar fallback.
- Export the original QR content as PNG, JPG, SVG and PDF.
- Generate printable A4 sticker sheets in 1x, 4x, 9x and 16x layouts.
- Provide a clean menu-driven Telegram UX.

## Project Structure

```text
project/
├── bot.py
├── app/
│   ├── bot.py
│   ├── config.py
│   ├── database/
│   │   ├── crud.py
│   │   ├── db.py
│   │   └── models.py
│   ├── handlers/
│   │   ├── export.py
│   │   ├── my_qrcodes.py
│   │   ├── qr_decode.py
│   │   ├── qr_generate.py
│   │   └── start.py
│   ├── services/
│   │   ├── decode_service.py
│   │   ├── pdf_service.py
│   │   └── qr_service.py
│   └── utils/
│       ├── keyboards.py
│       └── text.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=123456:ABCDEF_your_telegram_token
DATABASE_URL=sqlite+aiosqlite:///./data/qrbot.db
```

## Installation

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. The default SQLite database file will be created automatically on startup.

## Running

```bash
python bot.py
```

or

```bash
python app/bot.py
```

## Notes

- The bot creates database tables on startup.
- Temporary export data is kept in memory and not written to disk.
- Large QR content may produce denser codes; the bot validates message length before rendering.

