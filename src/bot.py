from datetime import datetime
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import settings, TIMEZONE
from src.handlers import router as main_router
from src.handlers.admin_handlers import mailing
from src.utils import set_menu
from src.db.redis_connection import redis

# 1. Условно добавляем ../src в sys.path, если режим не PROD
if settings.MODE != 'PROD':
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
        # Временно логируем до полной настройки логгера
        temp_logger = logging.getLogger('temp_logger')
        temp_logger.setLevel(logging.DEBUG)
        temp_logger.addHandler(logging.StreamHandler(sys.stdout))
        temp_logger.debug(f"Added '{src_path}' to sys.path for non-PROD mode.")

# 2. Настройка логирования
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    
    if settings.MODE == 'PROD':
        log_dir = '/var/www/resto_bot/src/'
        log_file = os.path.join(log_dir, 'bot.log')
        if not os.path.isdir(log_dir):
            raise FileNotFoundError(f"Log directory does not exist: {log_dir}")

        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
logger.info("Logger initialized successfully.")

async def main():
    logger.info('Starting main function')
    try:
        # Инициализация бота, диспетчера и планировщика
        bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')
        logger.info('Bot initialized')
        
        storage = RedisStorage(redis=redis)
        logger.info('Redis storage initialized')
        
        dp = Dispatcher(storage=storage)
        dp.include_router(main_router)
        logger.info('Dispatcher and router set up')

        # Настройка планировщика
        execution_time = datetime.now(TIMEZONE).replace(hour=9, minute=0)
        trigger = CronTrigger(hour=execution_time.hour, minute=execution_time.minute, timezone=TIMEZONE)
        
        scheduler = AsyncIOScheduler(timezone=TIMEZONE)
        scheduler.add_job(mailing.create_mail_group_auto, trigger=trigger, kwargs={'bot': bot})
        scheduler.start()
        logger.info('Scheduler started')

        # Установка главного меню
        await set_menu.create_set_main_menu(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info('Webhook deleted and main menu set')
        
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Unhandled exception occurred in main: %s", e)

if __name__ == '__main__':
    logger.info("Starting main program.")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("Unhandled exception occurred during bot startup: %s", e)