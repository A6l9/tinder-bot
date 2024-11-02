from database.models import Users, BotReplicas
from loader import user_manager, db, bot
from keyboards.inline.inline_kbs import create_start_button, create_change_search_buttons
from utils.clear_back import clear_back


async def func_for_send_search_parameters(message):
    temp_storage = user_manager.get_user(message.chat.id)
    user_data = await db.get_row(Users, tg_user_id=str(message.chat.id))
    if user_data and user_data.done_questionnaire:
        replica = await db.get_row(BotReplicas, unique_name='choice_search_parameters')
        if user_data.range_age:
            range_age = user_data.range_age
        else:
            range_age = 'Не указан'
        if user_data.preference == 'man':
            sex = 'Парней'
        elif user_data.preference == 'woman':
            sex = 'Девушек'
        else:
            sex = 'Все равно'
        await message.answer(replica.replica.format(
            sex=sex,
            age=range_age
        ).replace('|n', '\n'), protect_content=False,
                             reply_markup=create_change_search_buttons())
    else:
        temp_storage.start_message = message
        replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
        await message.answer(replica.replica, protect_content=False, reply_markup=create_start_button())
    try:
        await clear_back(bot=bot, message=message, anchor_message=temp_storage.start_message)
    except:
        ...
