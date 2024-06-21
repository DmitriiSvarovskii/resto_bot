from aiogram.fsm.storage.redis import Redis
from src.config import settings

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
