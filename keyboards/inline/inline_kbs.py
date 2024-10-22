from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.buttons import start_button, sex_buttons, preference_buttons, location_buttons


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
