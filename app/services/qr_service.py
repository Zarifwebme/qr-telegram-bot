"""QR rendering helpers for image and SVG export formats."""

from __future__ import annotations

from io import BytesIO

import qrcode
from PIL import Image
import segno


def build_qr_image(content: str, box_size: int = 12, border: int = 4) -> Image.Image:
    """Render a QR code as a Pillow image."""

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    qr.add_data(content)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    pil_image = image.get_image() if hasattr(image, "get_image") else image
    return pil_image.convert("RGB")


def build_png_bytes(content: str) -> bytes:
    """Render a QR code and return PNG bytes."""

    image = build_qr_image(content)
    buffer = BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def build_jpg_bytes(content: str) -> bytes:
    """Render a QR code and return JPG bytes."""

    image = build_qr_image(content)
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=95, optimize=True)
    return buffer.getvalue()


def build_svg_bytes(content: str) -> bytes:
    """Render a QR code and return SVG bytes using segno."""

    qr = segno.make(content, error="h")
    buffer = BytesIO()
    qr.save(buffer, kind="svg", xmldecl=True)
    return buffer.getvalue()