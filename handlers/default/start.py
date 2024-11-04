
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from loader import db, user_manager, bot
from loguru import logger
from database.models import Users, BotReplicas
from keyboards.inline.inline_kbs import create_start_button
from utils.function_for_sending_questionnairies import send_questionnaire_first_time
from utils.clear_back import clear_back, clear_back_if_blocked_user
from utils.user_lock import get_user_lock

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message):
    temp_storage = user_manager.get_user(message.chat.id)
    logger.info('Command start')
    await db.initial()
    if not message.reply_markup:
        temp_storage.start_message = message
    user_lock = await get_user_lock(message.chat.id)
    async with user_lock:
        user = await db.get_row(Users, tg_user_id=str(message.chat.id))
        temp_storage.profile_message = 0
        if not user:
            if message.from_user.username:
                try:
                    temp_storage.start_message = message
                    user_tg_data = await bot.get_chat(chat_id=message.chat.id)
                    await db.add_row(Users, tg_user_id=str(message.from_user.id),
                                     tg_username=user_tg_data.username)
                    replica = await db.get_row(BotReplicas, unique_name='start_message')
                    await message.answer(replica.replica, protect_content=True, reply_markup=create_start_button())
                except Exception as exc:
                    logger.error(exc)
                    await message.answer('Произошла ошибка, попробуйте еще раз!', protect_content=True)
            else:
                replica = await db.get_row(BotReplicas, unique_name='no_tg_username')
                await message.answer(replica.replica, protect_content=True)
        elif user.is_blocked:
            replica = await db.get_row(BotReplicas, unique_name='is_blocked')
            await message.answer(replica.replica, protect_content=True)
            try:
                await clear_back_if_blocked_user(bot=bot, message=message,
                                                 anchor_message=temp_storage.start_message)
            except:
                ...
        else:
            user_tg_data = await bot.get_chat(chat_id=message.chat.id)
            await db.update_user_row(Users, tg_user_id=str(message.chat.id), tg_username=user_tg_data.username)
            await send_questionnaire_first_time(message)
        try:
            await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
        except:
            ...

@start_router.callback_query(F.data == 'goto_start')
async  def go_to_start(call: CallbackQuery):
    await start(message=call.message)
