from aiogram import Router, types, Bot
from aiogram.filters import CommandStart

from src.db import customer_db
from src.config import settings
from src.utils import customer_utils
from src.keyboards import main_kb, admin_kb
from src.lexicons import text_main_menu_en, text_main_menu_ru


router = Router(name=__name__)
bot: Bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')


@router.message(CommandStart())
async def process_start_command(message: types.Message):
    if message.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    if message.chat.type == 'private':
        customer_data = await customer_utils.create_customer_data_from_message(
            message=message
        )
        await customer_db.add_new_user_to_database(
            customer_data=customer_data
        )
        keyboard = await main_kb.create_kb_main(
            language=message.from_user.language_code,
            user_id=message.chat.id,
        )

        await message.answer(
            text=text_main_menu.main_menu_dict['start'],
            reply_markup=keyboard
        )
    else:
        await message.reply(
            text=text_main_menu.main_menu_dict['error_private_chat'],
            reply_markup=admin_kb.create_kb_sale_group()
        )
