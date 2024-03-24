from . import text_common_ru


def create_comments_message():
    message = (
        'Пожалуйста, пришлите сообщением комментарии для наших поваров.'
        f' Для отмены нажмите на кнопку "{text_common_ru.common_dict["cancel"]}"'
    )
    return message


comment_dict: dict[str, str] = {
    'comment_input_cancelled': 'Вы отменили ввод комментария.\n\n',
}
