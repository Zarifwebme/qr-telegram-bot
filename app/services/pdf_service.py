"""PDF generation for single QR exports and printable sticker sheets."""

from __future__ import annotations

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from app.services.qr_service import build_qr_image


def _draw_centered_title(pdf: canvas.Canvas, title: str, page_width: float, page_height: float) -> None:
    """Draw a simple title at the top of the page."""

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(page_width / 2, page_height - 42, title)


def build_single_qr_pdf_bytes(content: str) -> bytes:
    """Generate a one-page PDF that contains a single QR code."""

    page_width, page_height = A4
    qr_image = build_qr_image(content, box_size=12)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    _draw_centered_title(pdf, "QR Kod Fayli", page_width, page_height)

    target_size = min(page_width, page_height) * 0.58
    x_position = (page_width - target_size) / 2
    y_position = (page_height - target_size) / 2 - 10
    pdf.drawImage(
        ImageReader(qr_image),
        x_position,
        y_position,
        width=target_size,
        height=target_size,
        preserveAspectRatio=True,
        mask="auto",
    )

    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(page_width / 2, 40, content[:120])
    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def build_sticker_sheet_pdf_bytes(content: str, copies: int) -> bytes:
    """Generate an A4 printable sheet with QR codes arranged in a grid."""

    grid_map = {1: 1, 4: 2, 9: 3, 16: 4}
    grid_size = grid_map.get(copies, 2)
    page_width, page_height = A4
    margin = 24
    gap = 12
    header_height = 36

    available_width = page_width - (2 * margin) - ((grid_size - 1) * gap)
    available_height = page_height - (2 * margin) - header_height - ((grid_size - 1) * gap)
    cell_size = min(available_width / grid_size, available_height / grid_size)

    qr_image = build_qr_image(content, box_size=10)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    _draw_centered_title(pdf, f"Chop Etish Uchun QR Varaq - {copies}x", page_width, page_height)
    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(page_width / 2, page_height - 58, "A4 formatda chop etish uchun")

    start_x = (page_width - ((grid_size * cell_size) + ((grid_size - 1) * gap))) / 2
    start_y = page_height - margin - header_height - cell_size

    for row_index in range(grid_size):
        for column_index in range(grid_size):
            x_position = start_x + column_index * (cell_size + gap)
            y_position = start_y - row_index * (cell_size + gap)
            pdf.roundRect(x_position, y_position, cell_size, cell_size, 10, stroke=1, fill=0)
            qr_padding = cell_size * 0.10
            pdf.drawImage(
                ImageReader(qr_image),
                x_position + qr_padding,
                y_position + qr_padding,
                width=cell_size - (2 * qr_padding),
                height=cell_size - (2 * qr_padding),
                preserveAspectRatio=True,
                mask="auto",
            )

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()