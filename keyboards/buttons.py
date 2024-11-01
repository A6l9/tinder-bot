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

sex_buttons_edit = (
    InlineKeyboardButton(
    text='Я парень',
    callback_data='editsex_man'
    ),
    InlineKeyboardButton(
    text='Я девушка',
    callback_data='editsex_woman'
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
        text='Добавить медиа',
        callback_data='add_media'
    ),
    InlineKeyboardButton(
        text='Изменить имя',
        callback_data='edit_name'
    ),
    InlineKeyboardButton(
        text='Сменить пол',
        callback_data='edit_sex'
    ),
    InlineKeyboardButton(
        text='Изменить возраст',
        callback_data='edit_age'
    ),
    InlineKeyboardButton(
        text='Изменить город',
        callback_data='edit_city'
    ),
    InlineKeyboardButton(
        text='Изменить описание',
        callback_data='edit_description'
    ),
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

add_or_no_buttons = (
    InlineKeyboardButton(
        text='Да',
        callback_data='yes_more_media'
    ),
    InlineKeyboardButton(
        text='Нет',
        callback_data='no_more_media'
    )
)

show_my_profile_if_limit_photo_button = (
    InlineKeyboardButton(
        text='Хорошо, перейти к профилю',
        callback_data='ok_goto_profile'
    ),
)

change_search_parameters_buttons = (
    InlineKeyboardButton(
        text='Изменить диапазон возраста',
        callback_data='change_age_range'
    ),
    InlineKeyboardButton(
        text='Изменить предпочтение',
        callback_data='change_sex_preference'
    ),
)

cancel_search_button = (
    InlineKeyboardButton(
        text='❌Отмена',
        callback_data='search_cancel'
    ),
)

search_preference_buttons = (
    InlineKeyboardButton(
    text='Парней',
    callback_data='search_preference_man'
    ),
    InlineKeyboardButton(
    text='Девушек',
    callback_data='search_preference_woman'
    ),
    InlineKeyboardButton(
    text='Все равно',
    callback_data='search_preference_no'
    )
)


pagination_questionnaire_buttons = (
    InlineKeyboardButton(
        text='👎',
        callback_data='dislike'
    ),
    InlineKeyboardButton(
        text='️️️️️◀️',
        callback_data='swipe_left',
    ),
    InlineKeyboardButton(
        text='▶️',
        callback_data='swipe_right'
    ),
    InlineKeyboardButton(
        text='👍',
        callback_data='like'
    ),
)

pagination_questionnaire_buttons_start = (
    InlineKeyboardButton(
        text='👎',
        callback_data='dislike'
    ),
    InlineKeyboardButton(
        text='️️️️️◀️',
        callback_data='swipe_left',
    ),
    InlineKeyboardButton(
        text='▶️',
        callback_data='swipe_right'
    ),
    InlineKeyboardButton(
        text='👍',
        callback_data='like'
    ),
)

pagination_questionnaire_buttons_middle = (
    InlineKeyboardButton(
        text='👎',
        callback_data='dislike'
    ),
    InlineKeyboardButton(
        text='️️️️️◀️',
        callback_data='swipe_left',
    ),
    InlineKeyboardButton(
        text='▶️',
        callback_data='swipe_right'
    ),
    InlineKeyboardButton(
        text='👍',
        callback_data='like'
    ),
)

pagination_questionnaire_buttons_end = (
    InlineKeyboardButton(
        text='👎',
        callback_data='dislike'
    ),
    InlineKeyboardButton(
        text='️️️️️◀️',
        callback_data='swipe_left',
    ),
    InlineKeyboardButton(
        text='▶️',
        callback_data='swipe_right'
    ),
    InlineKeyboardButton(
        text='👍',
        callback_data='like'
    ),
)

pagination_questionnaire_match_buttons = (
    InlineKeyboardButton(
        text='️️️️️◀️',
        callback_data='swipe_left_match'
    ),
    InlineKeyboardButton(
        text='▶️',
        callback_data='swipe_right_match'
    ),
)

go_to_somewhere = (
    InlineKeyboardButton(
        text='️️️️Смотреть анкеты',
        callback_data='goto_start'
    ),
    InlineKeyboardButton(
        text='Профиль',
        callback_data='goto_show_profile'
    ),
    InlineKeyboardButton(
        text='Параметры поиска',
        callback_data='goto_change_parameters'
    ),
)

admin_panel = (
    InlineKeyboardButton(
        text='⚙️ Панель администратора',
        callback_data='admin_panel'
    ),
)

admin_panel_buttons = (
    InlineKeyboardButton(
        text='Статистика📈',
        callback_data='statistics'
    ),
    InlineKeyboardButton(
        text='Рассылка📢',
        callback_data='mailing'
    ),
    InlineKeyboardButton(
        text='Удалить анкету пользователя🗑',
        callback_data='delete_user_profile'
    ),
    InlineKeyboardButton(
        text='Заблокировать пользователя🚫',
        callback_data='ban_user'
    ),
    InlineKeyboardButton(
        text='Закрыть❌',
        callback_data='close_admin_panel'
    ),
)

close_admin_panel = (
    InlineKeyboardButton(
        text='Закрыть❌',
        callback_data='close_wrap_admin_panel'
    ),
)
