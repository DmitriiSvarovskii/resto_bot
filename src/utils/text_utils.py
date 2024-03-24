def get_text(text_ru, text_en, language_code):
    if language_code == 'ru':
        return text_ru
    else:
        return text_en


def is_number(text):
    if not text:
        return False
    if text[0] == '-':
        return text[1:].isdigit()
    return text.isdigit()
