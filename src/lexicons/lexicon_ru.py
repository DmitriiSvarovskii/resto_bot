import pytz
from aiogram.types import CallbackQuery
from datetime import datetime
from typing import Optional, Union

from src.schemas import customer_schemas, delivery_schemas, order_schemas
from src.services import get_status_name_by_id
from src.callbacks import (
    TimeOrdersCallbackFactory,
    CheckOrdersCallbackFactory,
    OrderStatusCallbackFactory
)

LEXICON_RU: dict[str, str] = {
    'start':
        "Добро пожаловать в нашу пиццерию! Наслаждайтесь аутентичными "
        "вкусами и разнообразием свежих пицц на каждый вкус.",
    'main_menu':
        "Добро пожаловать в нашу пиццерию! Отведайте истинные итальянские "
        "вкусы с 12:00 до 04:00. Нежное тесто, сочные начинки и уютная "
        "атмосфера ждут вас!\n\n",
    'store': "Наше меню",
    'delivery': 'Информаци по доставке 🛵'
                '\n\nСтомость доставки по районам:'
                '\nMorjim 100r'
                '\nAshwem 150r'
                '\nAgarvado 150r'
                '\nSiolim 200r'
                '\nМаndrem 200r'
                '\nUpper Mandrem 250r'
                '\nАrambol 250r'
                '\nVagator 350r'
                '\nКеrim 350r'
                '\nPaliem 350r\n\n'
                'P.s. При оформении доставки следуйте подсказкам нашего бота)',
    'contact': 'Pizzeria Marcello🍕🍝\n\n'
               'Самая Итальянская пицца в Гоа🍕🍝🔥.\n\n'
               'Морджим, Turtle Beach road.\n\n'
               'По всем вопросам пишите или звоните\n'
               '@POKANEPOZDN0\n+918149843927\n\n'
               '<a href="https://t.me/+V7peNNs0XqRlYjll">Наша группа в телеграм</a>',
    'personal_area': 'Добро пожаловать в личный кабинет.\n\n'
    'Вы можете посмотреть историю своих заказов, чтобы посмотреть'
    ' детали заказа, нажмите кнопку "Подробнее"\n\n'
    '"Отменить ✖️" - кнопка, для отмены заказа\n\n'
    '<i>Отмена заказа возможна в течении '
    '15 минут, после его оформления</i>',
    'edit_cart': 'Отредактируйте выбранные товары используя кнопки: '
                 '"➕", "➖" или "✖️".\n\n'
                 '"➕" - добавить ещё 1 единицу товара в корзину\n\n'
                 '"➖" - убрать 1 единицу товара из корзины\n\n'
                 '"✖️" - полностью удалить выбранный товар\n\n'
                 'Также вы можете полностью очистить корзину, '
                 'нажав кнопку "Очистить"\n\n',
    'category': 'Что хотите купить?',
    'closing_time_reminder': 'Внимание, в 04:00 мы закрываемся, но у вас ещё '
                             'есть время) не затягивайте с выбором)',
    'closing_time': 'Упсsrc..((\n\nИзвините, оформить заказ не получится.\n'
                    'Мы работаем с 12:00 до 04:00.\n'
                    'Будем рады накормить вас в рабочие часы)',
    'finish_category': 'Извините, блюда из данной категории сейчас закончились'
                       ', они появятся в ближайшее время, а пока можете '
                       'заказать что-нибудь другое)',
    'cart_text': 'Ваш заказ:\n\n',
    'empty_cart': 'Ваша корзина пуста',
    'cart_error': 'Товар в корзине отсутствует!',


    'delivery_districts': 'Для оформления доставки ответьте пожалуйста '
                          'на несколько вопросов, буквально пара минут.\n\n'
                          'Выберите район, куда необходимо доставить заказ',
    'abort_delivery': 'Вы прервали оформление доставки.\n\n',
    'order_saved_message': 'Ваш заказ по прежнему сохранен в корзине, '
                           'вы можете продолжить оформление в любое '
                           'удобное для Вас время.',
    'phone_input': 'А теперь введите ваш местный (Индийский) номер '
                   'телефона в формате "7812345678", без +91. '
                   'Если у вас нет местного номера телефона, '
                   'нажмите "Пропустить шаг"',
    'phone_number_error_message': 'Похоже в номере допущена ошибка, проверьте '
                                  'пожалуйста корректность номера\n\n'
                                  'Номер телефона должен состоять из '
                                  '10 цифр\n\n'
                                  'Если у вас нету местного номера, '
                                  'нажмите кнопку "Пропустить шаг"',
    'delivery_comment_prompt': 'Окей, идем дальше.\n\n'
                               'Теперь напишите комментарий для курьера.\n\n'
                               'Если комментариев нет, '
                               'нажмите "Пропустить шаг")',
    'location_request_step': 'Супер, остался последний шаг и закончили))\n\n'
                             'Теперь пришлите Вашу геолокацию\n\n'
                             'ВАЖНО. Для прикрепления геолокации используйте '
                             'отправку местоположения через телеграм.\n\n'
                             'Если нет возмодности отправить геолокацию, '
                             'нажмите "Пропустить шаг" и свяжитесь с нашим '
                             'менеджером, для уточнения деталей заказа '
                             '@POKANEPOZDN0',
    'error_comment': 'Произошла какая-то ошибкаsrc..\n\n'
                     'Пожалуйста повторите коментария для курьера\n\n'
                     'Или нажмите кнопку "Пропустить шаг"',
    'error_location': 'То, что вы отправили не похоже на локацию\n\n'
                      'Пожалуйста убедитесть, что Вы '
                      'прикрепляете именно местоположение\n\n'
                      'Если вы хотите прервать заполнение анкеты - '
                      'нажмите на кнопку "Прервать оформление ❌"',
    'done_fsm_delivery': 'Для подтверждения заказа нажмите на кнопку.',
    'use_buttons_for_districts': 'Пожалуйста, пользуйтесь кнопками '
                                 'при выборе района\n\nЕсли вы хотите прервать'
                                 ' оформление доставки - нажмите на кнопку '
                                 '"Прервать оформление ❌"',
    'skip': 'Пропустить шаг',
    'good': 'Отлично!\n\n',
    'link_input_cancelled': 'Вы отменили создание qr-code.\n\n',
    'comment_input_cancelled': 'Вы отменили ввод комментария.\n\n',
    'error': 'Повторный запрос',
    'store_not_active': 'В настоящий момент наше заведение не работает',
    'non_working_hours': 'Упс...((\n\nИзвините, оформить заказ не получится.\n'
                         'Мы работаем с 12:00 до 04:00.\n'
                         'Будем рады накормить вас в рабочие часы)',
    'invalid_request_message': 'Некорректный запрос',
}

