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


@router.message(Command('13'))
async def create_mail_group_auto(bot: Bot):
    max_retries = 7
    logger.info("Handler 'create_mail_group_auto' started")

    for attempt in range(max_retries):
        logger.info(f"Attempt {attempt + 1} of {max_retries}")
        try:
            logger.debug("Fetching store information")
            store_info = await store_db.get_store_info(store_id=1)
            logger.info(f"Store info retrieved: {store_info}")

            text = (
                'Всем хорошего дня 🔥\n'
                'Эта кнопка для заказа через приложение Marcello 👇\n'
                'При заказе через приложение постоянная скидка на все меню 5% 👍\n'
                'Новая локация + лучший кофе ☕️ и кондиционер 🫶'
            )

            current_dir = os.path.dirname(os.path.abspath(__file__))
            static_folder = os.path.abspath(
                os.path.join(current_dir, '../../static'))
            logger.debug(f"Static folder path: {static_folder}")

            if not os.path.isdir(static_folder):
                logger.error(
                    f"Папка static не найдена по пути: {static_folder}")
                return

            file_list = os.listdir(static_folder)
            logger.debug(f"Files in static folder: {file_list}")

            if not file_list:
                logger.warning("В папке static нет файлов для отправки.")
                return

            random_file = random.choice(file_list)
            logger.info(f"Selected file: {random_file}")

            random_file_path = os.path.join(static_folder, random_file)
            if not os.path.isfile(random_file_path):
                logger.error(f"Файл не найден: {random_file_path}")
                return

            photo_file = types.FSInputFile(random_file_path)
            logger.debug(f"Photo file prepared: {photo_file}")

            await bot.send_photo(
                chat_id=store_info.sale_group,
                photo=photo_file,
                caption=text,
                reply_markup=admin_kb.create_kb_sale_group()
            )
            logger.info("Photo sent successfully.")
            break  # Выход из цикла при успешной отправке
        except TelegramBadRequest as e:
            logger.error(f"TelegramBadRequest: {e}")
            if attempt < max_retries - 1:
                logger.info("Retrying after TelegramBadRequest...")
                await asyncio.sleep(1)
            else:
                logger.critical(
                    "Максимальное количество попыток достигнуто. Сообщение не отправлено.")
        except Exception as e:
            logger.exception(f"Произошла непредвиденная ошибка: {e}")
            break
