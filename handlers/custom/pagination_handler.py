from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo
from loader import db, bot, user_manager
from database.models import Users, BotReplicas
import json
from loguru import logger
from keyboards.inline.inline_kbs import create_points_buttons
from utils.clear_back import clear_back_if_blocked_user

pagination_router = Router()


@pagination_router.callback_query(F.data == 'left')
async def move_left(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    temp_storage.num_elem -= 1
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    if user_data.is_blocked:
        replica = await db.get_row(BotReplicas, unique_name='is_blocked')
        await call.message.answer(replica.replica, protect_content=False)
        try:
            await clear_back_if_blocked_user(bot=bot, message=call.message,
                                             anchor_message=temp_storage.start_message)
        except:
            ...
    else:
        content = None
        replica = await db.get_row(BotReplicas, unique_name='show_profile')
        if json.loads(user_data.media).get('media'):
            content = json.loads(user_data.media).get('media')
            if user_data.about_yourself:
                description = user_data.about_yourself
            else:
                description = 'Нет описания'
            if content[temp_storage.num_elem][0] == 'photo':
                sex = None
                if user_data.sex == 'man':
                    sex = 'Мужской'
                elif user_data.sex == 'woman':
                    sex = 'Женский'
                media_type = InputMediaPhoto(media=content[temp_storage.num_elem][1],
                                             caption=replica.replica.replace('|n', '\n').format(
                                                                 name=user_data.username,
                                                                 sex=sex,
                                                                 age=user_data.age,
                                                                 city=user_data.city,
                                                                 desc=description))
                try:
                    await bot.edit_message_media(chat_id=call.from_user.id,
                                     media=media_type, message_id=call.message.message_id,
                                     reply_markup=await create_points_buttons(call.from_user.id,
                                                                              is_admin=user_data.is_admin))
                except Exception as exc:
                    logger.debug(f'This exception absolutely normal {exc}')
            elif content[temp_storage.num_elem][0] == 'video':
                if user_data.about_yourself:
                    description = user_data.about_yourself
                else:
                    description = 'Нет описания'
                sex = None
                if user_data.sex == 'man':
                    sex = 'Мужской'
                elif user_data.sex == 'woman':
                    sex = 'Женский'
                media_type = InputMediaVideo(media=content[temp_storage.num_elem][1],
                                             caption=replica.replica.replace('|n', '\n').format(
                                                 name=user_data.username,
                                                 age=user_data.age,
                                                 sex=sex,
                                                 city=user_data.city,
                                                 desc=description))
                try:
                    await bot.edit_message_media(chat_id=call.from_user.id,
                                     media=media_type, message_id=call.message.message_id,
                                     reply_markup=await create_points_buttons(call.from_user.id,
                                                                              is_admin=user_data.is_admin))
                except Exception as exc:
                    logger.debug(f'This exception absolutely normal {exc}')
        else:
            replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
            await call.answer(replica.replica)


@pagination_router.callback_query(F.data == 'right')
async def move_right(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    temp_storage.num_elem += 1
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    if user_data.is_blocked:
        replica = await db.get_row(BotReplicas, unique_name='is_blocked')
        await call.message.answer(replica.replica, protect_content=False)
        try:
            await clear_back_if_blocked_user(bot=bot, message=call.message,
                                             anchor_message=temp_storage.start_message)
        except:
            ...
    else:
        content = None
        replica = await db.get_row(BotReplicas, unique_name='show_profile')
        if json.loads(user_data.media).get('media'):
            content = json.loads(user_data.media).get('media')
            if user_data.about_yourself:
                description = user_data.about_yourself
            else:
                description = 'Нет описания'
            if content[temp_storage.num_elem][0] == 'photo':
                sex = None
                if user_data.sex == 'man':
                    sex = 'Мужской'
                elif user_data.sex == 'woman':
                    sex = 'Женский'
                media_type = InputMediaPhoto(media=content[temp_storage.num_elem][1],
                                             caption=replica.replica.replace('|n', '\n').format(
                                                 name=user_data.username,
                                                 sex=sex,
                                                 age=user_data.age,
                                                 city=user_data.city,
                                                 desc=description))
                try:
                    await bot.edit_message_media(chat_id=call.from_user.id,
                                             media=media_type, message_id=call.message.message_id,
                                             reply_markup=await create_points_buttons(call.from_user.id,
                                                                              is_admin=user_data.is_admin))
                except Exception as exc:
                    logger.debug(f'This exception absolutely normal {exc}')
            elif content[temp_storage.num_elem][0] == 'video':
                if user_data.about_yourself:
                    description = user_data.about_yourself
                else:
                    description = 'Нет описания'
                sex = None
                if user_data.sex == 'man':
                    sex = 'Мужской'
                elif user_data.sex == 'woman':
                    sex = 'Женский'
                media_type = InputMediaVideo(media=content[temp_storage.num_elem][1],
                                             caption=replica.replica.replace('|n', '\n').format(
                                                 name=user_data.username,
                                                 sex=sex,
                                                 age=user_data.age,
                                                 city=user_data.city,
                                                 desc=description))
                try:
                    await bot.edit_message_media(chat_id=call.from_user.id,
                                             media=media_type, message_id=call.message.message_id,
                                             reply_markup=await create_points_buttons(call.from_user.id,
                                                                              is_admin=user_data.is_admin))
                except Exception as exc:
                    logger.debug(f'This exception absolutely normal {exc}')
        else:
            replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
            await call.answer(replica.replica)
