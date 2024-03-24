from . import text_common_en


def create_comments_message():
    message = (
        'Please send your comments to our chefs by message.'
        f' To cancel, press the "{text_common_en.common_dict["cancel"]}" '
        'button.'
    )
    return message


comment_dict: dict[str, str] = {
    'comment_input_cancelled': 'You have canceled the comment input.\n\n',
}
