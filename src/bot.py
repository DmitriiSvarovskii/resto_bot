import asyncio
import logging
import sys
import os
# from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
# from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage, Redis
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN
from handlers import register_user_commands, register_admin_commands
from utils import set_menu


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "src.")))

# run_time = datetime.now().replace(hour=13,
# minute=46, second=0, microsecond=0)

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)
    # schedular = AsyncIOScheduler(timezone='Asia/Kolkata')
    # schedular.add_job(create_mail_group_auto, trigger='date',
    #                   run_date=run_time,
    #                   kwargs={'bot': bot})
    # schedular.start()

    register_user_commands(dp)
    register_admin_commands(dp)

    await set_menu.create_set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
