import asyncio
import logging
import sys
import os

from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import settings, TIMEZONE
from src.handlers import router as main_router
from src.handlers.mailing import create_mail_group_auto
from src.utils import set_menu


sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../src")))


execution_time = datetime.now(TIMEZONE).replace(hour=13, minute=0)

trigger = CronTrigger(hour=execution_time.hour,
                      minute=execution_time.minute, timezone=TIMEZONE)

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')
    bot: Bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    storage = RedisStorage(redis=redis)
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(main_router)
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(create_mail_group_auto,
                      trigger=trigger, kwargs={'bot': bot})

    scheduler.start()

    await set_menu.create_set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
