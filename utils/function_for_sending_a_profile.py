from aiogram.types import InputMediaVideo, InputMediaPhoto

from loader import db, bot
import json
from database.models import BotReplicas, Users
from keyboards.inline.inline_kbs import create_points_buttons
from loader import user_manager
from loguru import logger
from utils.clear_back import clear_back


async def func_for_send_prof(user_id, message):
    temp_storage = user_manager.get_user(user_id)
    temp_storage.num_elem = 0
    user = await db.get_row(Users, tg_user_id=str(user_id))
    replica = await db.get_row(BotReplicas, unique_name='show_profile')
    if json.loads(user.media).get('media'):
        content = json.loads(user.media).get('media')
        if user.about_yourself:
            description = user.about_yourself
        else:
            description = 'Нет описания'
        if content[0][0] == 'photo':
            sex = None
            if user.sex == 'man':
                sex = 'Мужской'
            elif user.sex == 'woman':
                sex = 'Женский'
            media = InputMediaPhoto(media=content[0][1], caption=replica.replica.replace('|n', '\n').format(
                                                name=user.username,
                                                sex=sex,
                                                age=user.age,
                                                city=user.city,
                                                desc=description))
            try:
                await bot.edit_message_media(chat_id=user_id, message_id=temp_storage.profile_message,
                                             media=media, reply_markup=await create_points_buttons(user_id,
                                                                          is_admin=user.is_admin))
            except Exception as exc:
                logger.debug(f'This exception absolutely normal {exc}')
        elif content[0][0] == 'video':
            if user.about_yourself:
                description = user.about_yourself
            else:
                description = 'Нет описания'
            sex = None
            if user.sex == 'man':
                sex = 'Мужской'
            elif user.sex == 'woman':
                sex = 'Женский'
            media = InputMediaVideo(media=content[0][1], caption=replica.replica.replace('|n', '\n').format(
                name=user.username,
                sex=sex,
                age=user.age,
                city=user.city,
                desc=description))
            try:
                await bot.edit_message_media(chat_id=user_id, message_id=temp_storage.profile_message,
                                             media=media, reply_markup=await create_points_buttons(user_id,
                                                                          is_admin=user.is_admin))
            except Exception as exc:
                logger.debug(f'This exception absolutely normal {exc}')
    try:
        await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
    except:
        ...


async def func_for_send_prof_first_time(user_id, message):
    temp_storage = user_manager.get_user(user_id)
    temp_storage.num_elem = 0
    user = await db.get_row(Users, tg_user_id=str(user_id))
    replica = await db.get_row(BotReplicas, unique_name='show_profile')
    if json.loads(user.media).get('media'):
        content = json.loads(user.media).get('media')
        if user.about_yourself:
            description = user.about_yourself
        else:
            description = 'Нет описания'
        if content[0][0] == 'photo':
            sex = None
            if user.sex == 'man':
                sex = 'Мужской'
            elif user.sex == 'woman':
                sex = 'Женский'
            await bot.send_photo(chat_id=user_id,
                                 photo=content[0][1],
                                 protect_content=False,
                                 caption=replica.replica.replace('|n', '\n').format(
                                     name=user.username,
                                     age=user.age,
                                     sex=sex,
                                     city=user.city,
                                     desc=description),
                                 reply_markup=await create_points_buttons(user_id,
                                                                          is_admin=user.is_admin))
        elif content[0][0] == 'video':
            if user.about_yourself:
                description = user.about_yourself
            else:
                description = 'Нет описания'
            sex = None
            if user.sex == 'man':
                sex = 'Мужской'
            elif user.sex == 'woman':
                sex = 'Женский'
            await bot.send_video(chat_id=user_id,
                                 video=content[0][1],
                                 protect_content=False,
                                 caption=replica.replica.replace('|n', '\n').format(
                                     name=user.username,
                                     sex=sex,
                                     age=user.age,
                                     city=user.city,
                                     desc=description),
                                 reply_markup=await create_points_buttons(user_id,
                                                                          is_admin=user.is_admin))
    try:
        await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
    except:
        ...
