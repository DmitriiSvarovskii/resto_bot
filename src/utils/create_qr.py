import qrcode
from qrcode.main import QRCode

# data = 'https://t.me/Pizzeria_Marcello_bot'
# data = 'https://reka-group.ru'

# # Создаем объект QR-кода
# qr = QRCode(
#     version=1,
#     error_correction=qrcode.ERROR_CORRECT_L,
#     box_size=10,
#     border=4
# )

# # Добавляем данные в QR-код
# qr.add_data(data)
# qr.make(fit=True)

# # Создаем изображение QR-кода
# img = qr.make_image(fill_color="black", back_color="white")

# # Сохраняем изображение
# img.save("qrcode.png")


async def generate_qr_code():
    data = 'https://t.me/Pizzeria_Marcello_bot'
    qr = QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_L,
                box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img
