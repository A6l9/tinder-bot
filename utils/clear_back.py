import asyncio
from contextlib import suppress
from loader import user_manager


async def delete_wrap(message):
    with suppress(Exception):
        await message.delete()


async def delete_wrap_by_call(func):
    with suppress(Exception):
        await func

async def clear_back(bot, message, start_num=0, anchor_message=None):
    temp_storage = user_manager.get_user(message.chat.id)
    for i in list(range(15))[start_num:]:
        if anchor_message and message.message_id - i == anchor_message.message_id:
                continue
        if message.message_id - i in temp_storage.exceptions_messages:
            continue
        if message.message_id - i == temp_storage.profile_message:
            continue
        asyncio.create_task(
            delete_wrap_by_call(bot.delete_message(message.chat.id, message.message_id - i))
        )