LEXICON_KEYBOARDS_RU: dict[str, str] = {
    'menu': 'Наше меню',
    'main_menu': 'Наша главная страница',
    'group_telegram': 'Наша группа',
    'contact': 'Наши контакты',
    'delivery': 'Условия доставки',
}


LEXICON_KEYBOARDS_RU: dict[str, str] = {
    'menu': 'Наше меню',
    'main_menu': 'Наша главная страница',
    'group_telegram': 'Наша группа',
    'contact': 'Наши контакты',
    'delivery': 'Условия доставки',
    'sale': 'Наши акции',
    'cart': 'Корзина',
    'feedback': 'Оставить отзыв',
    'clear': 'Очистить',
    'edit': 'Редактировать',
    'free_delivery': 'Самовывоз',
    'delivery_pay': 'Доставка 🚚',
    'delivery_done': 'Подтвердить доставку 🚚',
    'check_balance': 'Текущие остатки',
    'add_products': 'Добавить новый продукт',
    'check_orders': 'Заказы в очереди',
    'check_done_orders': 'Заказы выполненые',
    'balance': 'Текущие остатки',  # удалить дубль
    'search_orders': 'Поиск заказа по номеру',
    'yes': 'Подтвердить заказ',
    'order_done': 'Выполнено ✔️',
    'denied': 'Отказ ✖️',
    'go_delivery': 'Подтвердить заказ',  # удалить дубль
    'back': '<<< назад',
    'back_menu': 'Меню бота',
    'comment': 'Комментарий к заказу',
    'location': 'Наша геолокация',
    'change_count_products': 'Корректировака остатков',
    'cancel': 'Кнопка отмены',
    'cancel_add_product': 'Отменить добавление товара ❌',
    'cancel_qr': 'Отменить создание qr-code',
    'cancel_2': 'Прервать оформление ❌',
    'skip': 'Пропустить шаг',
    'cancel_add_category': 'Отменить добавление категории ❌',


    'edit_menu': 'Редакторование меню',
    'exit_admin_menu': 'Закрыть админ-панель',


    'report_today': 'Продажи за сегодня',
    'report_month': 'Продажи за месяц',
    'report_all_time': 'Продажи за весь период',
    'reports': 'Отчеты',

    'admin_menu': '<<< назад',  # удалить дубль
    'superadmin_menu': 'Руководительская панель',

    'del_locations': 'Скрыть локацию',
    'del_product': 'Удалить блюдо ❌',
    'add_category': 'Добавить категорию',
    'del_category': 'Удалить категорию ❌',

    'admin_list': 'Список администраторов',
    'update_role_personal': 'Редактировать права сотрудников',
    'del_admin': 'Удалить администратора ❌',
    'add_superadmin': 'Добавить нового руководителя',
    'del_superadmin': 'Удалить руководителя ❌',

    'cancel_personal': 'Отменить редактирование ❌',

    'personal_account': 'Личный кабинет',

    'stop_list': 'Стоп-лист',

    'accept_order': 'Принять',
    'reject_order': 'Отклонить',

    'cutlery': 'Приборы',

    'admin': 'Админка',
}


