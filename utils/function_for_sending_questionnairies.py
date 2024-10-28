from aiogram.types import InputMediaVideo, InputMediaPhoto

from loader import bot, db, user_manager
from database.models import Users, Matches, BotReplicas
from keyboards.inline.inline_kbs import create_start_button, create_buttons_for_viewing_profiles
import json


async def send_questionnaire_first_time(message):
    temp_storage = user_manager.get_user(message.chat.id)
    temp_storage.another_users_id = []
    temp_storage.another_photo_storage = []
    temp_storage.num_page_photo_for_another_user = 0
    temp_storage.index_another_user = 0
    user_data = await db.get_row(Users, tg_user_id=str(message.chat.id))
    if user_data and user_data.done_questionnaire and user_data.range_age:
        all_users = await db.get_row(Users, to_many=True)
        matches = await db.get_row(Matches, to_many=True)
        for i_user in all_users:
            for i_match in matches:
                if (int(i_match.user_id_one) == int(user_data.tg_user_id)
                    and int(i_match.user_id_two) == int(i_user.tg_user_id) and i_match.user_reaction_one is not None):
                    break
                elif (int(i_match.user_id_one) == int(i_user.tg_user_id)
                      and int(i_match.user_id_two) == int(user_data.tg_user_id)
                      and i_match.user_reaction_two is not None):
                    break
            else:
                if ((i_user.sex == user_data.preference or user_data.preference == 'no')
                and i_user.city == user_data.city and int(user_data.range_age.split('-')[0]) <= int(i_user.age)
                        <= int(user_data.range_age.split('-')[1]) and i_user.tg_user_id != str(message.chat.id)):
                    temp_storage.another_users_id.append(i_user.tg_user_id)
        if len(temp_storage.another_users_id) != 0:
            replica = await db.get_row(BotReplicas, unique_name='show_profile_another_user')
            another_user_data = await db.get_row(Users, tg_user_id=str(temp_storage.another_users_id[0]))
            content = json.loads(another_user_data.media).get('media')
            if another_user_data.about_yourself:
                description = another_user_data.about_yourself
            else:
                description = 'Нет описания'
            if content[0][0] == 'photo':

                await bot.send_photo(chat_id=user_data.tg_user_id,
                                     photo=content[0][1],
                                     protect_content=True,
                                     caption=replica.replica.replace('|n', '\n').format(
                        name=another_user_data.username,
                        age=another_user_data.age,
                        city=another_user_data.city,
                        desc=description),
                                     reply_markup=await create_buttons_for_viewing_profiles(
                                         user_id=message.chat.id, another_user_id=another_user_data.tg_user_id))
            elif content[0][0] == 'video':
                if another_user_data.about_yourself:
                    description = another_user_data.about_yourself
                else:
                    description = 'Нет описания'
                await bot.send_video(chat_id=user_data.tg_user_id,
                                     video=content[0][1],
                                     protect_content=True,
                                     caption=replica.replica.replace('|n', '\n').format(
                        name=another_user_data.username,
                        age=another_user_data.age,
                        city=another_user_data.city,
                        desc=description),
                                     reply_markup=await create_buttons_for_viewing_profiles(
                                         user_id=message.chat.id, another_user_id=another_user_data.tg_user_id))
        else:
            replica = await db.get_row(BotReplicas, unique_name='not_available_profiles')
            await message.answer(replica.replica, protect_content=True)
    elif not user_data.range_age:
        replica = await db.get_row(BotReplicas, unique_name='nodone_parameters')
        await message.answer(replica.replica, protect_content=True)
    else:
        temp_storage.start_message = message
        replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
        await message.answer(replica.replica, protect_content=True, reply_markup=create_start_button())


async def send_questionnaire(message):
    temp_storage = user_manager.get_user(message.chat.id)
    temp_storage.num_page_photo_for_another_user = 0
    user_data = await db.get_row(Users, tg_user_id=str(message.chat.id))
    if user_data and user_data.done_questionnaire:
        if len(temp_storage.another_users_id) != 0:
            replica = await db.get_row(BotReplicas, unique_name='show_profile_another_user')
            another_user_data = await db.get_row(Users, tg_user_id=str(
                temp_storage.another_users_id[temp_storage.index_another_user]))
            content = json.loads(another_user_data.media).get('media')
            if another_user_data.about_yourself:
                description = another_user_data.about_yourself
            else:
                description = 'Нет описания'
            if content[0][0] == 'photo':
                media_type = InputMediaPhoto(media=content[temp_storage.num_page_photo_for_another_user][1],
                                             caption=replica.replica.replace('|n', '\n').format(
                                                 name=another_user_data.username,
                                                 age=another_user_data.age,
                                                 city=another_user_data.city,
                                                 desc=description))
                await bot.edit_message_media(chat_id=user_data.tg_user_id,
                                     media=media_type, message_id=message.message_id,
                                     reply_markup=await create_buttons_for_viewing_profiles(
                                         user_id=message.chat.id, another_user_id=another_user_data.tg_user_id))
            elif content[0][0] == 'video':
                if another_user_data.about_yourself:
                    description = another_user_data.about_yourself
                else:
                    description = 'Нет описания'
                media_type = InputMediaVideo(media=content[temp_storage.num_page_photo_for_another_user][1],
                                             caption=replica.replica.replace('|n', '\n').format(
                                                 name=another_user_data.username,
                                                 age=another_user_data.age,
                                                 city=another_user_data.city,
                                                 desc=description))
                await bot.edit_message_media(chat_id=user_data.tg_user_id,
                                     media=media_type, message_id=message.message_id,
                                     reply_markup=await create_buttons_for_viewing_profiles(
                                         user_id=message.chat.id, another_user_id=another_user_data.tg_user_id))
        else:
            replica = await db.get_row(BotReplicas, unique_name='not_available_profiles')
            await message.answer(replica.replica, protect_content=True)
    else:
        temp_storage.start_message = message
        replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
        await message.answer(replica.replica, protect_content=True, reply_markup=create_start_button())
