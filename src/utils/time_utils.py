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

    opening_time_base = data.opening_time
    closing_time = data.closing_time

    current_time = datetime.now(TIMEZONE)

    opening_datetime = datetime.combine(datetime.today(), opening_time_base)

    print(opening_datetime)
    print(closing_time)
    print(current_time)
    opening_time = opening_datetime - timedelta(minutes=15)

    start_hour, start_minute = opening_time.hour, opening_time.minute
    end_hour, end_minute = closing_time.hour, closing_time.minute

    current_hour, current_minute = current_time.hour, current_time.minute

    if (
        (start_hour < current_hour < end_hour) or
        (start_hour == current_hour and start_minute <= current_minute) or
        (end_hour == current_hour and current_minute <= end_minute)
    ):
        return True
    else:
        return False


async def check_time(timestamp):
    db_time = timestamp.replace(tzinfo=timezone.utc).astimezone(TIMEZONE)

    current_time = datetime.now(TIMEZONE)

    time_difference = current_time - db_time

    if time_difference > timedelta(minutes=15):
        return False
    else:
        return True
