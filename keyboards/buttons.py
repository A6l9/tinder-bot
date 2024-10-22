from aiogram.types import InlineKeyboardButton


start_button = (InlineKeyboardButton(
    text='👌Давай начнем',
    callback_data='start_completion'
))


sex_buttons = (
    InlineKeyboardButton(
    text='Я парень',
    callback_data='sex_man'
    ),
    InlineKeyboardButton(
    text='Я девушка',
    callback_data='sex_woman'
    ),
)

preference_buttons = (
    InlineKeyboardButton(
    text='Парни',
    callback_data='preference_man'
    ),
    InlineKeyboardButton(
    text='Девушки',
    callback_data='preference_woman'
    ),
    InlineKeyboardButton(
    text='Все равно',
    callback_data='preference_no'
    )
)

location_buttons = (
    InlineKeyboardButton(
        text='📍Поделиться геолокацией',
        request_location=True,
        callback_data='location_share'
    ),
    InlineKeyboardButton(
        text='🖨Ввести вручную адрес',
        callback_data='location_write'
    )
)
