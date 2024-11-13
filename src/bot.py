print("Script started")

from datetime import datetime
print("Imported datetime")

import sys
print("Imported sys")

import os
print("Imported os")

import logging
from logging.handlers import RotatingFileHandler
print("Imported logging and handlers")

import asyncio
print("Imported asyncio")

from aiogram import Bot, Dispatcher
print("Imported aiogram Bot and Dispatcher")

from aiogram.fsm.storage.redis import RedisStorage
print("Imported RedisStorage from aiogram")

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
print("Imported AsyncIOScheduler and CronTrigger")

from src.config import settings, TIMEZONE
print("Imported settings and TIMEZONE from src.config")

from src.handlers import router as main_router
print("Imported main_router from src.handlers")

from src.handlers.admin_handlers import mailing
print("Imported mailing from src.handlers.admin_handlers")

from src.utils import set_menu
print("Imported set_menu from src.utils")

from src.db.redis_connection import redis
print("Imported redis from src.db.redis_connection")

# Условно добавляем ../src в sys.path, если режим не PROD
if settings.MODE != 'PROD':
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
        print(f"Added '{src_path}' to sys.path for non-PROD mode.")

# Настройка логирования
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    
    if settings.MODE == 'PROD':
        log_dir = '/var/www/resto_bot/src/'
        log_file = os.path.join(log_dir, 'bot.log')
        if not os.path.isdir(log_dir):
            print(f"Log directory does not exist: {log_dir}")
            raise FileNotFoundError(f"Log directory does not exist: {log_dir}")

        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    print("Logging setup completed")
    return logger

# Инициализация логирования
logger = setup_logging()
logger.info("Logger initialized successfully.")

async def main():
    logger.info("Starting main function")
    print("Starting main function")
    try:
        # Инициализация бота, диспетчера и планировщика
        bot = Bot(token=settings.BOT_TOKEN, parse_mode='HTML')
        logger.info('Bot initialized')
        print("Bot initialized")
        
        storage = RedisStorage(redis=redis)
        logger.info('Redis storage initialized')
        print("Redis storage initialized")
        
        dp = Dispatcher(storage=storage)
        dp.include_router(main_router)
        logger.info('Dispatcher and router set up')
        print("Dispatcher and router set up")

        # Настройка планировщика
        execution_time = datetime.now(TIMEZONE).replace(hour=9, minute=0)
        trigger = CronTrigger(hour=execution_time.hour, minute=execution_time.minute, timezone=TIMEZONE)
        
        scheduler = AsyncIOScheduler(timezone=TIMEZONE)
        scheduler.add_job(mailing.create_mail_group_auto, trigger=trigger, kwargs={'bot': bot})
        scheduler.start()
        logger.info('Scheduler started')
        print("Scheduler started")

        # Установка главного меню
        await set_menu.create_set_main_menu(bot)
        logger.info('Main menu set up')
        print("Main menu set up")
        
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info('Webhook deleted')
        print("Webhook deleted")
        
        await dp.start_polling(bot)
        print("Polling started")
    except Exception as e:
        logger.exception("Unhandled exception occurred in main: %s", e)
        print(f"Exception in main: {e}")

if __name__ == '__main__':
    logger.info("Starting main program.")
    print("Starting main program")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("Unhandled exception occurred during bot startup: %s", e)
        print(f"Exception during bot startup: {e}")