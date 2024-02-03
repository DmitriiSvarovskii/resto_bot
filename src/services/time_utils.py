import pytz
from datetime import datetime


def is_valid_time_warning():
    tz = pytz.timezone('Asia/Kolkata')  # GMT+5:30 (Goa)
    current_time = pytz.utc.localize(datetime.utcnow()).astimezone(tz)
    return 23 <= current_time.hour and 30 <= current_time.minute < 59


def is_valid_time():
    tz = pytz.timezone('Asia/Kolkata')  # GMT+5:30
    current_time = pytz.utc.localize(datetime.utcnow()).astimezone(tz)

    # Устанавливаем значения часов и минут для начала и конца интервала
    start_hour, start_minute = 00, 1
    end_hour, end_minute = 23, 59

    # Получаем текущие часы и минуты
    current_hour, current_minute = current_time.hour, current_time.minute

    # Проверяем, находится ли текущее время в заданном интервале
    if start_hour < current_hour < end_hour:
        return True
    elif start_hour == current_hour and start_minute <= current_minute:
        return True
    elif end_hour == current_hour and current_minute <= end_minute:
        return True

    return False
