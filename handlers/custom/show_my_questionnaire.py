import json

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from loguru import logger

from database.models import Users, BotReplicas
from keyboards.inline.inline_kbs import create_points_buttons, create_start_button
from loader import db, bot, user_manager
from utils.clear_back import clear_back

show_router = Router()


@show_router.message(Command('show_my_profile'))
async def show_questionnaire(message: Message):
    temp_storage = user_manager.get_user(message.from_user.id)
    logger.info('Command show_profile')
    user_data = await db.get_row(Users, tg_user_id=str(message.from_user.id))
    content = None
    replica = await db.get_row(BotReplicas, unique_name='show_profile')
    if user_data and user_data.done_questionnaire:
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
                await bot.send_photo(chat_id=message.from_user.id,
                                photo=content[temp_storage.num_elem][1], caption=replica.replica.replace('|n',
                                                                                                         '\n').format(
                                                                 name=user_data.username,
                                                                 age=user_data.age,
                                                                 sex=sex,
                                                                 city=user_data.city,
                                                                 desc=description),
                                                                 reply_markup=await create_points_buttons(
                                                                     message.from_user.id))
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
                await bot.send_video(chat_id=message.from_user.id,
                                     video=content[temp_storage.num_elem][1],
                                     caption=replica.replica.replace('|n', '\n').format(
                                                                    name=user_data.username,
                                                                    age=user_data.age,
                                                                    sex=sex,
                                                                    city=user_data.city,
                                                                    desc=description),
                                                                    reply_markup=await create_points_buttons(
                                                                        message.from_user.id))
    else:
        replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
        await message.answer(replica.replica, reply_markup=create_start_button())

    try:
        await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
    except:
        ...
