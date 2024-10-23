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

skip_button = (
    InlineKeyboardButton(
        text='Пропустить',
        callback_data='skip'
    ),
)

edit_button = (
    InlineKeyboardButton(
        text='Изменить анкету',
        callback_data='show_edit_points'
    ),
)

pagination_buttons_start = (
    InlineKeyboardButton(
        text='Удалить',
        callback_data='delete'
    ),
    InlineKeyboardButton(
        text='▶️',
        callback_data='right'
    )
)

pagination_buttons_middle = (
    InlineKeyboardButton(
        text='◀️',
        callback_data='left'
    ),
    InlineKeyboardButton(
        text='Удалить',
        callback_data='delete'
    ),
    InlineKeyboardButton(
        text='▶️',
        callback_data='right'
    )
)

pagination_buttons_end = (
    InlineKeyboardButton(
        text='️️️️️◀️',
        callback_data='left'
    ),
    InlineKeyboardButton(
        text='Удалить',
        callback_data='delete'
    )
)

pagination_buttons = (
    InlineKeyboardButton(
        text='Удалить',
        callback_data='delete'
    ),
)

edit_points_buttons = (
    InlineKeyboardButton(
        text='Изменить имя',
        callback_data='edit_name'
    ),
    InlineKeyboardButton(
        text='Изменить город',
        callback_data='edit_city'
    ),
    InlineKeyboardButton(
        text='Изменить описание',
        callback_data='edit_description'
    ),
    InlineKeyboardButton(
        text='Добавить медиа',
        callback_data='add_media'
    ),
    InlineKeyboardButton(
        text='Заполнить анкету заново',
        callback_data='change_questionnaire'
    )
)

location_edit_buttons = (
    InlineKeyboardButton(
        text='📍Поделиться геолокацией',
        request_location=True,
        callback_data='editlocation_share'
    ),
    InlineKeyboardButton(
        text='🖨Ввести вручную адрес',
        callback_data='editlocation_write'
    )
)

cancel_button = (
    InlineKeyboardButton(
        text='❌Отмена',
        callback_data='cancel'
    ),
)

delete_or_no_button = (
    InlineKeyboardButton(
        text='Да',
        callback_data='yes'
    ),
)
