"""Telegram handlers and routers used by the bot dispatcher."""

from app.handlers.export import router as export_router
from app.handlers.my_qrcodes import router as my_qrcodes_router
from app.handlers.qr_decode import router as qr_decode_router
from app.handlers.qr_generate import router as qr_generate_router
from app.handlers.start import router as start_router


routers = (
    start_router,
    qr_generate_router,
    qr_decode_router,
    export_router,
    my_qrcodes_router,
)