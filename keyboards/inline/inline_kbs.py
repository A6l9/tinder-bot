from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.buttons import start_button, sex_buttons, \
    preference_buttons, location_buttons, skip_button, edit_button, edit_points_buttons, \
    location_edit_buttons, pagination_buttons, pagination_buttons_start, \
    pagination_buttons_middle, pagination_buttons_end, cancel_button, delete_or_no_button, \
    add_or_no_buttons, show_my_profile_if_limit_photo_button, sex_buttons_edit, cancel_search_button, \
    change_search_parameters_buttons, search_preference_buttons, pagination_questionnaire_buttons, \
    pagination_questionnaire_buttons_start, pagination_questionnaire_buttons_middle, \
    pagination_questionnaire_buttons_end, pagination_questionnaire_match_buttons, go_to_somewhere, \
    admin_panel, admin_panel_buttons, close_admin_panel
from loader import db
from database.models import Users
import json
from loader import user_manager


def create_start_button():
    inline_kb_list = [
        [start_button]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_sex_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*sex_buttons)

    return builder.as_markup()

def create_sex_edit_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*sex_buttons_edit, *cancel_button)
    builder.adjust(2)
    return builder.as_markup()

def create_preference_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*preference_buttons)

    return builder.as_markup()

def create_location_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*location_buttons)
    builder.adjust(1)
    return builder.as_markup()

def create_name_question(username, flag=None):
    if flag == 'first_name':
        inline_kb_list = [
            [InlineKeyboardButton(
            text='{name}'.format(name=username),
            callback_data='name_firstname_button'
        )]
        ]
        return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    elif flag == 'username':
        inline_kb_list = [
            [InlineKeyboardButton(
                text='{name}'.format(name=username),
                callback_data='name_username_button'
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

async def create_points_buttons(user_id, is_admin=False):
    temp_storage = user_manager.get_user(user_id)
    user = await db.get_row(Users, tg_user_id=str(user_id))
    temp_storage.photo_storage[user_id] = json.loads(user.media).get('media')
    builder = InlineKeyboardBuilder()
    if len(temp_storage.photo_storage[user_id]) == 1:
        builder.row(*pagination_buttons)
    elif temp_storage.num_elem == 0:
        builder.row(*pagination_buttons_start)
    elif temp_storage.num_elem == len(temp_storage.photo_storage[user_id]) - 1:
        builder.row(*pagination_buttons_end)
    elif 0 < temp_storage.num_elem < len(temp_storage.photo_storage[user_id]) - 1:
        builder.row(*pagination_buttons_middle)
    for i_elem in edit_points_buttons:
        builder.row(i_elem)
    if is_admin:
        builder.row(*admin_panel)
    return builder.as_markup()

def create_location_edit_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*location_edit_buttons, *cancel_button)
    builder.adjust(1)
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

def create_cancel_button():
    inline_kb_list = [
        [
            *cancel_button
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_delete_or_no_buttons():
    inline_kb_list = [
        [
            *delete_or_no_button,
            *cancel_button
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_add_or_no_buttons():
    inline_kb_list = [
        [
            *add_or_no_buttons
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_goto_profile_if_limit_photo_button():
    inline_kb_list = [
        [
            *show_my_profile_if_limit_photo_button
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def create_change_search_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*change_search_parameters_buttons)
    builder.adjust(1)
    return builder.as_markup()

def create_search_preference_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*search_preference_buttons, *cancel_search_button)
    builder.adjust(1)
    return builder.as_markup()

async def create_buttons_for_viewing_profiles(user_id):
    temp_storage = user_manager.get_user(user_id)
    builder = InlineKeyboardBuilder()
    if len(temp_storage.another_photo_storage) == 1:
        builder.row(*pagination_questionnaire_buttons)
    elif temp_storage.num_page_photo_for_another_user == 0:
        builder.row(*pagination_questionnaire_buttons_start)
    elif temp_storage.num_page_photo_for_another_user == len(temp_storage.another_photo_storage) - 1:
        builder.row(*pagination_questionnaire_buttons_end)
    elif 0 < temp_storage.num_page_photo_for_another_user < len(temp_storage.another_photo_storage) - 1:
        builder.row(*pagination_questionnaire_buttons_middle)
    return builder.as_markup()

async def create_buttons_for_viewing_match(user_id, another_user_id):
    temp_storage = user_manager.get_user(user_id)
    another_user = await db.get_row(Users, tg_user_id=str(another_user_id))
    temp_storage.another_photo_storage = json.loads(another_user.media).get('media')
    builder = InlineKeyboardBuilder()
    if len(temp_storage.another_photo_storage) == 1:
        builder.row(*pagination_questionnaire_match_buttons)
    elif temp_storage.num_page_photo_for_another_user == 0:
        builder.row(*pagination_questionnaire_match_buttons)
    elif temp_storage.num_page_photo_for_another_user == len(temp_storage.another_photo_storage) - 1:
        builder.row(*pagination_questionnaire_match_buttons)
    elif 0 < temp_storage.num_page_photo_for_another_user < len(temp_storage.another_photo_storage) - 1:
        builder.row(*pagination_questionnaire_match_buttons)
    return builder.as_markup()

def create_go_to_somewhere_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*go_to_somewhere)
    builder.adjust(1)
    return builder.as_markup()

def create_admin_panel_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(*admin_panel_buttons)
    builder.adjust(1)
    return builder.as_markup()

def create_close_wrap_admin_panel_button():
    inline_kb_list = [
        [
            *close_admin_panel
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
