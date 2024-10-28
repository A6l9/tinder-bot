from aiogram import F, Router

from loader import user_manager, bot, db
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo
from database.models import BotReplicas, Users, Matches
import json
from keyboards.inline.inline_kbs import create_buttons_for_viewing_profiles
from utils.clear_back import clear_back
from utils.function_for_sending_questionnairies import send_questionnaire


show_questionnaire_router = Router()

@show_questionnaire_router.callback_query(F.data == 'swipe_right')
async def swipe_right_photo(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    if temp_storage.num_page_photo_for_another_user + 1 == len(temp_storage.another_photo_storage):
        replica = await db.get_row(BotReplicas, unique_name='no_more_photos')
        await call.answer(text=replica.replica)
    else:
        temp_storage.num_page_photo_for_another_user += 1
        another_user_data = await db.get_row(Users, tg_user_id=str(
            temp_storage.another_users_id[temp_storage.index_another_user]))
        content = None
        replica = await db.get_row(BotReplicas, unique_name='show_profile_another_user')
        if json.loads(another_user_data.media).get('media'):
            content = json.loads(another_user_data.media).get('media')
            if another_user_data.about_yourself:
                description = another_user_data.about_yourself
            else:
                description = 'Нет описания'
            if content[temp_storage.num_page_photo_for_another_user][0] == 'photo':
                media_type = InputMediaPhoto(media=content[temp_storage.num_page_photo_for_another_user][1],
                                             caption=replica.replica.replace('|n', '\n').format(
                                                 name=another_user_data.username,
                                                 age=another_user_data.age,
                                                 city=another_user_data.city,
                                                 desc=description))
                await bot.edit_message_media(chat_id=call.from_user.id,
                                             media=media_type, message_id=call.message.message_id,
                                             reply_markup=await create_buttons_for_viewing_profiles(call.from_user.id,
                                                            temp_storage.another_users_id[temp_storage.index_another_user]))
            elif content[temp_storage.num_page_photo_for_another_user][0] == 'video':
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
                await bot.edit_message_media(chat_id=call.from_user.id,
                                             media=media_type, message_id=call.message.message_id,
                                             reply_markup=await create_buttons_for_viewing_profiles(call.from_user.id,
                                                            temp_storage.another_users_id[temp_storage.index_another_user]))
        else:
            replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
            await call.answer(replica.replica)


@show_questionnaire_router.callback_query(F.data == 'swipe_left')
async def swipe_left_photo(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    if temp_storage.num_page_photo_for_another_user == 0:
        replica = await db.get_row(BotReplicas, unique_name='no_more_photos')
        await call.answer(text=replica.replica)
    else:
        temp_storage.num_page_photo_for_another_user -= 1
        another_user_data = await db.get_row(Users,
                                         tg_user_id=str(temp_storage.another_users_id[temp_storage.index_another_user]))
        content = None
        replica = await db.get_row(BotReplicas, unique_name='show_profile_another_user')
        if json.loads(another_user_data.media).get('media'):
            content = json.loads(another_user_data.media).get('media')
            if another_user_data.about_yourself:
                description = another_user_data.about_yourself
            else:
                description = 'Нет описания'
            if content[temp_storage.num_page_photo_for_another_user][0] == 'photo':
                media_type = InputMediaPhoto(media=content[temp_storage.num_page_photo_for_another_user][1],
                                             caption=replica.replica.replace('|n', '\n').format(
                                                 name=another_user_data.username,
                                                 age=another_user_data.age,
                                                 city=another_user_data.city,
                                                 desc=description))
                await bot.edit_message_media(chat_id=call.from_user.id,
                                             media=media_type, message_id=call.message.message_id,
                                             reply_markup=await create_buttons_for_viewing_profiles(call.from_user.id,
                                                            temp_storage.another_users_id[temp_storage.index_another_user]))
            elif content[temp_storage.num_page_photo_for_another_user][0] == 'video':
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
                await bot.edit_message_media(chat_id=call.from_user.id,
                                             media=media_type, message_id=call.message.message_id,
                                             reply_markup=await create_buttons_for_viewing_profiles(call.from_user.id,
                                                            temp_storage.another_users_id[temp_storage.index_another_user]))
        else:
            replica = await db.get_row(BotReplicas, unique_name='nodone_questionnaire')
            await call.answer(replica.replica)


@show_questionnaire_router.callback_query(F.data == 'like')
async def like_questionnaire(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    if (await db.get_row(Matches, user_id_one=str(call.from_user.id),
                        user_id_two=temp_storage.another_users_id[temp_storage.index_another_user])):
        await db.update_matches_row(Matches, tg_user_id=str(call.from_user.id),
                        tg_user_id_another_user=str(temp_storage.another_users_id[temp_storage.index_another_user]),
                        user_id_one=1, user_reaction_one=True)
    elif (await db.get_row(Matches, user_id_two=str(call.from_user.id),
                        user_id_one=temp_storage.another_users_id[temp_storage.index_another_user])):
        await db.update_matches_row(Matches, tg_user_id=str(call.from_user.id),
                        tg_user_id_another_user=str(temp_storage.another_users_id[temp_storage.index_another_user]),
                        user_id_two=1, user_reaction_two=True)
    else:
        await db.add_row(Matches, user_id_one=str(call.from_user.id),
                         user_reaction_one=True, user_reaction_two=None,
                         user_id_two=temp_storage.another_users_id[temp_storage.index_another_user])
    if len(temp_storage.another_users_id) > temp_storage.index_another_user + 1:
        temp_storage.index_another_user += 1
        await send_questionnaire(call.message)
    else:
        replica = await db.get_row(BotReplicas, unique_name='сome_back_later')
        await bot.send_message(chat_id=call.from_user.id, text=replica.replica)
        try:
            await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
        except:
            ...



@show_questionnaire_router.callback_query(F.data == 'dislike')
async def like_questionnaire(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    if (await db.get_row(Matches, user_id_one=str(call.from_user.id),
                        user_id_two=temp_storage.another_users_id[temp_storage.index_another_user])):
        await db.update_matches_row(Matches, tg_user_id=str(call.from_user.id),
                        tg_user_id_another_user=str(temp_storage.another_users_id[temp_storage.index_another_user]),
                        user_id_one=1, user_reaction_one=False)
    elif (await db.get_row(Matches, user_id_two=str(call.from_user.id),
                        user_id_one=temp_storage.another_users_id[temp_storage.index_another_user])):
        await db.update_matches_row(Matches, tg_user_id=str(call.from_user.id),
                        tg_user_id_another_user=str(temp_storage.another_users_id[temp_storage.index_another_user]),
                        user_id_two=1, user_reaction_two=False)
    else:
        await db.add_row(Matches, user_id_one=str(call.from_user.id),
                         user_reaction_one=False, user_reaction_two=None,
                         user_id_two=temp_storage.another_users_id[temp_storage.index_another_user])
    if len(temp_storage.another_users_id) > temp_storage.index_another_user + 1:
        temp_storage.index_another_user += 1
        await send_questionnaire(call.message)
    else:
        replica = await db.get_row(BotReplicas, unique_name='сome_back_later')
        await bot.send_message(chat_id=call.from_user.id, text=replica.replica)
        try:
            await clear_back(bot=bot, message=call.message, anchor_message=temp_storage.start_message)
        except:
            ...
