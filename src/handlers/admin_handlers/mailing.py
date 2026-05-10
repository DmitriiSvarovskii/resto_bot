import logging
import asyncio
import random
import os

from aiogram import Bot, types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from src.db import customer_db, store_db
from src.keyboards import admin_kb, main_kb


router = Router(name=__name__)

logger = logging.getLogger(__name__)


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
async def create_mail_chats(message: types.Message,
                            bot: Bot,
                            state: FSMContext):
    user_info = await customer_db.get_user_info_by_id(
        user_id=message.chat.id
    )

    # store_info = await store_db.get_store_info()
    customer_list = await customer_db.db_get_users_list()
    if user_info.admin:
        for user_data in customer_list:
            try:
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

            except TelegramForbiddenError:
                continue
            except Exception:
                continue
        await message.answer(
            text='Рассылка завершена.'
        )
    else:
        await message.answer(
            text='Данная команда доступна только для администраторов бота',
            reply_markup=await main_kb.create_kb_main(
                language=message.from_user.language_code,
                user_id=message.chat.id
            )
        )


async def send_mail_group_auto(bot: Bot):
    max_retries = 7
    logger.info("Function 'send_mail_group_auto' started")

    for attempt in range(max_retries):
        try:
            store_info = await store_db.get_store_info(store_id=1)

            # text = (
            #     'Всем хорошего дня 🔥\n'
            #     'Эта кнопка для заказа через приложение Marcello 👇\n'
            #     'При заказе через приложение постоянная скидка на все меню 5% 👍\n'
            #     'Новая локация + лучший кофе ☕️ 🍕 🫶'
            # )
            text = store_info.welcome_message
            current_dir = os.path.dirname(os.path.abspath(__file__))
            static_folder = os.path.abspath(
                os.path.join(current_dir, '../../static')
            )

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

            logger.info("Photo sent successfully.")
            break

        except TelegramBadRequest as e:
            logger.error(f"TelegramBadRequest: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(1)

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            break


@router.message(Command('13'))
async def create_mail_group_auto(message: types.Message, bot: Bot):
    await send_mail_group_auto(bot=bot)
    await message.answer("Рассылка отправлена ✅")
