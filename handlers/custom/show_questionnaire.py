from aiogram import Router
import json
from aiogram.filters.command import Command
from aiogram.types import Message, InputMediaPhoto
from loader import db, bot
from database.models import Users, BotReplicas
from loguru import logger
from keyboards.inline.inline_kbs import create_change_button


show_router = Router()


@show_router.message(Command('show_my_profile'))
async def show_questionnaire(message: Message):
    logger.info('Command show_profile')
    user_data = await db.get_row(Users, tg_user_id=str(message.from_user.id))
    content = None
    if json.loads(user_data.photos).get('photos'):
        content = json.loads(user_data.photos).get('photos')
        if user_data.about_yourself:
            description = user_data.about_yourself
        else:
            description = 'Нет описания'
        if len(content) == 1:
            await bot.send_photo(chat_id=message.from_user.id,
                            photo=content[0], caption='Имя: {name}\nВозраст: {age}\nГород: {city}\n'
                                                                                 'Описание: {desc}'.format(
                                                                                 name=user_data.username,
                                                                                 age=user_data.age,
                                                                                 city=user_data.city,
                                                                                 desc=description),
                                                                                reply_markup=create_change_button())
        else:
            media_group = [InputMediaPhoto(media=media_id) for media_id in content]
            await bot.send_media_group(chat_id=message.from_user.id,
                                 media=media_group, caption='Имя: {name}\nВозраст: {age}\nГород: {city}\n'
                                                                                    'Описание: {desc}'.format(
                                                                                    name=user_data.username,
                                                                                    age=user_data.age,
                                                                                    city=user_data.city,
                                                                                    desc=description),
                                                                                    reply_markup=create_change_button())
    elif user_data.video:
        content = user_data.video
        if user_data.about_yourself:
            description = user_data.about_yourself
        else:
            description = 'Нет описания'
        await bot.send_video(chat_id=message.from_user.id,
                             video=content, caption='Имя: {name}\nВозраст: {age}\nГород: {city}\n'
                                                                                 'Описание: {desc}'.format(
                                                                                name=user_data.username,
                                                                                age=user_data.age,
                                                                                city=user_data.city,
                                                                                desc=description),
                                                                                reply_markup=create_change_button())
    else:
        replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
        await message.answer(replica.replica)