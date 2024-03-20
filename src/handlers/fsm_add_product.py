from aiogram import types, Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.utils import create_product
from src.db import product_db, category_db
from src.keyboards import (
    admin_kb,
    category_kb,
    fsm_add_new_product_kb,
)
from src.state import FSMAddNewProduct
from src.callbacks import (
    AddProductAvailabilityCallbackFactory,
    CategoryAdminAddCallbackFactory,
)


router = Router(name=__name__)


@router.callback_query(F.data == 'press_add_product')
async def process_add_new_product(
    callback: types.CallbackQuery,
    state: FSMContext
):
    categories = await category_db.get_all_categories_admin()
    keyboard = await category_kb.create_kb_category_admin_add_prod(
        categories=categories
    )
    await callback.message.answer(
        text='Выберите категорию, к которой относится товар. Если необходимой '
        'категории нет в наличии, необходимо отменить добавление нового '
        'товара, далее создать новую категорию, а уже после, в эту '
        'категорию добавить новый товар.',
        reply_markup=keyboard
    )
    await state.set_state(FSMAddNewProduct.category_id)


@router.message(F.text == LEXICON_KEYBOARDS_RU['cancel_add_product'])
async def process_cancel_command_state_order(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text='Вы отменили добавление нового товара',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await message.answer(
        text='Выберите пункт меню',
        reply_markup=admin_kb.create_kb_edit_menu()
    )


@router.callback_query(
    FSMAddNewProduct.category_id,
    CategoryAdminAddCallbackFactory.filter()
)
async def process_waiting_category_id(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: CategoryAdminAddCallbackFactory
):
    await state.update_data(
        category_id=callback_data.category_id,
        category_name=callback_data.category_name
    )
    if callback.message:
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass
    await callback.message.answer(
        text='Введите название продукта',
        reply_markup=fsm_add_new_product_kb.create_kb_fsm_canel()
    )
    await state.set_state(FSMAddNewProduct.product_name)


@router.message(FSMAddNewProduct.product_name, F.text)
async def process_waiting_product_name(
    message: types.Message,
    state: FSMContext
):
    await state.update_data(name=message.text)
    await message.answer(
        text='Введите описание продукта, либо перейдите к следующему шагу',
        reply_markup=fsm_add_new_product_kb.create_kb_fsm_canel_and_skip()

    )
    await state.set_state(FSMAddNewProduct.description)


@router.message(FSMAddNewProduct.description, F.text)
async def process_waiting_description(
    message: types.Message,
    state: FSMContext
):
    if message.text == LEXICON_KEYBOARDS_RU['skip']:
        await state.update_data(description='Описание отсутствует')
    else:
        await state.update_data(description=message.text)
    await message.answer(
        text='Введите цену продукта',
        reply_markup=fsm_add_new_product_kb.create_kb_fsm_canel()

    )
    await state.set_state(FSMAddNewProduct.price)


@router.message(FSMAddNewProduct.price, F.text.isdigit())
async def process_waiting_price(message: types.Message, state: FSMContext):
    await state.update_data(price=int(message.text))
    await message.answer(
        text='Введите цену упаковки, если товар отдаётся без упаковки, пропустите шаг',
        reply_markup=fsm_add_new_product_kb.create_kb_fsm_canel_and_skip()

    )
    await state.set_state(FSMAddNewProduct.price_box)


@router.message(FSMAddNewProduct.price, F.text)
async def process_error_price(message: types.Message, state: FSMContext):
    await message.answer(
        text='Отправленное значение не похоже на число, введите цену продукта, используйте только цифры.',
        reply_markup=fsm_add_new_product_kb.create_kb_fsm_canel()

    )


@router.message(
    FSMAddNewProduct.price_box,
    F.text.isdigit() | (F.text == LEXICON_KEYBOARDS_RU['skip'])
)
async def process_waiting_price_box(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price_box=int(message.text))
    else:
        await state.update_data(price_box=0)
    await message.answer(
        text='Укажите, товар сейчас есть в наличии или он отсутствует',
        reply_markup=fsm_add_new_product_kb.create_kb_availability()
    )
    await state.set_state(FSMAddNewProduct.availability)


@router.message(FSMAddNewProduct.price_box, F.text)
async def process_error_price_box(message: types.Message, state: FSMContext):
    await message.answer(
        text='Отправленное значение не похоже на число, введите цену упаковки, используйте только цифры.',

    )


@router.callback_query(
    FSMAddNewProduct.availability,
    AddProductAvailabilityCallbackFactory.filter()
)
async def process_waiting_availability(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: AddProductAvailabilityCallbackFactory
):
    await state.update_data(availability=callback_data.availability)
    data = await state.get_data()
    await callback.message.edit_reply_markup(
        inline_message_id=callback.inline_message_id,
        reply_markup=None)
    await callback.message.answer(
        text=(
            'Проверьте корректность введённых данных.'
            'Если всё верно, нажмите на кнопку "Подтвердить добавление",'
            'Если вы видети ошибку, нажмите кнопку "Изменить данные" и '
            'повторите процесс добавления нового товара'
        ),
        reply_markup=fsm_add_new_product_kb.create_kb_fsm_canel()

    )
    await callback.message.answer(
        text=(
            f"Категория: {data['category_name']}\n"
            f"Название товара: {data['name']}\n"
            f"Описание товара: {data['description']}\n"
            f"Цена товара: {data['price']}\n"
            f"Цена упаковки: {data['price_box']}\n"
        ),
        reply_markup=fsm_add_new_product_kb.create_kb_approval()
    )
    await state.set_state(FSMAddNewProduct.check)


@router.callback_query(
    FSMAddNewProduct.check,
    F.data == 'press_make_changes_prod'
)
async def process_waiting_make_changes(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    categories = await category_db.get_all_categories_admin()
    keyboard = await category_kb.create_kb_category_admin_add_prod(
        categories=categories
    )
    await callback.message.answer(
        text='Выберите категорию, к которой относится товар. Если необходимой '
        'категории нет в наличии, необходимо отменить добавление нового '
        'товара, далее создать новую категорию, а уже после, в эту '
        'категорию добавить новый товар.',
        reply_markup=keyboard
    )
    await state.set_state(FSMAddNewProduct.category_id)


@router.callback_query(
    FSMAddNewProduct.check,
    F.data == 'press_approval_prod'
)
async def process_waiting_approval(
    callback: types.CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()
    data_product = await create_product.create_data_product(data=data)
    await product_db.db_create_new_product(data=data_product)
    message_text = 'Выберите пункт меню'
    await callback.message.edit_reply_markup(
        inline_message_id=callback.inline_message_id,
        reply_markup=None)
    await callback.message.answer(
        text='Продукт успешно добавлен',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await callback.message.answer(
        text=message_text,
        reply_markup=admin_kb.create_kb_edit_menu()
    )
    await state.clear()
