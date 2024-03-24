import random
import os

from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError

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


@router.message((Command('mail')))
async def create_mail_chats(message: types.Message, bot: Bot):
    # user_info = await customer_db.get_user_info_by_id(
    #     user_id=message.chat.id
    # )

    # store_info = await store_db.get_store_info()
    customer_list = await customer_db.db_get_users_list()
    # if user_info.admin:
    if 1 == 1:
        for user_data in customer_list:
            try:
                user_info = await bot.get_chat_member(-1001738942783, user_data.user_id)
                language_code = str(user_info).split(
                    "language_code='")[1].split("'")[0]
                if language_code == 'ru':
                    await bot.send_message(
                        chat_id=user_data.user_id,
                        text="Друзья, у нашего бота вышло долгожданное обновление:\n"
                        "🌐 Наше меню доступно на английском и русском языках (язык определяется автоматически, от настроек вашего телефона)!\n"
                        "🔥 Добавили раздел 'Специальное предложение' - следите за лучшими предложениями!\n"
                        "🍽 В меню бота всегда только актуальные блюда!\n"
                        "🛒 Также добавили раздел 'Магазин', где вы можете приобрести различные товары, от заморозок собственного производства до электронных курилок.\n\n"
                        "Не пропустите лучшие предложения и новинки! Следите за обновлениями и приятного аппетита! 🥂",
                        reply_markup=await main_kb.create_kb_main(
                            language='ru', user_id=user_data.user_id
                        )
                    )

                else:
                    await bot.send_message(
                        chat_id=user_data.user_id,
                        text="Friends, our bot has received a long-awaited update:\n"
                        "🌐 Our menu is now available in English and Russian (language is automatically detected based on your phone settings)!\n"
                        "🔥 We've added a 'Special Offer' section - stay tuned for the best deals!\n"
                        "🍽 The menu in the bot always features only the most up-to-date dishes!\n"
                        "🛒 We've also added a 'Market' section where you can purchase various items, from our own frozen products to electronic hookahs.\n\n"
                        "Don't miss out on the best deals and new arrivals! Stay tuned for updates and enjoy your meal! 🥂",
                        reply_markup=await main_kb.create_kb_main(
                            language='en', user_id=user_data.user_id
                        )
                    )
            except TelegramForbiddenError:
                await message.answer(text=f'{user_data.user_id} заблокировал бота')
                continue  # Переходим к следующей итерации цикла при возникновении ошибки TelegramForbiddenError
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
        await message.answer(
            text='Рассылка завершена'
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
