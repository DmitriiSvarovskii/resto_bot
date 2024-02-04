import logging
import asyncio
from aiogram import Bot, Dispatcher

from src.keyboards import set_main_menu
from src.handlers import register_user_commands, register_admin_commands
from src.config import BOT_TOKEN


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    register_user_commands(dp)
    register_admin_commands(dp)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
