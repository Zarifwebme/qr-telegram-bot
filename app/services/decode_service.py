"""QR code decoding helpers using pyzbar with an OpenCV fallback."""

from __future__ import annotations

from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageOps


def _decode_with_pyzbar(image: Image.Image) -> list[str]:
    """Decode QR codes with pyzbar when the runtime dependency is available."""

    try:
        from pyzbar.pyzbar import decode as zbar_decode
    except Exception:
        return []

    decoded_items: list[str] = []
    for item in zbar_decode(image):
        if item.data:
            decoded_items.append(item.data.decode("utf-8", errors="replace"))
    return decoded_items


def _decode_with_opencv(image: Image.Image) -> list[str]:
    """Decode a QR code image with OpenCV's QRCodeDetector."""

    numpy_image = np.array(image.convert("RGB"))
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(numpy_image)
    return [data] if data else []


def decode_qr_from_bytes(image_bytes: bytes) -> list[str]:
    """Decode one or more QR codes from image bytes."""

    image = Image.open(BytesIO(image_bytes))
    image = ImageOps.exif_transpose(image).convert("RGB")
    decoded_items = _decode_with_pyzbar(image)
    if decoded_items:
        return list(dict.fromkeys(decoded_items))

    decoded_items = _decode_with_opencv(image)
    return list(dict.fromkeys(decoded_items))