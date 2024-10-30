from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from loguru import logger

from database.models import BotReplicas, Users
from loader import db, bot, user_manager
from aiogram.fsm.context import FSMContext
from keyboards.inline.inline_kbs import create_search_preference_buttons
from utils.func_for_send_search_parameters import func_for_send_search_parameters
import re
from storage.states import States


change_search_parameters_router = Router()


@change_search_parameters_router.message(Command('change_search_parameters'))
async def change_search_parameters(message: Message):
    temp_storage = user_manager.get_user(message.chat.id)
    temp_storage.profile_message = 0
    await func_for_send_search_parameters(message)


@change_search_parameters_router.callback_query(F.data == 'change_age_range')
async def change_age_range(call: CallbackQuery, state: FSMContext):
    replica = await db.get_row(BotReplicas, unique_name='write_age_range')
    await call.message.edit_text(replica.replica)
    await state.set_state(States.edit_age_range_search)


@change_search_parameters_router.message(States.edit_age_range_search, F.text,
                                         ~F.text.in_({'/start', '/show_my_profile', '/change_search_parameters'}))
async def change_age_range_take_answer(message: Message, state: FSMContext):
    if message.text:
        pattern = r'^\d{2}-\d{2}$'
        match = re.search(pattern, str(message.text))
        if match:
            if (int(match.group().split('-')[0]) == int(match.group().split('-')[1]) and
                16 <= int(match.group().split('-')[0]) < 46 and 16 <= int(match.group().split('-')[1]) < 46):
                await db.update_user_row(Users, tg_user_id=message.from_user.id, range_age=str(message.text))
                await func_for_send_search_parameters(message)
                await state.clear()
            elif (16 <= int(match.group().split('-')[0]) < 46 and 16 <= int(match.group().split('-')[1]) < 46
                and int(match.group().split('-')[0]) < int(match.group().split('-')[1])):
                await db.update_user_row(Users, tg_user_id=message.from_user.id, range_age=str(message.text))
                await func_for_send_search_parameters(message)
                await state.clear()
            else:
                replica = await db.get_row(BotReplicas, unique_name='wrong_age_range')
                await message.answer(replica.replica, protect_content=True)
        else:
            replica = await db.get_row(BotReplicas, unique_name='wrong_type_age_range')
            await message.answer(replica.replica.replace('|n', '\n'), protect_content=True)
    else:
        replica = await db.get_row(BotReplicas, unique_name='wrong_type_age_range')
        await message.answer(replica.replica.replace('|n', '\n'), protect_content=True)


@change_search_parameters_router.callback_query(F.data == 'change_sex_preference')
async def change_sex_preference(call: CallbackQuery, state: FSMContext):
    replica = await db.get_row(BotReplicas, unique_name='who_search')
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=replica.replica,
                                reply_markup=create_search_preference_buttons())
    await state.set_state(States.edit_preference_search)

@change_search_parameters_router.callback_query(States.edit_preference_search, F.data.startswith('search_preference_'))
async def change_sex_preference(call: CallbackQuery, state: FSMContext):
    sex = call.data.split('_')[2]
    try:
        await db.update_user_row(model=Users, tg_user_id=call.from_user.id, preference=sex)
        await func_for_send_search_parameters(call.message)
        await state.clear()
    except Exception as exc:
        logger.error(f'Error updating user sex: {exc}')

@change_search_parameters_router.callback_query(F.data == 'search_cancel')
async def cancel_search(call: CallbackQuery, state: FSMContext):
    await func_for_send_search_parameters(message=call.message)
    await state.clear()


@change_search_parameters_router.callback_query(F.data == 'goto_change_parameters')
async def go_to_change_parameters(call: CallbackQuery):
    await change_search_parameters(message=call.message)
