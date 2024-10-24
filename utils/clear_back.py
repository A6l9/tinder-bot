import asyncio
from contextlib import suppress


async def delete_wrap(message):
    with suppress(Exception):
        await message.delete()


async def delete_wrap_by_call(func):
    with suppress(Exception):
        await func

async def clear_back(bot, message, start_num=0, anchor_message=None):
    for i in list(range(15))[start_num:]:
        if anchor_message and message.message_id - i == anchor_message.message_id:
                continue
        asyncio.create_task(
            delete_wrap_by_call(bot.delete_message(message.chat.id, message.message_id - i))
        )