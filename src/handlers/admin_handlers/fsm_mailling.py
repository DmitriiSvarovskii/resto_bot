from aiogram import Bot, types, Router, F
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.context import FSMContext

from src.db import customer_db, store_db
from src.keyboards import main_kb
from src.callbacks import StoreAdminCbData


router = Router(name=__name__)


# @router.callback_query(F.data == 'press_mailling')
async def start_fsm_mailling(callback: types.CallbackQuery,
                             state: FSMContext):
    pass


@router.callback_query(StoreAdminCbData.filter(F.type_press == 'mailling'))
async def create_mail_chats(callback: types.CallbackQuery,
                            bot: Bot,
                            state: FSMContext):
    customer_list = await customer_db.db_get_users_list()
    store_list = await store_db.db_get_store_list()
    for user_data in customer_list:
        try:
            await bot.send_message(
                chat_id=user_data.user_id,
                text=('🎉 Мы с радостью объявляем, что вторая точка пиццерии Marcello теперь открыта в Гоа!'

                      '\n\nА также мы добавили новый точку в наш телеграм-бот. Теперь при запуске бота, Вам сначала нужно выбрать точку, в которой хотите сделать заказ 🤖'

                      '\n\nПрисоединяйтесь к нам, чтобы насладиться вкусом и атмосферой, которые вы полюбили.'
                      '\nЖдем вас! 🍕🎈'
                      '\nВагатор, напротив заправки ⛽️'
                      '\nЛокация прикреплена в меню бота Vagator outlet 📍'
                      '\nГрафик работы в Вагаторе 5pm - 12 am'),
                reply_markup=await main_kb.create_kb_select_store(
                    language='ru', store_list=store_list
                )
            )

        except TelegramForbiddenError:
            continue
        except Exception:
            continue
    await callback.message.answer(
        text='Рассылка завершена.'
    )
