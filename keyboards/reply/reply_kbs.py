from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_share_location_button():
    kb_list = [
        [KeyboardButton(text="📍Поделиться геолокацией", request_location=True)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return keyboard
