import pytz
from datetime import datetime

time_zone = pytz.timezone('Asia/Kolkata')  # GMT+5:30 (Goa)


def is_valid_time_warning():
    current_time = pytz.utc.localize(datetime.utcnow()).astimezone(time_zone)
    return 22 <= current_time.hour and 30 <= current_time.minute < 59


def is_valid_time():
    current_time = pytz.utc.localize(datetime.utcnow()).astimezone(time_zone)

    start_hour, start_minute = 11, 45
    end_hour, end_minute = 22, 59

    current_hour, current_minute = current_time.hour, current_time.minute

    if start_hour < current_hour < end_hour:
        return True
    elif start_hour == current_hour and start_minute <= current_minute:
        return True
    elif end_hour == current_hour and current_minute <= end_minute:
        return True

    return False
