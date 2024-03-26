from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from src.lexicons import LEXICON_KEYBOARDS_RU
from src.db import category_db
from src.schemas import category_schemas
from src.keyboards import (
    admin_kb,
    fsm_add_new_category_kb,
)
from src.state import FSMAddNewCategory
from src.callbacks import (
    AddCategoryAvailabilityCallbackFactory,
)


router = Router(name=__name__)


@router.callback_query(F.data == 'press_add_category')
async def process_add_new_product(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.message.answer(
        text='Введите название новой категории на русском языке',
        reply_markup=fsm_add_new_category_kb.create_kb_fsm_canel()
    )
    await state.set_state(FSMAddNewCategory.category_name_rus)


@router.message(F.text == LEXICON_KEYBOARDS_RU['cancel_add_category'])
async def process_cancel_command_state_order(
    message: types.Message,
    state: FSMContext
):
    await message.answer(
        text='Вы отменили добавление новой категории',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
    await message.answer(
        text='Выберите пункт меню',
        reply_markup=admin_kb.create_kb_edit_menu()
    )


@router.message(
    FSMAddNewCategory.category_name_rus,
    F.text
)
async def process_waiting_category_name(
    message: types.Message,
    state: FSMContext,
):
    await state.update_data(
        name_rus=message.text
    )
    await message.answer(
        text='Введите название новой категории на английском языке',
        reply_markup=fsm_add_new_category_kb.create_kb_fsm_canel()
    )
    await state.set_state(FSMAddNewCategory.category_name_en)


@router.message(
    FSMAddNewCategory.category_name_en,
    F.text
)
async def process_waiting_category_id(
    message: types.Message,
    state: FSMContext,
):
    await state.update_data(
        name_en=message.text
    )
    await message.answer(
        text='Укажите, данная категория сейчас есть в наличии или он отсутствует',
        reply_markup=fsm_add_new_category_kb.create_kb_availability()
    )
    await state.set_state(FSMAddNewCategory.availability)


@router.callback_query(
    FSMAddNewCategory.availability,
    AddCategoryAvailabilityCallbackFactory.filter()
)
async def process_waiting_availability(
    callback: types.CallbackQuery,
    state: FSMContext,
    callback_data: AddCategoryAvailabilityCallbackFactory
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
            'повторите процесс добавления новой категории'
        ),
        reply_markup=fsm_add_new_category_kb.create_kb_fsm_canel()

    )
    await callback.message.answer(
        text=(
            f"Категория (рус): {data['name_rus']}\n"
            f"Категория (англ): {data['name_en']}\n"
        ),
        reply_markup=fsm_add_new_category_kb.create_kb_approval()
    )
    await state.set_state(FSMAddNewCategory.check)


@router.callback_query(
    FSMAddNewCategory.check,
    F.data == 'press_make_changes_cat'
)
async def process_waiting_make_changes(
    callback: types.CallbackQuery,
    state: FSMContext
):
    await callback.message.delete()
    await callback.message.answer(
        text='Выберите название новой категории на русском языке',
        reply_markup=fsm_add_new_category_kb.create_kb_fsm_canel()
    )
    await state.set_state(FSMAddNewCategory.category_name_rus)


@router.callback_query(
    FSMAddNewCategory.check,
    F.data == 'press_approval_cat'
)
async def process_waiting_approval(
    callback: types.CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()
    data_category = category_schemas.CreateCategory(**data)
    await category_db.db_create_new_category(data=data_category)
    message_text = 'Выберите пункт меню'
    await callback.message.edit_reply_markup(
        inline_message_id=callback.inline_message_id,
        reply_markup=None)
    await callback.message.answer(
        text='Категория успешно добавлена',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await callback.message.answer(
        text=message_text,
        reply_markup=admin_kb.create_kb_edit_menu()
    )
    await state.clear()
