from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from loader import db
from loguru import logger
from database.models import Users, BotReplicas
from keyboards.inline.inline_kbs import create_start_button
from utils.function_for_sending_a_profile import func_for_send_prof

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
            await func_for_send_prof(message.from_user.id)
        else:
            replica = await db.get_row(BotReplicas, unique_name='start_message')
            await message.answer(replica.replica, reply_markup=create_start_button())
