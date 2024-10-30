
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from loader import db, user_manager, bot
from loguru import logger
from database.models import Users, BotReplicas
from keyboards.inline.inline_kbs import create_start_button
from utils.function_for_sending_questionnairies import send_questionnaire_first_time
from utils.clear_back import clear_back
from utils.user_lock import get_user_lock

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message):
    temp_storage = user_manager.get_user(message.chat.id)
    logger.info('Command start')
    await db.initial()
    user = await db.get_row(Users, tg_user_id=str(message.chat.id))
    if not message.reply_markup:
        temp_storage.start_message = message
    user_lock = await get_user_lock(message.chat.id)
    async with user_lock:
        temp_storage.profile_message = 0
        if not user:
            try:
                temp_storage.start_message = message
                await db.add_row(Users, tg_user_id=str(message.from_user.id))
                replica = await db.get_row(BotReplicas, unique_name='start_message')
                await message.answer(replica.replica, protect_content=True, reply_markup=create_start_button())
            except Exception as exc:
                logger.error(exc)
                await message.answer('Произошла ошибка, попробуйте еще раз!', protect_content=True)
        else:
            await send_questionnaire_first_time(message)
        try:
            await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
        except:
            ...

@start_router.callback_query(F.data == 'goto_start')
async  def go_to_start(call: CallbackQuery):
    await start(message=call.message)
