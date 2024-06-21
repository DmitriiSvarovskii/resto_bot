import json
from typing import Optional, Any, Dict

from src.db.redis_connection import redis


async def save_data_to_redis(
    key_prefix: str,
    user_id: int,
    data: dict
) -> None:
    redis_key = f"{key_prefix}:{user_id}"
    await redis.set(redis_key, json.dumps(data))


async def get_data_from_redis(
    key_prefix: str,
    user_id: int
) -> Optional[Dict[str, Any]]:
    redis_key = f"{key_prefix}:{user_id}"
    data = await redis.get(redis_key)
    if data is not None:
        data_dict = json.loads(data)
        data_dict.pop('store_id', None)
        return data_dict
    return None


async def delete_data_from_redis(
    key_prefix: str,
    user_id: int
) -> None:
    redis_key = f"{key_prefix}:{user_id}"
    exists = await redis.exists(redis_key)
    if exists:
        await redis.delete(redis_key)
