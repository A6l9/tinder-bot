
from aiogram import F, Router

from loader import user_manager, bot, db
from aiogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo
from database.models import BotReplicas, Users, Matches
from keyboards.inline.inline_kbs import create_buttons_for_viewing_profiles
from utils.clear_back import clear_back, clear_back_if_blocked_user
from utils.function_for_sending_questionnairies import send_questionnaire
from utils.user_lock import get_user_lock


show_questionnaire_router = Router()

@show_questionnaire_router.callback_query(F.data == 'swipe_right')
async def swipe_right_photo(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    user_lock = await get_user_lock(call.from_user.id)
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    print('RIGHT')
    print(f'{call.from_user.id=}')
    print(f'{len(temp_storage.another_photo_storage)=}')
    print(f'{temp_storage.num_page_photo_for_another_user=}')
    async with user_lock:
        if user_data.is_blocked:
            replica = await db.get_row(BotReplicas, unique_name='is_blocked')
            await call.message.answer(replica.replica, protect_content=True)
            try:
                await clear_back_if_blocked_user(bot=bot, message=call.message,
                                                 anchor_message=temp_storage.start_message)
            except:
                ...
        else:
            if (temp_storage.num_page_photo_for_another_user + 1 == len(temp_storage.another_photo_storage)
                    and len(temp_storage.another_photo_storage) != 1):
                temp_storage.num_page_photo_for_another_user = - 1
            if len(temp_storage.another_photo_storage) != 1:
                temp_storage.num_page_photo_for_another_user += 1
                another_user_data = await db.get_row(Users, tg_user_id=str(
                    temp_storage.another_users_id[temp_storage.index_another_user]))
                content = None
                replica = await db.get_row(BotReplicas, unique_name='show_profile_another_user')
                content = temp_storage.another_photo_storage
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
                                             reply_markup=await create_buttons_for_viewing_profiles(call.from_user.id))
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
                                             reply_markup=await create_buttons_for_viewing_profiles(call.from_user.id))
            else:
                replica = await db.get_row(BotReplicas, unique_name='no_more_photos')
                await call.answer(replica.replica)


@show_questionnaire_router.callback_query(F.data == 'swipe_left')
async def swipe_left_photo(call: CallbackQuery):
    temp_storage = user_manager.get_user(call.from_user.id)
    user_lock = await get_user_lock(call.from_user.id)
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    print('LEFT')
    print(f'{call.from_user.id=}')
    print(f'{len(temp_storage.another_photo_storage)=}')
    print(f'{temp_storage.num_page_photo_for_another_user=}')
    async with user_lock:
        if user_data.is_blocked:
            replica = await db.get_row(BotReplicas, unique_name='is_blocked')
            await call.message.answer(replica.replica, protect_content=True)
            try:
                await clear_back_if_blocked_user(bot=bot, message=call.message,
                                                 anchor_message=temp_storage.start_message)
            except:
                ...
        else:
            if temp_storage.num_page_photo_for_another_user == 0 and len(temp_storage.another_photo_storage) != 1:
                temp_storage.num_page_photo_for_another_user = len(temp_storage.another_photo_storage)
            if len(temp_storage.another_photo_storage) != 1:
                temp_storage.num_page_photo_for_another_user -= 1
                another_user_data = await db.get_row(Users,
                                    tg_user_id=str(temp_storage.another_users_id[temp_storage.index_another_user]))
                content = None
                replica = await db.get_row(BotReplicas, unique_name='show_profile_another_user')
                content = temp_storage.another_photo_storage
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
                                             reply_markup=await create_buttons_for_viewing_profiles(call.from_user.id))
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
                                             reply_markup=await create_buttons_for_viewing_profiles(call.from_user.id))
            else:
                replica = await db.get_row(BotReplicas, unique_name='no_more_photos')
                await call.answer(replica.replica)


@show_questionnaire_router.callback_query(F.data == 'like')
async def like_questionnaire(call: CallbackQuery):
    user_lock = await get_user_lock(call.from_user.id)
    temp_storage = user_manager.get_user(call.from_user.id)
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    async with user_lock:
        if user_data.is_blocked:
            replica = await db.get_row(BotReplicas, unique_name='is_blocked')
            await call.message.answer(replica.replica, protect_content=True)
            try:
                await clear_back_if_blocked_user(bot=bot, message=call.message,
                                                 anchor_message=temp_storage.start_message)
            except:
                ...
        else:
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
async def dislike_questionnaire(call: CallbackQuery):
    user_lock = await get_user_lock(call.from_user.id)
    temp_storage = user_manager.get_user(call.from_user.id)
    user_data = await db.get_row(Users, tg_user_id=str(call.from_user.id))
    async with user_lock:
        if user_data.is_blocked:
            replica = await db.get_row(BotReplicas, unique_name='is_blocked')
            await call.message.answer(replica.replica, protect_content=True)
            try:
                await clear_back_if_blocked_user(bot=bot, message=call.message,
                                                 anchor_message=temp_storage.start_message)
            except:
                ...
        else:
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
