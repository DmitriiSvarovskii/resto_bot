from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from src.state import FSMProductChangeCategory
from src.callbacks import (
    ProductChangeCategoryCallbackFactory,
    ChangeCategoryProductCallbackFactory,
)
from src.lexicons import LEXICON_RU
from src.db import product_db, category_db
from src.keyboards import product_kb, category_kb
from src.handlers import admin_handlers

router = Router(name=__name__)


@router.callback_query(ProductChangeCategoryCallbackFactory.filter())
async def process_waiting_new_product_name(
    callback: types.CallbackQuery,
    callback_data: ProductChangeCategoryCallbackFactory,
    state: FSMContext
):
    await state.update_data(product_id=callback_data.product_id)
    try:
        await callback.message.delete()
    except Exception as e:
        print(e)
    await callback.message.answer(
        text='Для отмены воспользуйтесь кнопкой отмены',
        reply_markup=product_kb.create_kb_fsm_change_name()
    )
    categories = await category_db.get_all_categories()
    keyboard = await category_kb.create_kb_category_admin(
        categories=categories,
        callback_data=ChangeCategoryProductCallbackFactory,
        language=callback.from_user.language_code
    )
    await callback.message.answer(
        text='Выберите новую категорию для товара',
        reply_markup=keyboard
    )
    await state.set_state(FSMProductChangeCategory.id)


@router.message(F.text == 'Отменить изменение')
async def process_cancel_command_state(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text='Вы отменили изменение категории',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await admin_handlers.process_edit_menu_mess(
        message=message,
    )


@router.callback_query(
    FSMProductChangeCategory.id,
    ChangeCategoryProductCallbackFactory.filter()
)
async def process_comment_sent(
    callback: types.CallbackQuery,
    callback_data: ChangeCategoryProductCallbackFactory,
    state: FSMContext
):
    await state.update_data(category_id=callback_data.category_id)
    data = await state.get_data()
    await callback.message.answer(
        text=LEXICON_RU['good'],
        reply_markup=types.ReplyKeyboardRemove()
    )
    await product_db.db_update_product(
        product_id=data['product_id'],
        data=data
    )
    await state.clear()

    await admin_handlers.press_admin_menu(
        callback=callback,
    )