LEXICON_COMMANDS_RU: dict[str, str] = {
    '/start': 'Запуск бота / Launching the bot',
}


def func_cart_text(
        bill: int,
        order_text: str,
        order_comment: Optional[str] = None,
        box_price: Optional[int] = None
):
    if not order_comment:
        message = (
            'Ваш заказ:\n\n'
            f'{order_text}'
            "\n--------------------\n"
            f'Итого без скидки: {bill} ₹\n'
            f'Скидка: {bill*0.05} ₹\n'
            f'Итоговая цена со скидкой: {bill*0.95} ₹\n'
        )
    else:
        message = (
            'Ваш заказ:\n\n'
            f'{order_text}'
            "\n--------------------\n"
            f'Итого без скидки: {bill} ₹\n'
            f'Итого цена со скидкой: {bill * 0.95} ₹\n'
            f'Комментарий к заказу: {order_comment}\n'
        )
    if box_price and box_price > 0:
        message += (
            f'Дополнительная плата за упаковку: {box_price} ₹\n'
            "--------------------\n"
            f'Итоговая сумма к оплате:: {bill * 0.95 + box_price} ₹\n'
        )
    return message


async def new_order_mess_text_order_chat(
        order_text: str,
        data_order: order_schemas.CreateOrder,
        order_info: Optional[order_schemas.CreateOrderInfo] = None,
        delivery_village: Optional[delivery_schemas.ReadDelivery] = None,
        user_info: Optional[customer_schemas.CustomerBase] = None,
        box_price: Optional[int] = None,
        callback: Optional[CallbackQuery] = None,
):
    desired_timezone = pytz.timezone('Asia/Kolkata')

    current_time = datetime.now(desired_timezone)

    total_price = data_order.total_price
    sale_price = total_price*0.95

    user_id = user_info.user_id if user_info else callback.message.chat.id
    first_name = user_info.first_name if user_info else callback.message.chat.first_name  # noqa: E501
    username = user_info.username if user_info else callback.message.chat.username  # noqa: E501

    customer_comment = (
        order_info.order_comment
        if order_info.order_comment is not None
        else 'Отсутствует'
    )

    order_header = (
        f"ЗАКАЗ №{order_info.order_id} от "
        f"{current_time.strftime('%d.%m.%Y')} в "
        f"{current_time.strftime('%H:%M')}\n"
        f"ТИП ЗАКАЗА: {data_order.order_type}\n"
        "--------------------\n"
    )

    customer_info = (
        "Информация о клиенте:\n"
        f"Код клиента: {user_id}\n"
        f"Имя клиента: {first_name}\n"
        f"Ссылка tg: @{username}\n"
        "--------------------\n"
    )

    order_details = (
        "Заказ:\n\n"
        f"{order_text}"
        f"\nКомментарий к заказу: {customer_comment}\n"
        "--------------------"
        f"\nСумма заказа: {total_price} ₹\n"
        f'Скидка: {total_price*0.05} ₹\n'
        f"\nСумма заказа с учётом скидки: {sale_price} ₹\n"
    )
    if box_price and box_price > 0:
        sale_price += box_price
        order_details += (
            f'Дополнительная плата за упаковку: {box_price} ₹\n'
            "--------------------\n"
            f'Итоговая сумма к оплате:: {sale_price} ₹\n'
        )

    chat_text = (
        order_header + customer_info + order_details
    )

    user_text = (
        order_header + order_details
    )

    if data_order.order_type == "Доставка":
        delivery_price = delivery_village.price

        delivery_info = (
            "--------------------\n"
            f"Стоимость доставки: {delivery_price} руп.\n"
            f"Итого (заказ + доставка): {sale_price + delivery_price} ₹\n"
            "--------------------\n"
            f"Район доставки: {delivery_village.name}\n"
        )

        courier_info = (
            f"Индийский номер клиента: {order_info.customer_phone}\n"
            f"Комментарий для курьера: {order_info.delivery_comment}\n"

        )
        if (
            order_info.delivery_latitude
            and
            order_info.delivery_longitude
        ):
            courier_info += (
                "Геолокация будет отправлена следующим сообщением\n"
            )
        else:
            courier_info += (
                "--------------------\n"
                "<b>Пользователь не прикрепил геолокацию. "
                "Пожалуйста свяжитесь с клиентом для "
                "уточнения деталей доставки\n</b>"
            )

        chat_text += delivery_info + courier_info

        user_text += delivery_info

    status_info = (
        "--------------------\n"
        f"Статус заказа: {data_order.order_status}\n"

    )

    cancel_text = (
        "--------------------\n"
        '<i>В случае отмены заказа воспользуйтесь личным кабинетом. '
        'Отмена заказа доступна в течении 15 минут.\n'
        '(Меню бота -> Личный кабинет -> *номер заказа* -> "Отменить ✖️")</i>'
    )

    chat_text += status_info
    user_text += status_info + cancel_text

    return chat_text, user_text


