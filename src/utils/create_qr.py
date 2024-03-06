import io
import qrcode

from qrcode.main import QRCode
from aiogram import types

from src.config import settings


async def generate_qr_code(data: str):
    buffer = io.BytesIO()
    link = settings.BOT_LINK + '?start='
    qr = QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_L,
                box_size=10, border=4)
    qr.add_data(link+data)

    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img.save(buffer)
    buffer.seek(0)
    return types.BufferedInputFile(buffer.getvalue(), 'qr-code')
