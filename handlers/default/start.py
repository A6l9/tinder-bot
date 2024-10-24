import json

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from loader import db, bot
from loguru import logger
from database.models import Users, BotReplicas
from keyboards.inline.inline_kbs import create_start_button, create_points_buttons

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message):
    logger.info('Command start')
    await db.initial()
    user = await db.get_row(Users, tg_user_id=str(message.from_user.id))
    if not user:
        try:
            await db.add_row(Users, tg_user_id=str(message.from_user.id))
            replica = await db.get_row(BotReplicas, unique_name='start_message')
            await message.answer(replica.replica, reply_markup=create_start_button())
        except Exception as exc:
            logger.error(exc)
            await message.answer('Произошла ошибка, попробуйте еще раз!')
    else:
        if user.done_questionnaire:
            content = None
            replica = await db.get_row(BotReplicas, unique_name='show_profile')
            if json.loads(user.media).get('media'):
                content = json.loads(user.media).get('media')
                if user.about_yourself:
                    description = user.about_yourself
                else:
                    description = 'Нет описания'
                if content:
                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo=content[0], caption=replica.replica.replace('|n', '\n').format(
                            name=user.username,
                            age=user.age,
                            city=user.city,
                            desc=description),
                                         reply_markup=await create_points_buttons(message.from_user.id))
            elif user.video:
                content = user.video
                if user.about_yourself:
                    description = user.about_yourself
                else:
                    description = 'Нет описания'
                await bot.send_video(chat_id=message.from_user.id,
                                     video=content, caption=replica.replica.replace('|n', '\n').format(
                        name=user.username,
                        age=user.age,
                        city=user.city,
                        desc=description),
                                     reply_markup=await create_points_buttons(message.from_user.id))
        else:
            replica = await db.get_row(BotReplicas, unique_name='start_message')
            await message.answer(replica.replica, reply_markup=create_start_button())
