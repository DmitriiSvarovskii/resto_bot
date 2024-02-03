from aiogram.filters.callback_data import CallbackData


class DeliveryIdCallbackFactory(CallbackData, prefix="dlv"):
    delivery_id: int
