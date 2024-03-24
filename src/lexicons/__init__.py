from .lexicon_ru import (
    LEXICON_KEYBOARDS_RU,
    LEXICON_RU,
    LEXICON_COMMANDS_RU,
    func_cart_text,
    new_order_mess_text_order_chat,
    get_comments_prompt_message,
    generate_order_info_text,
    generate_order_info_time_text,
)
from . import admin_text, cart_text

from .ru import (
    text_main_menu_ru,
    text_cart_ru,
    text_menu_ru,
    text_order_ru,
    text_fsm_delivery_ru,
    text_common_ru,
    text_comment_ru,
)
from .en import (
    text_main_menu_en,
    text_cart_en,
    text_menu_en,
    text_order_en,
    text_fsm_delivery_en,
    text_common_en,
    text_comment_en,
)

__all__ = [
    'text_comment_ru',
    'text_comment_en',
    'text_common_ru',
    'text_common_en',
    'text_fsm_delivery_ru',
    'text_fsm_delivery_en',
    'text_order_ru',
    'text_order_en',
    'text_menu_ru',
    'text_menu_en',
    'text_cart_ru',
    'text_cart_en',
    'text_main_menu_en',
    'text_main_menu_ru',
    'admin_text',
    'LEXICON_KEYBOARDS_RU',
    'LEXICON_COMMANDS_RU',
    'LEXICON_RU',
    'cart_text',
    'func_cart_text',
    'new_order_mess_text_order_chat',
    'get_comments_prompt_message',
    'generate_order_info_text',
    'generate_order_info_time_text',
]
