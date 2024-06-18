main_btn: dict[str, dict[str, str]] = {
    'menu': {
        'text': 'Наше меню',
        'callback_data': 'press_menu'
    },
    'contact': {
        'text': 'Наши контакты',
        'callback_data': 'press_contact'
    },
    'delivery': {
        'text': 'Условия доставки',
        'callback_data': 'press_delivery'
    },
    'location': {
        'text': 'Наша геолокация',
        'callback_data': 'press_location'
    },
    'personal_account': {
        'text': 'Личный кабинет',
        'callback_data': 'press_account'
    },
    'group_telegram': {
        'text': 'Наша группа',
        'url': 'https://t.me/PizzaGoaFood'
    },
    'admin': {
        'text': 'Админка',
        'callback_data': 'press_admin'
    },
}


main_menu_dict: dict[str, str] = {
    'start':
        'Добро пожаловать в нашу пиццерию 🍕🇮🇹'
        '\nНаслаждайтесь аутентичными вкусами и '
        'разнообразием итальянских пицц на любой'
        'вкус прямо у себя дома 🏠'
        '\nРаботает доставка до вашего стола 🍕🫶',
    'main_menu':
        "Добро пожаловать в нашу пиццерию! Отведайте истинные итальянские "
        "вкусы с 14:00 до 23:00. Нежное тесто, сочные начинки и уютная "
        "атмосфера ждут вас!\n\n",
    'store': "Наше меню",
    'delivery': 'Информаци по доставке 🛵'
                '\n\nСтомость доставки по районам:'
                '\nМорджим 100r'
                '\nАшвем 150r'
                '\nАгарвадо 150r'
                '\nСиолим 200r'
                '\nМандрем 200r'
                '\nВерхний Мандрем 250r'
                '\nАрамболь 250r'
                '\nВагатор 350r'
                '\nКерим 350r'
                '\nПалием 350r\n\n'
                'P.s. При оформении доставки следуйте подсказкам нашего бота)',
    'contact': 'Pizzeria Marcello🍕🍝\n\n'
               'Самая Итальянская пицца в Гоа🍕🍝🔥.\n\n'
               'Морджим, Turtle Beach road.\n\n'
               'По всем вопросам пишите или звоните\n'
               '@AyratZiganshin59\n+918149843927\n\n'
               '<a href="t.me/PizzaGoaFood">Наша группа в телеграм</a>',
    'personal_area': 'Добро пожаловать в личный кабинет.\n\n'
                     'Вы можете посмотреть историю своих заказов, '
                     'чтобы посмотреть'
                     ' детали заказа, нажмите кнопку "Подробнее"\n\n'
                     '"Отменить ✖️" - кнопка, для отмены заказа\n\n'
                     '<i>Отмена заказа возможна в течении '
                     '15 минут, после его оформления</i>',
    'error_private_chat': 'Извините, этот бот предназначен '
                          'для использования только в '
                          'личных чатах. Если вы хотите сделать заказ, '
                          'пожалуйста, перейдите в сам бот',
}

delete_location_btn: dict[str, dict[str, str]] = {
    'del_locations': {
        'text': 'Скрыть локацию',
        'callback_data': 'press_del'
    }
}


def create_navigation_main_btn() -> dict[str, dict[str, str]]:
    return {
        'back': {
            'text': '<<< Назад',
            'callback_data': 'press_main_menu'
        },
        'cart': {
            'text': 'Главное меню',
            'callback_data': 'press_main_menu'
        }
    }
