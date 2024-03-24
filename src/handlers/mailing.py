import random
import os

from aiogram import Bot, types, Router
from aiogram.filters import Command

from src.db import customer_db, store_db
from src.keyboards import admin_kb, main_kb


router = Router(name=__name__)


@router.message((Command('m')))
async def create_mail_group(message: types.Message, bot: Bot):
    user_info = await customer_db.get_user_info_by_id(
        user_id=message.chat.id
    )
    store_info = await store_db.get_store_info()
    if user_info.admin:
        await bot.send_photo(
            chat_id=store_info.sale_group,
            photo=message.photo[-1].file_id,
            caption=message.caption[2:],
            reply_markup=admin_kb.create_kb_sale_group()
        )

        await message.answer(
            text='Пост опубликован успешно',
            reply_markup=await main_kb.create_kb_main(
                language=message.from_user.language_code,
                user_id=message.chat.id
            )
        )
    else:
        await message.answer(
            text='Данная команда доступна только для администраторов бота',
            reply_markup=await main_kb.create_kb_main(
                language=message.from_user.language_code,
                user_id=message.chat.id
            )
        )


async def create_mail_group_auto(bot: Bot):
    store_info = await store_db.get_store_info()

    text = ('Всем хорошего дня 🔥\n'
            'Эта кнопка для заказа через приложение Marcello 👇\n'
            'При заказе через приложение постоянная скидка на все меню 5% 👍')

    current_dir = os.path.dirname(os.path.abspath(__file__))

    static_folder = os.path.join(current_dir, '..', 'static')

    file_list = os.listdir(static_folder)

    random_file = random.choice(file_list)

    random_file_path = os.path.join(static_folder, random_file)

    photo_file = types.FSInputFile(random_file_path)

    await bot.send_photo(
        chat_id=store_info.sale_group,
        photo=photo_file,
        caption=text,
        reply_markup=admin_kb.create_kb_sale_group()
    )
