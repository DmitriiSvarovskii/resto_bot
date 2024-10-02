from aiogram import Router, types, F

from src.keyboards import main_kb
from src.db import store_db, customer_db
from src.lexicons import text_main_menu_en, text_main_menu_ru
from src.callbacks import StoreCbDataList


router = Router(name=__name__)


@router.callback_query(StoreCbDataList.filter(F.type_press == "select-one"))
async def press_select_store(
    callback: types.CallbackQuery,
    callback_data: StoreCbDataList
):
    store_info = await store_db.get_store_info(store_id=callback_data.store_id)
    user_info = await customer_db.get_user_info_by_id(
        user_id=callback.message.chat.id
    )

    if store_info.is_active or user_info.admin:
        if callback.from_user.language_code == 'ru':
            text_main_menu = text_main_menu_ru
        else:
            text_main_menu = text_main_menu_en

        keyboard = await main_kb.create_kb_main(
            language=callback.from_user.language_code,
            user_id=callback.message.chat.id,
            store_id=callback_data.store_id
        )

        await callback.message.edit_text(
            text=text_main_menu.main_menu_dict['start'],
            reply_markup=keyboard
        )
    else:
        await callback.answer(
            text="Извините, магазин временно не работает",
            show_alert=True
        )


@router.callback_query(StoreCbDataList.filter(F.type_press == 'view-list'))
async def press_store_list(
    callback: types.CallbackQuery,
    callback_data: StoreCbDataList
):
    if callback.from_user.language_code == 'ru':
        text_main_menu = text_main_menu_ru
    else:
        text_main_menu = text_main_menu_en

    store_data = await store_db.db_get_store_list()

    keyboard = await main_kb.create_kb_select_store(
        language=callback.from_user.language_code,
        store_list=store_data
    )

    # await callback.message.answer(
    #     text=text_main_menu.main_menu_dict['start'],
    #     reply_markup=keyboard
    # )
    await callback.message.edit_text(
        text=text_main_menu.main_menu_dict['start'],
        reply_markup=keyboard
    )


# Добро пожаловать в нашу пиццерию 🍕🇮🇹
# Наслаждайтесь аутентичными вкусами и разнообразием итальянских пицц на любойвкус прямо у себя дома 🏠
# Работает доставка до вашего стола 🍕🫶

# Добро пожаловать в нашу пиццерию 🍕🇮🇹
# Наслаждайтесь аутентичными вкусами и разнообразием итальянских пицц на любойвкус прямо у себя дома 🏠
# Работает доставка до вашего стола 🍕🫶
