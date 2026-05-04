from datetime import datetime, timedelta, time
from datetime import datetime, timezone, timedelta

from src.config import TIMEZONE
from src.db import store_db


async def is_valid_time_warning(store_id: int):
    data = await store_db.get_store_info(store_id=store_id)

    closing_time = data.closing_time

    current_time = datetime.now(TIMEZONE)

    today = datetime.now().date()
    closing_datetime = datetime.combine(today, closing_time)

    closing_datetime = closing_datetime.astimezone(TIMEZONE)

    time_until_closing = closing_datetime - current_time

    return time_until_closing <= timedelta(minutes=30)


async def is_valid_time(store_id: int):
    data = await store_db.get_store_info(store_id=store_id)

    opening_time = data.opening_time
    closing_time = data.closing_time

    current_datetime = datetime.now(TIMEZONE)
    current_time = current_datetime.time()

    if opening_time is None or closing_time is None:
        return True

    opening_time_with_buffer = (
        datetime.combine(current_datetime.date(), opening_time)
        - timedelta(minutes=15)
    ).time()

    # Обычный график, например 10:00–22:00
    if opening_time_with_buffer < closing_time:
        return opening_time_with_buffer <= current_time <= closing_time

    # График через полночь, например 12:00–04:00
    return current_time >= opening_time_with_buffer or current_time <= closing_time


async def check_time(timestamp):
    db_time = timestamp.replace(tzinfo=timezone.utc).astimezone(TIMEZONE)

    current_time = datetime.now(TIMEZONE)

    time_difference = current_time - db_time

    if time_difference > timedelta(minutes=15):
        return False
    else:
        return True
