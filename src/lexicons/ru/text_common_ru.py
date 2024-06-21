common_dict: dict[str, str] = {
    'cancel': 'Прервать ❌',
    'cancel_delivery': 'Прервать оформление ❌',
    'skip': 'Пропустить шаг',
    'good': 'ок!',
    'invalid_request': 'Некорректный запрос',
}


def get_telegram_id(user_id):
    return f'Ваш id в телеграм {user_id}'
