import io
import qrcode
from qrcode.main import QRCode
from aiogram import types


async def generate_qr_code():
    buffer = io.BytesIO()
    data = 'https://t.me/Pizzeria_Marcello_bot'
    qr = QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_L,
                box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(buffer)
    buffer.seek(0)
    # buffer.getvalue()
    return types.BufferedInputFile(buffer.getvalue(), 'qr-menu')
