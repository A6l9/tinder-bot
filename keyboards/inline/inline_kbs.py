from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.buttons import start_button, sex_buttons, \
                              preference_buttons, location_buttons, skip_button, edit_button, edit_points_buttons, \
                              location_edit_buttons



def create_start_button():
    inline_kb_list = [
        [start_button]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_sex_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*sex_buttons)

    return builder.as_markup()

def create_preference_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*preference_buttons)

    return builder.as_markup()

def create_location_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*location_buttons)

    return builder.as_markup()

def create_name_question(username):
    inline_kb_list = [
        [InlineKeyboardButton(
        text='{name}'.format(name=username),
        callback_data='name_button'
    )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def create_buttons_cities(list_cities):
    builder = InlineKeyboardBuilder()
    for i_elem in list_cities:
        builder.row(
            InlineKeyboardButton(
                text='{}'.format(i_elem.address),
                callback_data='city_{}'.format(i_elem.postal_code)
            )
        )
        builder.adjust(1)
    return builder.as_markup()

def create_skip_button():
    inline_kb_list = [
        [
            *skip_button
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_change_button():
    inline_kb_list = [
        [
            *edit_button
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_points_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*edit_points_buttons)
    builder.adjust(1)
    return builder.as_markup()

def create_name_question_edit(username):
    inline_kb_list = [
        [InlineKeyboardButton(
        text='{name}'.format(name=username),
        callback_data='editname_button'
    )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_location_edit_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*location_edit_buttons)

    return builder.as_markup()

def create_buttons_cities_edit(list_cities):
    builder = InlineKeyboardBuilder()
    for i_elem in list_cities:
        builder.row(
            InlineKeyboardButton(
                text='{}'.format(i_elem.address),
                callback_data='editcity_{}'.format(i_elem.postal_code)
            )
        )
        builder.adjust(1)
    return builder.as_markup()
