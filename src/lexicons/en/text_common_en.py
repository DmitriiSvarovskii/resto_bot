common_dict: dict[str, str] = {
    'cancel': 'Cancel ❌',
    'cancel_delivery': 'Abort the design ❌',
    'skip': 'Skip step',
    'good': 'ok!',
    'invalid_request': 'Invalid request',
}


def get_telegram_id(user_id):
    return f'Your id in Telegram is {user_id}'