def get_comments_prompt_message():
    message = (
        'Пожалуйста, пришлите сообщением комментарии для наших поваров.'
        f' Для отмены нажмите на кнопку "{LEXICON_KEYBOARDS_RU["cancel"]}"'
    )
    return message


def generate_order_info_time_text(callback_data: TimeOrdersCallbackFactory):
    desired_timezone = pytz.timezone('Asia/Kolkata')

    # Получаем текущее время с указанной временной зоной
    current_time = datetime.now(desired_timezone)
    message = (
        "--------------------\n"
        f"Заказ № {callback_data.order_id} от "
        f"{current_time.strftime('%d.%m.%Y')}\n"
        f"Время приготовления: {callback_data.time} минут\n"
    )
    if callback_data.order_type == 2:
        message += (
            f"Ориентировочное время поездки: {callback_data.time_del} минут"
        )
    return message


async def generate_order_info_text(
    callback_data: Union[
        CheckOrdersCallbackFactory,
        OrderStatusCallbackFactory
    ]
):
    status = await get_status_name_by_id(callback_data.status)
    desired_timezone = pytz.timezone('Asia/Kolkata')

    current_time = datetime.now(desired_timezone)
    message = (
        "--------------------\n"
        f"Заказ № {callback_data.order_id} от "
        f"{current_time.strftime('%d.%m.%Y')}\n"
        f"Статус заказа: {status}"
    )
    return message
