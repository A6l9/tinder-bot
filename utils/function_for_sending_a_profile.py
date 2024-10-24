from loader import db, bot
import json
from database.models import BotReplicas, Users
from keyboards.inline.inline_kbs import create_points_buttons
from misc.temp_storage import UserManager


user_manager = UserManager()


async def func_for_send_prof(user_id):
    temp_storage = user_manager.get_user(user_id)
    temp_storage.num_elem = 0
    user = await db.get_row(Users, tg_user_id=str(user_id))
    replica = await db.get_row(BotReplicas, unique_name='show_profile')
    if json.loads(user.media).get('media'):
        content = json.loads(user.media).get('media')
        if user.about_yourself:
            description = user.about_yourself
        else:
            description = 'Нет описания'
        if content[0][0] == 'photo':
            await bot.send_photo(chat_id=user_id,
                                 photo=content[0][1], caption=replica.replica.replace('|n', '\n').format(
                    name=user.username,
                    age=user.age,
                    city=user.city,
                    desc=description),
                                 reply_markup=await create_points_buttons(user_id))
        elif content[0][0] == 'video':
            if user.about_yourself:
                description = user.about_yourself
            else:
                description = 'Нет описания'
            await bot.send_video(chat_id=user_id,
                                 video=content[0][1], caption=replica.replica.replace('|n', '\n').format(
                    name=user.username,
                    age=user.age,
                    city=user.city,
                    desc=description),
                                 reply_markup=await create_points_buttons(user_id))
