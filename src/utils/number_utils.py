def is_number(text):
    if not text:
        return False
    if text[0] == '-':
        return text[1:].isdigit()
    return text.isdigit()
