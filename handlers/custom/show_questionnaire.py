from aiogram import Router
import json
from aiogram.filters.command import Command
from aiogram.types import Message
from loader import db, bot, user_manager
from database.models import Users, BotReplicas
from loguru import logger
from keyboards.inline.inline_kbs import create_points_buttons


show_router = Router()


@show_router.message(Command('show_my_profile'))
async def show_questionnaire(message: Message):
    temp_storage = user_manager.get_user(message.from_user.id)
    logger.info('Command show_profile')
    user_data = await db.get_row(Users, tg_user_id=str(message.from_user.id))
    content = None
    replica = await db.get_row(BotReplicas, unique_name='show_profile')
    if json.loads(user_data.photos).get('photos'):
        content = json.loads(user_data.photos).get('photos')
        if user_data.about_yourself:
            description = user_data.about_yourself
        else:
            description = 'Нет описания'
        if content:
            await bot.send_photo(chat_id=message.from_user.id,
                            photo=content[temp_storage.num_elem], caption=replica.replica.replace('|n', '\n').format(
                                                             name=user_data.username,
                                                             age=user_data.age,
                                                             city=user_data.city,
                                                             desc=description),
                                                             reply_markup=await create_points_buttons(message.from_user.id))
    elif user_data.video:
        content = user_data.video
        if user_data.about_yourself:
            description = user_data.about_yourself
        else:
            description = 'Нет описания'
        await bot.send_video(chat_id=message.from_user.id,
                             video=content, caption=replica.replica.replace('|n', '\n').format(
                                                            name=user_data.username,
                                                            age=user_data.age,
                                                            city=user_data.city,
                                                            desc=description),
                                                            reply_markup=await create_points_buttons(message.from_user.id))
    else:
        replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
        await message.answer(replica.replica)