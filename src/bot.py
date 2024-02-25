from pytz import timezone
import asyncio
import logging
import sys
import os

from apscheduler.triggers.cron import CronTrigger
from datetime import time

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings
from handlers import (
    register_user_commands,
    register_admin_commands,
    create_mail_group_auto,
)
from utils import set_menu


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "src.")))


kolkata_timezone = timezone('Asia/Kolkata')

# Установка времени выполнения в соответствии с таймзоной
execution_time = time(hour=13, minute=0, tzinfo=kolkata_timezone)


trigger = CronTrigger(hour=execution_time.hour, minute=execution_time.minute)

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    bot: Bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')
    redis = Redis(host=settings.DB_HOST)
    storage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)
    scheduler = AsyncIOScheduler(timezone='Asia/Kolkata')
    scheduler.add_job(create_mail_group_auto,
                      trigger=trigger, kwargs={'bot': bot})

    scheduler.start()

    register_user_commands(dp)
    register_admin_commands(dp)

    await set_menu.create_set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
