# from typing import List, Union
# from aiogram.types import CallbackQuery

# from src.services import ORDER_STATUSES
# from src.lexicons import new_order_mess_text_order_chat
# from src.schemas import (
#     CreateOrder,
#     CartItem,
#     ReadCustomerInfo,
#     CreateOrderInfo,
# )
# from src.fsm_state import user_dict_comment, user_dict
# from services.order_constants import ORDER_TYPES
# from src.db import store_db, order_db, delivery_db
# from src.callbacks import (
#     CheckOrdersCallbackFactory,
#     OrderStatusCallbackFactory,
#     CreateOrderCallbackFactory,
# )

# async def 
#     store_info = await store_db.get_store_info()


# async def get_store_info():
#     async for session in get_async_session():
#         store_info = await crud_get_store_info(session=session)

#         keyboard = create_keyboard_toggle_bot(
#             store_info=store_info
#         )
#         break
#     return keyboard