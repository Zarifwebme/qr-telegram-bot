# Telegram QR Bot

Aiogram 3, async SQLAlchemy va SQLite asosida yozilgan zamonaviy Telegram QR bot.

## Imkoniyatlar

- Matn yoki URL dan QR kod yaratadi.
- QR ni PNG ko‘rinishda yuboradi va ma'lumotni SQLite bazaga saqlaydi.
- Rasm ichidagi QR ni OpenCV va pyzbar yordamida o‘qiydi.
- Bir xil mazmundan PNG, JPG, SVG va PDF formatlarda fayl beradi.
- 1x, 4x, 9x, 16x variantlarda A4 stiker varaqasini yaratadi.
- Menyu asosidagi qulay Telegram interfeysiga ega.

## Loyiha Tuzilmasi

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

## Muhit O‘zgaruvchilari

Loyiha ildizida `.env` fayl yarating:

```env
BOT_TOKEN=123456:ABCDEF_your_telegram_token
DATABASE_URL=sqlite+aiosqlite:///./data/qrbot.db
MAX_QR_CONTENT_LENGTH=500
```

## O‘rnatish

1. Virtual muhit yarating va faollashtiring.
2. Kerakli kutubxonalarni o‘rnating:

```bash
pip install -r requirements.txt
```

3. Bot ishga tushganda SQLite fayli avtomatik yaratiladi.

## Ishga Tushirish

```bash
python bot.py
```

yoki

```bash
python app/bot.py
```

## PythonAnywhere (nohup bilan doimiy ishga tushirish)

1. Bash konsolda loyiha papkasiga kiring:

```bash
cd ~/qrtelebot/qr-telegram-bot
```

2. Virtual muhit yarating (agar hali bo'lmasa) va kutubxonalarni o'rnating:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. `.env` faylni to'ldiring (`BOT_TOKEN` majburiy).

4. Botni fon rejimida ishga tushiring:

```bash
nohup .venv/bin/python bot.py >> bot.log 2>&1 &
```

Yoki tayyor skriptlar bilan:

```bash
chmod +x scripts/start_bot.sh scripts/stop_bot.sh
./scripts/start_bot.sh
```

5. Jarayon ishlayotganini tekshiring:

```bash
ps -ef | grep "python bot.py" | grep -v grep
tail -f bot.log
```

6. To'xtatish:

```bash
pkill -f "python bot.py"
```

Yoki:

```bash
./scripts/stop_bot.sh
```

Muhim:
- `nohup` faqat jarayonni fon rejimida qoldiradi, server restart bo'lsa jarayon qayta turmaydi.
- PythonAnywhere'da haqiqiy 24/7 uchun eng yaxshi variant: "Always-on task" (pullik akkauntda).
- Agar free akkaunt ishlatsangiz, Scheduled task orqali botni periodik tekshirib qayta ishga tushirish tavsiya qilinadi.

## Eslatma

- Bot ishga tushganda kerakli jadvallar avtomatik yaratiladi.
- Vaqtinchalik export fayllari diskka yozilmaydi, xotirada ishlanadi.
- QR uchun matn uzunligi `MAX_QR_CONTENT_LENGTH` orqali cheklanadi (standart: 500 belgi).

