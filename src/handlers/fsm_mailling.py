import random
import os
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram import Bot, types, Router, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramForbiddenError

from src.db import customer_db, store_db
from src.keyboards import admin_kb, main_kb
from src.state import FSMMailingPhoto

router = Router(name=__name__)


@router.callback_query(F.data == 'press_mailling')
async def start_fsm_mailling(callback: types.CallbackQuery,
                             state: FSMContext):
    pass


async def create_mail_chats(callback: types.CallbackQuery,
                            bot: Bot,
                            state: FSMContext):
    customer_list = await customer_db.db_get_users_list()
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
    await callback.message.answer(
        text='Рассылка завершена.'
    )